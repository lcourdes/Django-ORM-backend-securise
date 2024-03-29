# Generated by Django 4.1.7 on 2023-03-15 13:14

import application.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.contrib.auth.management import create_permissions

def add_permissions(apps, schema_migration):
    for app_config in apps.get_app_configs():
        app_config.models_module = True
        create_permissions(app_config, verbosity=0)
        app_config.models_module = None

def set_event_permissions_for_administrators(apps, schema_migration):
    Group = apps.get_model('auth', 'Group')
    administrators = Group.objects.get(name='administrators')
    salers = Group.objects.get(name='salers')

    Permission = apps.get_model('auth', 'Permission')

    add_event = Permission.objects.get(codename='add_event')
    change_event = Permission.objects.get(codename='change_event')
    delete_event = Permission.objects.get(codename='delete_event')
    view_event = Permission.objects.get(codename='view_event')

    administrators_permissions = [
        add_event,
        change_event,
        delete_event,
        view_event,
    ]
    all_permissions_list = [permission.id for permission in administrators_permissions]
    administrators.permissions.add(*all_permissions_list)
    administrators.save()

    salers.permissions.add(view_event)
    salers.save()

class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_contract'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attendees', models.IntegerField(blank=True, null=True)),
                ('event_date', models.DateTimeField()),
                ('notes', models.TextField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(limit_choices_to={'is_client': 'True'}, on_delete=django.db.models.deletion.CASCADE, to='application.client')),
                ('event_status', models.ForeignKey(limit_choices_to={'status': 'True'}, on_delete=django.db.models.deletion.CASCADE, to='application.event')),
                ('support_contact', models.ForeignKey(limit_choices_to=application.models.limit_users_support_contact, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunPython(add_permissions),
        migrations.RunPython(set_event_permissions_for_administrators)
    ]
