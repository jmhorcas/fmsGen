import shutil
import tempfile
from enum import Enum
from typing import Any
from abc import ABC, abstractmethod

from language_constructs.models import FMGenerator, SerializationFormat
from language_constructs.models.constructs import (
    OptionalFeature, 
    MandatoryFeature, 
    XorGroup,
    OrGroup,
    XorChildFeature,
    OrChildFeature,
    RequiresConstraint,
    ExcludesConstraint
)

from celery import shared_task 


class ConfigParam(ABC):
    """It defines the configuration parameters."""

    def __init__(self, 
                 title: str = None,
                 default_value: Any = None,
                 description: str = None) -> None:
        self.title = title
        self.description = description
        self._default_value = default_value
        self._value: Any = self._parse_value(default_value)

    @property
    def value(self) -> Any:
        return self._value
    
    @value.setter
    def value(self, value: Any) -> None:
        self._value = self._parse_value(value)

    @abstractmethod
    def _parse_value(self, value: Any) -> Any:
        pass

    def to_dict(self) -> dict[str, Any]:
        return {'title': self.title, 'value': self.value, 'description': self.description}


class StrConfigParam(ConfigParam):

    def _parse_value(self, value: Any) -> str:
        return self._default_value if value is None else str(value)


class IntConfigParam(ConfigParam):

    def _parse_value(self, value: Any) -> int:
        return self._default_value if value is None else int(value)


class FloatConfigParam(ConfigParam):

    def _parse_value(self, value: Any) -> float:
        return self._default_value if value is None else float(value)


class CheckBoxConfigParam(ConfigParam):

   def _parse_value(self, value: Any) -> bool:
        return value is not None and str(value).lower() in ['on', 'true']


class AnyConfigParam(ConfigParam):

   def _parse_value(self, value: Any) -> bool:
        return value
   

class NoneConfigParam(ConfigParam):

   def _parse_value(self, value: Any) -> bool:
        return None
   

class Params(Enum):
    # Visible configurable options
    # Basic configs
    NUM_MODELS = IntConfigParam('#Models', 10, 'Number of models to be generated (minimum 1).')
    MODEL_NAME_PREFIX = StrConfigParam('Name/Prefix', 'fm', 'Name or prefix of the model.')
    INCLUDE_NUMFEATURES_PREFIX = CheckBoxConfigParam("Include #Features as name's sufix", True, "Models' names ends with '_Xf' where X is the number of features.")
    INCLUDE_NUMCONSTRAINTS_PREFIX = CheckBoxConfigParam("Include #Constraints as name's sufix", True, "Models' names ends with '_Xc' where X is the number of constraints.")
    
    ##########
    # Advanced configs
    FEATURES = NoneConfigParam('#Features', None, 'Features of the model.')
    MIN_NUM_FEATURES = IntConfigParam('Minimum number of features', 10, 'Minimum number of features.')
    MAX_NUM_FEATURES = IntConfigParam('Maximum number of features', 10, 'Maximum number of features.')
    UNIFORM_NUM_FEATURES = CheckBoxConfigParam('Uniform number of features', False, 'Generate the models with a uniform number of features between min and max (default random).')
    MIN_NUM_CONSTRAINTS = IntConfigParam('#Constraints min', 1, 'Minimum number of constraints.')
    MAX_NUM_CONSTRAINTS = IntConfigParam('max', 1, 'Maximum number of constraints.')
    UNIFORM_NUM_CONSTRAINTS = CheckBoxConfigParam('Uniform number of constraints', False, 'Generate the models with a uniform number of constraints between min and max (default random).')
    # Abstract features
    ABSTRACT_FEATURES = CheckBoxConfigParam('Abstract features', False, 'Include abstract features.')
    NUM_ABSTRACT_FEATURES = IntConfigParam('', 0, 'Number of abstract features.')
    PERCENTAGE_ABSTRACT_FEATURES = IntConfigParam('', 0, 'Percentage of abstract features.')
    ABSTRACT_LEAF_FEATURES = CheckBoxConfigParam('Allow abstract leaf features', False, 'Leaf features can be abstract too.')
    INTERNAL_ABSTRACT_FEATURES = CheckBoxConfigParam('Make all internal features abstract', False, 'All non-leaf features will be abstract features.')
    ROOT_ABSTRACT_FEATURE = CheckBoxConfigParam('Make the root abstract', False, 'The root feature is always abstract.')
    # Formats
    UVL = CheckBoxConfigParam('UVL', True, 'Universal Variability Language (.uvl).')
    GLENCOE = CheckBoxConfigParam('Glencoe', False, 'Glencoe (.gfm.json).')
    SPLOT = CheckBoxConfigParam('SPLOT', False, 'S.P.L.O.T. (.sxfm).')

    ##########
    # Non-visible configurable options
    SERIALIZATION_TEMPORAL_DIR = StrConfigParam('Temporal dir', 'tmp/generated', 'Temporal directory used for generating the models.')
    TASK_ID = StrConfigParam('Task id', None, 'Task id for long running task of generating models.')
    ZIP_FILE = StrConfigParam('Zip file', None, 'Zip file containing all generated models.')
    ZIP_FILENAME = StrConfigParam('Zip filename', None, 'Name of the zip file containing all generated models.')


@shared_task(ignore_result=False, bind=True)
def generate_feature_models(self, config_params: dict[dict[str, Any]]) -> dict[dict[str, Any]]:
    tree_lcs = [OptionalFeature, MandatoryFeature, XorGroup, OrGroup, XorChildFeature, OrChildFeature]
    constraints_lcs = [RequiresConstraint, ExcludesConstraint]

    #serialization_formats = [format for format in SerializationFormat if config_params[format.name]['value']]
    serialization_formats = dict()
    with tempfile.TemporaryDirectory() as temp_dir:
        # Prepare serialization paths
        config_params[Params.SERIALIZATION_TEMPORAL_DIR.name] = Params.SERIALIZATION_TEMPORAL_DIR.value.to_dict()
        config_params[Params.SERIALIZATION_TEMPORAL_DIR.name]['value'] = temp_dir
        for format in SerializationFormat:
            if config_params[format.name]['value']:
                output_path = tempfile.mkdtemp(prefix=f'{format.name.lower()}_', dir=temp_dir)
                serialization_formats[format] = output_path
        # Create and configure FMGenerator instance
        fm_gen = FMGenerator(tree_language_constructs=tree_lcs,
                            constraints_language_constructs=constraints_lcs)
        fm_gen.set_serialization(models_name_prefix=config_params[Params.MODEL_NAME_PREFIX.name]['value'], 
                                dir=temp_dir,
                                formats=serialization_formats,
                                include_num_features=config_params[Params.INCLUDE_NUMFEATURES_PREFIX.name]['value'],
                                include_num_constraints=config_params[Params.INCLUDE_NUMCONSTRAINTS_PREFIX.name]['value'])
        fm_gen.set_features(min_num_features=config_params[Params.MIN_NUM_FEATURES.name]['value'],
                            max_num_features=config_params[Params.MAX_NUM_FEATURES.name]['value'],
                            uniform_num_features=config_params[Params.UNIFORM_NUM_FEATURES.name]['value'])
        fm_gen.set_abstract_features(num_abstract_features=config_params[Params.NUM_ABSTRACT_FEATURES.name]['value'],
                                    make_root_abstract=config_params[Params.ROOT_ABSTRACT_FEATURE.name]['value'],
                                    make_all_internal_features_abstract=config_params[Params.INTERNAL_ABSTRACT_FEATURES.name]['value'],
                                    allow_abstract_leaf_features=config_params[Params.ABSTRACT_LEAF_FEATURES.name]['value'])
        fm_gen.set_constraints(min_num_constraints=config_params[Params.MIN_NUM_CONSTRAINTS.name]['value'],
                            max_num_constraints=config_params[Params.MAX_NUM_CONSTRAINTS.name]['value'],
                            uniform_num_constraints=config_params[Params.UNIFORM_NUM_CONSTRAINTS.name]['value'])
        fm_gen.generate_n_fms(n_models=config_params[Params.NUM_MODELS.name]['value'], celery_task=self)

        temp_file = tempfile.NamedTemporaryFile(mode='w', encoding='utf8')
        temp_zipfile = shutil.make_archive(temp_file.name, 'zip', temp_dir)
        zip_filename = f"{config_params[Params.MODEL_NAME_PREFIX.name]['value']}{config_params[Params.NUM_MODELS.name]['value']}.zip"
        config_params[Params.ZIP_FILE.name]['value'] = temp_zipfile
        config_params[Params.ZIP_FILENAME.name]['value'] = zip_filename
    return config_params
