#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import urllib2
import sys
class zabbixtools:
    def __init__(self):
        self.url = "http://zabbix.qkvoice.com/api_jsonrpc.php"
        self.header = {"Content-Type": "application/json"}
        self.authID = self.user_login()
    def user_login(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "user.login",  #使用user.login方法请求
                    "params": {
                        "user": "Admin",
                        "password": "zabbix"
                        },
                    "id": 0
                    })
        request = urllib2.Request(self.url,data)   #创建Request实例，url 作为Request()方法的参数，构造并返回一个Request对象
        for key in self.header:
            request.add_header(key,self.header[key])
            #调用Request.add_header() 添加/修改一个特定的header 也可以通过调用Request.get_header()来查看已有的header。
        try:
            ResultAuth = urllib2.urlopen(request)       #Request对象作为urlopen()方法的参数，发送给服务器并接收响应

            '''     urlopen()的参数可以直接是一个url地址；但是如果需要执行更复杂的操作，
             比如增加HTTP报头，必须创建一个 Request 实例来作为urlopen()的参数；
             而需要访问的url地址则作为 Request 实例的参数。
            '''
        except URLError as e:
            print "Auth Failed, Please Check Your Name And Password:",e.code
        else:
            response = json.loads(ResultAuth.read())
            ResultAuth.close()
            authID = response['result']   #得到请求返回中的result值。
            # 请求返回的格式
            # {
            #     "jsonrpc": "2.0",
            #     "result": "0424bd59b807674191e7d77572075f33",
            #     "id": 1
            # }
            #
            return authID
    def get_data(self,data,hostip=""):
        request = urllib2.Request(self.url,data)
        for key in self.header:
            request.add_header(key,self.header[key])
        try:
            result = urllib2.urlopen(request)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
            return 0
        else:
            response = json.loads(result.read())
            result.close()
            return response
    def host_get(self,hostip=""):
        hostip = raw_input("\033[1;35;40m%s\033[0m" % 'Enter Your Check Host:Host_ip :')
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.get",
                    "params": {
                        "output":["hostid","name","status","host"],
                        "filter": {"host": [hostip]}
                        },
                    "auth": self.authID,
                    "id": 1
                })
        res = self.get_data(data)['result']
        if (res != 0) and (len(res) != 0):
            #for host in res:
            host = res[0]
            if host['status'] == '1':
                print "\t","\033[1;31;40m%s\033[0m" % "Host_IP:","\033[1;31;40m%s\033[0m" % host['host'].ljust(15),'\t',"\033[1;31;40m%s\033[0m" % "Host_Name:","\033[1;31;40m%s\033[0m" % host['name'].encode('utf-8'),'\t',"\033[1;31;40m%s\033[0m" % u'未在监控状态'.encode('utf-8')
                return host['hostid']
            elif host['status'] == '0':
                print "\t","\033[1;32;40m%s\033[0m" % "Host_IP:","\033[1;32;40m%s\033[0m" % host['host'].ljust(15),'\t',"\033[1;32;40m%s\033[0m" % "Host_Name:","\033[1;32;40m%s\033[0m" % host['name'].encode('utf-8'),'\t',"\033[1;32;40m%s\033[0m" % u'在监控状态'.encode('utf-8')
                return host['hostid']
            print
        else:
            print '\t',"\033[1;31;40m%s\033[0m" % "Get Host Error or cannot find this host,please check !"
            return 0
    def host_del(self):
        hostip = raw_input("\033[1;35;40m%s\033[0m" % 'Enter Your Check Host:Host_ip :')
        hostid = self.host_get(hostip)
        if hostid == 0:
            print '\t',"\033[1;31;40m%s\033[0m" % "This host cannot find in zabbix,please check it !"
            sys.exit()
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "host.delete",
                    "params": [{"hostid": hostid}],
                    "auth": self.authID,
                    "id": 1
                })
        res = self.get_data(data)['result']
        if 'hostids' in res.keys():
            print "\t","\033[1;32;40m%s\033[0m" % "Delet Host:%s success !" % hostip
        else:
            print "\t","\033[1;31;40m%s\033[0m" % "Delet Host:%s failure !" % hostip
    def hostgroup_get(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "hostgroup.get",
                    "params": {
                        "output": "extend",
                        },
                    "auth": self.authID,
                    "id": 1,
                    })
        res = self.get_data(data)
        if 'result' in res.keys():
            res = res['result']
            if (res !=0) or (len(res) != 0):
                print "\033[1;32;40m%s\033[0m" % "Number Of Group: ", "\033[1;31;40m%d\033[0m" % len(res)
                for host in res:
                    print "\t","HostGroup_id:",host['groupid'],"\t","HostGroup_Name:",host['name'].encode('utf-8')
                print
        else:
            print "Get HostGroup Error,please check !"
    def template_get(self):
        data = json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "template.get",
                    "params": {
                        "output": "extend",
                        },
                    "auth": self.authID,
                    "id": 1,
                    })
        res = self.get_data(data)#['result']
        if 'result' in res.keys():
            res = res['result']
            if (res !=0) or (len(res) != 0):
                print "\033[1;32;40m%s\033[0m" % "Number Of Template: ", "\033[1;31;40m%d\033[0m" % len(res)
                for host in res:
                    print "\t","Template_id:",host['templateid'],"\t","Template_Name:",host['name'].encode('GBK')
                print
        else:
            print "Get Template Error,please check !"
    def host_create(self):
        hostip = raw_input("\033[1;35;40m%s\033[0m" % 'Enter your:Host_ip :')
        groupid = raw_input("\033[1;35;40m%s\033[0m" % 'Enter your:Group_id :')
        templateid = raw_input("\033[1;35;40m%s\033[0m" % 'Enter your:Tempate_id :')
        g_list=[]
        t_list=[]
        for i in groupid.split(','):
            var = {}
            var['groupid'] = i
            g_list.append(var)
        for i in templateid.split(','):
            var = {}
            var['templateid'] = i
            t_list.append(var)
        if hostip and groupid and templateid:
            data = json.dumps(
                    {
                        "jsonrpc": "2.0",
                        "method": "host.create",
                        "params": {
                            "host": hostip,
                            "interfaces": [
                                {
                                    "type": 1,
                                    "main": 1,
                                    "useip": 1,
                                    "ip": hostip,
                                    "dns": "",
                                    "port": "10050"
                                }
                            ],
                            "groups": g_list,
                            "templates": t_list,
                    },
                        "auth": self.authID,
                        "id": 1,
                        })
            res = self.get_data(data,hostip)
            if 'result' in res.keys():
                res = res['result']
                if 'hostids' in res.keys():
                    print "\033[1;32;40m%s\033[0m" % "Create host success"
            else:
                print "\033[1;31;40m%s\033[0m" % "Create host failure: %s" % res['error']['data']
        else:
            print "\033[1;31;40m%s\033[0m" % "Enter Error: ip or groupid or tempateid is NULL,please check it !"
def main():
    test = zabbixtools()
    #test.template_get()
    test.hostgroup_get()
    #test.host_get()
    #test.host_del()
    #test.host_create()
if __name__ == "__main__":
    main()