# Generated by Django 2.1.4 on 2019-01-01 02:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamanagement', '0006_auto_20190101_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='commodity_info',
            name='goods',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='teamanagement.Goods'),
            preserve_default=False,
        ),
    ]
