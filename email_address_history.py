# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 12:12:31 2020

@author: SCFNL21211
"""
import os
import sys

sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))
import database_tools as dbt

import time
import Flexmail_API as api
import pandas as pd
def set_connection(parameters_connection):
    return dbt.connect_to_db(parameters_connection)



def connection_to_db():
    parameters = ('Driver={SQL Server};'
                  'Server=appsql29nl;'
                  'Database=ODD_CRM;'
                  'UID=sas_ciuser;'
                  'PWD=resuic_sas;')
    conn = set_connection(parameters)

    return conn


def sqlc_query():
    sqlc = """
    select email
    from SHIVA_USR_COM.dbo.NL_EM_PL210330_Renovation
    
    """

    return sqlc


def loading_table(sql, conn):
    table = loading_data(sql, conn)
    return table

def loading_data(sql, connection, chunk=False):
    start_time = time.time()
    df = dbt.execute_query_to_dataframe(sql, connection, chunk=False)
    print("--- %s seconds ---" % (time.time() - start_time))
    return df


def main ():
    connection = connection_to_db()
    t_table = loading_data(sqlc_query(), connection)
    t_table_columns = t_table.columns.to_list()
    t_table_columns.append('History_code')
    results = pd.DataFrame(columns=t_table_columns)
    for index , row in t_table.iterrows():#table_campaing_Id_name.shape[0]):
        report_results = api.email_addresses_history (t_table.loc[index,'Emailadress']);
        results.loc [index,'CustomerID'] = t_table.loc[index,'CustomerID'];
        results.loc [index,'Emailadress'] = t_table.loc[index,'Emailadress'];
        print(index)
        try:
            report_results.emailAddressHistoryType.emailAddressHistoryActionTypeItems
        except AttributeError:
            results.loc [index,'History_code'] = None
            print(index)
        else:
            results.loc [index,'History_code'] = [x[0] for x in report_results.emailAddressHistoryType.emailAddressHistoryActionTypeItems];
            
            
    return results





def main_v1 ():
    connection = connection_to_db()
    t_table = loading_data(sqlc_query(), connection)
    t_table_columns = t_table.columns.to_list()
    t_table_columns.append('History_code')
    results = pd.DataFrame(columns=t_table_columns)
    for index , row in t_table.iterrows():#table_campaing_Id_name.shape[0]):
        report_results = api.email_addresses_history (t_table.loc[index,'Emailadress']);
        results.loc [index,'CustomerID'] = t_table.loc[index,'CustomerID'];
        results.loc [index,'Emailadress'] = t_table.loc[index,'Emailadress'];
        print(index)
        try:
            report_results.emailAddressHistoryType.emailAddressHistoryActionTypeItems
        except AttributeError:
            results.loc [index,'History_code'] = None
            print(index)
        else:
            results.loc [index,'History_code'] = [x[0] for x in report_results.emailAddressHistoryType.emailAddressHistoryActionTypeItems];
            
            
    return results