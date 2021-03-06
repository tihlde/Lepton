# Generated by Django 3.1.3 on 2020-11-10 19:51

import app.common.enums
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumchoicefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('group', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('membership_type', enumchoicefield.fields.EnumChoiceField(default=app.common.enums.MembershipType(1), enum_class=app.common.enums.MembershipType, max_length=6)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Membership History',
                'verbose_name_plural': 'Membership Histories',
                'unique_together': {('user', 'group', 'end_date')},
            },
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('membership_type', enumchoicefield.fields.EnumChoiceField(default=app.common.enums.MembershipType(1), enum_class=app.common.enums.MembershipType, max_length=6)),
                ('expiration_date', models.DateField(blank=True, null=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='group.group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'group')},
            },
        ),
    ]
