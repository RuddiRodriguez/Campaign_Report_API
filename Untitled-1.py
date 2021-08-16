#%%
import pandas as  pd 
import os
import sys
import time
from tqdm import tqdm
tqdm.pandas()
sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))

import Flexmail_API as api
# %%
data = pd.read_csv(r'N:\SalesMarketing\CRM - Analysis George new\Campaigns and Campaign Reporting\Campaign Selections\Loans\2020\October Living Month\201015_EM2_REM1_.csv',sep=';')
# %%
start_time = time.time()
results = pd.DataFrame(columns=['Emails','History_code'])
results['Emails'] = data.iloc[5:50].email
results['History_code']=results['Emails'].progress_apply(lambda x:[y.actionId for y  in api.email_addresses_history(x,user_id='11793',
                            user_token="F40A3704-84726810-732DA059-4549C832-3179A85CD2339373131").emailAddressHistoryType.emailAddressHistoryActionTypeItems if y.actionId>1])
print("--- %s seconds ---" % (time.time() - start_time))

# %%
def find(sample_list,list_1):
    import re

    str_1 = str(list_1)[1:-1]
    return (len(re.findall(str_1, str(sample_list))))

results['Campaing_Sent'] = results['History_code'].apply(lambda x: x.count(17))
results.drop(results[results['Campaing_Sent'] == 0].index, inplace = True) 
results['Campaing_Read'] = results['History_code'].apply(lambda x: (find(x,[17,18])/x.count(17)*100))
results['Campaing_Click'] = results['History_code'].apply(lambda x: (find(x,[18,20])/x.count(17)*100))
results['Campaing_Read_info'] = results['History_code'].apply(lambda x: (x.count(22)/x.count(17))*100)
results['Campaing_Read_Form_visited'] = results['History_code'].apply(lambda x: (x.count(23)/x.count(17))*100)
results['Campaing_Read_Form_Submitted'] = results['History_code'].apply(lambda x: (x.count(24)/x.count(17))*100)
# %%
results
# %%
