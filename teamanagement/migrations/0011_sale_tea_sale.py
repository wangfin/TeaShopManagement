# Generated by Django 2.1.4 on 2019-01-05 01:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teamanagement', '0010_auto_20190105_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='sale_tea',
            name='sale',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teamanagement.Sale_info'),
            preserve_default=False,
        ),
    ]
