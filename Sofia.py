#!/usr/bin/python
# -*- coding: windows-1252 -*-

"""
NOMBRE: 
  app.py
DESCRIPCION:
  
REALIZADO POR:
  Equipo de Desarrollo "SOFIA" cucsofia@gmail.com
"""

import wxversion
wxversion.select('2.8')
import wx

import sys, os, signal, commands

from modules import *

class Sofia(wx.App):

  def OnInit(self):
    self.SetAppName("Sofia")
#--Presentacion Ventana Splash--#
    bmp = wx.Image("./images/splash.png").ConvertToBitmap()
    wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN | wx.SPLASH_TIMEOUT, 1500, None, -1)
#--Fin de la Ventana Splash--#
    self.config = config.GetConfig()
    showPos = self.config.Read("pos")
    if showPos:
      posx, posy, sizex, sizey = eval(showPos)
    else:
      posx, posy, sizex, sizey = (0, 0, 500, 300)
      self.config.Write("pos", str( (posx, posy, sizex, sizey) ))
      self.config.Flush()
    self.tool = self.config.Read("tool")
    self.frame = MainFrame(self, posx, posy, sizex, sizey)
    wx.SystemOptions.SetOptionInt("mac.window-plain-transition", 1)
    showTipText = self.config.Read("tips")
    if showTipText:
      showTip, index = eval(showTipText)
    else:
      showTip, index = (1, 0)
    if showTip:
      tp = wx.CreateFileTipProvider(config.opj("tips.txt"), index)
      showTip = wx.ShowTip(self.frame, tp)
      index = tp.GetCurrentTip()
      self.config.Write("tips", str( (showTip, index) ))
      self.config.Flush()
    self.frame.Show()
    
    return True

  def SaveConfig(self, evt):
    self.config = config.GetConfig()
    self.config.Write("pos", str( (self.frame.GetPosition()[0], self.frame.GetPosition()[1], self.frame.GetSize()[0], self.frame.GetSize()[1]) ))
    self.config.Flush()
    
  def GetFrame(self):
    return self.frame
  
  def Senal(self, signum, frame):
    if sys.platform == 'linux2':
      status, enlace = commands.getstatusoutput("cat %s/argumentos.txt" % config.GetDataDir())
      if status == 0:
        self.GetFrame().AbrirModeloDirecto(enlace)

if __name__ == '__main__':
  app = Sofia()
  for enlace in sys.argv[1:]:
    app.GetFrame().AbrirModeloDirecto(enlace)
  if sys.platform == 'linux2':
    signal.signal(signal.SIGUSR1, app.Senal)
  app.MainLoop()