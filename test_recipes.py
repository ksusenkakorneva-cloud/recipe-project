import pytest
from recipes import Ingredient, Recipe, DietaryRecipe


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
