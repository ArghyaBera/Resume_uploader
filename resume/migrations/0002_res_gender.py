# Generated by Django 5.1.4 on 2025-02-28 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='res',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'female')], default='M', max_length=1),
        ),
    ]
