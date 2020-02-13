# Generated by Django 3.0.3 on 2020-02-13 09:08

import app.content.enums
from django.db import migrations, models
import enumchoicefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_user_is_tihlde_member'),
    ]

    operations = [
        migrations.CreateModel(
            name='Priority',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('priority_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_class', enumchoicefield.fields.EnumChoiceField(default=app.content.enums.UserClass(1), enum_class=app.content.enums.UserClass, max_length=6)),
                ('user_study', enumchoicefield.fields.EnumChoiceField(default=app.content.enums.UserStudy(1), enum_class=app.content.enums.UserStudy, max_length=7)),
            ],
            options={
                'verbose_name_plural': 'Priorities',
                'ordering': ('user_class', 'user_study'),
            },
        ),
        migrations.AddField(
            model_name='event',
            name='registration_priorities',
            field=models.ManyToManyField(blank=True, default=None, related_name='priorities', to='content.Priority'),
        ),
    ]
