# Generated by Django 5.2 on 2025-04-08 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0008_customuser_enrolled_courses_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='enrolled_courses',
        ),
    ]
