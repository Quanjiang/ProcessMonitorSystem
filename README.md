# ProcessMonitorSystem

Python with flask simple system for monitor and start the process by scheduler
(I'm working on this simple project right now. maybe ready for 2week)
-----

##

I write some script for deal some business in workday. Some time I just forget which server I put them at and what's the current status of those script.(only when email never come up I know one of those script crash). Recently I plan to set up the openshift cluser on my lab to put all of those script into openshift as server. it will be help for manager and control. But the issue still there I need some way to check those script status when I need. the simple web page will be great. That's the reason I create this project. I think maybe some people meet the same requet so open source this project to save other people's time.

## Baisc

Python3.x with Flask for web, apscheduler

https://github.com/agronholm/apscheduler
http://flask.pocoo.org/

## Concept

* Communication : The communication between script/process which need monitor with this system was some files.

** pms.conf : In this file define the basic info for script/process. It was write in json struct in python way. ( this file will be run as python script to get define may have risk if anyone can access this script and modify it. I run all the code in docker(openshift))

** up.log (option):  In this file every time the script/process and write the current state into this file.

** main.log(this file can point to other name define in pms.conf) : All of the script/process stdout and errout will be point into here.

** td1.log (option): td1.log,td2.log .... each file was used as each sub-threading stdout or anyother output. Need script/process to generate the log. The page will show below's file in real time on the web.

##  How to use

### script/process need todo:

* generate *pms.conf* file under it's folder.

### put the path of script/process folder into : monitor_list file.

### Use python2/3 runing start.py

### open the URL: http://your_server:1234/

## Features

### Email notice
set the rule to send email.

### Http Hook
set the rule to trigger the hook (http access other pls like jenkins)

### Module system

For different script/process. you can define your own style dashboard by use module.
It design in very easy way.

## END
