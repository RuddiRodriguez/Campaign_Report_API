# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 14:02:15 2021

@author: scfnl21211
"""

import os
import shutil
import sys
from datetime import timedelta

import numpy as np
import pandas as pd
import datetime

import Config

sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))

import Flexmail_API as api

def get_sudo_objects(x):
    test = api.email_addresses_history(x, Config.user_id,
                                       Config.user_token).emailAddressHistoryType
    if test is not None:
        z = [y.actionId for y in test.emailAddressHistoryActionTypeItems if y.actionId > 16]
    else:
        z = None

    return z


def campaign_data():
    data = api.get_campaign_data(Config.user_id,
                                       Config.user_token).campaignTypeItems
    

    return data

def get_dataframe (data):
    
    df = pd.DataFrame({'Name':[x[1] for x in data.campaignTypeItems],
       'Id':[x[0] for x in data.campaignTypeItems],
       'Sent_Date':[x[3] for x in data.campaignTypeItems],
       'Message_Id':[x[8] for x in data.campaignTypeItems],
       'MailingIds':[x[9] for x in data.campaignTypeItems],
       'Campaign_type':[x[13] for x in data.campaignTypeItems]
       })
    return df


def extract_primary_campaing_info():
        data = campaign_data ()
        table_campaing = get_dataframe (data)
        return table_campaing
    
table = extract_primary_campaing_info()