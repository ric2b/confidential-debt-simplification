# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-01 18:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=80)),
                ('key', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='UOMe',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('value', models.PositiveIntegerField()),
                ('description', models.CharField(max_length=80)),
                ('issuing_date', models.DateField(auto_now_add=True, verbose_name='date issued')),
                ('issuer_signature', models.CharField(default='', max_length=400)),
                ('borrower_signature', models.CharField(default='', max_length=400)),
            ],
            options={
                'verbose_name_plural': "UOMe's",
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('key', models.CharField(max_length=400, primary_key=True, serialize=False)),
                ('balance', models.IntegerField(default=0)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_server_app.Group')),
            ],
        ),
        migrations.CreateModel(
            name='UserDebt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField()),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='debt_borrower', to='main_server_app.User')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_server_app.Group')),
                ('lender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='debt_lender', to='main_server_app.User')),
            ],
        ),
        migrations.AddField(
            model_name='uome',
            name='borrower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='uome_borrower', to='main_server_app.User'),
        ),
        migrations.AddField(
            model_name='uome',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_server_app.Group'),
        ),
        migrations.AddField(
            model_name='uome',
            name='lender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='uome_lender', to='main_server_app.User'),
        ),
    ]