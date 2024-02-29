from typing import Any
from abc import ABC, abstractmethod

from flamapy.metamodels.fm_metamodel.models import FeatureModel


class LanguageConstruct(ABC):

    @staticmethod
    @abstractmethod
    def name() -> str:
        """Name of the language construct."""
        pass

    @staticmethod
    @abstractmethod
    def count(fm: FeatureModel) -> int:
        """Count the number of instance of this language construct in the given feature model."""
        pass

    @abstractmethod
    def get(self) -> Any:
        """Instance of the element create after the application of the language construct (e.g., a feature)."""
        pass

    @abstractmethod
    def apply(self, fm: FeatureModel) -> FeatureModel:
        """Apply the language construct to the given feature model."""
        pass

    @abstractmethod
    def is_applicable(self, fm: FeatureModel) -> bool:
        """Check if the language construct can be applied to the given feature model."""
        pass

    @staticmethod
    @abstractmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        """Return a list of all possible instances of this language construct applicable to the given feature model using the given features."""
        pass

    @staticmethod
    @abstractmethod
    def get_random_applicable_instance(fm: FeatureModel, features_names: list[str]) -> 'LanguageConstruct':
        """Return a random applicable instance to the given feature model using the given features."""
        pass

    @abstractmethod
    def get_features(self) -> list[str]:
        """Return the list of features this language construct uses."""
        pass