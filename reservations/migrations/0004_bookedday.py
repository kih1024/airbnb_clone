# Generated by Django 3.0.6 on 2020-06-10 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_auto_20200422_1442'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookedDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.DateField()),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.Reservation')),
            ],
            options={
                'verbose_name': 'Booked Day',
                'verbose_name_plural': 'Booked Days',
            },
        ),
    ]
