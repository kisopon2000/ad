#--------------------
# analysisclient.py
#--------------------

import copy
import pandas as pd
import pickle
import base64

import config.defines as const
from lib.dbapi import DBApi
from lib.analysis import AnalysisApi

class AnalysisClient(DBApi):
    #--------------------
    # private
    #--------------------
    m_init = False
    m_analysisapi = None
    def __init(self):
        self.m_analysisapi = AnalysisApi()
        self.m_init = True
    def __getAdUserHistoriesDataFrame(self):
        sql = "SELECT * FROM ad_user_history"
        self.m_cursor.execute(sql)
        column_all = [column[0] for column in self.m_cursor.description]
        row_all = []
        for row in self.m_cursor.fetchall():
            s_row_all = [elem for elem in row]
            row_all.append(s_row_all)
        df = pd.DataFrame(row_all)
        df.columns = column_all
        df.dropna()
        # df = df.sort_values('ad_click_count', ascending=False)
        # df = round(df.describe(), 2)
        return df
    def __pivotDataFrame(self, in_df, in_name, in_column, in_value):
        df = in_df.pivot(index=in_name, columns=in_column, values=in_value)
        print(df)
        return df
    def __updateLearnedModel(self, in_model):
        # Ç¢Ç¡ÇΩÇÒçÌèú
        sql = "DELETE FROM ad_models WHERE model_id = 'ad_model'"
        self.m_cursor.execute(sql)
        # í«â¡
        model = base64.b64encode(in_model).decode("utf-8")
        sql = "INSERT INTO ad_models VALUES ('ad_model', '" + model + "', 0, 0, 0)"
        self.m_cursor.execute(sql)
        self.m_cursor.commit()
    #--------------------
    # public
    #--------------------
    def createModel(self):
        if not self.m_init:
            self.__init()
        df = self.__getAdUserHistoriesDataFrame()
        df = self.__pivotDataFrame(df, 'user_id', 'ad_id', 'ad_click_count')
        self.m_analysisapi.learnModel(df)
        # DBÇ÷ÇÃÉÇÉfÉãìoò^
        model = self.m_analysisapi.getLearnedModel()
        model = pickle.dumps(model)
        self.__updateLearnedModel(model)
