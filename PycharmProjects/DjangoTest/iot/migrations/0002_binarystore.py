# Generated by Django 2.2 on 2019-04-03 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BinaryStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.TimeField()),
                ('binaryData', models.BinaryField()),
            ],
        ),
    ]
