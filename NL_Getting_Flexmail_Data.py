# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 15:08:56 2021

@author: scfnl21211
"""

import pandas as pd
import Config
import os
import sys

sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))
# import database_tools as db
import Flexmail_API as api


def get_data_frame(data):
    df = pd.DataFrame(dict(Name=[x[1] for x in data.campaignTypeItems], Id=[x[0] for x in data.campaignTypeItems],
                           Sent_Date=[x[3] for x in data.campaignTypeItems],
                           Message_Id=[x[8] for x in data.campaignTypeItems],
                           MailingIds=[x[9] for x in data.campaignTypeItems],
                           Campaign_type=[x[13] for x in data.campaignTypeItems]))
    return df


def main():
    data = api.get_campaign_data(userID='11793', userToken="F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
    df = get_data_frame(data)
    df.to_csv(Config.path_save_primary_data)
    # db.exporting_to_sql_table (df,name='NL_Campaign_Data_Flexmail',parameters=Config.DB,schema='dbo')


if __name__ == '__main__':
    main()
