import random 

from flamapy.metamodels.fm_metamodel.models import FeatureModel, Feature, Relation

from language_constructs.models import LanguageConstruct 


class MandatoryFeature(LanguageConstruct):

    def __init__(self, name: str, parent_name: str) -> None:
        self._name = name
        self.parent_name = parent_name
        self.feature = None

    @staticmethod
    def name() -> str:
        return 'Mandatory Feature'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return len(fm.get_mandatory_features())

    def get(self) -> Feature:
        return self.feature

    def apply(self, fm: FeatureModel) -> FeatureModel:
        parent = fm.get_feature_by_name(self.parent_name)
        self.feature = Feature(name=self._name, parent=parent)
        relation = Relation(parent=parent, children=[self.feature], card_min=1, card_max=1)
        parent.add_relation(relation)
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        if fm is None:
            return False
        feature = fm.get_feature_by_name(self._name) 
        parent = fm.get_feature_by_name(self.parent_name)
        return feature is None and parent is not None and any(not f.is_group() for f in fm.get_features())

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        if fm is None:
            return []
        lcs = []
        parents = [f for f in fm.get_features() if not f.is_group()]
        for f_name in features_names:
            for p in parents:
                lc = MandatoryFeature(f_name, p.name)
                if lc.is_applicable(fm):
                    lcs.append(lc)
        return lcs

    @staticmethod
    def get_random_applicable_instance(fm: FeatureModel, features_names: list[str]) -> 'LanguageConstruct':
        if not features_names:
            return None
        else:
            
            features = [f.name for f in fm.get_features() if not f.is_group()]
            if not features:
                return None
            parent = random.choice(features)
            random_feature = random.choice(features_names)
            instance = MandatoryFeature(random_feature, parent)
            while not instance.is_applicable(fm):
                parent = random.choice(features)
                random_feature = random.choice(features_names)
                instance = MandatoryFeature(random_feature, parent)
            return instance
    
    def get_features(self) -> list[str]:
        return [self._name]
    
    @staticmethod
    def get_instances(fm: FeatureModel) -> list[Feature]:
        return fm.get_mandatory_features()