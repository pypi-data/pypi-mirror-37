"""
jdcpy模块
本模块是吉富数据中心的python版接口
提供下载基金相关信息的功能
大致使用方法如下:
from jdcpy import jdcpy
jdcpy.login('username','password')
jdcpy.info(基金list,基本信息list,投资分布信息list,业绩表现list)
jdcpy.nav(基金list,起始日期,最终日期,信息类别list)
"""
import io
import json
import struct
from datetime import date, datetime

import pandas as P
import requests

# loginUrl = 'http://192.168.80.154:8084/QuantSystem'
loginUrl = 'http://120.27.238.50:8084/QuantSystem'
url = 'http://jdcbackend.thiztech.com/'
# url = 'http://139.196.90.112:8082'


class jdcpy:
    def __init__(self):
        self.sess = requests.session()
        self.token = ''
        self.lastErrorMsg = ""
        self.lastErrorCode = 0
        self.sess.headers['Content-Type'] = 'application/json'

    def login(self, username, password):
        """
        登录
        :param username: 用户名
        :param password: 密码
        :return: 返回0则登录成功,否则返回的是string类型的错误信息
        """
        self.sess.headers['Content-Type'] = 'application/json'
        juser = json.dumps({'userAccount': username, 'password': password})
        r = self.sess.post(loginUrl + '/api/v1/user/login', data=juser)
        jresponse = json.loads(r.content)
        if jresponse['errorCode'] != 0:
            return jresponse['errorMsg']
        self.token = jresponse['token']
        # self.sess.headers['Authorization'] = self.token
        return 0

    def info(self, idList, basicInfo, classification, performance):
        """
        基金的基本信息
        :param idList:基金的标识列表,格式如list(string,string...)
        :param basicInfo:基金的基本信息列表,格式如list(string,string...)
        :param classification:投资分布信息列表,格式如list(string,string...)
        :param performance:业绩表现列表,格式如list(string,string...)
        :return: pandas.DataFrame
        """
        try:
            idList = list(idList)
            basicInfo = list(basicInfo)
            classification = list(classification)
            performance = list(performance)
            idList.sort()
            basicInfo.sort()
            classification.sort()
            performance.sort()
            idList = tuple(idList)
            basicInfo = tuple(basicInfo)
            classification = tuple(classification)
            performance = tuple(performance)
            jdata = json.dumps({'idList': idList, 'basicInfo': basicInfo, 'classification': classification, 'performance': performance, 'token': self.token})
            r = self.sess.post(url + '/apiData/fundInfo', data=jdata).content
            jdata = json.loads(r)
            self.lastErrorCode = jdata['errorCode']
            self.lastErrorMsg = jdata['errorMsg']
            stream = io.StringIO(jdata['data'])
            if jdata['errorCode'] == 0:
                return P.read_csv(stream, index_col=0)  # date_parser
            else:
                return jdata['errorMsg']
        except Exception as e:
            return str(e)

    def nav(self, idList, startDate, endDate, navList):
        """
        返回基金的历史表现
        :param idList:基金的标识列表,格式如list(string,string...)
        :param startDate:起始日期,可以为timestamp格式,或者date,或者datetime,也可以为string如1999-08-10或1990/08/10格式
        :param endDate:结束日期
        :param navList:所要查询的信息列表,格式如list(string,string...)
        :return: pandas.DataFrame
        """
        try:
            idList = list(idList)
            navList = list(navList)
            idList.sort()
            navList.sort()
            idList = tuple(idList)
            navList = tuple(navList)
            if type(startDate) == str:
                try:
                    startDate = int(datetime.strptime(startDate, '%Y-%m-%d').timestamp() * 1000)
                    endDate = int(datetime.strptime(endDate, '%Y-%m-%d').timestamp() * 1000)
                except:
                    try:
                        startDate = int(datetime.strptime(startDate, '%Y/%m/%d').timestamp() * 1000)
                        endDate = int(datetime.strptime(endDate, '%Y/%m/%d').timestamp() * 1000)
                    except:
                        pass
            if type(startDate) == float:
                startDate = int(startDate * 1000)
                endDate = int(endDate * 1000)
            elif type(startDate) == date:
                startDate = int(datetime.fromordinal(startDate.toordinal()).timestamp() * 1000)
                endDate = int(datetime.fromordinal(endDate.toordinal()).timestamp() * 1000)
            elif type(startDate) == datetime:
                startDate = int(1000 * startDate.timestamp())
                endDate = int(1000 * endDate.timestamp())
            jdata = json.dumps({'idList': idList, 'startDate': startDate, 'endDate': endDate, 'navList': navList, 'token': self.token})
            jdata = json.loads(self.sess.post(url + '/apiData/fundNav', data=jdata).content)
            self.lastErrorCode = jdata['errorCode']
            self.lastErrorMsg = jdata['errorMsg']
            stream = io.StringIO(jdata['data'])
            if jdata['errorCode'] == 0:
                return P.read_csv(stream, index_col=0)  # date_parser
            else:
                return jdata['errorMsg']
        except Exception as e:
            return str(e)
