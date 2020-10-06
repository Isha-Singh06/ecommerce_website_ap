# Generated by Django 2.1.5 on 2020-10-02 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201002_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default='test prod'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('H', 'Home'), ('T', 'Toys'), ('M', ''), ('A', 'Accessories')], max_length=1),
        ),
    ]