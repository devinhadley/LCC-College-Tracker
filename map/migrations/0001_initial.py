# Generated by Django 4.0.4 on 2022-04-12 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=62)),
                ('is_anonymous', models.BooleanField()),
                ('college_long', models.DecimalField(decimal_places=3, max_digits=8)),
                ('college_lat', models.DecimalField(decimal_places=3, max_digits=8)),
            ],
        ),
    ]