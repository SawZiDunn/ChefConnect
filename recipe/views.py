from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
from .forms import NutritionalInfoForm
from django.contrib.auth.decorators import login_required
from .models import RecipeIngredient, Recipe, Ingredient, Instruction, Tag, NutritionalInfo
from interactions.models import Like
import logging

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "recipe/index.html", {"recipes": Recipe.objects.all()})


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    instructions = Instruction.objects.filter(recipe=recipe)
    nutrition_info = NutritionalInfo.objects.get(recipe=recipe)
    tags = recipe.tags.all()  # Tag.objects.filter(recipe=recipe)

    # checks if current user likes this recipe
    isLiked = Like.objects.filter(user=request.user, recipe=recipe).exists()
    print("isLike", isLiked)

    return render(request, "recipe/detail.html",
                  {"recipe": recipe, "ingredients": ingredients, "instructions": instructions,
                   "nutrition_info": nutrition_info, "tags": tags, "like_count": recipe.likes.count(),
                   "isLiked": isLiked})


@login_required
def add_recipe(request):
    if request.method == "POST":
        nutrition_form = NutritionalInfoForm(request.POST)

        # Process selected tags (existing ones)
        tag_ids = request.POST.get("existing_tags")  # Get selected tags

        if tag_ids:
            tag_ids = tag_ids.split(",")

        new_tag_names = request.POST.get("new_tags")  # Get new tags input

        if new_tag_names:
            new_tag_names = new_tag_names.split(",")

        print(tag_ids)
        print(new_tag_names)

        # Validate tag input
        if not tag_ids and not new_tag_names:
            raise ValidationError("At least one tag is required.")

        try:
            with transaction.atomic():

                recipe_data = {
                    "title": request.POST.get("title"),
                    "description": request.POST.get("description"),
                    "cooking_time": request.POST.get("cooking_time"),
                    "servings": request.POST.get("servings"),
                    "created_by": request.user
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
                recipe = Recipe(  # Recipe.objects.create()
                    **recipe_data,
                    food_pic=request.FILES.get("food_pic") if "food_pic" in request.FILES else None
                )

                recipe.full_clean()  # Validate model fields
                recipe.save()

                # Add selected existing tags
                for tag_id in tag_ids:
                    try:
                        tag = Tag.objects.get(pk=tag_id)
                        recipe.tags.add(tag)
                    except Tag.DoesNotExist:
                        raise ValidationError(f"Invalid tag ID: {tag_id}")

                # Add newly created tags
                for tag_name in new_tag_names:
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        recipe.tags.add(tag)

                messages.success(request, "Recipe added successfully!")

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
                            name=new_ingredient.strip()
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
            print(str(e))

        except Exception as e:
            logger.exception("Error creating recipe")
            messages.error(request, "An unexpected error occurred. Please try again.")

    # GET request or form validation failure
    context = {
        "nutrition_form": NutritionalInfoForm(),
        "ingredients": Ingredient.objects.all().order_by("name"),
        "tags": Tag.objects.all().order_by("name"),
        "form_data": request.POST if request.method == "POST" else None,
    }

    return render(request, "recipe/add_recipe.html", context)


def edit(request, recipe_id: int):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    instructions = Instruction.objects.filter(recipe=recipe)
    nutrition_info = NutritionalInfo.objects.get(recipe=recipe)
    tags = recipe.tags.all()  # Tag.objects.filter(recipe=recipe)

    return render(request, "recipe/edit_recipe.html",
                  {"recipe": recipe, "ingredients": ingredients, "instructions": instructions,
                   "nutrition_info": nutrition_info, "tags": tags})


def delete(request, recipe_id: int):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect("users:profile")
