#!/usr/bin/python3 -tt
# Sierra Telemetry decoder ver 0.5 by N7CK
# Version for Python 3
# September 2020

# Get the system and telnet libraries

import sys
import telnetlib

# Clear Screen function

from os import system, name

def clear():
# for Windows
  if name == 'nt':
    _ = system('cls')
# For mac and Linux (os.name ="posix")
  else:
    _ = system('clear')

#
# This is the input section to set variables.
#
clear()
print ("              Sierra Telemetry Decoder v0.5\n\n")
print ("Please have the site name, ip address and port ready.\n\n")

SITE = input ("Site Name: ")
if SITE == "":
  SITE = "Dragoon"

HOST = input ("Site ip address or Hostname: ")
if HOST == "":
  HOST = "192.168.97.20"

PORT = input ("Port: ")
if PORT == "":
  PORT = "5006"

print ("Trying: Site: "+SITE + "  Host: " + HOST + "  Port: " + PORT)
print ("Waiting for connection and some telemetry . . .")

# Site info for reference
#SITE = "Dragoon"
#HOST = "192.168.97.20"
#PORT = "5007"
#SITE = "HELIOGRAPH"
#HOST = "8.193.12.246"
#PORT = "5006"


# connect
telnetObj=telnetlib.Telnet(HOST,PORT)


# send cr / lf
message = ("\n\r").encode('ascii')

telnetObj.write(message)

#while  1 == 1:
def tcode():
  output1=telnetObj.read_until(b"]")
  output = output1.decode('ascii')
  telem = (output)
  telem = (telem.strip())
#  print (telem)
#  print (len(telem))
# Simulated Incoming data:
#telem = "[01 06 8F FF 05]"


# Get rid of brackets
  telem = telem [1:15]

# For future referemce Braces:
#linkon = "00"
#loop = "00"
#disabled = "00"
#subdisabled = "00"
#split_group = "00"
#interfaced = "00"

  Brackets = ("COR","PL","QuRX","DTMF","PTT")
  y=0
  telemlist= [0,0,0,0,0]
  for x in range (0,15,3):
    telem1 = telem [x:x+2]
    y=y+1
#  print (telem1)
    telemlist[y-1] = int(telem1,16)

#print (telemlist)

  telemread = [(0,""),(0,""),(0,""),(0,""),(0,"")]

  for x  in range(5):
#  print (telemlist[x])
    telemread[x] = telemlist[x], Brackets [x]
#print 9telemread
# Clear screen
  clear()
  print ( "     " + SITE + " Port Status --  Hit ENTER to exit. \n")
  for y in range(8):
    print ("Port " + str(y)+ "   ", end ='')

    for x in range(5):
      z= telemread[x]
      e = 1 << y
#    print z[0], e
      if z[0] & e >= 1:
        ron= z[1]+ " on   "
        print  (ron, end ='')
      else:
        ron= z[1]+ " off  "
        print ( ron, end = '')

    print (" ")

# This runs the main decode loop .. waiting for error (ctl-c) - Works on Linux
#try:
#  while True:
#    tcode()
#except:
#  pass


import threading as th

keep_going = True
def key_capture_thread():
  global keep_going
  input()
  keep_going = False

def do_stuff():
  th.Thread(target=key_capture_thread, args=(), name='key_capture_thread', daemon=True).start()
  while keep_going:
    tcode()

do_stuff()

# Close telent session, clear screen and exit

telnetObj.close()

clear()
print ("Telent session finished\n\n")


exit()

