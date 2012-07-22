#!/usr/bin/python
# -*- coding: windows-1252 -*-

"""
NOMBRE:
  runLinux.py
DESCRIPCION:

REALIZADO POR:
  Arturo J. Delgado S. ajdelgados@gmail.com
"""

import os, sys, commands, time, random

enlaces = ""
pid = ""

for abrir in sys.argv[1:]:
  enlaces += " "
  enlaces += abrir

time.sleep( 5 * random.random())

if sys.platform == 'linux2':
  status, pid = commands.getstatusoutput("pgrep Sofia.py")

if pid:
  if status == 0:
    os.system('echo "%s" > ~/.Sofia/argumentos.txt' % enlaces)
    coman = 'kill -USR1 ' + pid
    os.system(coman)
else:
  dir = 'cd %s && ./Sofia.py%s' % (os.path.abspath(os.path.dirname(sys.argv[0])), enlaces)
  os.system(dir)
