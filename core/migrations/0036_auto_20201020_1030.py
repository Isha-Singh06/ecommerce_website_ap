# Generated by Django 2.1.5 on 2020-10-20 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_auto_20201019_0951'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='default',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('T', 'Toys'), ('M', ''), ('A', 'Accessories'), ('H', 'Home Decor')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('N', 'New'), ('O', 'Out of Stock'), ('S', 'Sale')], max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='core.Order_Item'),
        ),
    ]
