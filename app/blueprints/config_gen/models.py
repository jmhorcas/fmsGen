import os
from enum import Enum
import shutil
import tempfile
from typing import Any
from abc import ABC, abstractmethod

import flask

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLWriter

from language_constructs.models import FMLanguage, FMGenerator
from language_constructs.models.constructs import (
    FeatureModelConstruct, 
    RootFeature, 
    OptionalFeature, 
    MandatoryFeature, 
    XorGroup,
    OrGroup,
    XorChildFeature,
    OrChildFeature,
    RequiresConstraint,
    ExcludesConstraint
)


class ConfigParam(ABC):
    """It defines the configuration parameters."""

    def __init__(self, default_value: Any) -> None:
        self._value: Any = default_value
        self._default_value = self._parse_value(default_value)

    @property
    def value(self) -> Any:
        return self._value
    
    @value.setter
    def value(self, value: Any) -> None:
        self._value = self._parse_value(value)

    @abstractmethod
    def _parse_value(self, value: Any) -> Any:
        pass


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
        

class Params(Enum):
    # Visible configurable options
    NUM_MODELS = IntConfigParam(10)
    MODEL_NAME_PREFIX = StrConfigParam('fm')
    INCLUDE_NUMFEATURES_PREFIX = CheckBoxConfigParam(True)
    INCLUDE_NUMCONSTRAINTS_PREFIX = CheckBoxConfigParam(True)

    # Non-visible configurable options
    SERIALIZATION_TEMPORAL_DIR = StrConfigParam('tmp/generated')


def generate_feature_models(config_params: dict[str, Any]) -> None:
    tree_lcs = [OptionalFeature, MandatoryFeature, XorGroup, OrGroup, XorChildFeature, OrChildFeature]
    constraints_lcs = [RequiresConstraint, ExcludesConstraint]
    n_features = 100
    n_constraints = 0
    features_names = [f'F{i}' for i in range(1, n_features + 1)]

    fm_gen = FMGenerator(tree_language_constructs=tree_lcs,
                         constraints_language_constructs=constraints_lcs,
                         features_names=features_names,
                         n_constraints = n_constraints)
    fm_gen.set_serialization(models_name_prefix=config_params[Params.MODEL_NAME_PREFIX.name], 
                             dir=config_params[Params.SERIALIZATION_TEMPORAL_DIR.name],
                             include_num_features=config_params[Params.INCLUDE_NUMFEATURES_PREFIX.name],
                             include_num_constraints=config_params[Params.INCLUDE_NUMCONSTRAINTS_PREFIX.name])
    fm_gen.generate_n_fms(n_models=config_params[Params.NUM_MODELS.name])
