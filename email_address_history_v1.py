# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 15:26:25 2020

@author: SCFNL21211
"""

import os
import sys
import time
sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))

import Flexmail_API as api
import pandas as pd
from ast import literal_eval

data = pd.read_csv(r'Z:\Python\Projects\BE_Automated_Reports\CRM\Flexmail_FTL_campaigns_2020\Data_for_Report\NL_primary_data.csv')
#data = pd.read_csv(r'Z:\Python\Projects\NL_Automated_Reports\CRM\Campaign_reports_API\Primary_data.csv')
data.drop(data[data['Campaign_type']!='Campaign'].index,inplace=True)
#emails_address = api.email_addresses (literal_eval(data.iloc[0].MailingIds))
#emails = [x[1] for x in emails_address.emailAddressTypeItems]
start_time = time.time()
test = data.iloc[0:5]['MailingIds'].apply(lambda x: api.email_addresses(literal_eval(x)) )
print("--- %s seconds ---" % (time.time() - start_time))
emails = [[x[1] for x in test[i].emailAddressTypeItems] for i in range(21)]
flat_emails = list(set([item for sublist in emails for item in sublist]))

## 5 seconds
#start_time = time.time()
#report_results = api.email_addresses_history (flat_emails[0])
#print("--- %s seconds ---" % (time.time() - start_time))

# 84 seconds
start_time = time.time()
results = pd.DataFrame(columns=['Emails','History_code'])
results['Emails'] = flat_emails

for index,items in  enumerate(flat_emails):
    results.loc [index,'History_code'] = [y[0] for y  in email_addresses_history(items).emailAddressHistoryType.emailAddressHistoryActionTypeItems]
    print(index)
    if index % 10 == 0 and index != 0:
        print('inside')
        
        results.to_csv('results.csv')
        time.sleep(30) 

results['History_code']=results.iloc[3:10]['Emails'].apply(lambda x:[y[0] for y  in email_addresses_history(x).emailAddressHistoryType.emailAddressHistoryActionTypeItems])
print("--- %s seconds ---" % (time.time() - start_time))

def find(sample_list,list_1):
    import re

    str_1 = str(list_1)[1:-1]
    return (len(re.findall(str_1, str(sample_list))))


results['Campaing_Sent'] = results['History_code'].apply(lambda x: x.count(17))
results['Campaing_Read'] = results.iloc[0:298]['History_code'].apply(lambda x: (find(x,[17,18])/x.count(17)*100))
#results['Campaing_Read'] = results.iloc[0:8]['History_code'].apply(lambda x: (x.count(18)/x.count(17))*100)
#results['Campaing_Read_online'] = results.iloc[0:8]['History_code'].apply(lambda x: (x.count(19)/x.count(17))*100)
results['Campaing_Click'] = results.iloc[0:298]['History_code'].apply(lambda x: (find(x,[18,20])/x.count(17)*100))

results['Campaing_Read_info'] = results.iloc[0:298]['History_code'].apply(lambda x: (x.count(22)/x.count(17))*100)
results['Campaing_Read_Form_visited'] = results.iloc[0:298]['History_code'].apply(lambda x: (x.count(23)/x.count(17))*100)
results['Campaing_Read_Form_Submitted'] = results.iloc[0:298]['History_code'].apply(lambda x: (x.count(24)/x.count(17))*100)
#results['Campaing_Click'] = results.iloc[0:8]['History_code'].apply(lambda x: x.count(20))









Action_id_dict = {1 : 'Address Created',2 : 'Address Deleted',3 : 'Address Visited Profile Update',
4 : 'Address Submitted Profile Update',5 : 'Address Subscribed',6 : 'Address Opted In',
7 : 'Address Visited Unsubscribe',8 : 'Address Unsubscribed',9 : 'Address Added To Group',
10 : 'Address Removed From Group',11 : 'Address Added To Account Blacklist',
12 : 'Address Removed From Account Blacklist',13 : 'Address Added To Mailing List Blacklist',
14 : 'Address Removed From Mailing List Blacklist',15 : 'Address Bounced',
16 : 'Address Bounced Out',17 : 'Campaign Sent',29 : 'Campaign Not Sent',
18 : 'Campaign Read',19 : 'Campaign Read Online',20 : 'Campaign Link Clicked',
21 : 'Campaign Link Group Click',22 : 'Campaign Read Infopage',23 : 'Campaign Form Visited',
24 : 'Campaign Form Submitted',25 : 'Campaign Survey Visited',26 : 'Campaign Survey Submitted',
27 : 'Campaign Forward Visited',28 : 'Campaign Forward Submitted',29 : 'Address Added To Preference',
30 : 'Address Removed From Preference',
}

