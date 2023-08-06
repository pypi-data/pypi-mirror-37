# -*- coding: utf-8 -*-

import win32api
import os
from win32com.client import GetObject
from time import sleep
import _winreg

import xlrd

from .GTFLibrary import Control


class PublicFunction():
    """加密锁设置"""
    def __init__(self):
        self.ctl = Control()
    
    def ConfigFindType(self, findtype):
        if findtype == "自动查找加密锁":
            if self.ctl.Checked("自动查找加密锁", "RadioButton") == "False":
                self.ctl.Click("自动查找加密锁", "RadioButton")
        elif findtype == "查找当前机器上的加密锁（单机锁、网络锁）":
            if self.ctl.Checked("指定查找加密锁", "RadioButton") == "False":
                self.ctl.Click("指定查找加密锁", "RadioButton")
            if self.ctl.Checked("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox") == "False":
                self.ctl.Click("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox")
            if self.ctl.Checked("查找同网段其他机器上的网络锁", "CheckBox") == "True":
                self.ctl.Click("查找同网段其他机器上的网络锁", "CheckBox")
            if self.ctl.Checked("查找指定的网络授权", "CheckBox") == "True":
                self.ctl.Click("查找指定的网络授权", "CheckBox")
        elif findtype == "查找同网段其他机器上的网络锁":
            if self.ctl.Checked("指定查找加密锁", "RadioButton") == "False":
                self.ctl.Click("指定查找加密锁", "RadioButton")
            if self.ctl.Checked("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox") == "True":
                self.ctl.Click("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox")
            if self.ctl.Checked("查找同网段其他机器上的网络锁", "CheckBox") == "False":
                self.ctl.Click("查找同网段其他机器上的网络锁", "CheckBox")
            if self.ctl.Checked("查找指定的网络授权", "CheckBox") == "True":
                self.ctl.Click("查找指定的网络授权", "CheckBox")
        elif findtype == "查找指定的网络授权":
            if self.ctl.Checked("指定查找加密锁", "RadioButton") == "False":
                self.ctl.Click("指定查找加密锁", "RadioButton")
            if self.ctl.Checked("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox") == "True":
                self.ctl.Click("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox")
            if self.ctl.Checked("查找同网段其他机器上的网络锁", "CheckBox") == "True":
                self.ctl.Click("查找同网段其他机器上的网络锁", "CheckBox")
            if self.ctl.Checked("查找指定的网络授权", "CheckBox") == "False":
                self.ctl.Click("查找指定的网络授权", "CheckBox")
        elif findtype == "查找当前机器上的加密锁+查找指定的网络授权":
            if self.ctl.Checked("指定查找加密锁", "RadioButton") == "False":
                self.ctl.Click("指定查找加密锁", "RadioButton")
            if self.ctl.Checked("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox") == "False":
                self.ctl.Click("查找当前机器上的加密锁（单机锁、网络锁）", "CheckBox")
            if self.ctl.Checked("查找同网段其他机器上的网络锁", "CheckBox") == "True":
                self.ctl.Click("查找同网段其他机器上的网络锁", "CheckBox")
            if self.ctl.Checked("查找指定的网络授权", "CheckBox") == "False":
                self.ctl.Click("查找指定的网络授权", "CheckBox")
        else:
            print("查找方式输入有误！")

    # 等待控件出现
    def WaitTimesUntilFlagIsFound(self, flag, controlName, times):
        for t in range(0, times):
            if self.ctl.Find(flag, controlName) == "False":
                sleep(1)
                if t == times-1:
                    #print("没有找到" + flag + controlName)
                    raise AssertionError("没有找到" + flag + controlName)   #未找到控件，则停止继续运行
            else:
                sleep(1)
                break

    # 查看进行是否存在，返回BOOL值
    def ProcExist(self, procname):
        is_exist = False
        wmi = GetObject('winmgmts:/root/cimv2')
        processCodeCov = wmi.ExecQuery('select * from Win32_Process where name=\"%s\"' % (procname))
        if len(processCodeCov) > 0:
            is_exist = True
        return is_exist

    
    def RunProc(self, procpath):
        """启动进程"""
        win32api.ShellExecute(0, 'open', procpath, '', '', 1)

    # 终止进程
    def KillProc(self, procname):
        os.system("taskkill /F /IM " + procname)

    def SignCode(self, filename, index):

        fname = filename.decode("utf-8")  # 文件名包含中文会报错，需要对文件名进行转码
        bk = xlrd.open_workbook(fname)  # 打开excel
 
        try:
            sh = bk.sheet_by_name("Sheet1")  # 获取sheet
        except:
            print "no sheet in %s named Sheet1" % fname

        nrows = sh.nrows

        index = int(index)
        if index <= nrows:
            value = int(sh.cell_value(index, 1))  # 从0开始计数的
            return value
        else:
            raise AssertionError("没有更多的产品签收码了~")
       
