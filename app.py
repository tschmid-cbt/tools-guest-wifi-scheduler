from flask import Flask, render_template, request
import app_db as db
import sqlite3
import datetime
import time
import pandas
from datetime import timedelta
import sys
from netmiko import ConnectHandler
import random
from deets import *
import emailsend as mail
import logging
from logging.handlers import RotatingFileHandler

app=Flask(__name__)
with open("nouns.txt") as noun_file:
    nouns=noun_file.read().split()
with open("adjectives.txt") as adj_file:
    adjs=adj_file.read().split()


@app.route("/",methods=['GET'])
def index():
    if request.method=='GET':
        return render_template("index.html")
@app.route("/success", methods=['POST'])
def success():
    if request.method=='POST':
        user=request.headers.get('REMOTE_USER')
        duration=request.form["numberOfHours"]
        starttime=request.form["date"]+" "+request.form["time"]
        endtime=pandas.to_datetime(starttime)+timedelta(hours=int(duration))
        endtime=endtime.strftime('%Y-%m-%d %H:%M')
        password=random.choice(adjs)+random.choice(nouns)
        rows=db.view()
        ssid="CBT-guest"
        conflict=0
        for row in rows:
            userstarttime=pandas.to_datetime(starttime)
            userendtime=pandas.to_datetime(endtime)
            dbstarttime=pandas.to_datetime(row[2])
            dbendtime=pandas.to_datetime(row[3])
            if userstarttime>dbstarttime and userstarttime<dbendtime:
                error=row[0]
                conflict=1
                return render_template("error.html", error=error)
            if userstarttime>dbstarttime and userstarttime<dbendtime and  userendtime>dbendtime:
                error=row[0]
                conflict=1
                return render_template("error.html", error=error)
            if userendtime<dbendtime and userendtime>dbstarttime:
                error=row[0]
                conflict=1
                return render_template("error.html", error=error)
            if userstarttime<dbstarttime and userstarttime<dbendtime and userendtime>dbendtime:
                error=row[0]
                conflict=1
                return render_template("error.html", error=error)
        if conflict==0:
            db.insert(user,starttime,endtime,duration,password)
            mail.mails(user,starttime,endtime,password,ssid)
            return render_template("success.html", password=password)
@app.route("/error.html", methods=['GET','POST'])
def error():
    return render_template("error.html")

@app.route("/view_schedule", methods=['GET','POST'])
def view_schedule():
    if request.method=='GET':
        con = sqlite3.connect("wifi.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from wifi")
        rows=cur.fetchall()
        con.close()
    if request.method=='POST':
        delete=request.form["Entry"]
        db.delete(delete)
        con = sqlite3.connect("wifi.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("select * from wifi")
        rows=cur.fetchall()
        con.close()
    return render_template("view_schedule.html",rows = rows)

@app.route("/wifi_status", methods=['GET'])
def wifi_status():
    text_out=wifiChecker()
    return render_template("wifi_status.html", text_out=text_out)

def wifiChecker():
    ssh_session=ConnectHandler(device_type='cisco_wlc_ssh',ip='172.17.1.5',username=ssh_username,password=ssh_password)
    text_out=ssh_session.send_command("show wlan 4")[177:236]
    ssh_session.disconnect()
    return(text_out)

if __name__ == '__main__':
    app.debug=True
    app.run()
