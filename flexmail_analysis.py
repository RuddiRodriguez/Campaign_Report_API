import pandas as pd 
import os
import sys
sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))
import Flexmail_API as api



df = pd.read_csv(r'D:\Python\Projects\NL_Automated_Reports\CRM\Campaign_reports_API\Data\NL_Raw_Data.csv')


# filters
def filters (df):
    filter1 = df['Campaign_type'] !='TestCampaign'
    filter2 = df['Campaign_type'] !='0'
    filter3 = df['Name'].str.contains('EM')
    filter4 = df['Name'].str.contains('Welcome')==False
    filter5 = df['Name'].str.contains('Vasteklantenactie_MM')==True
    df = df[filter1 & filter2 & filter3 & filter4 & filter5]
    return df 

def get_results (campaing_id=15265746):
    report_results = api.reports(campaing_id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
    table = get_dataframe(report_results)
    return table   

""" def get_dataframe(data):
    
    
    
    df = pd.DataFrame(zip([x[0] for x in data.campaignReportType],
                    [x[1] for x in data.campaignReportType]),
        columns=['Field','Value'])
    return df     
 """

def get_dataframe(data):
    
    
    
    df = pd.DataFrame([x[1] for x in data.campaignReportType]).T
    return df

def get_column_names (campaing_id=15265746):
    report_results = api.reports(campaing_id,userID = '11793',userToken = "F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131")
    
    return [x[0] for x in report_results.campaignReportType]


df_f = filters(df)
df_f  
#df_f.Sent_Date = pd.to_datetime(df_f.Sent_Date).dt.date
#df_f.set_index(df_f.Sent_Date.dt.date,inplace=True)
df_JM = df_f[(df_f['Sent_Date']>='2021-01-01') & (df_f['Sent_Date']<='2021-04-1')]
df_HQ = pd.read_excel(r'D:\Python\Projects\NL_Automated_Reports\CRM\Campaigns_Response\Total_Response\Data\Campaing_Results_HQ.xlsx',sheet_name='Data_v1')
df_JM.Sent_Date=pd.to_datetime(df_JM.Sent_Date)
df_JM['Launch Date'] = pd.to_datetime(df_JM.Sent_Date.dt.date)
df_HQ_flexmail = pd.merge(df_HQ,df_JM,on='Launch Date',how='left')
print(df_JM.shape)
print(df_HQ_flexmail.shape)

import math
campaing_id = [x for x in df_HQ_flexmail['Id'] if math.isnan(x)==False]

results =[ get_results(index) for index in campaing_id]
df_final = pd.concat(results, axis=0)
column_names  = get_column_names (campaing_id[0])
df_final.columns = column_names

df_final

df_merge = pd.merge(df_HQ_flexmail,df_final, left_on='Id', right_on='campaignId')

condition1 = (df_merge['Name'].str.contains('BW')) & (df_merge['Name'].str.contains('REM'))
condition2 = (df_merge['Name'].str.contains('BW')) & (df_merge['Name'].str.contains('REM')==False)

condition3 = (df_merge['Name'].str.contains('Renovation')) & (df_merge['Name'].str.contains('REM'))
condition4 = (df_merge['Name'].str.contains('Renovation')) & (df_merge['Name'].str.contains('REM')==False)

conds = [condition1,condition2,condition3,condition4]
choice = ['Best_Wishes_REM','Best_Wishes','Renovation_REM','Renovation']
df_merge['Campaign'] = np.select(conds,choice)
df_merge.Campaign.value_counts()



df_merge.to_excel(r'D:\Python\Projects\NL_Automated_Reports\CRM\Campaigns_Response\Total_Response\Data\Flexmail.xlsx')