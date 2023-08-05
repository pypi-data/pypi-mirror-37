# -*- coding: utf-8 -*-
"""Recipe documentation.
"""

import os
import json

KEYWORD_RECIPE = "recipe"
"""`str` : Keyword used in process dictionary to index a `Recipe`."""


class Recipe:
	"""Recipe that contains factories order of execution.

	Parameters
	----------
	recipe_id : `int`
		Id of the `Recipe`.
	factories : `list` of `str`, optional
		Name of the factories in `Recipe` (empty list, by default).

	Raises
	------
	TypeError
		Raised if any arguments for the `Recipe` is not the expected type.

	Notes
	-----
	The names of the factories inside ``factories`` should not have repeated factories names; to avoid problems in the
	process execution.
	"""

	def __init__(self, recipe_id, factories=None):
		if not isinstance(recipe_id, int) or (factories and not all(isinstance(f, str) for f in factories)):
			raise TypeError("Invalid arguments type for Recipe.")

		self._id = recipe_id
		self._factories_list = [] if factories is None else factories

	@property
	def id(self):
		"""`int`: Id of the recipe.
		"""
		return self._id

	@property
	def factories(self):
		"""`list` of `str`: List of factories names in recipe.
		"""
		return self._factories_list

	def get_factory_by_index(self, index):
		"""Get the name of the factory in the ``index`` position.

		Parameters
		----------
		index : `int`
			Position of the requested factory.

		Returns
		-------
		factory_name : `str`
			Name of the factory in the ``index`` position. ``None`` in case of invalid index.
		"""
		if 0 <= index < len(self._factories_list):
			return self._factories_list[index]
		return None

	def to_dict(self):
		"""Get the `Recipe` as dictionary.

		Returns
		-------
		dict : `dict`
			The `Recipe` as dictionary with the following format:

			- ``'id'``: id of the `Recipe`.
			- ``'factories'``: list of factories names.
		"""
		return {
			"id": self._id,
			"factories": self._factories_list
		}


class DictRecipeDAO:
	"""Data Access Object to manage a `Recipe` instances in dictionaries.
	"""

	@staticmethod
	def get_recipe(data):
		"""Get a `Process` instance from given dictionary.

		Parameters
		----------
		data : `dict`
			Dictionary with the content of the `Process`. Should have the next fields:

			- ``KEYWORD_RECIPE``: dictionary with the content of a `Recipe`. Should have the next fields:

				- ``'id'``: id of the `Recipe`.
				- ``'factories'``: list of factories names.

		Returns
		-------
		recipe : `Recipe`
			The `Recipe` result from parsing the ``data`` dictionary.

		Raises
		------
		Exception
			Raised if the constant ``KEYWORD_RECIPE`` is not in ``data`` keys.
		Exception
			Raised if the content in ``KEYWORD_RECIPE`` does not contains the correct format for a `Recipe`.

		See Also
		--------
		factory_manager.models.recipe.KEYWORD_RECIPE
		"""
		if KEYWORD_RECIPE not in data:
			raise Exception("Missing '{}' keyword in dictionary.".format(KEYWORD_RECIPE))

		recipe_data = data.get(KEYWORD_RECIPE)
		if not all(key in recipe_data.keys() for key in ['id', 'factories']):
			raise Exception("The data does not contains the correct format for a recipe.")

		recipe_id = recipe_data.get('id')
		factories = recipe_data.get('factories')

		return Recipe(recipe_id, factories)


class Recipes:
	"""Collection of `Recipe` instances.

	Parameters
	----------
	recipes : `list` of `Recipe`, optional
		Content of the `Recipes` (empty list, by default).

	Raises
	------
	TypeError
		Raised if any arguments for the `Recipes` is not the expected type.

	See Also
	--------
	factory_manager.models.recipe.Recipe
	"""

	def __init__(self, recipes=None):
		if recipes and not all(isinstance(r, Recipe) for r in recipes):
			raise TypeError("Invalid arguments type for Recipes.")

		self._recipes_list = [] if recipes is None else recipes

	def add_recipe(self, recipe):
		"""Add a `Recipe` at the end of the collection.

		Parameters
		----------
		recipe : `Recipe`
			Recipe to add to the collection.

		Raises
		------
		TypeError
			Raised if ``recipe`` is not an instance of `Recipe`.
		Exception
			Raised if in the collection exist already a `Recipe` with the same id as ``recipe``.
		"""
		if not isinstance(recipe, Recipe):
			raise TypeError("Invalid arguments type to add.")
		if any(recipe.id == r.id for r in self._recipes_list):
			raise Exception("Existing conflict between recipes with same id.")

		self._recipes_list.append(recipe)

	def get_recipe_by_id(self, recipe_id):
		"""Get the `Recipe` inside the collection by id.

		Parameters
		----------
		recipe_id : `int`
			Id of the recipe to search.

		Returns
		-------
		recipe : `Recipe`
			Recipe with the corresponding ``recipe_id`` if it is in the collection. ``None`` if it is not.
		"""
		for recipe in self._recipes_list:
			if recipe.id == recipe_id:
				return recipe
		return None


class FileRecipesDAO:
	"""Data Access Object to manage a `Recipes` instances in json formatted file.
	"""

	@staticmethod
	def get_recipes(path):
		"""Get a `Recipes` instance from given file in ``path``.

		Parameters
		----------
		path : `str`
			Path of the recipes file, to parse into `Recipes`.

		Returns
		-------
		recipes : `Recipes`
			The Recipes obtained from parsing the file in given ``path``.

		Raises
		------
		Exception
			Raised if the file in ``path`` does not exists.
		Exception
			Raised if the file cannot be opened for reading.
		Exception
			Raised if the content of the file does not have the json format.

		See Also
		--------
		factory_manager.models.recipe.Recipes
		"""
		recipes = Recipes()

		if not os.path.exists(path):
			raise Exception("The recipes file {} does not exist.".format(path))

		try:
			with open(path, 'r') as file:
				try:
					data = json.load(file)
				except ValueError:
					raise Exception("The file {} does not contains a valid json format.".format(path))

				for elem in data:
					if not all(key in elem.keys() for key in ['id', 'recipe']):
						raise Exception("The file in {} does not contains the correct format for a recipe.".format(path))

					recipe_id = elem.get('id')
					factories = elem.get('recipe')

					recipes.add_recipe(Recipe(recipe_id, factories))

		except IOError:
			raise Exception("Cannot open the recipes file {}.".format(path))

		return recipes
