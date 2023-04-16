# Generated by Django 4.1.5 on 2023-03-26 17:45

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('resume', models.FileField(default=None, null=True, upload_to='applicants/resume/')),
                ('cover_letter', models.FileField(default=None, null=True, upload_to='applicants/cover_letter/')),
                ('comments', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('Card_number', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('Ex_month', models.CharField(max_length=2)),
                ('Ex_Year', models.CharField(max_length=2)),
                ('CVV', models.CharField(max_length=3)),
                ('Balance', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('province', models.CharField(max_length=20)),
                ('img', models.ImageField(upload_to='pics')),
                ('number', models.IntegerField(default=50)),
            ],
        ),
        migrations.CreateModel(
            name='Destination_desc',
            fields=[
                ('dest_id', models.AutoField(primary_key=True, serialize=False)),
                ('province', models.CharField(max_length=20)),
                ('price', models.IntegerField(default=2000)),
                ('rating', models.IntegerField(default=5)),
                ('desc', models.TextField()),
                ('img_destin', models.ImageField(upload_to='pics')),
                ('type_skydive', models.CharField(choices=[('tandemskydive', 'Tandem Skydive'), ('learnskydive', 'Learn Skydive'), ('licenseskydive', 'Licensed Skydive')], max_length=50)),
                ('curr', models.CharField(choices=[('cad', 'CAD'), ('inr', 'INR'), ('usa', 'USA')], default='cad', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('age', models.IntegerField(default=18)),
            ],
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('Transactions_ID', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=10)),
                ('Amount', models.CharField(max_length=8)),
                ('Status', models.CharField(default='Failed', max_length=15)),
                ('Payment_method', models.CharField(blank=True, max_length=15)),
                ('Date_Time', models.CharField(default=datetime.datetime.now, max_length=19)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_available', models.DateField()),
                ('spots_total', models.IntegerField(default=50, null=True)),
                ('spots_free', models.IntegerField(default=50, null=True)),
                ('type_skydive', models.CharField(choices=[('tandemskydive', 'Tandem Skydive'), ('learnskydive', 'Learn Skydive'), ('licenseskydive', 'Licensed Skydive')], default='tandemskydive', max_length=50)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destin', to='skydive.destination')),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('booking_date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('total_fare', models.FloatField(blank=True, null=True)),
                ('type_skydive', models.CharField(choices=[('tandemskydive', 'Tandem Skydive'), ('learnskydive', 'Learn Skydive'), ('licenseskydive', 'Licensed Skydive')], max_length=50)),
                ('destination_desc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dest', to='skydive.destination_desc')),
                ('passengers', models.ManyToManyField(related_name='skydive_tickets', to='skydive.passenger')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]