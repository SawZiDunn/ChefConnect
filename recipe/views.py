from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.core.exceptions import ValidationError
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

    return render(request, "recipe/detail.html",
                  {"recipe": recipe, "ingredients": ingredients, "instructions": instructions,
                   "nutrition_info": nutrition_info, "tags": tags, "reviews": recipe.reviews.all(),
                   "like_count": recipe.likes.count(),
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
    existing_tags = recipe.tags.all()  # Tag.objects.filter(recipe=recipe)
    all_tags = Tag.objects.all()

    return render(request, "recipe/edit_recipe.html",
                  {"recipe": recipe, "ingredients": ingredients, "instructions": instructions,
                   "nutrition_info": nutrition_info, "all_tags": all_tags, "existing_tags": existing_tags})


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
    recipes = Recipe.objects.filter(isSaved=True)

    rating_choices = [
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    ]

    return render(request, 'recipe/saved_recipe.html', {"recipes": recipes})
