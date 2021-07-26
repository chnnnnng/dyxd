# Generated by Django 3.0.3 on 2020-03-01 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_display_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useridentitycodecheckinsheetbond',
            name='checkinsheet',
        ),
        migrations.AddField(
            model_name='useridentitycodecheckinsheetbond',
            name='checkinbook',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.Checkinbook'),
        ),
    ]
