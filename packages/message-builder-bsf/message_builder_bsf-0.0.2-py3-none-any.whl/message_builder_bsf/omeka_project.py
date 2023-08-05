# -*- coding: utf-8 -*-

KEYWORD_PROJECT = "project"
"""`str` : Keyword used in process dictionary to index a `OmekaProject`."""


class OmekaProject:
	"""Representation of a project in Omeka.

	Parameters
	----------
	project_id : `int`
		Id of the `ProjectOmeka`.
	name : `str`
		Name of the project.
	title : `str`, optional
		Title of the project ("no title", by default).
	description : `str`, optional
		Description of the project ("no description", by default).
	language : `str`, optional
		Language of the project ("fr", by default).
	device : `str`, optional
		Device name of the project ("koombook", by default).
	"""

	def __init__(self, project_id, name, title=None, description=None, language=None, device=None):

		self._id = project_id
		self._name = name

		self._title = "no title" if title is None else title
		self._description = "no description" if description is None else description
		self._language = "fr" if language is None else language
		self._device = "koombook" if device is None else device

	@property
	def id(self):
		"""`int`: Id of the project.
		"""
		return self._id

	@property
	def name(self):
		"""`str`: Name of the project.
		"""
		return self._name

	@property
	def title(self):
		"""`str`: Title of the project.
		"""
		return self._title

	@title.setter
	def title(self, value):
		self._title = value

	@property
	def description(self):
		"""`str`: Description of the project.
		"""
		return self._description

	@description.setter
	def description(self, value):
		self._description = value

	@property
	def language(self):
		"""`str`: Language of the project.
		"""
		return self._language

	@language.setter
	def language(self, value):
		self._language = value

	@property
	def device(self):
		"""`str`: Device name of the project.
		"""
		return self._device

	@device.setter
	def device(self, value):
		self._device = value

	def to_dict(self):
		"""Get the `OmekaProject` as dictionary.

		Returns
		-------
		dict : `dict`
			The `OmekaProject` as dictionary with the following format:

			- ``'id'``: Id of the project.
			- ``'name'``: Name of the project.
			- ``'title'``: Title of the project.
			- ``'description'``: Description of the project.
			- ``'language'``: Language of the project.
			- ``'device'``: Device name of the project.
		"""
		return {
			'id': self._id,
			'name': self._name,
			'title': self._title,
			'description': self._description,
			'language': self._language,
			'device': self._device
		}


class DictProjectDAO:
	"""Data Access Object to manage a `OmekaProject` instances in dictionaries.
	"""

	@staticmethod
	def get_project_base(data):
		"""Get an `OmekaProject` instance by given minimal information inside dictionary.

		Parameters
		----------
		data : `dict`
			Dictionary with the content of the `OmekaProject`. Should have the next fields:

			- ``'project_id'``: id of the `OmekaProject`.
			- ``'project_name'``: name of the `OmekaProject`.

		Returns
		-------
		project : `OmekaProject`
			The `OmekaProject` with the minimal information by result from parsing the given dictionary.

		Raises
		------
		Exception
			Raised if ``'project_id'`` or ``'project_name'`` are not in ``data`` keys.

		See Also
		--------
		factory_manager.models.omeka_project.OmekaProject
		"""
		if not all(key in data.keys() for key in ['project_id', 'project_name']):
			raise Exception("The data does not contains the correct format for a project.")

		project_id = data.get('project_id')
		name = data.get('project_name')

		return OmekaProject(project_id, name)

	@staticmethod
	def get_project_extended(data):
		"""Get a `OmekaProject` instance from given dictionary.

		Parameters
		----------
		data : `dict`
			Dictionary with the content of the `OmekaProject`. Should have the next fields:

			- ``KEYWORD_PROJECT``: dictionary with the content of a `Process`. Should have the next fields:

				- ``'id'``: id of the `OmekaProject`.
				- ``'name'``: name of the `OmekaProject`
				- ``'title'``: title of the `OmekaProject`.
				- ``'description'``: description of the `OmekaProject`.
				- ``'language'``: language of the `OmekaProject`.
				- ``'device'``: device name of the `OmekaProject`.

		Returns
		-------
		project : `OmekaProject`
			The `OmekaProject` result from parsing the ``data`` dictionary.

		Raises
		------
		Exception
			Raised if the constant ``KEYWORD_PROJECT`` is not in ``data`` keys.
		Exception
			Raised if the content in ``KEYWORD_PROJECT`` does not contains the correct format for a `OmekaProject`.

		See Also
		--------
		factory_manager.models.omeka_project.OmekaProject
		factory_manager.models.omeka_project.KEYWORD_PROJECT
		"""
		project_data = data.get(KEYWORD_PROJECT)
		if not all(key in project_data.keys() for key in ['id', 'name', 'title', 'description', 'language', 'device']):
			raise Exception("The data does not contains the correct format for a project.")

		project_id = project_data.get('id')
		name = project_data.get('name')

		title = project_data.get('title')
		description = project_data.get('description')
		language = project_data.get('language')
		device = project_data.get('device')

		return OmekaProject(project_id, name, title, description, language, device)
