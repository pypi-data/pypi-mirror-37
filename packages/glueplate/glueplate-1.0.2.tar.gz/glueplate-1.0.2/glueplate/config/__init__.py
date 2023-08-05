import os
import logging
from importlib import import_module
from .. import GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY, GLUE_PLATE_PARENT_MODULES


logger = logging.getLogger(__name__)

ENVIRONMENT_VARIABLE = 'GLUE_PLATE_MODULE'

def _merge_parents(settings):
    if GLUE_PLATE_PARENT_MODULES in settings:
        for parent_module_name in settings.GLUE_PLATE_PARENT_MODULES:
            parent_settings = import_module(parent_module_name).settings
            if GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY in parent_settings:
                if parent_settings.GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY in os.environ:
                    parent_child = os.environ[parent_settings.GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY]
                    _child = import_module(parent_child).settings
                    parent_settings.update(_child)
                    if GLUE_PLATE_PARENT_MODULES in parent_settings:
                        parent_settings = _merge_parents(parent_settings)
            parent_settings.update(settings)
            settings = parent_settings
    return settings

if __name__ == 'glueplate.config':
    if not os.environ.get('GLUE_PLATE_BASE_MODULE', None):
        raise ValueError("need glueplate's GLUE_PLATE_BASE_MODULE in environment.")
    base_module_name = os.environ['GLUE_PLATE_BASE_MODULE']
    logger.info('Load base glueplate config: {0}'.format(base_module_name))
    settings = import_module(base_module_name).settings
    if GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY not in settings:
        raise ValueError("neet GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY in base config settings.")
    settings = _merge_parents(settings)
    modified_module_name = os.environ[settings.GLUE_PLATE_ENVIRONMENT_VARIABLE_KEY]
    _settings = import_module(modified_module_name).settings
    settings.update(_settings)
