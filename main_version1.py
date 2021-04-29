# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 16:29:39 2020

@author: SCFNL21211
"""

#   Create a factory and assign the values
from suds.client import Client
import pandas as pd
import xlwings as xw
import time
client = Client("https://soap.flexmail.eu/3.0.0/flexmail.wsdl")
##print(client)

def hit_links (id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
    GetCampaignTrackingLinksReq = client.factory.create('GetCampaignTrackingLinksReq')


    GetCampaignTrackingLinksReq.header =  {
            
            'userId' : userID,
            'userToken' : userToken,
            
            }
     
    
    GetCampaignTrackingLinksReq.campaignId = id
    

 
    link_data = client.service.GetCampaignTrackingLinks(GetCampaignTrackingLinksReq)
    sum_hit_links = sum([x[3] for x in link_data.trackingLinkTypeItems])
    return sum_hit_links

def reports (id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
   GetCampaignReportReq = client.factory.create('GetCampaignReportReq')


   GetCampaignReportReq.header =  {
            
            'userId' : userID,
            'userToken' : userToken,
            
            }
     
    
   GetCampaignReportReq.campaignId = id;
   #GetCampaignReportReq.campaignRead = True
   #GetCampaignReportReq.linkClicked = True

 
   report_data = client.service.GetCampaignReport(GetCampaignReportReq);
   
   return report_data


def email_addresses (id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
   GetEmailAddressesReq = client.factory.create('GetEmailAddressesReq')
   
   import numpy as np


   GetEmailAddressesReq.header =  {
            
            'userId' : userID,
            'userToken' : userToken,
            
            
            }
     
   GetEmailAddressesReq. mailingListIds =  {
            
            'mailingListIds' :id#np.array([194795, 194797])
            
            }
     
    
   #GetEmailAddressesReq.mailingListIds = np.array([194795, 194797]);
   #GetCampaignReportReq.campaignRead = True
   #GetCampaignReportReq.linkClicked = True

 
   report_data = client.service.GetEmailAddresses(GetEmailAddressesReq);
   
   return report_data



def email_addresses_history (email ='giona.rosinda@hotmail.com' ,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
   GetEmailAddressHistoryReq = client.factory.create('GetEmailAddressHistoryReq')
   
   


   GetEmailAddressHistoryReq.header =  {
            
            'userId' : userID,
            'userToken' : userToken,
            
            
            }
#   
#   GetEmailAddressHistoryReq.emailAddressHistoryOptionsType = {
#        
#        'campaignRead':True   
#           }
     
   GetEmailAddressHistoryReq.emailAddress =email 
   GetEmailAddressHistoryReq.timestampFrom ="2021-04-01T00:00:00" 
   GetEmailAddressHistoryReq.timestampTill ="2021-04-22T00:00:00" 
   
     
    
   #GetEmailAddressesReq.mailingListIds = np.array([194795, 194797]);
   #GetCampaignReportReq.campaignRead = True
   #GetCampaignReportReq.linkClicked = True

 
   report_data = client.service.GetEmailAddressHistory(GetEmailAddressHistoryReq);
   
   return report_data








def get_campaign_data(userID='11793', userToken="F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131",
                      client=Client("https://soap.flexmail.eu/3.0.0/flexmail.wsdl")):
    GetCampaignsReq = client.factory.create('GetCampaignsReq')
    GetCampaignsReq.header = {

        'userId': userID,
        'userToken': userToken,

    }
    campaign_data = client.service.GetCampaigns(GetCampaignsReq)
    return campaign_data


def get_dataframe (data):
    
    df = pd.DataFrame({'Name':[x[1] for x in data.campaignTypeItems],
       'Id':[x[0] for x in data.campaignTypeItems],
       'Sent_Date':[x[3] for x in data.campaignTypeItems],
       'Message_Id':[x[8] for x in data.campaignTypeItems],
       'MailingIds':[x[9] for x in data.campaignTypeItems],
       'Campaign_type':[x[13] for x in data.campaignTypeItems]
       })
    return df
    
def extract_primary_campaing_info(userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
    campaign_data = get_campaign_data (userID,userToken)
    table_campaing_Id_name = get_dataframe (campaign_data)
    return  table_campaing_Id_name
    
    
   
def main(df):
    
    
    #link_data = get_dataframe (campaign_data)
    for index in range(0,2880):#table_campaing_Id_name.shape[0]):
        df.loc [index,'Hits'] = hit_links (df.loc[index,'Id'])#table_campaing_Id_name[index,'Id'].iloc[i].apply(lambda x:hit_links(x))
        print(index)
        if index % 10 == 0 and index != 0:
            print('inside')
            time.sleep(60) 
    excel_app = xw.App(visible=False)
    
    wb = excel_app.books.open('test2.xlsx')

    ws = wb.sheets('Full_table')  # Name of sheet where to append df
    # ws.cells(1, 1).options(index=False, header=True).value = table_final
    ws.range("A1").options(index=False, header=True).value = results#table_campaing_Id_name
    tbl_range = ws.range("A1").expand('table')
    ws.api.ListObjects.Add(1, ws.api.Range(tbl_range.address))
   
    wb.save()
    wb.close()
    
    return table_campaing_Id_name


def main_with_data(new_column):
    data = pd.read_csv(r'D:\Python\Projects\NL_Automated_Reports\CRM\Campaign_reports_API\Primary_data.csv')
    data[new_column] = None
    for index , row in data[0:2].iterrows():#table_campaing_Id_name.shape[0]):
        report_results = reports (data.loc[index,'Id'])
        data.loc [index,'Ratio'] = report_results.campaignReportType[13]
        data.loc [index,'Date'] = report_results.campaignReportType[1]
        
         #table_campaing_Id_name[index,'Id'].iloc[i].apply(lambda x:hit_links(x))
        #print(index)
        if index % 10 == 0 and index != 0:
            print('Waiting')
            time.sleep(10) 
    
    return data    

def post_processing(data = pd.read_csv(r'Z:\Python\Projects\NL_Automated_Reports\CRM\Campaign_reports_API\Primary_data.csv')):
    data = data
    data['Date'] = pd.to_datetime(data['Date'],errors='coerce') 
    data['Year'] = data.Date.dt.year
    data['month'] = data.Date.dt.month
    return data
    

    
if __name__ == '__main__':
    results = extract_primary_campaing_info() 