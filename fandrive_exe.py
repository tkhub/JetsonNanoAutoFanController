#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re
from fandrive import pwmout



ARG_DFLT_DUTY = 50
ARG_DFLT_DUTY_STR = str(ARG_DFLT_DUTY)

args = sys.argv

if len(args) == 1:
  # 引数省略時はDFLT_DUTYに固定
  pwmduty = ARG_DFLT_DUTY
else:
  # 引数ありの場合
  try:
    pwmduty = float(args[1])
  except ValueError as identifier:
    print("Error! Argument is NOT Number!")
    sys.exit(1)
  else:
    pass


try:
  rtnstrtmp = pwmout(pwmduty)
except FileNotFoundError:
  print ("Can't Find Fanpwm File.")
except PermissionError:
  print ("Can't Open Fanpwm File.")
else:
  print("PWM_DAT = " + str(rtnstrtmp))