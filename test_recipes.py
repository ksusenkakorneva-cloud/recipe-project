import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_creation():
    ingredient = Ingredient("Питахая", 500, "г")
    assert ingredient.name == "Питахая"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Питахая", 500, "г")
    assert str(ingredient) == "Питахая: 500.0 г"


def test_ingredient_eq():
    first_ingredient = Ingredient("Питахая", 500, "г")
    second_ingredient = Ingredient("Питахая", 600, "г")
    third_ingredient = Ingredient("Арбуз", 5000, "г")
    assert first_ingredient == second_ingredient
    assert first_ingredient != third_ingredient


def test_ingredient_negative_quantity():
    with pytest.raises(ValueError):
        Ingredient("Питахая", -100, "г")



def test_recipe_creation():
    ingredient = Ingredient("Мука", 500, "г")
    recipe = Recipe("Лазанья", [ingredient])
    assert recipe.title == "Лазанья"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Мука"


def test_recipe_add_new_ingredient():
    recipe = Recipe("Лазанья")
    recipe.add_ingredient(Ingredient("Листы для лазаньи", 250, "г"))
    assert len(recipe) == 1
    assert recipe.ingredients[0].name == "Листы для лазаньи"
    assert recipe.ingredients[0].quantity == 250.0


def test_recipe_add_existing_ingredient():
    recipe = Recipe("Лазанья")
    recipe.add_ingredient(Ingredient("Масло сливочное", 60, "г"))
    recipe.add_ingredient(Ingredient("Масло сливочное", 30, "г"))
    assert len(recipe) == 1
    assert recipe.ingredients[0].quantity == 90.0


def test_recipe_scale():
    recipe = Recipe("Лазанья")
    recipe.add_ingredient(Ingredient("Фарш мясной говяжий", 450, "г"))
    recipe.add_ingredient(Ingredient("Молоко", 800, "мл"))
    scaled_recipe = recipe.scale(2)
    assert scaled_recipe.title == "Лазанья"
    assert scaled_recipe.ingredients[0].quantity == 900.0
    assert scaled_recipe.ingredients[1].quantity == 1600.0
    assert recipe.ingredients[0].quantity == 450.0
    assert recipe.ingredients[1].quantity == 800.0


def test_recipe_scale_invalid_ratio():
    recipe = Recipe("Лазанья")
    with pytest.raises(ValueError):
        recipe.scale(0)


def test_recipe_len():
    recipe = Recipe("Лазанья")
    recipe.add_ingredient(Ingredient("Листы для лазаньи", 250, "г"))
    recipe.add_ingredient(Ingredient("Фарш мясной говяжий", 450, "г"))
    assert len(recipe) == 2



def test_shopping_list_add_recipe():
    recipe = Recipe("Лазанья")
    recipe.add_ingredient(Ingredient("Листы для лазаньи", 250, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Листы для лазаньи"
    assert result[0].quantity == 500.0


def test_shopping_list_add_recipe_invalid_portions():
    recipe = Recipe("Лазанья")
    shopping_list = ShoppingList()
    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    lasagna = Recipe("Лазанья")
    lasagna.add_ingredient(Ingredient("Листы для лазаньи", 250, "г"))
    soup = Recipe("Суп")
    soup.add_ingredient(Ingredient("Картофель", 3, "шт."))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(lasagna, 1)
    shopping_list.add_recipe(soup, 1)
    shopping_list.remove_recipe("Лазанья")
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Картофель"


def test_shopping_list_get_list_sums_same_ingredients():
    lasagna = Recipe("Лазанья")
    lasagna.add_ingredient(Ingredient("Морковь", 1, "шт."))
    soup = Recipe("Суп")
    soup.add_ingredient(Ingredient("Морковь", 2, "шт."))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(lasagna, 1)
    shopping_list.add_recipe(soup, 1)
    result = shopping_list.get_list()
    assert len(result) == 1
    assert result[0].name == "Морковь"
    assert result[0].quantity == 3.0


def test_shopping_list_get_list_sorted():
    recipe = Recipe("Лазанья")
    recipe.add_ingredient(Ingredient("Сыр пармезан", 120, "г"))
    recipe.add_ingredient(Ingredient("Мука", 60, "г"))
    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)
    result = shopping_list.get_list()
    assert result[0].name == "Мука"
    assert result[1].name == "Сыр пармезан"


def test_shopping_list_add_operator():
    first_list = ShoppingList()
    second_list = ShoppingList()
    lasagna = Recipe("Лазанья")
    lasagna.add_ingredient(Ingredient("Мука", 60, "г"))
    soup = Recipe("Суп")
    soup.add_ingredient(Ingredient("Картофель", 3, "шт."))
    first_list.add_recipe(lasagna, 1)
    second_list.add_recipe(soup, 1)
    result_list = first_list + second_list
    result = result_list.get_list()
    assert len(result) == 2
    assert len(first_list.get_list()) == 1
    assert len(second_list.get_list()) == 1