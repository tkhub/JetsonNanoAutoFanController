#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import re


# PWM Fan Control File
FANPWM_DEVICE_FILE="/sys/devices/pwm-fan/target_pwm"

def fanpwmout(duty):
  pwmduty = 255.0 * duty / 100
  if pwmduty < 0:
    pwmduty = 0
  if 100 < pwmduty:
    pwmduty = 100
  pwmdat = round(pwmduty)
  dutyfile.write(str(pwmdat))
  return str(pwmdat)

ARG_DFLT_DUTY = 50
ARG_DFLT_DUTY_STR = str(ARG_DFLT_DUTY)


args = sys.argv
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


