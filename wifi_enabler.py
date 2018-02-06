import sqlite3
import datetime
from datetime import timedelta
import time
import pandas
from netmiko import ConnectHandler
import app_db as db
from deets import *

def wifiChecker():
    ssh_session=ConnectHandler(device_type='cisco_wlc_ssh',ip='172.17.1.5',username=ssh_username,password=ssh_password)
    enabled=ssh_session.send_command("show wlan 4")[228:236]
    ssh_session.disconnect()
    return(enabled)

def wifiDisabler():
    ssh_session=ConnectHandler(device_type='cisco_wlc_ssh',ip='172.17.1.5',username=ssh_username,password=ssh_password)
    ssh_session.config_mode()
    ssh_session.send_command("wlan disable 4")
    ssh_session.exit_config_mode()
    enabled=ssh_session.send_command("show wlan 4")[228:236]
    ssh_session.disconnect()
    return(enabled)

def wifiEnabler(password):
    ssh_session=ConnectHandler(device_type='cisco_wlc_ssh',ip='172.17.1.5',username=ssh_username,password=ssh_password)
    ssh_session.config_mode()
    ssh_session.send_config_set("wlan security wpa akm psk set-key ascii " + str(password) + " 4")
    ssh_session.send_command("wlan enable 4")
    ssh_session.exit_config_mode()
    ssh_session.disconnect()

def wifiMonitor():
    enablestatus=0
    _sleep_=60
    print(_sleep_)
    now=datetime.datetime.now()
    _cur_date_=now.strftime("%Y-%m-%d")
    rows=db.view()
    if not rows:
        cur_status=wifiChecker()
        if "Enabled" in cur_status:
            cur_status=wifiDisabler()
            print("Exiting our attempt to remove configuration.  Current wifi status is "+cur_status)
    for row in rows:
        password=row[5]
        _id_=row[0]
        starttime=pandas.to_datetime(row[2])
        startdate=starttime.strftime("%Y-%m-%d")
        print(startdate)
        if startdate<=_cur_date_:
            print("Found entry with date of "+row[2])
            endtime=pandas.to_datetime(row[3])
            if now>=endtime:
                print("Time has passed for entry "+str(row[0])+" need to disable wifi and delete from db.")
                cur_status=wifiChecker()
                print(cur_status)
                if "Enabled" in cur_status:
                    cur_status=wifiDisabler()
                    print("Exiting our attempt to remove configuration.  Current wifi status is "+cur_status)
                if "Disabled" in cur_status:
                    print("Entering attempt to delete from db")
                    db.delete(_id_)
                    continue
            if now>=starttime:
                enablestatus=1
                print("Connecting to controller to check status.")
                cur_status=wifiChecker()
                if "Disabled" in cur_status:
                    print("Wifi is disabled, attemptying to remedy.")
                    wifiEnabler(password)
    if enablestatus==0:
        print("Connecting to controller to check status.")
        cur_status=wifiChecker()
        if "Enabled" in cur_status:
            print("Wifi should not be enabled.  Disabling...")
            wifiDisabler()
    print("Sleeping for "+str(_sleep_))
    time.sleep(int(_sleep_))

while True:
    wifiMonitor()
