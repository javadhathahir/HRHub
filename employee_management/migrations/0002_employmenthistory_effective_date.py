# Generated by Django 5.1.4 on 2024-12-13 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employmenthistory',
            name='effective_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
