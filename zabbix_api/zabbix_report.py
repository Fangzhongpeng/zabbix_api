#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import urllib2
from urllib2 import URLError
import sys
import zabbix_sendmail
import sys
import datetime
reload(sys)
sys.setdefaultencoding('utf8')
# 接收人
mailtolist = ['fangzhongpeng9@163.com','fangzhongpeng@iqingka.com' ]
# 格式：zabbix地址，zabbix帐号，zabbix密码，邮件标题
zabbix_addresses = ['http://zabbix.qkvoice.com,Admin,zabbix,今日告警统计']
now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
class ZabbixTools:

    def __init__(self, address, username, password):
        self.address = address
        self.username = username
        self.password = password
        self.url = '%s/api_jsonrpc.php' % self.address
        self.header = {"Content-Type": "application/json"}  #声明消息体的字段类型
    def user_login(self):
        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": self.username,
                "password": self.password
            },
            "id": 0
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Auth Failed, please Check your name and password:", e.code
        else:
            response = json.loads(result.read())
            result.close()
            # print response['result']
            self.authID = response['result']
            return self.authID
    def trigger_get(self):

        data = json.dumps({
            "jsonrpc": "2.0",
            "method": "trigger.get",
            "params": {
                "output": [
                    "triggerid",
                    "description",
                    "priority"
                ],
                "filter": {
                    "value": 1
                },
                "expandData": "hostname",
                "sortfield": "priority",
                "sortorder": "DESC",
                "expandDescription":1,  #expandDescription参数，将trigger的description字段中的宏变量使用实际的数值进行替代；
                "selectHosts": ['host'],   #在hosts属性中返回触发器所属的主机.
                # "selectGroups": ['name'],  #在groups属性中返回触发器所属的主机组.
                # "skipDependent": 1,
                "active": 1,  # 只返回所属被监控主机的启用状态的触发器的触发器信息
                "monitored": 1, #只返回所属被监控主机的启用状态的触发器，并且监控项在启用状态的触发器信息.
                #"only_true": 1,  #只返回最近处于问题状态的触发器.
                #"min_severity": 1  #只返回严重级别大于或等于给定严重性的触发器.
            },
            "auth": self.user_login(),
            "id": 1
        })
        request = urllib2.Request(self.url, data)
        for key in self.header:
            request.add_header(key, self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            print "Error as ", e
        else:
            response = json.loads(result.read())
            result.close()
            issues = response['result']
            content = ''
            hostips = []
            alerts = []
            if issues:
                for line in issues:
                     #content = content + "%s:%s\r\n" % (line['hosts'], line['description'])
                     #content = content + "%s :  %s\r\n" % (line['hosts'][0]['host'], line['description'])
                     #vhosts = vhosts + ","+ "%s" % line['hosts'][0]['host']
                     hostips.append(line['hosts'][0]['host'])
                     #alerts = alerts + "%s" % line['description']
                     alerts.append(line['description'])
            #return (vhosts,alerts)
            #print type(content)
            return (hostips,alerts)

    def get_html_msg(self):
        #issue = z.trigger_get()

        hostips,alerts = z.trigger_get()
        head ="""<head>
        <title>磁盘使用情况</title>
            <style type="text/css">
              .tftable {font-size:12px;color:#333333;width:100%;border-width: 1px;border-color: #9dcc7a;border-collapse: collapse;}
              .tftable th {font-size:12px;background-color:#abd28e;border-width: 1px;padding: 8px;border-style: solid;border-color: #9dcc7a;text-align:left;}
              .tftable tr {background-color:#ffffff;}
              .tftable td {font-size:12px;border-width: 1px;padding: 8px;border-style: solid;border-color: #9dcc7a;}
              .tftable tr:hover {background-color:#ffff99;}
            </style>
        </head>"""
        p = """<p><font face="宋体" size="3"><b>截止到 """ + now_time + """ 主机当前告警信息如下：</b></font></p>"""
        table = ''
        #htmlmodel = 'aaa'
        #table = """<tr><td>/</td><td>"""+ "ceshi" +"""</td><td>16G</td><td>54%</td></tr>"""
        for ip,alert in zip(hostips,alerts):
        #for alert  in alerts:
              table = table+ """<tr><td>"""+ ip + """</td><td>"""+ alert +"""</td><td>16G</td><td>54%</td></tr>"""
        #    print alert
        body = p + """
            <table class="tftable" border="1">
                <tr><th>主机<th>告警<th>可用</th><th>使用率</th></tr> """ + table + """
            </table>
            </br>"""
        htmlmodel = """<html>""" + head + body + """</html>"""
        #print("test:\n", list(zip(hostip, alert)))
            #print ip,alert
        return htmlmodel


if __name__ == "__main__":
    for zabbix_addres in zabbix_addresses:
        address, username, password, subject = zabbix_addres.split(',')
        z = ZabbixTools(address=address, username=username, password=password)
        #AuthID = z.user_login()
        #print AuthID
        #content = z.trigger_get()
        content = z.get_html_msg()
        #z.get_html_msg()
        #print(z.get_html_msg())
        zabbix_sendmail.send_mail(mailtolist, subject, content)
    print "Done!"


