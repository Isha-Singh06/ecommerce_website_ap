# Generated by Django 2.1.5 on 2020-10-16 08:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0027_auto_20201015_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('initial_date', models.DateTimeField(auto_now_add=True)),
                ('order_date', models.DateTimeField()),
                ('wishlist_present', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist_Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishlist_present', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('A', 'Accessories'), ('T', 'Toys'), ('M', ''), ('H', 'Home Decor')], max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='core.Order_Item'),
        ),
        migrations.AddField(
            model_name='wishlist_item',
            name='wishlist_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Item'),
        ),
        migrations.AddField(
            model_name='wishlist',
            name='wishlist_items',
            field=models.ManyToManyField(to='core.Wishlist_Item'),
        ),
    ]
