# Generated by Django 2.1.5 on 2020-10-06 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20201006_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('M', ''), ('H', 'Home Decor'), ('A', 'Accessories'), ('T', 'Toys')], max_length=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(upload_to=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('O', 'Out of Stock'), ('S', 'Sale'), ('N', 'New')], max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='core.Order_Item'),
        ),
    ]
