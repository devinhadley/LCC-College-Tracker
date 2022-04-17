# Generated by Django 4.0.4 on 2022-04-13 05:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('map', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('long', models.DecimalField(decimal_places=3, max_digits=8)),
                ('lat', models.DecimalField(decimal_places=3, max_digits=8)),
            ],
        ),
        migrations.RemoveField(
            model_name='entry',
            name='college_lat',
        ),
        migrations.RemoveField(
            model_name='entry',
            name='college_long',
        ),
        migrations.AddField(
            model_name='entry',
            name='college',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='map.college'),
        ),
    ]
