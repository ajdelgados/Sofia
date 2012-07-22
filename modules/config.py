#!/usr/bin/python
# -*- coding: windows-1252 -*-

import wxversion
wxversion.select('2.8')
import wx

import os

def opj(path):
  """Convert paths to the platform-specific separator"""
  st = apply(os.path.join, tuple(path.split('/')))
  # HACK: on Linux, a leading / gets lost...
  if path.startswith('/'):
    st = '/' + st
  return st

def GetDataDir():
  """
  Return the standard location on this platform for application data
  """
  sp = wx.StandardPaths.Get()
  return sp.GetUserDataDir()

def GetConfig():
  if not os.path.exists(GetDataDir()):
    os.makedirs(GetDataDir())
  config = wx.FileConfig(localFilename=os.path.join(GetDataDir(), "options.txt"))
  return config