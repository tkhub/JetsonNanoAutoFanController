#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from systemp import readsystemp

ARG_MODE_ALL_STR = 'all'
ARG_MODE_MAX_STR = 'max'
ARG_MODE_AVE_STR = 'ave'
ARG_MODE_MIN_STR = 'min'

args = sys.argv
ans = []
sns_name = []
sns_temp = []
if len(args) == 1:
  sns_name, sns_temp = readsystemp(ARG_MODE_ALL_STR)
  for sns, temp in zip(sns_name, sns_temp):
    print(sns + "\t: " + str(temp) + " degC")
  sys.exit(1)
elif args[1] == ARG_MODE_ALL_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_ALL_STR)
  for sns, temp in zip(sns_name, sns_temp):
    print(sns + "\t: " + str(temp) + " degC")
  sys.exit(0)
elif args[1] == ARG_MODE_MIN_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_MIN_STR)
  print(sns_name + "\t: " + str(sns_temp) + " degC")
  sys.exit(0)
elif args[1] == ARG_MODE_MAX_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_MAX_STR)
  print(sns_name + "\t: " + str(sns_temp) + " degC")
  sys.exit(0)
elif args[1] == ARG_MODE_AVE_STR:
  sns_name, sns_temp = readsystemp(ARG_MODE_AVE_STR)
  print("AVerage \t: " + str(sns_temp) + " degC")
  sys.exit(0)
else:
  print("Invalid Arg")
  sys.exit(1)

#print sys_ave_temp 
#print sys_max_temp 
#print sys_min_temp 

