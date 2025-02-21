from django.db import models
from django.conf import settings


# settings.Auth_User_Model means CustomerUser I created


class Tag(models.Model):
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
    preparation_time = models.PositiveIntegerField(help_text="Time in minutes")
    servings = models.PositiveIntegerField()
    food_pic = models.ImageField(upload_to="recipe_pictures/")
    tags = models.ManyToManyField(Tag, related_name='recipes')
    isSaved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='created_recipes')

    def get_avg_rating(self):
        total = 0
        for review in self.reviews.all():
            total += review.rating
        avg_rating = round(total / (len(self.reviews.all()) or 1))
        return range(avg_rating)

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ingredients")
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
