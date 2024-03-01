import os
import random
from enum import Enum

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import (
    UVLWriter, 
    GlencoeWriter,
    SPLOTWriter
)

from language_constructs.models import LanguageConstruct
from language_constructs.models.constructs import FeatureModelConstruct, RootFeature


class SerializationFormat(Enum):
    UVL = UVLWriter
    Glencoe = GlencoeWriter
    SPLOT = SPLOTWriter


class FMGenerator():

    def __init__(self,
                 tree_language_constructs: list[LanguageConstruct],
                 constraints_language_constructs: list[LanguageConstruct],
                 features_names: tuple[str],
                 n_constraints: int) -> None:
        self.features: tuple[str] = features_names
        self.tree_lcs: list[LanguageConstruct] = tree_language_constructs
        self.constraints_lcs: list[LanguageConstruct] = constraints_language_constructs
        self.n_constraints: int = n_constraints
        # Remove trivial constructs
        if FeatureModelConstruct in self.tree_lcs:
            self.tree_lcs.remove(FeatureModelConstruct)
        if RootFeature in self.tree_lcs:
            self.tree_lcs.remove(RootFeature)

        # Serialization options
        self.set_serialization()

    def generate_random_fm(self) -> FeatureModel:
        features = list(self.features)
        # Create an empty FM
        fm = self._generate_fm()
        # Create the root feature
        fm = self._generate_root_feature(fm, features)
        # Create the tree
        fm = self._generate_feature_tree(fm, features)
        # Create the constraints
        fm = self._generate_constraints(fm, self.features, self.n_constraints)
        return fm

    def _generate_fm(self) -> FeatureModel:
        return FeatureModelConstruct().apply(None)

    def _generate_root_feature(self, fm: FeatureModel, features: list[str]) -> FeatureModel:
        root_gen = RootFeature.get_random_applicable_instance(fm, features)
        fm = root_gen.apply(fm)
        features.remove(root_gen.get().name)
        return fm
    
    def _generate_feature_tree(self, fm: FeatureModel, features: list[str]) -> FeatureModel:
        while features:
            random_lc = random.choice(self.tree_lcs)
            random_applicable_instance = random_lc.get_random_applicable_instance(fm, features)
            if random_applicable_instance is not None:
                fm = random_applicable_instance.apply(fm)
                features_added = random_applicable_instance.get_features()
                for f in features_added:
                    features.remove(f)
        return fm
    
    def _generate_constraints(self, fm: FeatureModel, features: tuple[str], n_constraints: int) -> FeatureModel:
        count = 0
        while count < n_constraints:
            random_lc = random.choice(self.constraints_lcs)
            random_applicable_instance = random_lc.get_random_applicable_instance(fm, features)
            if random_applicable_instance is not None:
                fm = random_applicable_instance.apply(fm)
                count += 1
        return fm

    def set_serialization(self,
                          models_name_prefix: str = 'fm',
                          dir: str = 'tmp/generated',
                          format: SerializationFormat = SerializationFormat.UVL,
                          include_num_features: bool = False,
                          include_num_constraints: bool = False) -> None:
        self._models_name_prefix = models_name_prefix
        self._serialization_dir = dir
        self._serialization_format = format
        self._include_num_features = include_num_features
        self._include_num_constraints = include_num_constraints

    def generate_n_fms(self, n_models: int) -> None:
        for i in range(n_models):
            # Generate a random FM
            fm = self.generate_random_fm()
            # Serialize the FM
            self._serialize_fm(fm, i)

    def _serialize_fm(self, fm: FeatureModel, id: int) -> str:
        """Serialize the feature model according to the serialization options and return its path."""
        output_file = os.path.join(self._serialization_dir, f'{self._models_name_prefix}{id}')
        if self._include_num_features:
            output_file += f'_{len(fm.get_features())}f'
        if self._include_num_constraints:
            output_file += f'_{len(fm.get_constraints())}c'
        fm_writer = self._serialization_format.value
        output_file += f'.{fm_writer.get_destination_extension()}'
        fm_writer(source_model=fm, path=output_file).transform()
        return output_file
