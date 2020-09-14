#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
FANPWM_DEVICE_FILE="/sys/devices/pwm-fan/target_pwm"
PWMDAT_MAX = 255
PWMDATF_MAX = float(PWMDAT_MAX)
PWMDUTYF_MAX = 100.0



def fanchk():
  if os.access(FANPWM_DEVICE_FILE, os.W_OK):
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

def main(args):
    if len(args) == 2:
        print(pwmout(float(args[1])))
    else:
        print("arg err")
        print(fanchk())


if __name__ == "__main__":
  strin = sys.argv
  try:
    main(strin)
  except Exception as e:
    print(e)
  else:
    print("end")


