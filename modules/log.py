#!/usr/bin/python
# -*- coding: windows-1252 -*-

import config

import os
import codecs

class Log():
  
  def __init__(self, proyecto):
    self.proyecto = proyecto
  
  def ConstruirStringModelo(self, fecha, nombreObjeto, transaccion):
    stringModelo = "FECHA Y HORA :" + fecha + '\n' + "TRANSACCION: " + transaccion + '\n' + "NOMBRE DEL OBJETO: " + nombreObjeto 
    self.RegistrarEvento(stringModelo)
    self.RegistrarEvento("______________________________________________________________________________________________________")
  
  def RegistrarEvento(self, stringLog):
    if not os.path.exists("%s/log" % config.GetDataDir()):
        os.makedirs("%s/log" % config.GetDataDir())
    self.archivo = codecs.open(os.path.join("%s/log" % config.GetDataDir(), "%s.log" % self.proyecto.nombre), encoding='windows-1252', mode='a')
    self.archivo.write(stringLog + '\n')
    self.archivo.close()
  
  def VerEventos(self):
    if not os.path.exists("%s/log" % config.GetDataDir()):
        os.makedirs("%s/log" % config.GetDataDir())
    self.archivo = codecs.open(os.path.join("%s/log" % config.GetDataDir(), "%s.log" % self.proyecto.nombre), encoding='windows-1252', mode='r')
    lineas = self.archivo.read()
    self.archivo.close()
    return lineas