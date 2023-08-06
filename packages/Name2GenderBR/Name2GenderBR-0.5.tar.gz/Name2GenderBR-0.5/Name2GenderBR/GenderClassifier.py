import pandas as pd
import pickle
import os
import unicodedata
import Levenshtein
import pkg_resources

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

class GenderClassifier:

    def __init__(self):
        self._initialize_summary_df()

    def _initialize_summary_df(self):
        file = pkg_resources.resource_stream(__name__, 'summary.p')
        # if not os.path.isfile(''):
        #     names_df = pd.read_csv('nomes.csv', delimiter=',')
        #     summary_df = names_df[
        #         ['first_name', 'frequency_male', 'frequency_female', 'frequency_total', 'classification']]
        #
        #     summary_df.set_index('first_name', inplace=True)
        #
        #     del names_df
        #
        #     with open('summary.p', 'wb') as output:
        #         pickle.dump(summary_df, output)
        #
        #     self.summary_df = summary_df
        # else:
        #     with open(file, 'rb') as input:
        self.summary_df = pickle.load(file)

    def _find_closest_name(self, name):

        distance = len(name) * 2
        name_aux = ''

        for n in self.summary_df.index:

            l = Levenshtein.distance(name, n)

            if l < distance:
                distance = l
                name_aux = n

            if distance == 0:
                break

        return name_aux


    def _sanitize(self, name):

        if ' ' in name:
            name = name.split(' ')[0]

        name = strip_accents(name).upper()

        if name not in self.summary_df.index:
            name = self._find_closest_name(name)

        return name

    def get_gender(self, name):
        name = self._sanitize(name)
        # gender = self.summary_df[self.summary_df['first_name'] == name]['classification'].values.tolist()[0]
        gender = self.summary_df.at[name, 'classification']
        return gender

    def is_male(self, name):
        return self.get_gender(name) == 'M'

    def is_female(self, name):
        return self.get_gender(name) == 'F'

    def get_stats(self, name):
        return self.summary_df.loc[[self._sanitize(name)]]

    def test(self):
        classifier = GenderClassifier()
        print(classifier.get_gender('Gabriela'))