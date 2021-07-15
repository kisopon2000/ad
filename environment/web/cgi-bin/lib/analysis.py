#====================
# analysis.py
#====================

import os
import numpy
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

import config.defines as const
from lib.utility import SystemConfigApi

class AnalysisApi():
    #--------------------
    # private
    #--------------------
    m_init = False
    m_cConfig = None
    m_type = None
    m_model = None
    m_cModel = None
    m_cLearnedModel = None
    def __init(self):
        self.m_cConfig = SystemConfigApi()
        self.m_type = self.m_cConfig.getAnalysisType()
        self.m_model = self.m_cConfig.getAnalysisModel()
        if self.m_model == 'NearestNeighbors':
            self.m_cModel = NearestNeighbors(n_neighbors=9, algorithm='brute', metric='cosine')
        else:
            self.m_cModel = NearestNeighbors(n_neighbors=9, algorithm='brute', metric='cosine')
        self.m_init = True
    #--------------------
    # public
    #--------------------
    def getAnalysisType(self):
        if not self.m_init:
            self.__init()
        return self.m_type
    def getTrainTestData(self, in_x, in_y):
        if not self.m_init:
            self.__init()
        x_train, x_test, y_train, y_test = train_test_split(in_x, in_y, test_size = const.ANALYSIS_TEST_SIZE, random_state = 0)
        return x_train, x_test, y_train, y_test
    def getDistance(self, in_x1, in_y1, in_x2, in_y2):
        if not self.m_init:
            self.__init()
        a = numpy.array([in_x1, in_y1])
        b = numpy.array([in_x2, in_y2])
        u = b - a
        return numpy.linalg.norm(u)
    def normalize(self, in_x, in_xmin, in_xmax):
        if not self.m_init:
            self.__init()
        return (in_x - in_xmin) / (in_xmax - in_xmin)
    def sparse(self, in_df):
        if not self.m_init:
            self.__init()
        return csr_matrix(in_df.values)
    def learnModel(self, in_df):
        if not self.m_init:
            self.__init()
        self.m_cLearnedModel = self.m_cModel.fit(in_df)
    def getLearnedModel(self):
        if not self.m_init:
            self.__init()
        return self.m_cLearnedModel
    def setLearnedModel(self, in_model):
        if not self.m_init:
            self.__init()
        self.m_cLearnedModel = in_model
    def getRecommendedData(self, in_df, in_userid):
        if not self.m_init:
            self.__init()
        distance, indice = self.m_cLearnedModel.kneighbors(in_df.iloc[in_df.index==in_userid].values.reshape(1, -1), n_neighbors=5)
        # for i in range(0, len(distance.flatten())):
        #     print('user_id: {0} with distance: {1}'.format(in_df.index[indice.flatten()[i]], distance.flatten()[i]))
