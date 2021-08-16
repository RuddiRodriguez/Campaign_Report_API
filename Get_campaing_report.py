# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 15:39:25 2021

@author: scfnl21211
"""

import pandas as pd
from suds.client import Client
import plotly.graph_objects as go
client = Client("https://soap.flexmail.eu/3.0.0/flexmail.wsdl")
import os
import sys
sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))
import database_tools as db
import Flexmail_API as api




df = pd.read_csv(r'D:\Python\Projects\NL_Automated_Reports\CRM\Campaign_reports_API\Data\NL_Raw_Data.csv')
campaing_id = [x for x in df[df['Name'].str.contains('EM-MT2')]['Id']]


def get_dataframe(data):
    
    
    
    df = pd.DataFrame(zip([x[0] for x in data.campaignReportType],
                    [x[1] for x in data.campaignReportType]),
        columns=['Field','Value'])
    return df



def get_results (campaing_id):
    report_results = api.reports(campaing_id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
    table = get_dataframe(report_results)
    return table


def export_results(df):
    
    

    fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                fill_color='darkred',
                font_color='white',
                align='left'),
                        cells=dict(values=[df.Field, df.Value],
               fill_color='lavender',
               
               align='left'))
            ])

    fig.update_layout(title_text='Flexmail Report')
    fig.show()
    fig.write_html(r'N:\SalesMarketing\CRM - Analysis George new\Campaigns and Campaign Reporting\Campaign Selections\Loans\2021\Money_Talk\Data\Report_Batch2_3.html')

def main ():
    results =[ get_results(index) for index in campaing_id]
    df = pd.concat(results, axis=0)
    
    export_results(df)

