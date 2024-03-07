import requests
import json
import re
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def get_info(target_url,headers,auth):
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.get(target_url,auth=auth,headers=headers,verify=False)
    #response = requests.get(target_url, headers=headers, verify=False, proxies=proxies)
    print("1 System Info")
    # print(response)
    # 查看响应内容，response.text 返回的是Unicode格式的数据
    #print(response.text)
    response_class = response.text
    stud_obj = json.loads(response_class)
    # print(type(stud_obj))
    # print(stud_obj)
    # print("stud_obj : %s" %  stud_obj.keys())
    entris = stud_obj["entries"]
    print("-------CPU_Avg---------")
    CPU_info = entris["https://localhost/mgmt/tm/sys/performance/system/Utilization"]
    CPU_netstats = CPU_info["nestedStats"]
    CPU_netstats_entries = CPU_netstats["entries"]
    CPU_Average = CPU_netstats_entries["Average"]
    CPU_Average_Num = CPU_Average["description"]
    print("CPU_Average_Num:\t%s" % CPU_Average_Num)

    print("-------MemOther---------")
    MEM_Other_info = entris["https://localhost/mgmt/tm/sys/performance/system/Other%20Memory%20Used"]
    MEM_Other_netstats = ((MEM_Other_info["nestedStats"])["entries"])["Average"]
    MEM_Other_Average_Num = MEM_Other_netstats["description"]
    print("MEM_Other_Average_Num:\t%s" % MEM_Other_Average_Num)

    print("-------MemTMM---------")
    MEM_TMM_info = entris["https://localhost/mgmt/tm/sys/performance/system/TMM%20Memory%20Used"]
    MEM_TMM_netstats = ((MEM_TMM_info["nestedStats"])["entries"])["Average"]
    MEM_TMM_Average_Num = MEM_TMM_netstats["description"]
    print("MEM_TMM_Average_Num:\t%s" % MEM_TMM_Average_Num)

    print("-------MemSwap---------")
    Mem_Swap_info = entris["https://localhost/mgmt/tm/sys/performance/system/Swap%20Used"]
    Mem_Swap_netstats = ((Mem_Swap_info["nestedStats"])["entries"])["Average"]
    Mem_Swap_Average_Num = Mem_Swap_netstats["description"]
    print("Mem_Swap:\t%s" % Mem_Swap_Average_Num)
    print("-------Performance Info\n---------")
    return CPU_Average_Num,MEM_Other_Average_Num,MEM_TMM_Average_Num,Mem_Swap_Average_Num
def get_log(target_url,headers,auth):
    data={"command":"run","utilCmdArgs":"-c 'cat /var/log/ltm'"}
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.post(target_url,auth=auth, json=data, headers=headers, verify=False, timeout=20)
    response_class = json.loads(response.text)
    Log = response_class["commandResult"]
    # stud_obj = json.loads(response_class)
    # Log_RawValues=stud_obj["apiRawValues"]
    # Log=Log_RawValues["apiAnonymous"]
    #print(Log)
    # print(type(Log))
    #print(target_url)
    for i in Log:
        pattern = r':\b[0-9]'
        pattern = re.compile(pattern)
        # result = pattern.findall(log)

    print("2 Log Info")
    num_emerg = Log.count("emerg")
    print("Log level emerg:%s\t" %num_emerg)

    num_alert = Log.count("alert")
    print("Log level alert:%s\t" %num_alert)

    num_crit = Log.count("crit")
    print("Log level crit:%s\t" % num_crit)

    num_err = Log.count("err")
    print("Log level err:%s\t" % num_err)

    num_warning = Log.count("warning")
    print("Log level warning:%s\t" % num_warning)

    num_notice = Log.count("notice")
    print("Log level notice:%s\t" % num_notice)

    num_info = Log.count("info")
    print("Log level info:%s\t" % num_info)
    filename = target_url.split('/')[2] + ".txt"
    #print(filename)
    try:
        f = open(filename, 'w')
        f.write(Log)
        f.close()
    except:
        print("!!!!!!Log File Get failed!")
    #For ipv6 log,the id like 010719e8 with [a-z],the script re can not find it!!!!
    listLoglevel = list()
    for line in open(filename, 'r', encoding='utf-8'):
        patternLogLevel = r'\b[0-9a-z]]{5,10}:'
        patternLogLevel = re.compile(patternLogLevel)
        resultLoglevel = patternLogLevel.findall(line)
        if len(resultLoglevel) != 0:
            resultLoglevel = resultLoglevel[0]
            listLoglevel.append(resultLoglevel)
    listIndex = set(listLoglevel)
    for i in listIndex:
        num_emerg = listLoglevel.count(i)
        # print(len(listLoglevel))
        for logCode in open('log_code.txt', 'r', encoding='utf-8'):
            # print(logCode)
            # print(type(logCode))
            # print(logmessege)
            if i in logCode:
                print("times:%s  %s" % (num_emerg, logCode), end='')
                # print(logCode)
        #01010028:No members available for pool %s
        #01010221:Pool %s now has available members
        #01070727:Pool %s member %s:%u monitor status up.
        #01071682:SNMP_TRAP: Virtual %s has become unavailable
        #01071681:SNMP_TRAP: Virtual %s has become available
        #01070638:"Pool %s member %s:%u monitor status %s."
    print("-------Log Info---------\n")
def get_cm_status(target_url,headers,auth):
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    #response = requests.get(target_url, headers=headers,verify=False,proxies=proxies)
    response = requests.get(target_url, auth=auth,headers=headers, verify=False)
    #print(response.text)
    response_class = response.text
    stud_obj = json.loads(response_class)
    #print("stud_obj : %s" % stud_obj.keys())
    items_list=stud_obj["items"]
    print("3 CM Info")
    for items_dict in items_list:
        hostname = items_dict["hostname"]
        failoverState = items_dict["failoverState"]
        print(" %s failoverState is : %s" % (hostname,failoverState))
    print("-------CM Info---------\n")
def get_mgmt_route(target_url,headers,auth):
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    #response = requests.get(target_url, headers=headers, verify=False, proxies=proxies)
    response = requests.get(target_url, auth=auth,headers=headers,verify=False)
    #print(response.text)
    response_class = response.text
    stud_obj = json.loads(response_class)
    items_list=stud_obj["items"]
    print("4 Mgmt Route")
    for items_dict in items_list:
        name = items_dict["name"]
        network = items_dict["network"]
        gateway = items_dict["gateway"]
        print("%s\t%s\t%s\t"%(name,network,gateway))
    print("-------Mgmt Route---------\n")
    #print("stud_obj : %s" % stud_obj.keys())
    items_list=stud_obj["items"]
def get_hardware_info(target_url,headers,auth):
    #proxies = {"http": "http://10.212.222.22:8896", "https": "https://10.212.222.22:8896"}
    #response = requests.get(target_url, headers=headers, verify=False, proxies=proxies)
    response = requests.get(target_url, auth=auth,headers=headers,verify=False)
    #print(response.text)
    response_class = response.text
    #print(response_class)
    #print(type(response_class))
    stud_obj = json.loads(response_class)
    items_list=stud_obj["entries"]
    serial_list = items_list["https://localhost/mgmt/tm/sys/hardware/system-info"]
    serial_index = (serial_list["nestedStats"])["entries"]
    #serial2 = serial["bigipChassisSerialNum"]
    #print("items_list : %s" % items_list.keys())
    #print(serial)
    for items_dict in serial_index:
        #print(type(items_dict))
        serial = ((((serial_index[items_dict])["nestedStats"])["entries"])["bigipChassisSerialNum"])["description"]
        #print("serial_number : %s" % serial)
        #serial = bigipChassisSerialNum
    power_list=items_list["https://localhost/mgmt/tm/sys/hardware/chassis-power-supply-status-index"]
    #print(power_list)
    power_index = (power_list["nestedStats"])["entries"]
    #print(power_index)
    #print("power_list : %s" % (power_list["nestedStats"])["entries"].keys())
    print("-------Hardware Info---------")
    for items_dict in power_index:
        #print(type(items_dict))
        print(((power_index[items_dict])["nestedStats"])["entries"])
    fan_list = items_list["https://localhost/mgmt/tm/sys/hardware/chassis-fan-status-index"]
    fan_index = (fan_list["nestedStats"])["entries"]
    for items_dict in fan_index:
        #print(items_dict)
        print(((fan_index[items_dict])["nestedStats"])["entries"])
    temperature_list = items_list["https://localhost/mgmt/tm/sys/hardware/chassis-temperature-status-index"]
    temperature_index = (temperature_list["nestedStats"])["entries"]
    for items_dict in temperature_index:
        #print(items_dict)
        print(((temperature_index[items_dict])["nestedStats"])["entries"])
    print("-------Hardware Info---------")
def get_serial_number(target_url,headers,auth):
    #proxies = {"http": "http://10.212.222.22:8896", "https": "https://10.212.222.22:8896"}
    #response = requests.get(target_url, headers=headers, verify=False, proxies=proxies)
    response = requests.get(target_url,auth=auth, headers=headers,verify=False)
    #print(response.text)
    response_class = response.text
    #print(response_class)
    #print(type(response_class))
    stud_obj = json.loads(response_class)
    items_list=stud_obj["entries"]
    serial_list = items_list["https://localhost/mgmt/tm/sys/hardware/system-info"]
    serial_index = (serial_list["nestedStats"])["entries"]
    #serial2 = serial["bigipChassisSerialNum"]
    #print("items_list : %s" % items_list.keys())
    #print(serial)
    for items_dict in serial_index:
        #print(type(items_dict))
        serial = ((((serial_index[items_dict])["nestedStats"])["entries"])["bigipChassisSerialNum"])["description"]
        print("serial_number: %s\n" % serial)
def get_per_info(target_url,headers,auth):
    #proxies = {"http": "http://10.212.222.22:8896", "https": "https://10.212.222.22:8896"}
    #response = requests.get(target_url, headers=headers, verify=False, proxies=proxies)
    response = requests.get(target_url,auth=auth, headers=headers,verify=False)
    #print(response.text)
    response_class = response.text
    stud_obj = json.loads(response_class)
    entris = stud_obj["entries"]
    print("5 Performance Info")
    print("-------CurConn---------")
    conn_index = entris["https://localhost/mgmt/tm/sys/performance/all-stats/Connections"]
    conn = (conn_index["nestedStats"])["entries"]
    conn_act = (conn["Current"])["description"]
    print("Current connection: %s" % conn_act)
    print("-------Throught In---------")
    throught_in_index = entris["https://localhost/mgmt/tm/sys/performance/all-stats/In"]
    throught_in = (throught_in_index["nestedStats"])["entries"]
    throught_in_avg = (throught_in["Average"])["description"]
    print("throught_in_avg pkt/s: %s" % throught_in_avg)
    #print(throught_in)
    print("-------Throught Out---------")
    throught_out_index = entris["https://localhost/mgmt/tm/sys/performance/all-stats/In"]
    throught_out = (throught_out_index["nestedStats"])["entries"]
    throught_out_avg = (throught_out["Average"])["description"]
    print("throught_out_avg pkt/s: %s\n" % throught_out_avg)
def get_soft_ware(target_url,headers,auth):
    #data={"command":"run","utilCmdArgs":"-c 'tmsh show sys software status'"}
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.get(target_url,auth=auth,headers=headers, verify=False)
    response_class = json.loads(response.text)
    items_list =  response_class["items"]
    for items in items_list:
        #print("items : %s" % items.keys())
        items_active = 'active' in items.keys()
        #print(items_active)
        if items_active == True:
            software = items["version"]
            print("Software Version: %s" % software)
def get_user_info(target_url,headers,auth):
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.get(target_url,auth=auth,headers=headers, verify=False)
    response_class = json.loads(response.text)
    items_list =  response_class["items"]
    #print(items_list)
    for items in items_list:
        #print("items : %s" % items.keys())
        #items_active = 'active' in items.keys()
        #print(items)
        username = items["name"]
        #userrole = items["partitionAccess"]
        UserPartition = items["partitionAccess"][0]["name"]
        UserRole = items["partitionAccess"][0]["role"]
        #print(userrole2)
        print("username: %s" % username)
        print("userrole: %s  %s" % (UserPartition,UserRole))
        #json.loads(userrole)
        # print((userrole[0])["name"])
        # print((userrole[0])["role"])
        #print(type(userrole[0]))
        #print("userrole : %s" % userrole.keys())
        if items == True:
            # print()
            software = items["name"]
            print("Software Version: %s" % software)
def get_sync_status(target_url,headers,auth):
    response = requests.get(target_url,auth=auth, headers=headers,verify=False)
    #print(response.text)
    response_class = response.text
    stud_obj = json.loads(response_class)
    entris = stud_obj["entries"]
    #print(entris)
    for items_dict in entris:
        SyncStatus = ((((entris[items_dict])["nestedStats"])["entries"])["status"])["description"]
        print("SyncStatus: %s" % SyncStatus)
def get_device_sync_action(target_url,headers,auth):
    response = requests.get(target_url,auth=auth, headers=headers,verify=False)
    #print(response.text)
    response_class = response.text
    stud_obj = json.loads(response_class)
    items= stud_obj["items"]
    for items_dict in items:
        group_name =items_dict["name"]
        auto_sync = items_dict["autoSync"]
        print("GroupName: %s AutoSync: %s" % (group_name,auto_sync))
def create_user(target_url,headers,auth):
    data={"name":"monitor_ywbz", "password":"YWbzb123&88", "partitionAccess":[ { "name":"all-partitions", "role":"guest"} ] }
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.post(target_url, auth=auth,json=data, headers=headers, verify=False, timeout=20)
    print(response.text)
def get_ntp(target_url,headers,auth):
    data={"command":"run","utilCmdArgs":"-c 'ntpq -np'"}
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.post(target_url,auth=auth, json=data, headers=headers, verify=False, timeout=20)
    response_class = json.loads(response.text)
    Log = response_class["commandResult"]
    print("-------NTP State---------")
    print(Log)
def get_disk_use(target_url,headers,auth):
    data={"command":"run","utilCmdArgs":"-c 'df -h '"}
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.post(target_url,auth=auth, json=data, headers=headers, verify=False, timeout=20)
    response_class = json.loads(response.text)
    Log = response_class["commandResult"]
    print("-------Disk State---------")
    print(Log)
def get_proc_info(target_url,headers,auth):
    response = requests.get(target_url,auth=auth, headers=headers,verify=False)
    #print(response.text)
    response_class = response.text
    stud_obj = json.loads(response_class)
    entris = stud_obj["entries"]
    #print(entris)
    for entris_list in entris:
        #print(entris_list)
        #print("items_list : %s" % entris_list.keys())
        cpuUsageRecent = ((((entris[entris_list])["nestedStats"])["entries"])["cpuUsageRecent"])["value"]
        procName=((((entris[entris_list])["nestedStats"])["entries"])["procName"])["description"]
        vsz=((((entris[entris_list])["nestedStats"])["entries"])["vsize"])["value"]
        print("cpuUsageRecent:  %s，procName: %s" %(cpuUsageRecent,procName))
        # format函数进行单位转换，转换成MB
        print('vsz: {:.1f} MB '' procName:{}'.format(vsz/1024 /1024,procName))
        #print("vsz:  %s，procName: %s" % (vsz,procName))
        # print("procName: %s" % procName)
def get_virtual(target_url,headers,auth):
    proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
    response = requests.get(target_url,auth=auth,headers=headers, verify=False)
    response_class = json.loads(response.text)
    items_list =  response_class["items"]
    for items in items_list:
        virtual_name = items["name"]
        virtual_destination = items["destination"]
        if 'pool' in items.keys():
            pool_name = items["pool"]
            #print("%s,%s,%s" %(virtual_name,virtual_destination,pool_name))
            sql = "INSERT INTO `f5`.`byyltmconfig` (`device_name`,`VirtualName`,`Destination`,`PoolName`) VALUES ('" + url_ip +  "'"+","+ "'" + virtual_name +  "'"+","+"'" + virtual_destination +  "'"+","+"'" + pool_name +  "'" + ")"
            #print(sql)
            f = open('sql.txt', 'a+')
            f.write(sql+'\n')
            f.close()
        else:
            pool_name = "NonePool"
            #print("%s,%s,%s" % (virtual_name, virtual_destination,pool_name))
            sql = "INSERT INTO `f5`.`byyltmconfig` (`device_name`,`VirtualName`,`Destination`,`PoolName`) VALUES ('" + url_ip +  "'"+","+ "'" + virtual_name +  "'"+","+"'" + virtual_destination +  "'"+","+"'" + pool_name +  "'" + ")"
            #print("None Pool")
            f = open('sql.txt', 'a+')
            f.write(sql+'\n')
            f.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser("f5 auto xunjian")
    parser.add_argument('-f', '--file', type=str, help='Input your IP file name')
    parser.add_argument('-l', '--log', type=str, help='/mgmt/tm/sys/log/ltm/stats?options=lines,1000')
    parser.add_argument('-r', '--mgmtroute', type=str, help='/mgmt/tm/sys/management-route')
    parser.add_argument('-p', '--password', type=str, help='/mgmt/tm/sys/auth')
    args = parser.parse_args()
    password=args.password
    ipfile = args.file
    print(ipfile)
    # print(password)

    #Change password and username as your device
    auth = ('admin','1')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'}

    url_log = args.log
    url_mgmt = args.mgmtroute
    for url_ip in open(ipfile, 'r', encoding='utf-8'):
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print("Device: %s" %url_ip)
        url_ip=url_ip.strip()
        url_link_performance = "https://" + url_ip + "/mgmt/tm/sys/performance/system"
        url_link_log="https://" + url_ip + "/mgmt/tm/sys/log/ltm/stats?options=lines,1000"
        url_link_bash = "https://" + url_ip + "/mgmt/tm/util/bash"
        url_link_cm="https://" + url_ip + "/mgmt/tm/cm/device"
        url_link_mgmt_route = "https://" + url_ip + "/mgmt/tm/sys/management-route"
        url_link_hardware = "https://" + url_ip + "/mgmt/tm/sys/hardware/"
        url_link_software = "https://" + url_ip + "/mgmt/tm/sys/software/volume"
        url_link_per_info = "https://" + url_ip + "/mgmt/tm/sys/performance/all-stats"
        url_link_user_info = "https://" + url_ip + "/mgmt/tm/auth/user"
        url_link_sync_status = "https://" + url_ip + "/mgmt/tm/cm/sync-status"
        url_device_sync_action = "https://" + url_ip + "/mgmt/tm/cm/device-group"
        url_link_proc_info = "https://" + url_ip + "/mgmt/tm/sys/proc-info#/stats"
        url_link_virtual = "https://" + url_ip + "/mgmt/tm/ltm/virtual"
        # url_link = "https://" + url_ip + url
        # print(url_ip)
        # print(url_link)
        if args.log:
            url_link = "https://" + url_ip + url_log
            get_log(url_link, headers)
        elif args.mgmtroute:
            url_link = "https://" + url_ip + url_mgmt
            get_mgmt_route(url_link, headers)
        else:
            try:
                get_soft_ware(url_link_software, headers, auth)
                get_serial_number(url_link_hardware, headers, auth)
                get_info(url_link_performance,headers,auth)
            except:
                print("!!!!!!Part 1 get failed!")
            try:
                get_log(url_link_bash,headers,auth)
            except:
                print("!!!!!!Log get failed!")
            try:
                get_cm_status(url_link_cm,headers,auth)
            except:
                print("!!!!!!Cm status get failed!")
            #get_mgmt_route(url_link_mgmt_route,headers,auth)
            try:
                get_hardware_info(url_link_hardware, headers, auth)
            except:
                print("!!!!!!Hardware info get failed!")
            try:
                get_per_info(url_link_per_info,headers,auth)
                get_sync_status(url_link_sync_status,headers,auth)
                get_device_sync_action(url_device_sync_action,headers,auth)
                get_ntp(url_link_bash, headers, auth)
                get_disk_use(url_link_bash, headers, auth)
            except:
                print("!!!!!!Part 3 get failed!")
            try:
                get_virtual(url_link_virtual, headers, auth)
            except:
                print("!!!!!!Get Virtual failed!")
            #get_user_info(url_link_user_info,headers,auth)
            #get_proc_info(url_link_proc_info, headers, auth)
            #create_user(url_link_user_info,headers,auth)
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

