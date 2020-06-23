#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import re
import fandrive
import numpy
from systemp import readsystemp

SNS_MODE_AO = "AO-therm"
SNS_MODE_CPU = "CPU-therm"
SNS_MODE_GPU = "GPU-therm"
SNS_MODE_PLL = "PLL-therm"
SNS_MODE_TFE = "thermal-fan-est"
SNS_MODE_WIFI = "iwlwifi"
SNS_MODE_MAX = "max"
SNS_MODE_AVE = "ave"

FANPWM_DEVICE_FILE="/sys/devices/pwm-fan/target_pwm"

CSV_PATHF = "./fanspdcnf.csv"
LOG_PATH = "/var/log/"
LOG_FILE = "tempfan.log"

def readtemp(mode, ex_mode):
    sns_name = []
    sns_temp = []
    rtn_name = ""
    sns_name, sns_temp = readsystemp("all")
    if mode == SNS_MODE_AVE:
        rtn_name = "Average"
        rtn_temp = 0.0
        i = 0
        for srch_name, srch_temp in zip(sns_name, sns_temp):
            if not srch_name in ex_mode:
                rtn_temp += srch_temp
                i += 1
        rtn_temp = rtn_temp / i

    elif mode == SNS_MODE_MAX:
        rtn_temp = -100000.0
        for srch_name, srch_temp in zip(sns_name, sns_temp):
            if not srch_name in ex_mode:
                if rtn_temp < srch_temp:
                    rtn_temp = srch_temp
                    rtn_name = srch_name
    else:
        i = sns_name.index(mode)
        rtn_name = sns_name[i]
        rtn_temp = sns_temp[i]
    return rtn_name, rtn_temp
    

# 設定ファイルから設定を読み出す
# 設定ファイルを解釈してモード設定する
# 設定ファイルから温度PWMテーブルを読み出す
# PWMを制御する
""" SOURCE, MAX,
EX_source, iwlwifi,
STOP, EN
TABLE
#temp, #speed
30, 20
35, 30
40, 40
45, 50
50, 75
60, 100 """



FANSPD_CONF = "./fanspdcnf.csv"
class readconf:
    def __init__(self):
        self.stpen = False
        self.monsns = "max"
        self.exmonsns = [""]
        self.temptbl = []
        self.pwmtbl = []
        self.FMT_CONFMD = "CONF"
        self.CNF_STPEN = "STOP"
        self.FMT_TBLMD = "TABLE"
        self.FMT_SKIP = "SKIP"
        self.CNF_ENABLE = "ENABLE"
        self.CNF_DISABLE = "DISABLE"
        self.CNF_SOURCE = "SOURCE"
        self.CNF_EXSOURCE = "EX_SOURCE"

    def readcnf(self):
        try:
            conff = open(FANSPD_CONF,'r')
        except:
            self.stpen = False
            self.monsns="Can't_Open_conf.csv"
            self.exmonsns=[]
        else:
            csvobj = csv.reader(conff)
            readmode = self.FMT_CONFMD
            for row in csvobj:
                if row[0].startswith('#'):
                    pass
                elif readmode == self.FMT_CONFMD:
                    if row[0].upper() == self.CNF_STPEN:
                        if row[1].upper() == self.CNF_ENABLE:
                            self.stpen = 1
                        else:
                            self.stpen = 0

                    if row[0].upper() == self.CNF_SOURCE:
                        self.monsns = row[1]

                    if row[0].upper() == self.CNF_EXSOURCE:
                        for i in range(len(row)):
                            if 1 <= i:
                                self.exmonsns.append(row[i])

                    if row[0].upper() == self.FMT_TBLMD:
                        print("conf-> tbl")
                        readmode = self.FMT_TBLMD
                else:
                    print(row)
                    try:
                        ftmp = float(row[0])
                    except ValueError:
                        ftmp = 0
                        self.temptbl.append(ftmp)
                    else:
                        self.temptbl.append(ftmp)

                    try:
                        ftmp = float(row[1])
                    except ValueError:
                        ftmp = 100
                        self.pwmtbl.append(ftmp)
                    else:
                        self.pwmtbl.append(ftmp)

                    if row[0] == self.FMT_CONFMD:
                        print("tbl -> conf")
                        readmode = self.FMT_CONFMD
            conff.close()

    def readtbl(self):
        return self.temptbl, self.pwmtbl

    def readstpflg(self):
        return self.stpen

    def readmonsns(self):
        return self.monsns

    def readexmonsns(self):
        return self.exmonsns

class ctrlpwm:
    def __init__(self, ttbl, ptbl):
        self.temptbl = ttbl
        self.pwmtbl = ptbl
        self.rtnduty = 0.0

    def calcduty(self, temp):
        if self.temptbl[-1] < temp:
            self.rtnduty = self.pwmtbl[-1]
        elif self.temptbl[0] > temp:
            self.rtnduty = self.pwmtbl[0]
        else:

            for i in range(len(self.temptbl)):
               if self.temptbl[i] <= temp:
                    break
            self.rtnduty = self.pwmtbl[i]  + (temp - self.temptbl[i]) * (self.pwmtbl[i + 1] - self.pwmtbl[i]) / (self.temptbl[i + 1] - self.temptbl[i])
        return self.rtnduty




exname=["iwlwifi"]
print(readtemp("ave",exname))
print(readtemp("max",exname))
print(readtemp("iwlwifi",""))

fd =readconf()
fd.readcnf()
ttbl,ptbl = fd.readtbl()
print(fd.readtbl())
print(fd.readstpflg())
mode = fd.readmonsns()
print(fd.readexmonsns())
fc = ctrlpwm(ttbl,ptbl)
print(fc.calcduty(4.0))