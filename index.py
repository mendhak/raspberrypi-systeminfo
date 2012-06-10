#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
import os
import platform
import urllib2
from subprocess import Popen, PIPE, STDOUT
cgitb.enable()

print "Content-Type: text/html;charset=utf-8"
print

def GetBashOutput(cmd):
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE,
        stderr=STDOUT, close_fds=True)
    output = p.stdout.read()
    p.stdout.close()
    return output.strip().split('\n')


print "<h1>Raspberry Pi Diagnostic Info</h1>"

print "<p>Total memory: %s</p>" % (
    GetBashOutput("free | grep Mem | awk '{print $2}'"))


print "<p>Used memory: %s</p>" % (
    GetBashOutput("free | grep Mem | awk '{print $3}'"))


print "<p>Free memory: %s</p>" % (
    GetBashOutput("free | grep Mem | awk '{print $4}'"))

print "<p>Users: %s</p>" % (
    GetBashOutput("w | awk 'NR>2 {print $1\",\"$3\",\"$4}'"))

print "<p>Top procs: %s</p>" % (
    GetBashOutput("top -b -n 1 | awk 'NR>7 && NR<19 && $12 !~ \"top\" {print $12}'"))


def HumanDateString(seconds):
 
     total_seconds = float(seconds)
 
     # Helper vars:
     MINUTE  = 60
     HOUR    = MINUTE * 60
     DAY     = HOUR * 24
 
     # Get the days, hours, etc:
     days    = int( total_seconds / DAY )
     hours   = int( ( total_seconds % DAY ) / HOUR )
     minutes = int( ( total_seconds % HOUR ) / MINUTE )
     seconds = int( total_seconds % MINUTE )
 
     # Build up the pretty string (like this: "N days, N hours, N minutes, N seconds")
     string = ""
     if days > 0:
         string += str(days) + " " + (days == 1 and "day" or "days" ) + ", "
     if len(string) > 0 or hours > 0:
         string += str(hours) + " " + (hours == 1 and "hour" or "hours" ) + ", "
     if len(string) > 0 or minutes > 0:
         string += str(minutes) + " " + (minutes == 1 and "minute" or "minutes" ) + ", "
     string += str(seconds) + " " + (seconds == 1 and "second" or "seconds" )
 
     return string;

print "<p>Uptime: %s</p> " % HumanDateString(GetBashOutput("cat /proc/uptime | awk '{print $1}'")[0])

print "<p>CPU Usage: %s</p>" % GetBashOutput("top -bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\\([0-9.]*\\)%\\id.*/\\1/\" | awk '{print 100 - $1\"%\"}'")

print "<p>Disk Usage: %s</p>" % GetBashOutput("df -h | awk 'NR > 1 {print $6\",\"$2\",\"$3\",\"$5\",\"$4}'")


usock = urllib2.urlopen("http://icanhazip.com/")
ip = usock.read()
usock.close()

print "<p>External IP Address: %s</p>" % ip

print "<p>Local IP Addresses: %s</p>" % GetBashOutput("ifconfig  | awk '/inet addr/ {split ($2,A,\":\"); print A[2]}'")


print "<p>Hostname: %s</p>" % os.uname()[1]



print "<p>OS: %s</p>" % platform.system()
print "<p>Release: %s</p>" % platform.release()
print "<p>Version: %s</p>" % platform.version()
print "<p>Machine type: %s</p>" % platform.machine()
print "<p>Architecture: %s</p>" % platform.architecture()[0]

print "<p>Processor: %s</p>" % GetBashOutput("cat /proc/cpuinfo | awk -F: 'NR==1 {print $2}'")
