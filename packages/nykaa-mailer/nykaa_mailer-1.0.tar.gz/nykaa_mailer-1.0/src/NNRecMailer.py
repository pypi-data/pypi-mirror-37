import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.decomposition import TruncatedSVD
import logging
from math import *


class NNRecMailer:

    def __init__(self):
        self.n_feature_description = 90
        self.nykaaNetworkPosts = None

        self.singleColumnNNDataFrame = None
        self.NNAndMailerCombined = None

        self.mailerDataFrame = None
        self.parameter = None
        self.NNDataFrameWithCoordinate = None
        self.mailerDataFrameWithCoordinate = None
        self.similarityScoreDF = None

    def run(self, nn_path, descrptionText, output_path):
        self.loadArticles(nn_path)
        self.mergeColumnsOfNNPosts()
        self.convertMailerToDataFrame(descrptionText)
        self.vectorizeMailerAndDescription()
        self.reduceDimensionality()
        df = self.prepareDataFrame()
        self.prepareMailerDataWithCoordinate(df)
        self.prepareNNDataWithCoordinate(df)
        self.calculateSimilarity()
        similaritySQLFormat = self.processSimilarity()
        self.saveCSV(similaritySQLFormat, output_path)

    def loadArticles(self, nn_path):
        self.nykaaNetworkPosts = pd.read_csv(nn_path, encoding='utf-8')
        self.nykaaNetworkPosts = self.nykaaNetworkPosts[['Post_id', 'Category', 'Title', 'Content']]
        logging.debug("Number of articles: {0}\n".format(len(self.nykaaNetworkPosts)))

    def mergeColumnsOfNNPosts(self):
        self.singleColumnNNDataFrame = pd.DataFrame()

        self.singleColumnNNDataFrame = self.singleColumnNNDataFrame.assign(
            Description=self.nykaaNetworkPosts.Category.astype(str) + " "
                        + self.nykaaNetworkPosts.Title.astype(str) + " "
                        + self.nykaaNetworkPosts.Content.astype(str))

        self.singleColumnNNDataFrame = self.singleColumnNNDataFrame.reset_index()

    def convertMailerToDataFrame(self, descrptionText):
        self.mailerDataFrame = pd.DataFrame()
        self.mailerDataFrame = self.mailerDataFrame.assign(Description=[descrptionText])
        self.mailerDataFrame = self.mailerDataFrame.reset_index()

    def vectorizeMailerAndDescription(self):
        self.NNAndMailerCombined = pd.concat([self.mailerDataFrame, self.singleColumnNNDataFrame])

        vectorizer = self.get_vectorizer(ngram_range=(1, 2),
                                    min_df=4,
                                    max_df=0.3)

        parameter_description = vectorizer.fit_transform(self.NNAndMailerCombined['Description'].values.astype('U'))
        parameter_description = parameter_description.toarray()
        self.parameter = np.array(parameter_description, dtype=float)

    def reduceDimensionality(self):
        self.parameter = self.reduce_dimensionality(self.parameter, n_features=self.n_feature_description)

    def prepareDataFrame(self):
        df_description_vectors = pd.DataFrame()
        df_description_vectors['index'] = self.NNAndMailerCombined['index']
        df_description_vectors['Description'] = self.NNAndMailerCombined['Description']
        df_description_vectors['numbers'] = range(0, len(df_description_vectors))
        df_description_vectors['coordinates'] = df_description_vectors['numbers'].apply(
            lambda index: self.parameter[index, :])
        del df_description_vectors['numbers']
        return df_description_vectors

    def prepareMailerDataWithCoordinate(self, df_description_vectors):
        self.mailerDataFrameWithCoordinate = pd.merge(df_description_vectors, self.mailerDataFrame, how='inner', on=['index', 'Description'])

    def prepareNNDataWithCoordinate(self, df_description_vectors):
        self.NNDataFrameWithCoordinate = pd.merge(df_description_vectors, self.singleColumnNNDataFrame, how='inner', on=['index', 'Description'])

    def calculateSimilarity(self):
        similarity_score_dict = {}
        # Iterate over each article in DataFrame
        for index1, row1 in self.mailerDataFrameWithCoordinate.iterrows():
            # Initialize a dict to store the similarity scores to all other articles in
            similarity_scores = {}
            # Iterate again over all articles to calculate the similarity between article 1 and 2
            for index2, row2 in self.NNDataFrameWithCoordinate.iterrows():
                similarity_scores[index2] = self.calculate_similarity(row1['coordinates'], row2['coordinates'])
            # Save in dictionary
            similarity_score_dict[index1] = similarity_scores
        self.similarityScoreDF = pd.DataFrame(data=similarity_score_dict)
        self.similarityScoreDF = self.similarityScoreDF.fillna(0)

    def processSimilarity(self):
        similarityScoreIntPercent = self.similarityScoreDF.apply(lambda x: pd.to_numeric(x * 100, downcast='signed'))
        similaritySQLFormat = pd.melt(similarityScoreIntPercent.reset_index(), id_vars=["index"],
                                      var_name="description_id", value_name="percentage")
        # similaritySQLFormat["post_id_from"]
        similaritySQLFormat.fillna(0)

        similaritySQLFormat.rename(columns={'index': 'nn_post_id'}, inplace=True)
        similaritySQLFormat = similaritySQLFormat.fillna(0)
        nnPostID = self.nykaaNetworkPosts['Post_id'].tolist()

        def getIDForNNPost(number):
            return int(nnPostID[number])

        similaritySQLFormat['nn_post_id'] = similaritySQLFormat['nn_post_id'].map(getIDForNNPost)
        return similaritySQLFormat

    def saveCSV(self, similaritySQLFormat, output_path):
        similaritySQLFormat.to_csv(output_path, encoding='utf-8', sep=',', index=False)

    def get_vectorizer(self, ngram_range=(1, 3), min_df=2, max_df=1.0):
        vectorizer = CountVectorizer(
            ngram_range=ngram_range,
            tokenizer=self.tokenize,
            min_df=min_df,
            max_df=max_df,
            binary=True,
            stop_words='english')

        return vectorizer

    @staticmethod
    def tokenize(text):
        tokens = nltk.WhitespaceTokenizer().tokenize(text)
        tokens = list(set(re.sub("[^a-zA-Z\']", "", token) for token in tokens))
        tokens = [word for word in tokens if word not in stopwords.words('english')]
        tokens = list(set(re.sub("[^a-zA-Z]", "", token) for token in tokens))
        stems = []
        stemmer = SnowballStemmer("english")
        for token in tokens:
            token = stemmer.stem(token)
            if token != "":
                stems.append(token)
        return stems

    @staticmethod
    def reduce_dimensionality(X, n_features):
        # Initialize reduction method: PCA or SVD
        # reducer = PCA(n_components=n_features)
        reducer = TruncatedSVD(n_components=n_features)
        # Fit and transform data to n_features-dimensional space
        reducer.fit(X)
        X = reducer.transform(X)
        logging.debug("Reduced number of features to {0}".format(n_features))
        logging.debug("Percentage explained: %s\n" % reducer.explained_variance_ratio_.sum())
        return X

    def calculate_similarity(self, article1, article2):
        """
        Calculate the similarity between two articles, e.g. the cosine similarity or the Euclidean distance.
        :param article1: coordinates (feature values) of article 1
        :param article2: coordinates (feature values) of article 2
        :return:
        """
        similarity = self.cosine_similarity(article1, article2)  # Cosine similarity formula
        # similarity = euclidean_distance(article1, article2)    # Euclidean distance formula
        similarity = "{0:.2f}".format(round(similarity, 2))
        return float(similarity)

    @staticmethod
    def cosine_similarity(x, y):
        def square_rooted(v):
            return round(sqrt(sum([a * a for a in v])), 3)

        numerator = sum(a * b for a, b in zip(x, y))
        denominator = square_rooted(x) * square_rooted(y)
        return round(numerator / float(denominator), 3)
