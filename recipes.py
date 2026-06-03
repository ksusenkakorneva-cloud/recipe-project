class Ingredient:
    def __init__(self, name, quantity, unit):
        self.name = name
        self.quantity = quantity
        self.unit = unit


    @property
    def quantity(self):
        return self._quantity


    @quantity.setter
    def quantity(self, value):
        value = float(value)
        if value <= 0:
            raise ValueError("Количество ингредиента должно быть положительным")
        self._quantity = value


    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"
    

    def __repr__(self):
        return f"Ingredient('{self.name}', {self.quantity}, '{self.unit}')"


    def __eq__(self, other):
        if not isinstance(other, Ingredient):
            return False
        return self.name == other.name and self.unit == other.unit



class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        self.ingredients = []
        if ingredients is not None:
            for ingredient in ingredients:
                self.add_ingredient(ingredient)


    def add_ingredient(self, ingredient):
        for existing_ingredient in self.ingredients:
            if existing_ingredient == ingredient:
                existing_ingredient.quantity += ingredient.quantity
                return
        self.ingredients.append(
            Ingredient(ingredient.name, ingredient.quantity, ingredient.unit)
        )
    

    @staticmethod
    def is_valid_ratio(ratio):
        if isinstance(ratio, (int, float)) and ratio > 0:
            return True
        else:
            return False


    def scale(self, ratio):
        if not Recipe.is_valid_ratio(ratio):
            raise ValueError("Коэффициент должен быть положительным")
        scaled_ingredients = []
        for ingredient in self.ingredients:
            scaled_ingredients.append(
                Ingredient(
                    ingredient.name,
                    ingredient.quantity * ratio,
                    ingredient.unit
                )
            )
        return Recipe(self.title, scaled_ingredients)
    

    def __len__(self):
        return len(self.ingredients)
    

    def __str__(self):
        result = self.title + "\n"
        for ingredient in self.ingredients:
            result += f"- {ingredient}\n"
        return result.strip()



class ShoppingList:
    def __init__(self):
        self._items = []


    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть положительным")
        scaled_recipe = recipe.scale(portions)
        for ingredient in scaled_recipe.ingredients:
            self._items.append((ingredient, recipe.title))


    def remove_recipe(self, title):
        new_items = []
        for ingredient, recipe_title in self._items:
            if recipe_title != title:
                new_items.append((ingredient, recipe_title))
        self._items = new_items


    def get_list(self):
        result = {}
        for ingredient, recipe_title in self._items:
            key = (ingredient.name, ingredient.unit)
            if key in result:
                result[key] += ingredient.quantity
            else:
                result[key] = ingredient.quantity
        shopping_ingredients = []
        for key in result:
            name = key[0]
            unit = key[1]
            quantity = result[key]
            new_ingredient = Ingredient(name, quantity, unit)
            shopping_ingredients.append(new_ingredient)
        shopping_ingredients.sort(key=lambda ingredient: ingredient.name)
        return shopping_ingredients


    def __add__(self, other):
        new_shopping_list = ShoppingList()
        for ingredient, recipe_title in self._items:
            new_shopping_list._items.append((ingredient, recipe_title))
        for ingredient, recipe_title in other._items:
            new_shopping_list._items.append((ingredient, recipe_title))
        return new_shopping_list
    


class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type


    def scale(self, ratio):
        scaled_recipe = super().scale(ratio)
        dietary_recipe = DietaryRecipe(
            scaled_recipe.title,
            self.diet_type,
            scaled_recipe.ingredients
        )
        return dietary_recipe


    def __str__(self):
        return f"[{self.diet_type}] {super().__str__()}"