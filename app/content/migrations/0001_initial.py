# Generated by Django 2.2.6 on 2019-11-20 23:16

import app.content.models.user
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('user_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('cell', models.CharField(blank=True, max_length=8)),
                ('em_nr', models.CharField(blank=True, max_length=12)),
                ('home_busstop', models.IntegerField(blank=True, null=True)),
                ('gender', models.IntegerField(blank=True, choices=[(1, 'Mann'), (2, 'Kvinne'), (3, 'Annet')], default=2, null=True)),
                ('user_class', models.IntegerField(blank=True, choices=[(1, '1. Klasse'), (2, '2. Klasse'), (3, '3. Klasse'), (4, '4. Klasse'), (5, '5. Klasse')], default=1, null=True)),
                ('user_study', models.IntegerField(blank=True, choices=[(1, 'Dataing'), (2, 'DigFor'), (3, 'DigInc'), (4, 'DigSam'), (5, 'Drift')], default=1, null=True)),
                ('allergy', models.CharField(blank=True, max_length=250)),
                ('tool', models.CharField(blank=True, max_length=100)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', app.content.models.user.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(max_length=200)),
                ('start', models.DateTimeField()),
                ('location', models.CharField(max_length=200, null=True)),
                ('description', models.TextField(blank=True, default='')),
                ('priority', models.IntegerField(choices=[(0, 'Low'), (1, 'Normal'), (2, 'High')], default=0, null=True)),
                ('sign_up', models.BooleanField(default=False)),
                ('limit', models.IntegerField(default=0)),
                ('closed', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='content.Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(max_length=200)),
                ('ingress', models.CharField(max_length=800)),
                ('body', models.TextField(blank=True, default='')),
                ('location', models.CharField(max_length=200)),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('company', models.CharField(max_length=200)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('link', models.URLField(blank=True, max_length=300, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('title', models.CharField(max_length=200)),
                ('header', models.CharField(max_length=200)),
                ('body', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'News',
            },
        ),
        migrations.CreateModel(
            name='Warning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.CharField(max_length=400, null=True)),
                ('type', models.IntegerField(choices=[(0, 'Error'), (1, 'Warning'), (2, 'Message')], default=0, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserEvent',
            fields=[
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Signed up on')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_event_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_on_wait', models.BooleanField(default=False, verbose_name='waiting list')),
                ('has_attended', models.BooleanField(default=False)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.Event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('event', 'is_on_wait', 'created_at'),
                'verbose_name': 'User event',
                'verbose_name_plural': 'User events',
                'unique_together': {('user', 'event')},
            },
        ),
        migrations.AddField(
            model_name='event',
            name='registered_users_list',
            field=models.ManyToManyField(blank=True, default=None, through='content.UserEvent', to=settings.AUTH_USER_MODEL, verbose_name='registered users'),
        ),
    ]
