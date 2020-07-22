# -*- coding: utf-8 -*-
"""
Created on Wed Jun 10 17:29:05 2020

@author: SCFNL21211
"""

#%%from suds.client import Client
import pandas as pd
import xlwings as xw
import time
from suds.client import Client
client = Client("https://soap.flexmail.eu/3.0.0/flexmail.wsdl")
# %%
def hit_links (id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
   GetCampaignReportReq = client.factory.create('GetCampaignReportReq')


   GetCampaignReportReq.header =  {
            
            'userId' : userID,
            'userToken' : userToken,
            
            }
     
    
   GetCampaignReportReq.campaignId = id
   #GetCampaignReportReq.campaignRead = True
   #GetCampaignReportReq.linkClicked = True

 
   link_data = client.service.GetCampaignReport(GetCampaignReportReq)
    #sum_hit_links = sum([x[3] for x in link_data.trackingLinkTypeItems])
   return link_data

# %%
#import pandas as pd 
data = hit_links (3003134,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
#df = pd.DataFrame({'name':[x[1] for x in data.trackingLinkTypeItems],'link':[x[2] for x in data.trackingLinkTypeItems],
 #      'hits':[x[3] for x in data.trackingLinkTypeItems]})

# %%
data

# %%
import xlwings as xw
excel_app = xw.App(visible=False)
    
wb = excel_app.books.open('test2.xlsx')
#
ws = wb.sheets('Examples')  # Name of sheet where to append df
ws.cells(28, 1).options(index=False, header=True).value = df
#    ws.range("A1").options(index=False, header=True).value = table_campaing_Id_name
#    tbl_range = ws.range("A1").expand('table')
#    ws.api.ListObjects.Add(1, ws.api.Range(tbl_range.address))
#   
wb.save()
wb.close()

# %%
data.CampaignReportType

# %%
data.