# Generated by Django 2.2.7 on 2019-12-03 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sklep', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('shipping_method', models.CharField(max_length=100)),
            ],
        ),
    ]
