# Generated by Django 5.1.4 on 2025-02-28 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0002_res_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='res',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'female')], max_length=1),
        ),
    ]
