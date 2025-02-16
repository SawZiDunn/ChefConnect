from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.PositiveIntegerField()
    food_pic = models.ImageField(upload_to="recipe_pictures/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    units = models.CharField(max_length=50, help_text="e.g. grams, cups, tbsp")

    def __str__(self):
        return f"{self.quantity} {self.units} of {self.ingredient.name}"


class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="instructions")
    step_no = models.PositiveIntegerField()
    instruction = models.TextField()

    def __str__(self):
        return f"Step {self.step_no} for {self.recipe.title}"


class NutritionalInfo(models.Model):
    recipe = models.OneToOneField(Recipe, on_delete=models.CASCADE, related_name="nutrition_info")
    protein = models.FloatField(help_text="grams")
    carb = models.FloatField(help_text="grams")
    fat = models.FloatField(help_text="grams")
    calories = models.FloatField(help_text="per serving")

    def __str__(self):
        return f"Nutrition for {self.recipe.title}"