# coding:utf-8
import json
import _winreg
import datetime

class BaseFunc(object):
    
    def update_json(self, url, *parameters):
        """读取配置文件里的信息，拼接后转换为json格式"""
        if (url == 'nourl'):
            json_Str = "{}"
        else:
            json_Str = open(url).read()
        json_Str = json_Str.replace('\t', '').replace('\n', '')
        jsonStr = json.loads(json_Str)
        strDict = 'jsonStr'
        for parameter in parameters:
            print(strDict + parameter)
            try:
                exec (strDict + parameter)
            except:
                print 'Expression execute failed![', strDict + parameter, ']'
        return json.dumps(jsonStr)
    
    def get_uuid(self,key=_winreg.HKEY_LOCAL_MACHINE, sub_key=r'Software\Wow6432Node\Glodon\GDP\2.0'):
        """
        读取注册表信息，获取设备ID。
        :param key: 注册表主目录，默认为HKEY_LOCAL_MACHINE
        :param sub_key: 注册表从目录，默认Software\Wow6432Node\Glodon\GDP\2.0。
        :return: 设备ID(uuid)
        """
        return _winreg.QueryValueEx(_winreg.OpenKey(key, sub_key),'guid')[0].encode('utf-8')

    def get_verison(self, key=_winreg.HKEY_LOCAL_MACHINE, sub_key=r'Software\Wow6432Node\Glodon\GDP\2.0'):
        """
        读取注册表信息，获取版本号。
        :param key: 注册表主目录，默认为HKEY_LOCAL_MACHINE
        :param sub_key: 注册表从目录，默认Software\Wow6432Node\Glodon\GDP\2.0。
        :return: version
        """
        return _winreg.QueryValueEx(_winreg.OpenKey(key, sub_key), 'Version')[0].encode('utf-8')

        #
    def AfterDaysLocalTime(self, days, ntype):
        """
        获取xx天后的时间
        :param period: days 相隔的天数
        :param ntype: 必须为int类型，1返回时间格式："%Y-%m-%d %H:%M"，2返回时间格式："%Y年%m月%d日"
        :return:
        """
        peri = int(days)
        if not isinstance(ntype,int):
            raise TypeError('参数ntype类型错误，需为int类型!')
        
        if ntype == 1:
            return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y-%m-%d %H:%M")
        elif ntype == 2:
            return (datetime.datetime.now() + datetime.timedelta(days=days)).strftime("%Y年%m月%d日")
        else:
            raise ValueError('ntype赋值错误！')

    
    def SetRegValue(self, ValueName, ValueContent, key=_winreg.HKEY_LOCAL_MACHINE,
                    subkey="SOFTWARE\\Wow6432Node\\GrandSoft\\GrandDog\\3.0\\Server"):
        """
        注册表中创建键并赋值
        :param ValueName:
        :param ValueContent:
        :param key:默认值：HKEY_LOCAL_MACHINE
        :param subkey:默认值：SOFTWARE\\Wow6432Node\\GrandSoft\\GrandDog\\3.0\\Server
        :return:
        """
        _winreg.SetValueEx(
            _winreg.OpenKey(key, subkey, 0, _winreg.KEY_ALL_ACCESS),
            ValueName,
            0,
            _winreg.REG_SZ, ValueContent
        )

    # 注册表中删除键
    def DeleteRegValue(self, ValueName, key=_winreg.HKEY_LOCAL_MACHINE,
                       subkey="SOFTWARE\\Wow6432Node\\GrandSoft\\GrandDog\\3.0\\Server"):
        """
        注册表中删除键
        :param ValueName:
        :param key:默认值：HKEY_LOCAL_MACHINE
        :param subkey:默认为：SOFTWARE\\Wow6432Node\\GrandSoft\\GrandDog\\3.0\\Server
        :return:
        """
        try:
            _winreg.DeleteValue(_winreg.OpenKey(key, subkey, 0, _winreg.KEY_ALL_ACCESS), ValueName)
        except Exception as e:
            raise e