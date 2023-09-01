import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# テキストを追記する関数
def append_to_file(filename, text):
    with open(filename, 'a') as file:
        file.write(text)
        
input_directory = "/home/ec2-user/environment/observation/SYNOP/program/TEST/Precipitration/file/data/IDdata_result/"
output_directory = "/home/ec2-user/environment/observation/SYNOP/program/TEST/Precipitration/file/data/IDroop_result/"

output_files = []

for filename in os.listdir(input_directory):

  try:

      if filename.endswith(".csv"):

        input_file = os.path.join(input_directory, filename)

        df_org = pd.read_csv(input_file)

        df_org['localtime'] = pd.to_datetime(df_org['localtime'])

        localtime_list = sorted(df_org["localtime"].unique()) # 重複を除外してlocaltimeを取得

        df_all = pd.DataFrame()

        for (i, localtime) in enumerate(localtime_list, 1):
          df_single = df_org[df_org["localtime"] == localtime]
          if len(df_single) == 0:
            continue # df_single が空ならばスキップ
          hour_interval = df_single["PrecipitationTerm"].iloc[0]
          if hour_interval == 0:
            continue # hour_interval がゼロならばスキップ
          total_Precipitation = df_single["Precipitation"].iloc[0]
          Precipitation_1hour = total_Precipitation / hour_interval
          single_data = []
          for j in range(0, hour_interval):
            time_diff = pd.to_timedelta(-j, unit='h')
            valid_localtime = localtime + time_diff
            single_data.append([valid_localtime, Precipitation_1hour])
          df_single_data = pd.DataFrame(single_data, columns=['localtime', 'Precipitation'])
          df_all = df_all.append(df_single_data, ignore_index=True)
        df_all = df_all.sort_values(by=["localtime"], ascending=True)
        output_file = os.path.join(output_directory, f"processed_{filename}")
        df_all.to_csv(output_file, index=False)
        output_files.append(output_file)
    except:
        #errorを起こしたファイル名を追記するフォルダ
        append_to_file('/test/text.txt', '%s\n'%(filename))
    
for output_file in output_files:
  print(f"Data has been saved to {output_file}")