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
                 constraints_language_constructs: list[LanguageConstruct]) -> None:
        self.tree_lcs: list[LanguageConstruct] = tree_language_constructs
        self.constraints_lcs: list[LanguageConstruct] = constraints_language_constructs
        # Remove trivial constructs
        if FeatureModelConstruct in self.tree_lcs:
            self.tree_lcs.remove(FeatureModelConstruct)
        if RootFeature in self.tree_lcs:
            self.tree_lcs.remove(RootFeature)
        # Serialization options
        self.set_serialization()

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

    def set_features(self,
                     min_num_features: int,
                     max_num_features: int,
                     uniform_num_features: bool) -> None:
        self._min_num_features = min_num_features
        self._max_num_features = max_num_features
        self._features_names: tuple[str] = tuple(f'F{i}' for i in range(1, max_num_features + 1))
        self._uniform_num_features = uniform_num_features

    def set_abstract_features(self,
                              num_abstract_features: int = 0,
                              make_root_abstract: bool = False,
                              make_all_internal_features_abstract: bool = False,
                              allow_abstract_leaf_features: bool = False) -> None:
        self._num_abstract_features = num_abstract_features
        self._make_root_abstract = make_root_abstract
        self._make_all_internal_features_abstract = make_all_internal_features_abstract
        self._allow_abstract_leaf_features = allow_abstract_leaf_features

    def set_constraints(self,
                        min_num_constraints: int,
                        max_num_constraints: int,
                        uniform_num_constraints: bool) -> None:
        self._min_num_constraints = min_num_constraints
        self._max_num_constraints = max_num_constraints
        self._uniform_num_constraints = uniform_num_constraints

    def generate_random_fm(self,
                           features_names: list[str],
                           num_constraints: int) -> FeatureModel:
        # Create an empty FM
        fm = self._generate_fm()
        # Create the root feature
        fm = self._generate_root_feature(fm, features_names)
        features_names.remove(fm.root.name)
        # Create the tree
        fm = self._generate_feature_tree(fm, features_names)
        features_names.insert(0, fm.root.name)
        # Create the constraints
        fm = self._generate_constraints(fm, features_names, num_constraints)
        return fm

    def _generate_fm(self) -> FeatureModel:
        return FeatureModelConstruct().apply(None)

    def _generate_root_feature(self, fm: FeatureModel, features: list[str]) -> FeatureModel:
        root_gen = RootFeature.get_random_applicable_instance(fm, features)
        fm = root_gen.apply(fm)
        return fm
    
    def _generate_feature_tree(self, fm: FeatureModel, features_names: list[str]) -> FeatureModel:
        features = list(features_names)
        while features:
            random_lc = random.choice(self.tree_lcs)
            random_applicable_instance = random_lc.get_random_applicable_instance(fm, features)
            if random_applicable_instance is not None:
                fm = random_applicable_instance.apply(fm)
                features_added = random_applicable_instance.get_features()
                for f in features_added:
                    features.remove(f)    
        return fm
    
    def _generate_constraints(self, fm: FeatureModel, features: list[str], n_constraints: int) -> FeatureModel:
        count = 0
        while count < n_constraints:
            random_lc = random.choice(self.constraints_lcs)
            random_applicable_instance = random_lc.get_random_applicable_instance(fm, features)
            if random_applicable_instance is not None:
                fm = random_applicable_instance.apply(fm)
                count += 1
        return fm

    def generate_n_fms(self, n_models: int, celery_task):
        count_n_features = 0
        max_min_diff_features = self._max_num_features - self._min_num_features
        count_n_constraints = 0
        max_min_diff_constraints = self._max_num_constraints - self._min_num_constraints
        for i in range(n_models):
            # Get the number of features for this FM
            if self._uniform_num_features:
                n_features = count_n_features % (max_min_diff_features + 1) + self._min_num_features
                count_n_features += 1
            else:
                n_features = random.randint(self._min_num_features, self._max_num_features)
            features_names = random.sample(self._features_names, n_features)
            # Get the number of constraints
            if self._uniform_num_constraints:
                n_constraints = count_n_constraints % (max_min_diff_constraints + 1) + self._min_num_constraints
                count_n_constraints += 1
            else:
                n_constraints = random.randint(self._min_num_constraints, self._max_num_constraints)
            # Generate a random FM
            fm = self.generate_random_fm(features_names, n_constraints)
            # Convert abstract features
            fm = self._convert_abstract_features(fm)
            # Serialize the FM
            self._serialize_fm(fm, i)
            percentage_completed = (i / n_models) * 100
            celery_task.update_state(state='PROGRESS',
                                     meta={'current': i, 
                                           'total': n_models})
            #yield percentage_completed
        #yield percentage_completed

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

    def _convert_abstract_features(self, fm: FeatureModel) -> FeatureModel:
        features = []
        leaf_features = []
        internal_features = []
        for feature in fm.get_features():
            if feature.is_leaf():
                leaf_features.append(feature)
            else:
                internal_features.append(feature)
        count_abstract_features = 0
        # Make the root abstract
        if self._make_root_abstract:
            fm.root.is_abstract = True
            count_abstract_features += 1
            if fm.root in internal_features:
                internal_features.remove(fm.root)
            if fm.root in leaf_features:
                leaf_features.remove(fm.root)
        else:
            features.append(fm.root)
            
        # Make all internal features abstract
        if self._make_all_internal_features_abstract:
            for feature in internal_features:
                fm.get_feature_by_name(feature.name).is_abstract = True
            count_abstract_features += len(internal_features)
        else:
            features.extend(internal_features)
        if self._allow_abstract_leaf_features:
            features.extend(leaf_features)
        convert_n_features = min(len(features), max(0, self._num_abstract_features - count_abstract_features))
        features_to_convert = random.sample(features, convert_n_features)
        for feature in features_to_convert:
            feature.is_abstract = True
        return fm