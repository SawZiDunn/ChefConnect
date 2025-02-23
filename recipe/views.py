from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
import json
from django.template.defaultfilters import capfirst  # for capitalization in html
from users.models import CustomUser
from .forms import NutritionalInfoForm
from django.contrib.auth.decorators import login_required
from .models import RecipeIngredient, Recipe, Ingredient, Instruction, Tag, NutritionalInfo
from django.http import JsonResponse
from interactions.models import Like
from django.db.models import Avg
import logging

logger = logging.getLogger(__name__)


def index(request):
    all_tags = Tag.objects.all().order_by('name')
    all_ingredients = Ingredient.objects.all().order_by('name')

    # no need to use all()
    recipes = Recipe.objects.annotate(
        rating=Avg('reviews__rating')  # Now matches the property name
    )

    rating = request.GET.get('rating')
    if rating:
        # rating -> rating >=
        recipes = recipes.filter(rating__gte=rating)

    preparation_time = request.GET.get('preparation_time')
    if preparation_time:
        if preparation_time == '61':
            recipes = recipes.filter(preparation_time__gte=60)
        else:
            recipes = recipes.filter(preparation_time__lte=int(preparation_time))

    # Apply search filter
    search_query = request.GET.get('search', '')
    if search_query:
        recipes = recipes.filter(title__icontains=search_query)

    # Apply tags filter
    tag = request.GET.get('tag')
    if tag:
        recipes = recipes.filter(tags__id=tag).distinct()

    # Apply ingredients filter
    ingredient = request.GET.get('ingredient')
    if ingredient:
        # recipe -> recipe_ingredient -> ingredient -> id
        recipes = recipes.filter(ingredients__ingredient__id=ingredient).distinct()

    rating_choices = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]

    preparation_time_choices = [
        (20, 'Less than 20 minutes'),
        (40, 'Less than 40 minutes'),
        (60, 'Less than 1 hour'),
        (61, 'More than 1 hour'),
    ]

    print("prepar", preparation_time)
    context = {
        'recipes': recipes.distinct(),  # to remove duplicates from tag and ingredient filters
        'all_tags': all_tags,
        'all_ingredients': all_ingredients,
        'selected_tag': tag,
        'selected_ingredient': ingredient,
        'rating_choices': rating_choices,
        'selected_rating': rating,
        'preparation_time_choices': preparation_time_choices,
        'selected_preparation_time': preparation_time,
        'search_query': search_query,
    }

    return render(request, 'recipe/index.html', context)


def recipe_detail(request, recipe_id):
    recipe = Recipe.objects.get(pk=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    instructions = Instruction.objects.filter(recipe=recipe)
    nutrition_info = NutritionalInfo.objects.get(recipe=recipe)
    tags = recipe.tags.all()  # Tag.objects.filter(recipe=recipe)

    # checks if current user likes this recipe
    isLiked = Like.objects.filter(user=request.user, recipe=recipe).exists()

    user = recipe.saved_by.all().filter(id=request.user.id).first()

    isSaved = True if user else False

    return render(request, "recipe/detail.html",
                  {"recipe": recipe, "ingredients": ingredients, "instructions": instructions,
                   "nutrition_info": nutrition_info, "tags": tags, "reviews": recipe.reviews.all(),
                   "like_count": recipe.likes.count(),
                   "isLiked": isLiked, "is_saved": isSaved})


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
                    "preparation_time": request.POST.get("preparation_time"),
                    "servings": request.POST.get("servings"),
                    "created_by": request.user
                }

                # Check required string fields
                for field in ["title", "description"]:
                    if not recipe_data[field]:
                        raise ValidationError(f"{field.replace('_', ' ').title()} is required.")

                # Check required numeric fields
                for field in ["preparation_time", "servings"]:
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


def edit_recipe(request, recipe_id: int):
    nutrition_info = NutritionalInfo.objects.get(pk=recipe_id)
    recipe = get_object_or_404(Recipe, pk=recipe_id)

    # Check if user has permission to edit
    if recipe.created_by != request.user:
        messages.error(request, "You don't have permission to edit this recipe")
        return redirect('recipe:detail', recipe_id=recipe_id)

    if request.method == "POST":
        nutrition_form = NutritionalInfoForm(request.POST, instance=recipe.nutrition_info)

        # Get tag data
        tag_ids = request.POST.get("existing_tags", "").split(",") if request.POST.get("existing_tags") else []
        new_tag_names = request.POST.get("new_tags", "").split(",") if request.POST.get("new_tags") else []

        try:
            with transaction.atomic():
                # Update basic recipe fields
                recipe.title = request.POST.get("title")
                recipe.description = request.POST.get("description")
                recipe.preparation_time = request.POST.get("cooking_time")  # Changed to match template
                recipe.servings = request.POST.get("servings")

                # Handle food pic update if provided
                if "food_pic" in request.FILES:
                    recipe.food_pic = request.FILES["food_pic"]

                # Validate required fields
                if not all([recipe.title, recipe.description]):
                    raise ValidationError("Title and description are required.")

                # Validate numeric fields
                for field, value in [("preparation_time", recipe.preparation_time),
                                     ("servings", recipe.servings)]:
                    try:
                        float_value = float(value)
                        if float_value <= 0:
                            raise ValueError
                    except (ValueError, TypeError):
                        raise ValidationError(f"Invalid value for {field.replace('_', ' ')}")

                recipe.full_clean()
                recipe.save()

                # Update tags
                recipe.tags.clear()  # Remove existing tags

                # Add selected existing tags
                for tag_id in tag_ids:
                    if tag_id.strip():
                        try:
                            tag = Tag.objects.get(pk=tag_id)
                            recipe.tags.add(tag)
                        except Tag.DoesNotExist:
                            raise ValidationError(f"Invalid tag ID: {tag_id}")

                # Add new tags
                for tag_name in new_tag_names:
                    tag_name = tag_name.strip()
                    if tag_name:
                        tag, created = Tag.objects.get_or_create(name=tag_name)
                        recipe.tags.add(tag)

                # Update nutritional information directly since you're not using a form
                nutrition_info = recipe.nutrition_info
                nutrition_info.protein = request.POST.get("protein")
                nutrition_info.carb = request.POST.get("carb")
                nutrition_info.fat = request.POST.get("fat")
                nutrition_info.calories = request.POST.get("calories")

                try:
                    nutrition_info.full_clean()
                    nutrition_info.save()
                except ValidationError as e:
                    raise ValidationError(f"Invalid nutritional information: {str(e)}")

                messages.success(request, "Recipe updated successfully!")
                return redirect('recipe:detail', recipe_id=recipe_id)

        except ValidationError as e:
            messages.error(request, str(e))
            print(str(e))

        except Exception as e:
            logger.exception("Error updating recipe")
            messages.error(request, "An unexpected error occurred. Please try again.")

    # GET request or form validation failure

    ingredient_units = [
        ("g", "grams"),
        ("ml", "milliliters"),
        ("tsp", "teaspoons"),
        ("tbsp", "tablespoons"),
        ("cup", "cups"),
        ("piece", "pieces"),

    ]

    context = {
        "recipe": recipe,
        "nutrition_info": nutrition_info,
        "all_tags": Tag.objects.all().order_by("name"),
        "existing_tags": recipe.tags.all(),
        "ingredient_units": ingredient_units,
    }

    return render(request, "recipe/edit_recipe.html", context)


def edit_ingredients(request, recipe_id: int):
    recipe = Recipe.objects.get(pk=recipe_id)
    if request.method == "POST":
        print("submitted")

        existing_ingredients = request.POST.get('existing_ingredients', '').split(',')
        new_ingredients = request.POST.get('new_ingredients', '').split(',')
        quantities = request.POST.get('quantities', '').split(',')
        units = request.POST.get('units', '').split(',')

        # delet all ingredients of this recipe first
        RecipeIngredient.objects.filter(recipe=recipe).delete()

        # Process existing ingredients
        for i, ingredient_id in enumerate(existing_ingredients):
            if ingredient_id:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient_id=ingredient_id,
                    quantity=quantities[i],
                    unit=units[i]
                )

        # Process new ingredients
        for i, ingredient_name in enumerate(new_ingredients):
            if ingredient_name:
                # Create new ingredient
                ingredient = Ingredient.objects.create(name=ingredient_name)
                # Add to recipe
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    ingredient=ingredient,
                    quantity=quantities[i + len(existing_ingredients)],
                    unit=units[i + len(existing_ingredients)]
                )

        return redirect('recipe:detail', recipe_id=recipe_id)

    ingredient_units = [
        ("g", "grams"),
        ("ml", "milliliters"),
        ("tsp", "teaspoons"),
        ("tbsp", "tablespoons"),
        ("cup", "cups"),
        ("piece", "pieces"),

    ]

    print(RecipeIngredient.objects.filter(recipe=recipe))

    return render(request, "recipe/edit_ingredients.html",
                  {"recipe": recipe, "ingredients": Ingredient.objects.all().order_by("name"),
                   "ingredient_units": ingredient_units,
                   "recipe_ingredients": RecipeIngredient.objects.filter(recipe=recipe)})


def edit_instructions(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == "POST":
        instructions_json = request.POST.get('instructions', '[]')
        instructions = json.loads(instructions_json)

        # Clear existing instructions
        Instruction.objects.filter(recipe=recipe).delete()

        # Create new instructions
        for index, text in enumerate(instructions, 1):
            if text.strip():  # Only create if text is not empty
                Instruction.objects.create(
                    recipe=recipe,
                    step_no=index,
                    instruction=text
                )

        return redirect('recipe:detail', recipe_id=recipe.id)

    context = {
        'recipe': recipe,
        'recipe_instructions': recipe.instructions.all().order_by('step_no')
    }

    return render(request, 'recipe/edit_instructions.html', context)


@login_required
def delete(request, recipe_id: int):
    recipe = Recipe.objects.get(pk=recipe_id)
    recipe.delete()
    return redirect("users:profile")


# @login_required
def save(request, recipe_id: id):
    if request.method == "POST":
        recipe = Recipe.objects.get(pk=recipe_id)

        user = recipe.saved_by.all().filter(id=request.user.id).first()

        if user:
            recipe.saved_by.remove(user)
            isSaved = False
        else:
            recipe.saved_by.add(request.user)
            isSaved = True

        return JsonResponse({"isSaved": isSaved})


@login_required
def saved_recipe(request):
    # no need to use all()
    user = CustomUser.objects.get(pk=request.user.id)
    recipes = user.saved_recipes.all()

    rating_choices = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]

    return render(request, 'recipe/saved_recipe.html', {"saved_recipes": recipes})
