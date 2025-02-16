from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from .forms import NutritionalInfoForm
from .models import RecipeIngredient, Recipe, Ingredient, Instruction, Category, NutritionalInfo
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "recipe/index.html", {"recipes": Recipe.objects.all()})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    instructions = Instruction.objects.filter(recipe=recipe)
    nutrition_info = NutritionalInfo.objects.filter(recipe=recipe)

    return render(request, "recipe/detail.html", {"recipe": recipe, "ingredients": ingredients, "instructions": instructions, "nutrition_info": nutrition_info})


def add_recipe(request):
    if request.method == "POST":
        nutrition_form = NutritionalInfoForm(request.POST)

        try:
            with transaction.atomic():
                # Validate basic recipe data

                # Validate basic recipe data
                category_id = request.POST.get("category")
                if not category_id:
                    raise ValidationError("Category is required.")

                try:
                    category = Category.objects.get(pk=category_id)
                except Category.DoesNotExist:
                    raise ValidationError("Invalid category selected.")

                recipe_data = {
                    "title": request.POST.get("title"),
                    "description": request.POST.get("description"),
                    "cooking_time": request.POST.get("cooking_time"),
                    "servings": request.POST.get("servings"),
                    "category": category,
                }

                # Check required string fields
                for field in ["title", "description"]:
                    if not recipe_data[field]:
                        raise ValidationError(f"{field.replace('_', ' ').title()} is required.")

                # Check required numeric fields
                for field in ["cooking_time", "servings"]:
                    try:
                        value = float(recipe_data[field])
                        if value <= 0:
                            raise ValueError
                    except (ValueError, TypeError):
                        raise ValidationError(f"Invalid value for {field.replace('_', ' ')}")

                # Create recipe instance
                recipe = Recipe(
                    **recipe_data,
                    food_pic=request.FILES.get("food_pic") if "food_pic" in request.FILES else None
                )

                print("Recipe", recipe)
                recipe.full_clean()  # Validate model fields
                recipe.save()

                # Process ingredients
                ingredients = request.POST.getlist("ingredients[]")
                new_ingredients = request.POST.getlist("new_ingredients[]")
                quantities = request.POST.getlist("quantities[]")
                units = request.POST.getlist("units[]")

                if not any(ingredients) and not any(new_ingredients):
                    raise ValidationError("At least one ingredient is required.")

                recipe_ingredients = []

                for i, (ingredient_id, new_ingredient, quantity, unit) in enumerate(
                    zip(ingredients, new_ingredients, quantities, units)
                ):
                    if not quantity or (not ingredient_id and not new_ingredient.strip()):
                        continue

                    try:
                        quantity = float(quantity)
                        if quantity <= 0:
                            raise ValueError
                    except ValueError:
                        raise ValidationError(f"Invalid quantity at ingredient {i + 1}")

                    # Handle new or existing ingredient
                    if new_ingredient.strip():
                        ingredient, _ = Ingredient.objects.get_or_create(
                            name=new_ingredient.strip(),
                            defaults={"created_by": request.user}
                        )
                    else:
                        ingredient = Ingredient.objects.filter(id=ingredient_id).first()
                        if not ingredient:
                            raise ValidationError(f"Invalid ingredient selected at position {i + 1}")

                    recipe_ingredients.append(
                        RecipeIngredient(recipe=recipe, ingredient=ingredient, quantity=quantity, units=unit)
                    )

                if recipe_ingredients:
                    RecipeIngredient.objects.bulk_create(recipe_ingredients)

                # Process instructions
                instructions = [inst.strip() for inst in request.POST.getlist("instructions[]") if inst.strip()]

                if not instructions:
                    raise ValidationError("At least one instruction is required.")

                recipe_instructions = [
                    Instruction(recipe=recipe, step_no=index + 1, instruction=instruction_text)
                    for index, instruction_text in enumerate(instructions)
                ]

                if recipe_instructions:
                    Instruction.objects.bulk_create(recipe_instructions)

                # Handle nutritional information
                if nutrition_form.is_valid():
                    nutrition = nutrition_form.save(commit=False)
                    nutrition.recipe = recipe
                    nutrition.full_clean()
                    nutrition.save()
                else:
                    error_messages = "; ".join(f"{field}: {error[0]}" for field, error in nutrition_form.errors.items())
                    raise ValidationError(f"Invalid nutritional information: {error_messages}")

                messages.success(request, "Recipe added successfully!")
                return redirect("recipe:index")

        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            logger.exception("Error creating recipe")
            messages.error(request, "An unexpected error occurred. Please try again.")

    # GET request or form validation failure
    context = {
        "nutrition_form": NutritionalInfoForm(),
        "ingredients": Ingredient.objects.all().order_by("name"),
        "categories": Category.objects.all().order_by("name"),
        "form_data": request.POST if request.method == "POST" else None,
    }

    return render(request, "recipe/add_recipe.html", context)


