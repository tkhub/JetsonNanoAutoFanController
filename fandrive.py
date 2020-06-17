#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# togikai 81893782263

# import sys

# FANPWM_DEVICE_FILE="/sys/devices/pwm-fan/target_pwm"
PWMDAT_MAX = 255
PWMDATF_MAX = float(PWMDAT_MAX)
PWMDUTYF_MAX = 100.0

def fanpwmout(pwmdevice_path, duty):
  try:
    pwmdevice_file = open(pwmdevice_path, 'w')
  except FileNotFoundError:
    raise FileNotFoundError("CAN'T FINDE\""+ pwmdevice_path +"\".")
  except PermissionError:
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

# args = sys.argv
# if len(args) == 2:
#  print(fanpwmout(FANPWM_DEVICE_FILE, float(args[1])))
# else:
#   print("arg err")
