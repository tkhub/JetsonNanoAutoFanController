#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

sns_name_path = '/sys/devices/virtual/thermal/thermal_zoneX/YYYY'
ABSTEMP_ZERO = -235.15

ARG_MODE_ALL_NUM = 0
ARG_MODE_MAX_NUM = 1
ARG_MODE_AVE_NUM = 2
ARG_MODE_MIN_NUM = 3

sys_max_index = 0
sys_min_index = 0
sys_max_temp = ABSTEMP_ZERO
sys_min_temp = 1000.0
sys_ave_temp = 0
sys_ave_cnt = 0
""" def readsystemp(mode):
  ans = []

  for i in range(10):
    strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','type')
    try:
      typefile = open(strtmp)
    except :
      # センサファイルが存在しない
      sns_name.append('NON_SNS')
      sns_temp.append(ABSTEMP_ZERO)
      # rise Exception('')
    else:
      # ファイルが存在するので開く
      strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','temp')
      try:
        tempfile = open(strtmp)
      except:
        # 何らかの理由でファイルが開けない。
        sns_name.append('NON_SNS')
        sns_temp.append(ABSTEMP_ZERO)
      else:
  return ans """

ARG_MODE_ALL_STR = 'all'
ARG_MODE_MAX_STR = 'max'
ARG_MODE_AVE_STR = 'ave'
ARG_MODE_MIN_STR = 'min'

# open and store all active sensors
sns_name = []
sns_temp = []

for i in range(10):
  strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','type')
  try:
    typefile = open(strtmp)
  except :
    # センサファイルが存在しない
    sns_name.append('NON_SNS')
    sns_temp.append(ABSTEMP_ZERO)
  else:
    # ファイルが存在するので開く
    strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','temp')
    try:
      tempfile = open(strtmp)
    except:
      sns_name.append('NON_SNS')
      sns_temp.append(ABSTEMP_ZERO)
    else:

      strtmp = tempfile.read()
      strtmp = strtmp.rstrip('\n')
      temp = int(strtmp)

      if temp == 100000:
        sns_name.append('NON_SNS')
        sns_temp.append(ABSTEMP_ZERO)
      else:
        ftemp = temp/1000.0
        sns_temp.append(ftemp)
        strtmp = typefile.read()
        typefile.close()
        strtmp = strtmp.rstrip('\n')
        sns_name.append(strtmp)
        if sys_max_temp < ftemp:
          sys_max_temp = ftemp
          sys_max_index = i
        if sys_min_temp > ftemp:
          sys_min_temp = ftemp
          sys_min_index = i
        sys_ave_cnt += 1
        sys_ave_temp += ftemp
sys_ave_temp = sys_ave_temp / sys_ave_cnt

args = sys.argv

if len(args) == 1:
  args.append(ARG_MODE_ALL_STR)

if args[1] == ARG_MODE_ALL_STR:
  for i in range(len(sns_name)):
    if sns_name[i] != 'NON_SNS':
      print(sns_name[i] + ' : ' + str(sns_temp[i]) + 'degC')
  sys.exit(0)
elif args[1] == ARG_MODE_MAX_STR:
  print(sns_name[sys_max_index] + ' : ' + str(sns_temp[sys_max_index]) + 'degC')
  sys.exit(0)
elif args[1] == ARG_MODE_AVE_STR:
  print('Average : ' + str(sys_ave_temp))
  sys.exit(0)
elif args[1] == ARG_MODE_MIN_STR:
  print(sns_name[sys_min_index] + ' : ' + str(sns_temp[sys_min_index]) + 'degC')
  sys.exit(0)
else:
  sys.exit(1)
#print sys_ave_temp 
#print sys_max_temp 
#print sys_min_temp 

