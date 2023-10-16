# Generated by Django 4.2.6 on 2023-10-16 16:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(max_length=100, unique=True)),
                ('status', models.PositiveIntegerField(choices=[(1, 'Activo'), (2, 'Inactivo')], default=1)),
                ('score', models.FloatField()),
                ('preapproved_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]