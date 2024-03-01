import random 

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature

from language_constructs.models import LanguageConstruct 


class RootFeature(LanguageConstruct):

    def __init__(self, name: str) -> None:
        self._name = name
        self.feature = None

    @staticmethod
    def name() -> str:
        return 'Root Feature'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return 0 if fm.root is None else 1 

    def get(self) -> Feature:
        return self.feature

    def apply(self, fm: FeatureModel) -> FeatureModel:
        self.feature = Feature(name=self._name)
        fm.root = self.feature
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        return fm is not None and fm.root is None

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        if fm is None or fm.root is not None:
            return []
        return [RootFeature(f_name) for f_name in features_names]

    @staticmethod
    def get_random_applicable_instance(fm: FeatureModel, features_names: list[str]) -> 'LanguageConstruct':
        return RootFeature(random.choice(features_names)) if features_names else None

    def get_features(self) -> list[str]:
        return [self._name]
