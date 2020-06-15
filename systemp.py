#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sns_name_path = '/sys/devices/virtual/thermal/thermal_zoneX/YYYY'
ABSTEMP_ZERO = -235.15
SYSTEMP_GAIN = 1000.0
SYSTEMP_OL = 100000
ARG_MODE_ALL_NUM = 0
ARG_MODE_MAX_NUM = 1
ARG_MODE_AVE_NUM = 2
ARG_MODE_MIN_NUM = 3

def readsystemp(mode):
  ans = []
  sns_name = []
  sns_temp = []

  sys_max_index = 0
  sys_min_index = 0
  sys_max_temp = ABSTEMP_ZERO
  sys_min_temp = 1000.0
  sys_ave_temp = 0
  sys_ave_cnt = 0
  for i in range(10):
    strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','type')
    try:
      typefile = open(strtmp)
    except :
      # センサ名ファイルが存在しない
      #sns_name.append('NON_SNS')
      #sns_temp.append(ABSTEMP_ZERO)
      # rise Exception('')
      pass
    else:
      # センサ名ファイルが存在するので開く
      # センサ温度ファイルのファイル名を生成する
      strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','temp')
      try:
        tempfile = open(strtmp)
      except:
        # 何らかの理由でセンサ温度ファイルが開けない。
        # sns_name.append('NON_SNS')
        # sns_temp.append(ABSTEMP_ZERO)
        pass
      else:
        # 開けるファイルだけ開く
        strtmp = tempfile.read()
        strtmp = strtmp.rstrip('\n')
        int_temp = int(strtmp)
        tempfile.close()

        if int_temp == SYSTEMP_OL:
          # 温度が無効値（センサが実際には機能していない場合）
          # sns_name.append('NON_SNS')
          # sns_temp.append(ABSTEMP_ZERO)
          pass
        else:
          # センサが有効な場合のみセンサ名とセンサ温度療法を開く
          # センサ名を取得
          strtmp = typefile.read()
          strtmp = strtmp.rstrip('\n')
          typefile.close()
          sns_name.append(strtmp)
          # センサ温度を算出
          # 計測温度値は小数第3位までの固定小数点のため
          ftemp = float(int_temp) / SYSTEMP_GAIN
          sns_temp.append(ftemp)

          # 最大値取得
          if sys_max_temp < ftemp:
            sys_max_temp = ftemp
            sys_max_index = i
          # 最小値取得
          if sys_min_temp > ftemp:
            sys_min_temp = ftemp
            sys_min_index = i
          sys_ave_cnt += 1
          sys_ave_temp += ftemp
  sys_ave_temp = sys_ave_temp / sys_ave_cnt
  if mode == ARG_MODE_AVE_NUM:
    # ans.append(["Average", sys_ave_temp])
    return "Average" , sys_ave_temp
  elif mode == ARG_MODE_MAX_NUM:
    # ans.append([sns_name[sys_max_index], sns_temp[sys_max_index]])
    return sns_name[sys_max_index - 1], sns_temp[sys_max_index - 1]
  elif mode == ARG_MODE_MIN_NUM:
    # ans.append([sns_name[sys_min_index], sns_temp[sys_min_index]])
    return sns_name[sys_min_index - 1], sns_temp[sys_min_index - 1]
  else:
    #for i in range(len(sns_name)):
    #  ans.append([sns_name[i], sns_temp[i]])
    return sns_name, sns_temp

ARG_MODE_ALL_STR = 'all'
ARG_MODE_MAX_STR = 'max'
ARG_MODE_AVE_STR = 'ave'
ARG_MODE_MIN_STR = 'min'

args = sys.argv
ans = []
sns_name = []
sns_temp = []
if len(args) == 1:
  sns_name, sns_temp = readsystemp(ARG_MODE_ALL_NUM)
  for sns, temp in zip(sns_name, sns_temp):
    print(sns + "\t: " + str(temp) + "degC")
  sys.exit(1)
elif args[1] == ARG_MODE_ALL_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_ALL_NUM)
  for sns, temp in zip(sns_name, sns_temp):
    print(sns + "\t: " + str(temp) + "degC")
  sys.exit(0)
elif args[1] == ARG_MODE_MIN_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_MIN_NUM)
  print(sns_name + "\t: " + str(sns_temp) + "degC")
  sys.exit(0)
elif args[1] == ARG_MODE_MAX_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_MAX_NUM)
  print(sns_name + "\t: " + str(sns_temp) + "degC")
  sys.exit(0)
elif args[1] == ARG_MODE_AVE_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_AVE_NUM)
  print("AVerage \t: " + str(sns_temp) + "degC")
  sys.exit(0)
else:
  print("Invalid Arg")
  sys.exit(1)

#print sys_ave_temp 
#print sys_max_temp 
#print sys_min_temp 

