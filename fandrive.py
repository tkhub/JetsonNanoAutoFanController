#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# togikai 81893782263

import sys

FANPWM_DEVICE_FILE="/sys/devices/pwm-fan/target_pwm"
PWMDAT_MAX = 255
PWMDATF_MAX = float(PWMDAT_MAX)
PWMDUTYF_MAX = 100.0

def fanpwmout(pwmdevice_path, duty):
  try:
    pwmdevice_file = open(pwmdevice_path, 'w')
  except: 
    raise PermissionError("CAN'T OPEN \""+ pwmdevice_path +"\".")
  else:
    pwmduty = (PWMDATF_MAX * duty) / PWMDUTYF_MAX 
    pwmdat = round(pwmduty)
    # pwm dat limit
    if pwmdat < 0:
      pwmdat = 0
    if PWMDAT_MAX < pwmdat:
      pwmdat = PWMDAT_MAX

    pwmdevice_file.write(str(pwmdat))
    pwmdevice_file.close()
    return pwmdat
""" 
ARG_DFLT_DUTY = 50
ARG_DFLT_DUTY_STR = str(ARG_DFLT_DUTY)


pwmduty = ARG_DFLT_DUTY

# 引数省略時はDFLT_DUTYに固定
if len(args) == 1:
  args.append(ARG_DFLT_DUTY_STR)

# 引数を判定
if re.match(r'[0-9]{1,3}', args[1]):
  try:
    dutyfile = open(FANPWM_DEVICE_FILE,'w')
  except :
    print("CAN'T OPEN FILE")
    sys.exit(1)
  else:
    print("PWM_DAT=" + fanpwmout(float(args[1])))
    sys.exit(0)
else:
  print("Arg is ONLY num(0-100)")
  sys.exit(1)
 """
args = sys.argv
if len(args) == 2:
  print(fanpwmout(FANPWM_DEVICE_FILE, float(args[1])))
else:
  print("arg err")
