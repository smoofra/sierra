
import sys
import argparse
import os
import re

# pip install pyserial
from serial import Serial


def init_sierra(serial):
  serial.write(b'138065\r\n')  #unlock 
  serial.write(b'c22a 25\r\n') #enable telemetry

def scan_for_records(serial):
  buffer = ""
  while True:
    if len(buffer) > 2048:
      buffer = buffer[1024:]
    buffer += serial.read(1).decode('ascii')
    m = re.search(r'\[[\da-fA-F ]*\]$', buffer)
    if not m:
      m = re.search(r'\{[\da-fA-F ]*\}$', buffer)
    if not m:
      continue
    yield m.group()
    buffer = ""

def clear():
  if os.name == 'nt':
    os.system('cls')
  else:
    os.system('clear')

def main():

  parser = argparse.ArgumentParser("read telemetry from Sierra radio controller")
  parser.add_argument("port")
  parser.add_argument("baud", type=int)
  args = parser.parse_args()

  serial = Serial(args.port, baudrate=args.baud, timeout=.01)

  init_sierra(serial)
  for rec in scan_for_records(serial):
    clear()
    decode_record(rec)
    sys.stdout.flush()

def onoff(value):
  if value:
    return "ON "
  else:
    return "off"

def decode_record(record):
  if record[0] != '[':
    return

  telem = record[1:-1]

  # For future referemce Braces:
  #linkon = "00"
  #loop = "00"
  #disabled = "00"
  #subdisabled = "00"
  #split_group = "00"
  #interfaced = "00"

  names = ("COR","PL","QuRX","DTMF","PTT")
  telemlist = [int(x, 16) for x in record[1:-1].split()]

  for portnum in range(8):
    print ("Port " + str(portnum)+ "   ", end ='')
    for telem_value, name in zip(telemlist, names):
      mask = 1 << portnum
      print  (name, onoff(telem_value & mask), end =' ')
    print()

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    pass
