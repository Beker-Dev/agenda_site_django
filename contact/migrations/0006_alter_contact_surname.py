# Generated by Django 4.0.6 on 2022-07-11 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0005_remove_contact_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='surname',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]