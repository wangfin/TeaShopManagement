# Generated by Django 2.1.4 on 2019-01-07 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teamanagement', '0017_sale_info_staff_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale_tea',
            name='tea_name',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]