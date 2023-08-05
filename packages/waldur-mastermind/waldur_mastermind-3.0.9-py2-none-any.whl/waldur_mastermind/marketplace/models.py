from __future__ import unicode_literals

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.postgres.fields import JSONField as BetterJSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_fsm import transition, FSMIntegerField
from model_utils import FieldTracker
from model_utils.models import TimeStampedModel
import six

from waldur_core.core import models as core_models
from waldur_core.core.fields import JSONField
from waldur_core.core.validators import ImageValidator
from waldur_core.quotas import fields as quotas_fields
from waldur_core.quotas import models as quotas_models
from waldur_core.structure import models as structure_models
from waldur_core.structure.images import get_upload_path

from . import managers, plugins
from .attribute_types import ATTRIBUTE_TYPES
from ..common import mixins as common_mixins


@python_2_unicode_compatible
class ServiceProvider(core_models.UuidMixin,
                      core_models.DescribableMixin,
                      structure_models.StructureModel,
                      TimeStampedModel):
    customer = models.OneToOneField(structure_models.Customer, on_delete=models.CASCADE)
    enable_notifications = models.BooleanField(default=True)
    api_secret_code = models.CharField(max_length=255, null=True, blank=True)

    class Permissions(object):
        customer_path = 'customer'

    class Meta(object):
        verbose_name = _('Service provider')

    def __str__(self):
        return six.text_type(self.customer)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-service-provider'


@python_2_unicode_compatible
class Category(core_models.UuidMixin,
               quotas_models.QuotaModelMixin,
               TimeStampedModel):
    title = models.CharField(blank=False, max_length=255)
    icon = models.FileField(upload_to='marketplace_category_icons',
                            blank=True,
                            null=True,
                            validators=[ImageValidator])
    description = models.TextField(blank=True)

    class Quotas(quotas_models.QuotaModelMixin.Quotas):
        offering_count = quotas_fields.QuotaField(is_backend=True)

    class Meta(object):
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ('title',)

    def __str__(self):
        return six.text_type(self.title)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-category'


@python_2_unicode_compatible
class CategoryColumn(models.Model):
    """
    This model is needed in order to render resources table with extra columns.
    Usually each column corresponds to specific resource attribute.
    However, one table column may correspond to several resource attributes.
    In this case custom widget should be specified.
    If attribute field is specified, it is possible to filter and sort resources by it's value.
    """

    class Meta(object):
        ordering = ('category', 'index')

    category = models.ForeignKey(Category, related_name='columns')
    index = models.PositiveSmallIntegerField(help_text=_('Index allows to reorder columns.'))
    title = models.CharField(blank=False, max_length=255,
                             help_text=_('Title is rendered as column header.'))
    attribute = models.CharField(blank=True, max_length=255,
                                 help_text=_('Resource attribute is rendered as table cell.'))
    widget = models.CharField(blank=True, max_length=255,
                              help_text=_('Widget field allows to customise table cell rendering.'))

    def __str__(self):
        return six.text_type(self.title)

    def clean(self):
        if not self.attribute and not self.widget:
            raise ValidationError(_('Either attribute or widget field should be specified.'))


@python_2_unicode_compatible
class Section(TimeStampedModel):
    key = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(blank=False, max_length=255)
    category = models.ForeignKey(Category, related_name='sections')
    is_standalone = models.BooleanField(
        default=False, help_text=_('Whether section is rendered as a separate tab.'))

    def __str__(self):
        return six.text_type(self.title)


@python_2_unicode_compatible
class Attribute(TimeStampedModel):
    key = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(blank=False, max_length=255)
    section = models.ForeignKey(Section, related_name='attributes')
    type = models.CharField(max_length=255, choices=ATTRIBUTE_TYPES)
    required = models.BooleanField(default=False, help_text=_('A value must be provided for the attribute.'))

    def __str__(self):
        return six.text_type(self.title)


@python_2_unicode_compatible
class AttributeOption(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='options', on_delete=models.CASCADE)
    key = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    class Meta(object):
        unique_together = ('attribute', 'key')

    def __str__(self):
        return six.text_type(self.title)


class ScopeMixin(models.Model):
    class Meta(object):
        abstract = True

    content_type = models.ForeignKey(ContentType, null=True, related_name='+')
    object_id = models.PositiveIntegerField(null=True)
    scope = GenericForeignKey('content_type', 'object_id')


@python_2_unicode_compatible
class Offering(core_models.UuidMixin,
               core_models.NameMixin,
               core_models.DescribableMixin,
               quotas_models.QuotaModelMixin,
               structure_models.StructureModel,
               TimeStampedModel,
               ScopeMixin):

    class States(object):
        DRAFT = 1
        ACTIVE = 2
        PAUSED = 3
        ARCHIVED = 4

        CHOICES = (
            (DRAFT, 'Draft'),
            (ACTIVE, 'Active'),
            (PAUSED, 'Paused'),
            (ARCHIVED, 'Archived'),
        )

    thumbnail = models.FileField(upload_to='marketplace_service_offering_thumbnails',
                                 blank=True,
                                 null=True,
                                 validators=[ImageValidator])
    full_description = models.TextField(blank=True)
    vendor_details = models.TextField(blank=True)
    rating = models.IntegerField(null=True,
                                 validators=[MaxValueValidator(5), MinValueValidator(1)],
                                 help_text=_('Rating is value from 1 to 5.'))
    category = models.ForeignKey(Category, related_name='offerings')
    customer = models.ForeignKey(structure_models.Customer, related_name='+', null=True)
    attributes = BetterJSONField(blank=True, default=dict, help_text=_('Fields describing Category.'))
    options = BetterJSONField(blank=True, default=dict, help_text=_('Fields describing Offering request form.'))
    geolocations = JSONField(default=list, blank=True,
                             help_text=_('List of latitudes and longitudes. For example: '
                                         '[{"latitude": 123, "longitude": 345}, {"latitude": 456, "longitude": 678}]'))

    native_name = models.CharField(max_length=160, default='', blank=True)
    native_description = models.CharField(max_length=500, default='', blank=True)

    type = models.CharField(max_length=100)
    state = FSMIntegerField(default=States.DRAFT, choices=States.CHOICES)

    # If offering is not shared, it is available only to following user categories:
    # 1) staff user;
    # 2) global support user;
    # 3) users with active permission in original customer;
    # 4) users with active permission in allowed customers and nested projects.
    shared = models.BooleanField(default=False, help_text=_('Anybody can use it'))
    allowed_customers = models.ManyToManyField(structure_models.Customer, blank=True)

    objects = managers.MixinManager('scope')
    tracker = FieldTracker()

    class Permissions(object):
        customer_path = 'customer'

    class Meta(object):
        verbose_name = _('Offering')

    class Quotas(quotas_models.QuotaModelMixin.Quotas):
        order_item_count = quotas_fields.CounterQuotaField(
            target_models=lambda: [OrderItem],
            path_to_scope='offering',
        )

    @transition(field=state, source=[States.DRAFT, States.PAUSED], target=States.ACTIVE)
    def activate(self):
        pass

    @transition(field=state, source=States.ACTIVE, target=States.PAUSED)
    def pause(self):
        pass

    @transition(field=state, source='*', target=States.ARCHIVED)
    def archive(self):
        pass

    def __str__(self):
        return six.text_type(self.name)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-offering'

    @staticmethod
    def get_scope_models():
        return plugins.manager.get_scope_models()


class OfferingComponent(core_models.DescribableMixin):
    class Meta(object):
        unique_together = ('type', 'offering')

    class BillingTypes(object):
        FIXED = 'fixed'
        USAGE = 'usage'

        CHOICES = (
            (FIXED, 'Fixed-price'),
            (USAGE, 'Usage-based'),
        )

    offering = models.ForeignKey(Offering, related_name='components')
    billing_type = models.CharField(choices=BillingTypes.CHOICES,
                                    default=BillingTypes.FIXED,
                                    max_length=5)
    type = models.CharField(max_length=50,
                            help_text=_('Unique internal name of the measured unit, for example floating_ip.'))
    name = models.CharField(max_length=150,
                            help_text=_('Display name for the measured unit, for example, Floating IP.'))
    measured_unit = models.CharField(max_length=30,
                                     help_text=_('Unit of measurement, for example, GB.'))


class Plan(core_models.UuidMixin,
           TimeStampedModel,
           core_models.NameMixin,
           core_models.DescribableMixin,
           common_mixins.UnitPriceMixin,
           common_mixins.ProductCodeMixin,
           ScopeMixin):
    offering = models.ForeignKey(Offering, related_name='plans')
    archived = models.BooleanField(default=False, help_text=_('Forbids creation of new resources.'))
    objects = managers.MixinManager('scope')

    @classmethod
    def get_url_name(cls):
        return 'marketplace-plan'

    class Permissions(object):
        customer_path = 'offering__customer'


class PlanComponent(models.Model):
    class Meta(object):
        unique_together = ('plan', 'component')

    PRICE_MAX_DIGITS = 14
    PRICE_DECIMAL_PLACES = 10

    plan = models.ForeignKey(Plan, related_name='components')
    component = models.ForeignKey(OfferingComponent, related_name='components', null=True)
    amount = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0,
                                max_digits=PRICE_MAX_DIGITS,
                                decimal_places=PRICE_DECIMAL_PLACES,
                                validators=[MinValueValidator(Decimal('0'))],
                                verbose_name=_('Price per unit per billing period.'))


@python_2_unicode_compatible
class Screenshot(core_models.UuidMixin,
                 structure_models.StructureModel,
                 core_models.DescribableMixin,
                 TimeStampedModel,
                 core_models.NameMixin):
    image = models.ImageField(upload_to=get_upload_path)
    thumbnail = models.ImageField(upload_to=get_upload_path, editable=False, null=True)
    offering = models.ForeignKey(Offering, related_name='screenshots')

    class Permissions(object):
        customer_path = 'offering__customer'

    class Meta(object):
        verbose_name = _('Screenshot')

    def __str__(self):
        return six.text_type(self.name)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-screenshot'


class Order(core_models.UuidMixin,
            TimeStampedModel):
    class States(object):
        REQUESTED_FOR_APPROVAL = 1
        EXECUTING = 2
        DONE = 3
        TERMINATED = 4

        CHOICES = (
            (REQUESTED_FOR_APPROVAL, 'requested for approval'),
            (EXECUTING, 'executing'),
            (DONE, 'done'),
            (TERMINATED, 'terminated'),
        )

    created_by = models.ForeignKey(core_models.User, related_name='orders')
    approved_by = models.ForeignKey(core_models.User, blank=True, null=True, related_name='+')
    approved_at = models.DateTimeField(editable=False, null=True, blank=True)
    project = models.ForeignKey(structure_models.Project)
    state = FSMIntegerField(default=States.REQUESTED_FOR_APPROVAL, choices=States.CHOICES)
    total_cost = models.DecimalField(max_digits=22, decimal_places=10, null=True, blank=True)
    tracker = FieldTracker()

    class Permissions(object):
        customer_path = 'project__customer'
        project_path = 'project'

    class Meta(object):
        verbose_name = _('Order')
        ordering = ('created',)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-order'

    @transition(field=state, source=States.REQUESTED_FOR_APPROVAL, target=States.EXECUTING)
    def set_state_executing(self):
        pass

    @transition(field=state, source=States.EXECUTING, target=States.DONE)
    def set_state_done(self):
        pass

    @transition(field=state, source='*', target=States.TERMINATED)
    def set_state_terminated(self):
        pass

    def get_approvers(self):
        User = get_user_model()
        users = []

        if settings.WALDUR_MARKETPLACE['NOTIFY_STAFF_ABOUT_APPROVALS']:
            users = User.objects.filter(is_staff=True, is_active=True)

        if settings.WALDUR_MARKETPLACE['OWNER_CAN_APPROVE_ORDER']:
            order_owners = self.project.customer.get_owners()
            users = order_owners if not users else users.union(order_owners)

        if settings.WALDUR_MARKETPLACE['MANAGER_CAN_APPROVE_ORDER']:
            order_managers = self.project.get_users(structure_models.ProjectRole.MANAGER)
            users = order_managers if not users else users.union(order_managers)

        if settings.WALDUR_MARKETPLACE['ADMIN_CAN_APPROVE_ORDER']:
            order_admins = self.project.get_users(structure_models.ProjectRole.ADMINISTRATOR)
            users = order_admins if not users else users.union(order_admins)

        return users and users.distinct()


class OrderItem(core_models.UuidMixin,
                core_models.ErrorMessageMixin,
                TimeStampedModel,
                ScopeMixin):
    class States(object):
        PENDING = 1
        EXECUTING = 2
        DONE = 3
        ERRED = 4
        TERMINATED = 5

        CHOICES = (
            (PENDING, 'pending'),
            (EXECUTING, 'executing'),
            (DONE, 'done'),
            (ERRED, 'erred'),
            (TERMINATED, 'terminated'),
        )

        TERMINAL_STATES = {DONE, ERRED, TERMINATED}

    order = models.ForeignKey(Order, related_name='items')
    offering = models.ForeignKey(Offering)
    attributes = BetterJSONField(blank=True, default=dict)
    cost = models.DecimalField(max_digits=22, decimal_places=10, null=True, blank=True)
    plan = models.ForeignKey('Plan', null=True, blank=True)
    objects = managers.MixinManager('scope')
    state = FSMIntegerField(default=States.PENDING, choices=States.CHOICES)
    tracker = FieldTracker()

    class Permissions(object):
        customer_path = 'order__project__customer'
        project_path = 'order__project'

    class Meta(object):
        verbose_name = _('Order item')
        ordering = ('created',)

    @classmethod
    def get_url_name(cls):
        return 'marketplace-order-item'

    @transition(field=state, source=[States.PENDING, States.ERRED], target=States.EXECUTING)
    def set_state_executing(self):
        pass

    @transition(field=state, source=States.EXECUTING, target=States.DONE)
    def set_state_done(self):
        pass

    @transition(field=state, source='*', target=States.ERRED)
    def set_state_erred(self):
        pass

    @transition(field=state, source='*', target=States.TERMINATED)
    def set_state_terminated(self):
        pass

    def set_state(self, state):
        getattr(self, 'set_state_' + state)()
        self.save(update_fields=['state'])


class ComponentQuota(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name='quotas')
    component = models.ForeignKey(OfferingComponent,
                                  limit_choices_to={'billing_type': OfferingComponent.BillingTypes.USAGE})
    limit = models.PositiveIntegerField(default=-1)
    usage = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('order_item', 'component')


class ComponentUsage(TimeStampedModel):
    order_item = models.ForeignKey(OrderItem, related_name='usages')
    component = models.ForeignKey(OfferingComponent,
                                  limit_choices_to={'billing_type': OfferingComponent.BillingTypes.USAGE})
    usage = models.PositiveIntegerField(default=0)
    date = models.DateField()

    class Meta:
        unique_together = ('order_item', 'component', 'date')


class ProjectResourceCount(models.Model):
    """
    This model allows to count current number of project resources by category.
    """
    project = models.ForeignKey(structure_models.Project, related_name='+')
    category = models.ForeignKey(Category, related_name='+')
    count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('project', 'category')
