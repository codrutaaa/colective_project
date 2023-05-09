from datetime import datetime

import pandas as pd
from dateutil.relativedelta import relativedelta

from pp_utils.SharePoint import SharePoint
from pp_utils.account_Config import common_account
from pp_utils.db_conn_classes import DFDatabaseConnection
from pp_utils.pp_mappings import PPMapping


def main():
    credentials = {
        'username': common_account.email,
        'password': common_account.password_spo
    }

    target_url_param = "/sites/TribeSquadDashboard-DevTeam/Shared Documents/General/Colective Project/Date.csv"

    web_info = {
        'server_url': "https://nokia.sharepoint.com/",
        'site_url': "https://nokia.sharepoint.com/sites/TribeSquadDashboard-DevTeam/",
        'target_url': target_url_param
    }

    stored_file = "Date.csv"

    print("start download from sharepoint")
    sp = SharePoint(web_info['server_url'], web_info['site_url'], credentials['username'], credentials['password'],
                    web_info['target_url'], stored_file)
    sp.download()
    print("download from sharepoint done")

    df_util = DFDatabaseConnection("training_schema")
    table = 'date_colective_project'

    data_df = pd.read_csv('Date.csv')
    data_df.dropna(inplace=True)
    data_df['met_metric_id'] = 101
    data_df['usr_creator_id'] = 2424
    data_df['reporting_date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data_df.dropna(inplace=True)
    data_df = data_df.drop(['met_metric_id', 'usr_creator_id', 'reporting_date'], axis=1)
    data_df.columns = ['Year','Quarter','Month','Day','Month2','Period','Qtr','OtrID','Year2','YearPeriod','Year3','Qtr2','Month3']

    print(data_df)
    print()

    if data_df.empty is False:
        df_util.insert_processed_data_to_db(table, data_df, insert_type='append')
        print('Inserting into database finished...')
    else:
        print('There is no data to insert!')


if __name__ == "__main__":
    main()