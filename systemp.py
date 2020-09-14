#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sns_name_path = '/sys/devices/virtual/thermal/thermal_zoneX/YYYY'
ABSTEMP_ZERO = -235.15
SYSTEMP_GAIN = 1000.0
SYSTEMP_OL = 100000
ARG_MODE_ALL = "all"
ARG_MODE_MAX = "max"
ARG_MODE_MIN = "min"
ARG_MODE_AVE = "ave" 

def readsystemp(mode):
  sns_name = []
  sns_temp = []

  sys_max_index = 0
  sys_min_index = 0
  sys_max_temp = ABSTEMP_ZERO
  sys_min_temp = 1000.0
  sys_ave_temp = 0.0
  sys_temp_cnt = 0
  for i in range(10):
    # センサ名ファイルを開く
    strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','type')
    try:
      typefile = open(strtmp)
    except:
      # 開けないファイルもあって当然なのでスルー
      pass
    else:
      # センサ名ファイルが存在するので開く
      # センサ温度ファイルのファイル名を生成する
      strtmp = sns_name_path.replace('X',str(i)).replace('YYYY','temp')
      try:
        tempfile = open(strtmp)
      except:
        raise Exception("Can't Open Temp Files.")
      else:
        # 開けるファイルだけ開く
        strtmp = tempfile.read()
        strtmp = strtmp.rstrip('\n')
        int_temp = int(strtmp)
        tempfile.close()

        if int_temp == SYSTEMP_OL:
          # 温度が無効値（センサが実際には機能していない場合）
          pass
        else:
          # センサが有効な場合のみセンサ名とセンサ温度両方を開く
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
          sys_temp_cnt += 1
          sys_ave_temp += ftemp
  if sys_temp_cnt == 0:
    # 
    raise FileNotFoundError("CAN'T OPEN ANY TEMP SNS FILE!")
  else:
    sys_ave = sys_ave_temp / sys_temp_cnt
  
  if mode == ARG_MODE_AVE:
    print(sns_temp)
    return "Average" , sys_ave
  elif mode == ARG_MODE_MAX:
    return sns_name[sys_max_index - 1], sns_temp[sys_max_index - 1]
  elif mode == ARG_MODE_MIN:
    return sns_name[sys_min_index - 1], sns_temp[sys_min_index - 1]
  elif mode == ARG_MODE_ALL:
    return sns_name, sns_temp
  else:
    raise ValueError("Invalid Argument!")

def main(args):
  import sys
  from systemp import readsystemp

  ARG_MODE_ALL_STR = 'all'
  ARG_MODE_MAX_STR = 'max'
  ARG_MODE_AVE_STR = 'ave'
  ARG_MODE_MIN_STR = 'min'

  ans = []
  sns_name = []
  sns_temp = []
  if len(args) == 1:
    sns_name, sns_temp = readsystemp(ARG_MODE_ALL_STR)
    for sns, temp in zip(sns_name, sns_temp):
      print(sns + "\t: " + str(temp) + " degC")
  elif args[1] == ARG_MODE_ALL_STR:
    sns_name, sns_temp = readsystemp(ARG_MODE_ALL_STR)
    for sns, temp in zip(sns_name, sns_temp):
      print(sns + "\t: " + str(temp) + " degC")
  elif args[1] == ARG_MODE_MIN_STR:
    sns_name, sns_temp = readsystemp(ARG_MODE_MIN_STR)
    print(sns_name + "\t: " + str(sns_temp) + " degC")
  elif args[1] == ARG_MODE_MAX_STR:
    sns_name, sns_temp = readsystemp(ARG_MODE_MAX_STR)
    print(sns_name + "\t: " + str(sns_temp) + " degC")
  elif args[1] == ARG_MODE_AVE_STR:
    sns_name, sns_temp = readsystemp(ARG_MODE_AVE_STR)
    print("AVerage \t: " + str(sns_temp) + " degC")
  else:
    print("Invalid Arg")

if __name__ == "__main__":
  strin = sys.argv
  try:
    main(strin)
  except Exception as e:
    print(e)
  else:
    print("end")