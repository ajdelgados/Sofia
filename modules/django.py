#!/usr/bin/python
# -*- coding: windows-1252 -*-

from log import *

class Django():

  def __init__(self):
    self.variableDjango = [["BIT", 1, "CharField", 0], ["BIT VARYING", 1, "CharField", 0],
      ["BOOLEAN", 0, "IntegerField", 0], ["CHAR", 0, "CharField", 1], ["CHARACTER", 1, "CharField", 0],
      ["DATE", 0, "DateTimeField", 0], ["INTEGER", 0, "IntegerField", 0], ["NUMERIC", 1, "IntegerField", 0],
      ["SERIAL", 0, "IntegerField", 0], ["TEXT", 0, "TextField", 0], ["TIME WITHOUT TIME ZONE", 0, "DateTimeField", 0],
      ["VARCHAR", 1, "CharField", 0]]

  def ScriptDjango(self, proyecto):
    text = "# Script generado por el Software Sofia v0.073 para Django.\n\nfrom django.db import models\n\n"
    for entidad in proyecto.entidades:
      atributoText = ""
      for atributo in entidad.atributos:
        if atributo.nombreColumna == "":
          atributo.nombreColumna = atributo.nombre
        if atributo.claveForanea == True:
          for relacion in proyecto.relaciones:
            if relacion.entidadHija.nombre == entidad.nombre:
              if atributo.entidadPadre.nombre == relacion.entidadPadre.nombre:
                atributoText = atributoText + "\n  " + relacion.entidadPadre.nombre + " = models.ForeignKey(" + relacion.entidadPadre.nombre.capitalize() + ")"
        else:
          if atributo.nombreColumna == "id":
            pass
          else:
            coma = 0
            if self.ActivarLongitud(atributo.data["tipoDeAtributo"], atributo) == False:
              atributoText = atributoText + "\n  " + atributo.nombreColumna + " = models." + self.Pgsql2Django(atributo.tipo) + " ("
            else:
              if atributo.data["longitud"] == "0":
                atributo.data["longitud"] = "1"
              atributoText = atributoText + "\n  " + atributo.nombreColumna + " = models." + self.Pgsql2Django(atributo.tipo) + " (max_length="+ str(atributo.data["longitud"]).replace('.', ',')
              coma = 1
            if atributo.notNull:
              if coma:
                atributoText = atributoText + ", "
              atributoText = atributoText + "blank=False, null=False"
            atributoText = atributoText + ")"
      if atributoText:
        text = text + "class " + entidad.nombre.capitalize() + "(models.Model): " + atributoText + "\n\n"
      atributoText = ""
    self.log = Log(self)
    proyecto.log.ConstruirStringModelo("hora", "Archivo Plano SQL: " + text, "Archivo Plano SQL")
    return text

  def ActivarLongitud(self, string, objeto):
    for t in Django().variableDjango:
      if t[0] == string:
        if t[1] == 0:
          if t[3] == 1:
            objeto.data["longitud"] = "1"
            return True
          return False
        else:
          return True

  def Pgsql2Django(self, string):
    for t in Django().variableDjango:
      if t[0] == string:
        return t[2]