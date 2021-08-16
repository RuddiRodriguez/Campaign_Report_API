# %%

import pandas as pd
import xlwings as xw
import time
from suds.client import Client
client = Client("https://soap.flexmail.eu/3.0.0/flexmail.wsdl")
#%%
def get_campaign_data(userID='11793', userToken="F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131",
                      client=Client("https://soap.flexmail.eu/3.0.0/flexmail.wsdl")):
    GetCampaignsReq = client.factory.create('GetCampaignsReq')
    GetCampaignsReq.header = {

        'userId': userID,
        'userToken': userToken,

    }
    campaign_data = client.service.GetCampaigns(GetCampaignsReq)
    return campaign_data
#%%
data_c = get_campaign_data (userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
df = pd.DataFrame({'Name':[x[1] for x in data_c.campaignTypeItems],
       'Id':[x[0] for x in data_c.campaignTypeItems],
       'Sent_Date':[x[3] for x in data_c.campaignTypeItems],
       'Message_Id':[x[8] for x in data_c.campaignTypeItems],
       'MailingIds':[x[9] for x in data_c.campaignTypeItems],
       'Campaign_type':[x[13] for x in data_c.campaignTypeItems]
       })
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

def TrackingLink (id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
   GetCampaignTrackingLinksReq = client.factory.create('GetCampaignTrackingLinksReq')


   GetCampaignTrackingLinksReq.header =  {
            
            'userId' : userID,
            'userToken' : userToken,
            
            }
     
    
   GetCampaignTrackingLinksReq.campaignId = id
   #GetCampaignReportReq.campaignRead = True
   #GetCampaignReportReq.linkClicked = True

 
   link_data = client.service.GetCampaignTrackingLinks(GetCampaignTrackingLinksReq)
    #sum_hit_links = sum([x[3] for x in link_data.trackingLinkTypeItems])
   return link_data
#%%
def TrackingLink_hit (id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131"):
   GetTrackingLinkHitsReq = client.factory.create('GetTrackingLinkHitsReq')


   GetTrackingLinkHitsReq.header =  {
            
            'userId' : userID,
            'userToken' : userToken,
            
            }
     
    
   GetTrackingLinkHitsReq.trackingLinkId = id
   

 
   hit_links = client.service.GetTrackingLinkHits(GetTrackingLinkHitsReq)
    #sum_hit_links = sum([x[3] for x in link_data.trackingLinkTypeItems])
   return hit_links   
data_hit = TrackingLink (216,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
#%%
data = TrackingLink (8248524,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
#%%

# %%
#import pandas as pd 
data = hit_links (8248524,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
#df = pd.DataFrame({'name':[x[1] for x in data.trackingLinkTypeItems],'link':[x[2] for x in data.trackingLinkTypeItems],
 #      'hits':[x[3] for x in data.trackingLinkTypeItems]})

# %%
data.campaignReportType[1] 
# %%
def campaign_history(id, userID='11793', userToken="F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131",
                      client=Client("https://soap.flexmail.eu/3.0.0/flexmail.wsdl")):

    GetCampaignHistoryReq  = client.factory.create('GetCampaignHistoryReq')

    GetCampaignHistoryReq.header = {

        'userId': userID,
        'userToken': userToken,

    }

    GetCampaignHistoryReq.campaignId = id
    GetCampaignHistoryReq.timestampFrom  = "14-04-2020 13:12"
    GetCampaignHistoryReq.timestampTill = "14-04-2020 18:12"


    GetCampaignHistoryReq.campaignHistoryOptionsType ={
        # "campaignSent" : True
         # campaignNotSent = None
      #   "campaignRead" : True
         # campaignReadOnline = None
         # campaignLinkClicked = None
         # campaignLinkGroupClicked = None
         # campaignReadInfopage = None
         # campaignFormVisited = None
         # campaignFormSubmitted = None
         # campaignSurveyVisited = None
         # campaignSurveySubmitted = None
         # campaignForwardVisited = None
         # campaignForwardSubmitted = None
    }

    report_data = client.service.GetCampaignHistory(GetCampaignHistoryReq);

    return report_data
# %%
data1 = campaign_history (8248524,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
# %%
data1.campaignHistoryType[0].campaignId
# %%
