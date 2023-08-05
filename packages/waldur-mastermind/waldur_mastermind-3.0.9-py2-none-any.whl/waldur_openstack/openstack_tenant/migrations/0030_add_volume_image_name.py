# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-14 09:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('openstack_tenant', '0029_add_unique_constraint_for_properties'),
    ]

    operations = [
        migrations.AddField(
            model_name='volume',
            name='image_name',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='volume',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='openstack_tenant.Image'),
        ),
    ]
