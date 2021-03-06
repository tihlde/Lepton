# Generated by Django 3.1.5 on 2021-01-26 12:46

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0014_add_official_and_type_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.URLField(blank=True, max_length=600, null=True)),
                ('image_alt', models.CharField(blank=True, max_length=200, null=True)),
                ('page_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('content', models.TextField(blank=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='content.page')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
                'ordering': ['title'],
                'unique_together': {('parent', 'slug')},
            },
        ),
        migrations.DeleteModel(
            name='WikiPost',
        ),
    ]
