import os
from enum import Enum
import shutil
import tempfile

import flask

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLWriter

from language_constructs.models import FMLanguage
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


# class Params(Enum):
#     NUM_MODELS = 'num_models'


def generate_feature_models(num_models: int, dir: str) -> None:
    n_features = 100
    n_constraints = 10
    features_names = [f'F{i}' for i in range(1, n_features + 1)]
    language_constructs = [FeatureModelConstruct, RootFeature, OptionalFeature, MandatoryFeature, XorGroup, OrGroup, XorChildFeature, OrChildFeature]
    optional_language_constructs = [RequiresConstraint, ExcludesConstraint]
    language = FMLanguage(language_constructs, optional_language_constructs)
    for i in range(num_models):
        # Generate a random FM
        fm = language.generate_random_feature_model(features_names, n_constraints)
        # Serialize the FM
        output_file = os.path.join(dir, f'fm{i}_{len(fm.get_features())}f_{len(fm.get_constraints())}c.uvl')
        UVLWriter(source_model=fm, path=output_file).transform()
    return None


def zip_files():
    #zip_file = shutil.make_archive(path_src, 'zip', path_dst)
    pass


def create_fm_file(fm: FeatureModel, format: str) -> str:
    """Write a feature model object to a temporal file and returns its path."""
    temporal_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
    if format == 'uvl':
        UVLWriter(source_model=fm, path=temporal_filepath).transform()
    return temporal_filepath
    # elif format == 'gfm.json':
    #     temporal_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
    #     result = GlencoeWriter(source_model=fm, path=temporal_filepath).transform()
    #     print(result)
    # elif format == 'sxfm.xml':
    #     temporal_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
    #     result = SPLOTWriter(source_model=fm, path=temporal_filepath).transform()
    # elif format == 'json':
    #     result = JSONWriter(source_model=fm, path=None).transform()
    # elif format == 'xml':
    #     temporal_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
    #     result = FeatureIDEWriter(source_model=fm, path=temporal_filepath).transform()
    # elif format == 'txt':
    #     temporal_filepath = tempfile.NamedTemporaryFile(mode='w', encoding='utf8').name
    #     result = ClaferWriter(source_model=fm, path=temporal_filepath).transform()