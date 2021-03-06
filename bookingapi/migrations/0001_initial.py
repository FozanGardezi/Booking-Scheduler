# Generated by Django 3.0.7 on 2020-07-05 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('slotKey', models.CharField(max_length=100)),
                ('bookingKey', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('duration', models.IntegerField()),
                ('pitch', models.IntegerField()),
                ('rate', models.IntegerField()),
                ('start', models.CharField(max_length=30)),
                ('end', models.CharField(max_length=30)),
                ('status', models.CharField(max_length=30)),
                ('sumittedDate', models.DateTimeField()),
                ('lock_code', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(max_length=100)),
                ('email_sent', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookingSchedulerHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=100)),
                ('job_type', models.CharField(max_length=100)),
                ('slot_id', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('event_date', models.DateTimeField()),
            ],
        ),
    ]
