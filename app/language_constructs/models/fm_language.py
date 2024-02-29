import os
import copy
import queue
import random

from flamapy.metamodels.fm_metamodel.models import FeatureModel
from flamapy.metamodels.fm_metamodel.transformations import UVLWriter

from language_constructs.models import LanguageConstruct


class FMLanguage():

    def __init__(self, lcs: list[LanguageConstruct], optional_lcs: list[LanguageConstruct]) -> None:
        self.lcs = lcs
        self.optional_lcs = optional_lcs

    def generate_feature_models(self, features_names: set[str]) -> list[FeatureModel]:
        incomplete_feature_models = queue.Queue()
        incomplete_feature_models.put(None)
        completed_fms = []
        while not incomplete_feature_models.empty():
            print(f'#Completed/Incompleted fms: {len(completed_fms)} / {incomplete_feature_models.qsize()}')
            fm = incomplete_feature_models.get()
            applicable_lcs = []
            for lc in self.lcs:
                applicable_lcs.extend(lc.get_applicable_instances(fm, features_names))
            if not applicable_lcs:
                completed_fms.append(fm)
            else:
                for alc in applicable_lcs:
                    new_fm = copy.deepcopy(fm)
                    incomplete_feature_models.put(alc.apply(new_fm))
        return completed_fms
    
    def generate_feature_models_and_serializing(self, features_names: set[str],
                                                output_folder: str) -> int:
        incomplete_feature_models = queue.Queue()
        incomplete_feature_models.put(None)
        count = 0
        while not incomplete_feature_models.empty():
            print(f'#Completed/Incompleted fms: {count} / {incomplete_feature_models.qsize()}')
            fm = incomplete_feature_models.get()
            applicable_lcs = []
            for lc in self.lcs:
                applicable_lcs.extend(lc.get_applicable_instances(fm, features_names))
            if not applicable_lcs:
                count += 1
                print(f'FM{count}: {fm}')
                output_file = os.path.join(output_folder, f'fm{count}_{len(fm.get_features())}f_{len(fm.get_constraints())}c.uvl')
                UVLWriter(fm, output_file).transform()
                for olc in self.optional_lcs:
                    applicable_lcs.extend(olc.get_applicable_instances(fm, features_names))
                for alc in applicable_lcs:
                    new_fm = copy.deepcopy(fm)
                    incomplete_feature_models.put(alc.apply(new_fm))
            else:
                for alc in applicable_lcs:
                    new_fm = copy.deepcopy(fm)
                    incomplete_feature_models.put(alc.apply(new_fm))
        return count
    
    def generate_random_feature_model(self, features_names: list[str],
                                      n_constraints: int) -> FeatureModel:
        features_names = copy.deepcopy(features_names)
        original_features_names = copy.deepcopy(features_names)
        n_features = len(features_names)
        fm = None
        fm = self.lcs[0].get_random_applicable_instance(fm, features_names).apply(fm)
        fm = self.lcs[1].get_random_applicable_instance(fm, features_names).apply(fm)
        features_names.remove(fm.root.name)
        count = 1
        #print(f'  |-generating features... ', flush=True, end='')
        language_constructs = self.lcs[2:]
        while count < n_features:
            random_lc = random.choice(language_constructs)
            random_applicable_instance = random_lc.get_random_applicable_instance(fm, features_names)
            if random_applicable_instance is not None:
                fm = random_applicable_instance.apply(fm)
                features_added = random_applicable_instance.get_features()
                for f in features_added:
                    features_names.remove(f)
                count += len(features_added)
        #        print(f'{count} ', flush=True, end='')
        #print()
        fm = self.add_random_constraints(fm, original_features_names, n_constraints)
        return fm

    def add_random_constraints(self, fm: FeatureModel, features_names: list[str], n_constraints: int) -> FeatureModel:
        count = 0
        #print(f'  |generating constraints... ', flush=True, end='')
        while count < n_constraints:
            random_lc = random.choice(self.optional_lcs)
            random_applicable_instance = random_lc.get_random_applicable_instance(fm, features_names)
            if random_applicable_instance is not None:
                fm = random_applicable_instance.apply(fm)
                count = len(fm.get_constraints())
        #        print(f'{count} ', flush=True, end='')
        #print()
        return fm
