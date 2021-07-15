#--------------------
# adclient.py
#--------------------

from lib.dbapi import DBApi

class AdClient(DBApi):
    def getAds(self, in_adid=''):
        if not in_adid:
            sql = "SELECT ad_id,ad_landing_page_url,ad_type_id,ad_url,ad_click_count,ad_cpc,ad_ctr FROM ads"
        else:
            sql = "SELECT ad_id,ad_landing_page_url,ad_type_id,ad_url,ad_click_count,ad_cpc,ad_ctr FROM ads where ad_id = " + in_adid
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def postAds(self, in_companyid='', in_adlandingpageurl='', in_adtypeid='', in_adimageurl=''):
        sql = "INSERT INTO ads ( company_id, ad_landing_page_url, ad_type_id, ad_image_url ) VALUES ( " + in_companyid + ", '" + in_adlandingpageurl + "' ," + in_adtypeid + ", '" + in_adimageurl + "' )"
        self.m_cursor.execute(sql)
        self.m_connection.commit()
        if self.m_cursor.rowcount == 1:
            return 0
        else:
            return 1
    def putAds(self, in_adid='', in_companyid='', in_adlandingpageurl='', in_adtypeid='', in_adimageurl=''):
        sql = "UPDATE ads SET company_id = " + in_companyid + ", ad_landing_page_url = '" + in_adlandingpageurl + "', ad_type_id = " + in_adtypeid + ", ad_image_url = '" + in_adimageurl + "' WHERE ad_id = " + in_adid
        self.m_cursor.execute(sql)
        self.m_connection.commit()
        if self.m_cursor.rowcount == 1:
            return 0
        else:
            return 1
    def deleteAds(self, in_adid=''):
        sql = "DELETE ads WHERE ad_id = " + in_adid
        self.m_cursor.execute(sql)
        self.m_connection.commit()
        if self.m_cursor.rowcount == 1:
            return 0
        else:
            return 1
    def getAdTypes(self):
        sql = "SELECT * FROM m_ad_types"
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def getTargetCompanySectors(self, in_adid=''):
        if not in_adid:
            sql = "SELECT campany_sector_id,campany_sector_name,is_checked FROM ad_target_campany_sectors"
        else:
            sql = "SELECT campany_sector_id,campany_sector_name,is_checked FROM ad_target_campany_sectors where ad_id = " + in_adid
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def getTargetCompanyScales(self, in_adid=''):
        if not in_adid:
            sql = "SELECT * FROM ad_target_campany_scales"
        else:
            sql = "SELECT * FROM ad_target_campany_scales where ad_id = " + in_adid
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def getTargetUserDepartments(self, in_adid=''):
        if not in_adid:
            sql = "SELECT * FROM ad_target_user_departments"
        else:
            sql = "SELECT * FROM ad_target_user_departments where ad_id = " + in_adid
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def getTargetUserPositions(self, in_adid=''):
        if not in_adid:
            sql = "SELECT * FROM ad_target_user_positions"
        else:
            sql = "SELECT * FROM ad_target_user_positions where ad_id = " + in_adid
        self.m_cursor.execute(sql)
        columns = [column[0] for column in self.m_cursor.description]
        results = []
        for row in self.m_cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results
    def updateAdHistories(self, in_companyid, inuserid, in_adid, in_displayed, in_clicked):
        sql = "SELECT * FROM ad_user_history WHERE company_id=" + str(in_companyid) + " AND user_id=" + str(inuserid) + " AND ad_id=" + str(in_adid)
        datum = self.m_cursor.execute(sql)
        if len(datum.fetchall()) == 0:
            # �ǉ�
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
            # �X�V
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
