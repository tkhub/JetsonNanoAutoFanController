#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
FANPWM_DEVICE_FILE="/sys/devices/pwm-fan/target_pwm"
PWMDAT_MAX = 255
PWMDATF_MAX = float(PWMDAT_MAX)
PWMDUTYF_MAX = 100.0

def fanchk():
  if os.path.exists(FANPWM_DEVICE_FILE):
    return True
  else:
    return False

def pwmout(duty):
  try:
    pwmdevice_file = open(FANPWM_DEVICE_FILE, 'w')
  except FileNotFoundError:
    raise FileNotFoundError("CAN'T FINDE\""+ FANPWM_DEVICE_FILE + "\".")
  except PermissionError:
    raise PermissionError("CAN'T OPEN \""+ FANPWM_DEVICE_FILE + "\".")
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
