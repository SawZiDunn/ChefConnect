# Generated by Django 5.0 on 2025-02-24 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0009_rename_units_recipeingredient_unit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='food_pic',
            field=models.ImageField(blank=True, upload_to='recipe_pictures/'),
        ),
    ]
