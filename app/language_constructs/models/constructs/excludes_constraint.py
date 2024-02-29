import random
import itertools

from flamapy.core.models.ast import AST, ASTOperation, Node
from flamapy.metamodels.fm_metamodel.models import FeatureModel, Constraint

from language_constructs.models import LanguageConstruct 
from language_constructs.utils import utils


class ExcludesConstraint(LanguageConstruct):

    def __init__(self, left_feature_name: str, right_feature_name: str) -> None:
        self.left_feature_name = left_feature_name
        self.right_feature_name = right_feature_name
        self.constraint = None

    @staticmethod
    def name() -> str:
        return 'Excludes constraint'

    @staticmethod
    def count(fm: FeatureModel) -> int:
        return len(fm.get_constraints())

    def get(self) -> Constraint:
        return self.constraint

    def apply(self, fm: FeatureModel) -> FeatureModel:
        ast = AST.create_binary_operation(ASTOperation.EXCLUDES, 
                                          Node(self.left_feature_name), 
                                          Node(self.right_feature_name))
        self.constraint = Constraint(f'{self.left_feature_name} => ! {self.right_feature_name}', ast)
        fm.get_constraints().append(self.constraint)
        return fm

    def is_applicable(self, fm: FeatureModel) -> bool:
        if fm is None or len(fm.get_features()) < 2:
            return False
        left_feature = fm.get_feature_by_name(self.left_feature_name)
        right_feature = fm.get_feature_by_name(self.right_feature_name)
        if left_feature is None or right_feature is None:
            return False
        return not any(utils.is_excludes_constraint(ctc) and 
                       utils.left_right_features_from_simple_constraint(ctc) == (self.left_feature_name, self.right_feature_name) 
                       for ctc in fm.get_constraints())

    @staticmethod
    def get_applicable_instances(fm: FeatureModel, features_names: list[str]) -> list['LanguageConstruct']:
        if fm is None or len(fm.get_features()) < 2:
            return []
        lcs = []
        features_combinations = itertools.combinations(features_names, 2)
        for left_feature_name, right_feature_name in features_combinations:
            lc = ExcludesConstraint(left_feature_name, right_feature_name)
            if lc.is_applicable(fm):
                lcs.append(lc)
            lc = ExcludesConstraint(right_feature_name, left_feature_name)
            if lc.is_applicable(fm):
                lcs.append(lc)
        return lcs

    @staticmethod
    def get_random_applicable_instance(fm: FeatureModel, features_names: list[str]) -> 'LanguageConstruct':
        if len(features_names) < 2:
            return None
        else:
            feature_combinations = list(itertools.combinations(features_names, 2))
            features = list(random.choice(feature_combinations))
            random.shuffle(features)
            left = features[0]
            right = features[1]
            instance = ExcludesConstraint(left, right)
            while not instance.is_applicable(fm):
                features = list(random.choice(feature_combinations))
                random.shuffle(features)
                left = features[0]
                right = features[1]
                instance = ExcludesConstraint(left, right)
            return instance
    
    def get_features(self) -> list[str]:
        return []