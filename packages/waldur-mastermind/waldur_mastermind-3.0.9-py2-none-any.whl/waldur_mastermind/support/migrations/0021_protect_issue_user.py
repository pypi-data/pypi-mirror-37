# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-08-01 17:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0020_protect_offering_issue'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='assignee',
            field=models.ForeignKey(blank=True, help_text='Help desk user who will implement the issue', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issues', to='support.SupportUser'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='caller',
            field=models.ForeignKey(help_text='Waldur user who has reported the issue.', on_delete=django.db.models.deletion.PROTECT, related_name='created_issues', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='reporter',
            field=models.ForeignKey(blank=True, help_text='Help desk user who have created the issue that is reported by caller.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reported_issues', to='support.SupportUser'),
        ),
    ]
