# -*- coding: utf-8 -*-

from .omeka_project import OmekaProject, DictProjectDAO, KEYWORD_PROJECT
from .mc_config import MediaCenterConfig, DictMediaCenterConfigDAO, KEYWORD_CONFIG
from .recipe import Recipe, DictRecipeDAO, KEYWORD_RECIPE

KEYWORD_PROCESS = "process"
"""`str` : Keyword used in dictionary to index a `Process`."""


class Process:
	"""Process for the execution.

	Parameters
	----------
	process_id : `str`
		Id of the `Process`.
	recipe : `Recipe`
		Current recipe in execution.
	project : `OmekaProject`
		Omeka Project to build.
	config : `MediaCenterConfig`
		Configuration for the creation of the Media Center.

	Raises
	------
	TypeError
		Raised if any arguments for the `Process` is not the expected type.

	See Also
	--------
	factory_manager.models.recipe.Recipe
	factory_manager.models.omeka_project.OmekaProject
	factory_manager.models.mc_config.MediaCenterConfig
	"""

	def __init__(self, process_id, recipe, project, config):
		if not isinstance(recipe, Recipe) or not isinstance(project, OmekaProject) or not isinstance(config, MediaCenterConfig):
			raise TypeError("Invalid arguments type for Process.")

		self._id = process_id
		self._recipe = recipe
		self._project = project
		self._config = config

	@property
	def id(self):
		"""`str`: Id of the process.
		"""
		return self._id

	@property
	def recipe(self):
		"""`Recipe`: Current `Recipe` of the process.
		"""
		return self._recipe

	@recipe.setter
	def recipe(self, value):
		self._recipe = value

	@property
	def project(self):
		"""`OmekaProject`: Current `OmekaProject` of the process.
		"""
		return self._project

	@property
	def config(self):
		"""`MediaCenterConfig`: Current `MediaCenterConfig` of the process.
		"""
		return self._config

	def next_factory(self, factory_name):
		"""Get the name of the next factory in the `Recipe`.

		Parameters
		----------
		factory_name : `str`
			Name of the factory in execution.

		Returns
		-------
		next_factory : `str`
			Name of the next factory to execute.

		Notes
		-----
		Check in the process recipe for the ``factory_name`` position and returns the factory name placed next.
		Do not use when the `Recipe` includes multiple times the same factory name.
		"""
		current = self._recipe.factories.index(factory_name)
		return self._recipe.get_factory_by_index(current + 1)

	def to_dict(self):
		"""Get the `Process` as dictionary.

		Returns
		-------
		dict : `dict`
			The `Process` as dictionary with the following format:

			- ``'id'``: id of the `Process`.
			- ``KEYWORD_RECIPE``: dictionary of current `Recipe` of the process.
			- ``KEYWORD_PROJECT``: dictionary of current `OmekaProject` of the process.
			- ``KEYWORD_CONFIG``: dictionary of current `MediaCenterConfig` of the process.

		See Also
		--------
		factory_manager.models.recipe.KEYWORD_RECIPE
		factory_manager.models.omeka_project.KEYWORD_PROJECT
		factory_manager.models.mc_config.KEYWORD_CONFIG
		"""
		return {
			'id': self._id,
			KEYWORD_RECIPE: self._recipe.to_dict(),
			KEYWORD_PROJECT: self._project.to_dict(),
			KEYWORD_CONFIG: self._config.to_dict()
		}


class DictProcessDAO:
	"""Data Access Object to manage a `Process` instances in dictionaries.
	"""

	@staticmethod
	def get_process(data):
		"""Get a `Process` instance from given dictionary.

		Parameters
		----------
		data : `dict`
			Dictionary with the content of the `Process`. Should have the next fields:

			- ``KEYWORD_PROCESS``: dictionary with the content of a `Process`. Should have the next fields:

				- ``'id'``: id of the `Process`.
				- ``KEYWORD_RECIPE``: dictionary with the content of a `Recipe`.
				- ``KEYWORD_PROJECT``: dictionary with the content of a `OmekaProject`.
				- ``KEYWORD_CONFIG``: dictionary with the content of a `MediaCenterConfig`.

		Returns
		-------
		process : `Process`
			The `Process` result from parsing the ``data`` dictionary.

		Raises
		------
		Exception
			Raised if the constant ``KEYWORD_PROCESS`` is not in ``data`` keys.
		Exception
			Raised if the content in ``KEYWORD_PROCESS`` does not contains the correct format for a `Process`.

		See Also
		--------
		factory_manager.models.process.Process
		factory_manager.models.recipe.KEYWORD_RECIPE
		factory_manager.models.omeka_project.KEYWORD_PROJECT
		factory_manager.models.mc_config.KEYWORD_CONFIG
		"""
		if KEYWORD_PROCESS not in data:
			raise Exception("Missing '{}' in dictionary.".format(KEYWORD_PROCESS))

		process_data = data.get(KEYWORD_PROCESS)
		if not all(key in process_data.keys() for key in ['id', KEYWORD_RECIPE, KEYWORD_PROJECT, KEYWORD_CONFIG]):
			raise Exception("The data does not contains the correct format for a process.")

		process_id = process_data.get('id')
		recipe = DictRecipeDAO.get_recipe(process_data)
		project = DictProjectDAO.get_project_extended(process_data)
		config = DictMediaCenterConfigDAO.get_config(process_data)

		return Process(process_id, recipe, project, config)

	@staticmethod
	def update_process(data, process):
		"""Update in the given dictionary a `Process`.

		Parameters
		----------
		data : `dict`
			Dictionary to update in ``KEYWORD_PROCESS`` key.
		process : `Process`
			Content to update in ``data`` in ``KEYWORD_PROCESS`` key.

		See Also
		--------
		factory_manager.models.process.Process
		"""
		if not isinstance(process, Process):
			raise TypeError("The content type to update in the dictionary must be a Process.")
		data[KEYWORD_PROCESS] = process.to_dict()
