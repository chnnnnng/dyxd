# Generated by Django 3.0.3 on 2020-02-25 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20200225_0913'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='type',
            field=models.BooleanField(choices=[(0, '面对面快签'), (1, '定位签')], default=0),
        ),
    ]
