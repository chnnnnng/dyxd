# Generated by Django 3.0.3 on 2020-02-22 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Checkinbook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('status', models.BooleanField(choices=[(0, '未完结'), (1, '已完结')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=50)),
                ('session_key', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=11)),
                ('status', models.BooleanField(choices=[(0, '未登录'), (1, '已登陆')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('roster', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
        ),
        migrations.CreateModel(
            name='Checkinsheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('bt_address', models.CharField(max_length=20)),
                ('num_should', models.IntegerField(default=0)),
                ('num_actual', models.IntegerField(default=0)),
                ('num_leave', models.IntegerField(default=0)),
                ('num_absent', models.IntegerField(default=0)),
                ('attendance_rate', models.FloatField(default=0)),
                ('status', models.BooleanField(choices=[(0, '未完结'), (1, '已完结')], default=0)),
                ('checkinbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Checkinbook')),
                ('roster', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Roster')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
        ),
        migrations.CreateModel(
            name='Checkinitem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identity_code', models.CharField(max_length=20)),
                ('time', models.DateTimeField(auto_now=True)),
                ('status', models.IntegerField(choices=[(0, '待签'), (1, '已签'), (2, '请假'), (3, '缺席')], default=0)),
                ('checkinsheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Checkinsheet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.User')),
            ],
        ),
        migrations.AddField(
            model_name='checkinbook',
            name='roster',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Roster'),
        ),
    ]
