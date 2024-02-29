import random 

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Relation

from language_constructs.models import LanguageConstruct 


class XorChildFeature(LanguageConstruct):

    def __init__(self, child_name: str, parent_name: str) -> None:
        self.child_name = child_name
        self.parent_name = parent_name
        self.feature = None

    @staticmethod
    def name() -> str:
        return 'Xor child feature'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return sum(f.get_parent() is not None and f.get_parent().is_alternative_group() for f in fm.get_features())

    def get(self) -> Feature:
        return self.feature

    def apply(self, fm: FeatureModel) -> FeatureModel:
        parent = fm.get_feature_by_name(self.parent_name)
        relation = next(r for r in parent.get_relations() if r.is_alternative())  # Assume there is only one group relation per feature
        child = Feature(name=self.child_name, parent=parent)
        relation.add_child(child)
        self.feature = child
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        if fm is None:
            return False
        parent = fm.get_feature_by_name(self.parent_name)
        child = fm.get_feature_by_name(self.child_name)
        if parent is None or child is not None:
            return False
        relation = next(r for r in parent.get_relations() if r.is_alternative())  # Assume there is only one group relation per feature
        return relation is not None

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        if fm is None:
            return []
        lcs = []
        parents = [f for f in fm.get_features() if f.is_alternative_group()]
        for child_name in features_names:
            for p in parents:
                lc = XorChildFeature(child_name, p.name)
                if lc.is_applicable(fm):
                    lcs.append(lc)
        return lcs

    @staticmethod
    def get_random_applicable_instance(fm: FeatureModel, features_names: list[str]) -> 'LanguageConstruct':
        if not features_names:
            return None
        else:
            features = [f.name for f in fm.get_features() if f.is_alternative_group()]
            if not features:
                return None
            parent = random.choice(features)
            random_feature = random.choice(features_names)
            instance = XorChildFeature(random_feature, parent)
            while not instance.is_applicable(fm):
                parent = random.choice(features)
                random_feature = random.choice(features_names)
                instance = XorChildFeature(random_feature, parent)
            return instance
    
    def get_features(self) -> list[str]:
        return [self.child_name]