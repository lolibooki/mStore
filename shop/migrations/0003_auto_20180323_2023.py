# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-23 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_product_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='number',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]