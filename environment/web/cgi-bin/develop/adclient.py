#--------------------
# adclient.py
#--------------------

import pandas as pd
import pickle
import base64
import random

from lib.dbapi import DBApi

class AdClient(DBApi):
    #--------------------
    # private
    #--------------------
    m_init = False
    def __init(self):
        self.m_init = True
    def __getAdUserHistoriesDataFrame(self, in_adtypeid):
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
        return df
    def __pivotDataFrame(self, in_df, in_name, in_column, in_value):
        df = in_df.pivot(index=in_name, columns=in_column, values=in_value)
        return df
    def __getAdUserHistories(self, in_userid, in_attribute, in_adtypeid):
        sql = "SELECT ad_user_history.ad_id, ad_user_history." + in_attribute + " FROM ad_user_history INNER JOIN ads ON ad_user_history.ad_id = ads.ad_id WHERE user_id = " + str(in_userid) + " AND ad_type_id = " + str(in_adtypeid) + " ORDER BY ad_user_history.ad_click_count DESC;"
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def __getAdModels(self):
        sql = "SELECT * FROM ad_models WHERE model_id = 'ad_model'"
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def __getAds(self, in_adid=''):
        if not in_adid:
            sql = "SELECT * FROM ads"
        else:
            sql = "SELECT * FROM ads WHERE ad_id = " + str(in_adid)
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    #--------------------
    # public
    #--------------------
    def getRecommendedAd(self, in_userid, in_adtypeid, in_memcache=False, in_multi=False):
        if not self.m_init:
            self.__init()
        df = self.__getAdUserHistoriesDataFrame(in_adtypeid)
        df = self.__pivotDataFrame(df, 'user_id', 'ad_id', 'ad_click_count')
        if in_memcache:
            model = self.getMemcachedData("@@ad_models_memcached.ad_model")
        else:
            model = self.__getAdModels()
            model = (model[0])['model']
        model = pickle.loads(base64.b64decode(model.encode()))
        distance, indice = model.kneighbors(df.iloc[df.index==1].values.reshape(1, -1), n_neighbors=5)
        user_id = -1
        for i in range(0, len(distance.flatten())):
            # print('user_id: {0} with distance: {1}'.format(df.index[indice.flatten()[i]], distance.flatten()[i]))
            self.debug('user_id: {0} with distance: {1}'.format(df.index[indice.flatten()[i]], distance.flatten()[i]))
            if df.index[indice.flatten()[i]] != in_userid:
                user_id = df.index[indice.flatten()[i]]
                break
        if user_id != -1:
            userhistories = self.__getAdUserHistories(user_id, 'ad_click_count', in_adtypeid)
            indexmax = 5
            if in_multi:
                ads = []
                if len(userhistories) < indexmax:
                    indexmax = len(userhistories)
                userhistories = random.sample(userhistories, indexmax)
                for userhistory in userhistories:
                    ad = self.__getAds(userhistory['ad_id'])
                    if len(ad) > 0:
                        ads.append(ad[0])
                return ads
            else:
                index = random.randint(0, len(userhistories) - 1)
                if index > indexmax:
                    index = 0
                ad = self.__getAds(userhistories[index]['ad_id'])
                return ad
    def updateAdHistories(self, in_companyid, inuserid, in_adid, in_displayed, in_clicked):
        sql = "SELECT * FROM ad_user_history WHERE company_id=" + str(in_companyid) + " AND user_id=" + str(inuserid) + " AND ad_id=" + str(in_adid)
        datum = self.m_cursor.execute(sql)
        if len(datum.fetchall()) == 0:
            # í«â¡
            sql = "INSERT INTO ad_user_history (user_id, company_id, ad_id, ad_display_count) VALUES (" + str(inuserid) + ", " + str(in_companyid) + ", " + str(in_adid) + ", " + str(1) + ")"
            self.m_cursor.execute(sql)
            self.m_connection.commit()
            if self.m_cursor.rowcount != 1:
                return 1
            sql = "UPDATE ads SET ad_display_count=ad_display_count+1 WHERE ad_id=" + str(in_adid)
            self.m_cursor.execute(sql)
            if self.m_cursor.rowcount != 1:
                return 1
        else:
            # çXêV
            if in_displayed:
                sql = "UPDATE ad_user_history SET ad_display_count=ad_display_count+1 WHERE company_id=" + str(in_companyid) + " AND user_id=" + str(inuserid) + " AND ad_id=" + str(in_adid)
                self.m_cursor.execute(sql)
                if self.m_cursor.rowcount != 1:
                    return 1
                sql = "UPDATE ads SET ad_display_count=ad_display_count+1 WHERE ad_id=" + str(in_adid)
                self.m_cursor.execute(sql)
                if self.m_cursor.rowcount != 1:
                    return 1
            if in_clicked:
                sql = "UPDATE ad_user_history SET ad_click_count=ad_click_count+1 WHERE company_id=" + str(in_companyid) + " AND user_id=" + str(inuserid) + " AND ad_id=" + str(in_adid)
                self.m_cursor.execute(sql)
                if self.m_cursor.rowcount != 1:
                    return 1
                sql = "UPDATE ads SET ad_click_count=ad_click_count+1 WHERE ad_id=" + str(in_adid)
                self.m_cursor.execute(sql)
                if self.m_cursor.rowcount != 1:
                    return 1
        sql = "UPDATE ad_user_history SET ad_ctr=ad_click_count*100/ad_display_count WHERE company_id=" + str(in_companyid) + " AND user_id=" + str(inuserid) + " AND ad_id=" + str(in_adid)
        self.m_cursor.execute(sql)
        if self.m_cursor.rowcount != 1:
            return 1
        sql = "UPDATE ads SET ad_ctr=ad_click_count*100/ad_display_count WHERE ad_id=" + str(in_adid)
        self.m_cursor.execute(sql)
        if self.m_cursor.rowcount != 1:
            return 1
        self.m_connection.commit()
        return 0
