# Generated by Django 4.2.1 on 2025-01-08 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance_tracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='attendance',
            name='total_hours',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='status',
            field=models.CharField(max_length=20),
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='check_in_time',
        ),
        migrations.RemoveField(
            model_name='attendance',
            name='check_out_time',
        ),
    ]
