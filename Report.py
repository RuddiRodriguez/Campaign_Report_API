import pandas as pd
import os
import sys
import time
import re
from tqdm import tqdm

tqdm.pandas()
sys.path.insert(0, os.path.abspath(r'N:\SalesMarketing\Python_Scripts'))
import Config
import Flexmail_API as api


def get_data():
    df = pd.read_csv(Config.path_read_data, sep=';')
    return df


def find(sample_list, list_1):
    str_1 = str(list_1)[1:-1]
    return len(re.findall(str_1, str(sample_list)))


def get_sudo_objects(x):
    test = api.email_addresses_history(x, Config.user_id,
                                       Config.user_token).emailAddressHistoryType
    if test is not None:
        z = [y.actionId for y in test.emailAddressHistoryActionTypeItems if y.actionId > 16]
    else:
        z = None

    return z


def primary_data(data):
    start_time = time.time()
    df = pd.DataFrame(columns=['Emails', 'History_code'])
    df['Emails'] = data.iloc[6:100].CustomerEMailAddress1
    df['History_code'] = df['Emails'].progress_apply(lambda x: get_sudo_objects(x))
    df.dropna(subset=['History_code'], inplace=True)
    print("--- %s seconds ---" % (time.time() - start_time))
    return df


def create_new_columns(df):
    df['Campaign_Sent'] = df['History_code'].apply(lambda x: x.count(17))
    df.drop(df[df['Campaign_Sent'] == 0].index, inplace=True)
    df['Campaign_Read'] = df['History_code'].apply(lambda x: (find(x, [17, 18]) / x.count(17) * 100))
    df['Campaign_Read_Online'] = df['History_code'].apply(lambda x: (find(x, [17, 18, 19]) / x.count(17) * 100))
    df['Campaign_Click'] = df["History_code"].apply(lambda x: (find(x, [17, 18, 20]) / x.count(17) * 100))
    # df['Campaign_Read_info'] = df['History_code'].apply(lambda x: (x.count(22) / x.count(17)) * 100)
    # df['Campaign_Read_Form_visited'] = df['History_code'].apply(lambda x: (x.count(23) / x.count(17)) * 100)
    # df['Campaign_Read_Form_Submitted'] = df['History_code'].apply(lambda x: (x.count(24) / x.count(17)) * 100)
    return df


def main():
    print('get data')
    data = get_data()
    print('create new data')
    results = primary_data(data)
    print('create new columns')
    results = create_new_columns(results)
    print('save results')
    results.to_csv(r'D:\Python\Projects\NL_Automated_Reports\CRM\Campaign_reports_API\results2.csv', index=False)


if __name__ == '__main__':
    main()
