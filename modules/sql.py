#!/usr/bin/python
# -*- coding: windows-1252 -*-

from log import *

class SQL():

  def __init__(self):
    self.variablePostgreSQL = [["BIT", 1], ["BIT VARYING", 1], ["BOOLEAN", 0], ["CHAR", 0],
    ["CHARACTER", 1],  ["DATE", 0], ["INTEGER", 0],
    ["NUMERIC", 1], ["SERIAL", 0], ["TEXT", 0], ["TIME WITHOUT TIME ZONE", 0], ["VARCHAR", 1]]

  def ScriptPostgreSQL(self, proyecto):
    text = "-- Script generado por el Software Sofia v0.073 para PostgreSQL.\n"
    for entidad in proyecto.entidades:
      atributoText = ""
      primariKey = ""
      primariKeyAct = 1
      cont = 0
      primero = 0
      segundo = 0
      for atributo in entidad.atributos:
        if cont == 0:
          atributoText = atributoText + "\n"
        cont = cont + 1
        if primero == 1:
          atributoText = atributoText + ",\n"
        if segundo == 1:
          primarikey = primariKey + ", "
        if atributo.nombreColumna == "":
          atributo.nombreColumna = atributo.nombre
        if atributo.clavePrimaria == True:
          if primariKeyAct == 1:
            primariKey = primariKey + ", PRIMARY KEY ("
            primariKeyAct = 0
          else:
            primariKey = primariKey + ", "
          primariKey = primariKey + atributo.nombreColumna
        if self.ActivarLongitud(atributo.data["tipoDeAtributo"]) == False:
          atributoText = atributoText + "\t\t\t\t" + atributo.nombreColumna + " " + atributo.tipo
        else:
          if atributo.data["longitud"] == "0":
            atributo.data["longitud"] = "1"
          atributoText = atributoText + "\t\t\t\t" + atributo.nombreColumna + " " + atributo.tipo + " (" + str(atributo.data["longitud"]).replace('.', ',') + ")"
        if atributo.notNull:
            atributoText = atributoText + " NOT NULL"
        primero = 1
      if primariKeyAct == 0:
        primariKey = primariKey + ")"
      text = text + "\n-- Table: " + entidad.nombre + "\n"
      text = text + "-- DROP TABLE " + entidad.nombre + ";\n"
      text = text + "CREATE TABLE " + entidad.nombre + " (" + atributoText + primariKey +"\n);\n"
    text = text + "\n"
    for relacion in proyecto.relaciones:
      for entidad in proyecto.entidades:
        if relacion.entidadHija.nombre == entidad.nombre:
          for atributo in entidad.atributos:
            if atributo.claveForanea == True:
              if atributo.entidadPadre.nombre == relacion.entidadPadre.nombre:
                if atributo.nombreColumna == "":
                  atributo.nombreColumna = atributo.nombre
                text = text + "ALTER TABLE " + relacion.entidadHija.nombre + " ADD CONSTRAINT " + relacion.entidadHija.nombre + "_" + relacion.entidadPadre.nombre + "_" + atributo.nombreColumna + "_" + atributo.atributoPadreNombre + " FOREIGN KEY (" + atributo.nombreColumna + ") REFERENCES " + relacion.entidadPadre.nombre + " (" + atributo.atributoPadreNombre + ");\n\n"
    self.log = Log(self)
    proyecto.log.ConstruirStringModelo("hora", "Archivo Plano SQL: " + text, "Archivo Plano SQL")
    return text

  def ActivarLongitud(self, string):
    for t in SQL().variablePostgreSQL:
      if t[0] == string:
        if t[1] == 0:
          return False
        else:
          return True