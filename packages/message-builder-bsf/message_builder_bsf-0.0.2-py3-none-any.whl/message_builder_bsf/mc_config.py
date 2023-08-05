# -*- coding: utf-8 -*-

KEYWORD_CONFIG = "media_center_configuration"
"""`str` : Keyword used in process dictionary to index a `MediaCenterConfig`."""


class MediaCenterConfig:
	"""Configuration for the Media Center.

	Parameters
	----------
	engine : {'hugo', 'grav'}
		Engine on which the Media Center will be built.
	template : `str`
		Theme template of the Media Center.
	languages : `list` of `str`
		List of languages that the Media Center supports.
	"""

	def __init__(self, engine, template, languages):

		self._engine = engine
		self._template = template
		self._languages = languages

	@property
	def engine(self):
		"""`str`: Engine of the media center.
		"""
		return self._engine

	@property
	def template(self):
		"""`str`: Template of the media center.
		"""
		return self._template

	@property
	def languages(self):
		"""`list` of `str`:Languages of the media center.
		"""
		return self._languages

	def to_dict(self):
		"""Get the `MediaCenterConfig` as dictionary.

		Returns
		-------
		dict : `dict`
			The `MediaCenterConfig` as dictionary with the following format:

			- ``'engine'``: Engine of the media center.
			- ``'template'``: Template of the media center.
			- ``'languages'``: List of languages of the media center.
		"""
		return {
			'engine': self._engine,
			'template': self._template,
			'languages': self._languages,
		}


class DictMediaCenterConfigDAO:
	"""Data Access Object to manage a `MediaCenterConfig` instances in dictionaries.
	"""

	@staticmethod
	def get_config(data):
		"""Get a `MediaCenterConfig` instance from given dictionary.

		Parameters
		----------
		data : `dict`
			Dictionary with the content of the `MediaCenterConfig`. Should have the next fields:

			- ``KEYWORD_CONFIG``: dictionary with the content of a `MediaCenterConfig`. Should have the next fields:

				- ``'engine'``: engine of the `MediaCenterConfig`.
				- ``'template'``: template of the `MediaCenterConfig`
				- ``'languages'``: list of languages of the `MediaCenterConfig`.

		Returns
		-------
		config : `MediaCenterConfig`
			The `MediaCenterConfig` result from parsing the ``data`` dictionary.

		Raises
		------
		Exception
			Raised if the constant ``KEYWORD_CONFIG`` is not in ``data`` keys.
		Exception
			Raised if the content in ``KEYWORD_CONFIG`` does not contains the correct format for a `MediaCenterConfig`.

		See Also
		--------
		factory_manager.models.mc_config.MediaCenterConfig
		factory_manager.models.mc_config.KEYWORD_CONFIG
		"""
		config_data = data.get(KEYWORD_CONFIG)
		if not all(key in config_data.keys() for key in ['engine', 'template', 'languages']):
			raise Exception("The data does not contains the correct format for a media center configuration.")

		engine = config_data.get('engine')
		template = config_data.get('template')
		languages = config_data.get('languages')

		return MediaCenterConfig(engine, template, languages)
