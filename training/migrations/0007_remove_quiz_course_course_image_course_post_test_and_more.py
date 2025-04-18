# Generated by Django 5.2 on 2025-04-07 02:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0006_rename_module_progress_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='course',
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
        migrations.AddField(
            model_name='course',
            name='post_test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='post_test_courses', to='training.quiz'),
        ),
        migrations.AddField(
            model_name='course',
            name='pre_test',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pre_test_courses', to='training.quiz'),
        ),
        migrations.AlterField(
            model_name='course',
            name='materials',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
