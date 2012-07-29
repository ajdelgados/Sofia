#!/usr/bin/python
# -*- coding: windows-1252 -*-

import wxversion
wxversion.select('2.8')
import wx
import wx.lib.ogl as ogl

from log import *
from id import *
from dialog import *

import math
import datetime

def str2bool(string):
  return string == 'True'

class Entidad(ogl.CompositeShape):

  def __init__(self, nombre = "entidad", descripcion = "", tipo = 0):
    ogl.CompositeShape.__init__(self)
    self.id_entidad = None
    self.nombre = None
    self.nombreForma = ogl.TextShape(100, 48)
    self.descripcion = None
    self.tipo = tipo
    self.atributos = []
    self.atributosForma = ogl.DividedShape(100, 20)
    self.editar = 0
    self.data = {}
    self.data["nombre"] = nombre
    self.data["descripcion"] = descripcion
    self.relaciones = []
    self.entidadesPadres = []
    self.entidadesHijas = []
    self.nLetras = 10

  def CrearEntidad(self, frame, canvas, contador, posX = 60, posY = 65):
    self.frame = frame
    self.id_entidad = contador
    self.nombre = self.data.get("nombre")
    self.descripcion = self.data.get("descripcion")
    self.nombreForma.nombre = self.data.get("nombre")
    dc = wx.ClientDC(canvas)
    self.SetX(posX)
    self.SetY(posY)
    entity = []
    entity[len(entity):] = [self]
    for i in entity:
      canvas.AddShape(i)
    self.nombreForma.frame = frame
    self.nombreForma.SetFormatMode(0, 0)
    self.nombreForma.SetX(posX)
    self.nombreForma.SetY(posY - 10)
    entity = []
    entity[len(entity):] = [self.nombreForma]
    for i in entity:
      canvas.AddShape(i)
    self.nombreForma.AddText(self.nombre)
    self.nombreForma.evthandler = MyEvtHandler()
    self.nombreForma.evthandler.SetShape(self.nombreForma)
    self.nombreForma.evthandler.SetPreviousHandler(self.nombreForma.GetEventHandler())
    self.nombreForma.SetEventHandler(self.nombreForma.evthandler)
    self.atributosForma.nombre = self.data.get("nombre", "")
    self.atributosForma.frame = frame
    self.atributosForma.SetX(posX)
    self.atributosForma.SetY(posY)
    entity = []
    entity[len(entity):] = [self.atributosForma]
    for i in entity:
      canvas.AddShape(i)
    region = ogl.ShapeRegion()
    region.SetProportions(0.0, 0.50)
    self.atributosForma.AddRegion(region)
    region = ogl.ShapeRegion()
    region.SetProportions(0.0, 0.50)
    self.atributosForma.AddRegion(region)
    self.atributosForma.SetFormatMode(0, 0)
    self.atributosForma.SetFormatMode(0, 1)
    self.atributosForma.evthandler = MyEvtHandler()
    self.atributosForma.evthandler.SetShape(self.atributosForma)
    self.atributosForma.evthandler.SetPreviousHandler(self.atributosForma.GetEventHandler())
    self.atributosForma.SetEventHandler(self.atributosForma.evthandler)
    self.SetCanvas(canvas)
    self.AddChild(self.nombreForma)
    self.AddChild(self.atributosForma)
    self.nombreForma.SetDraggable(False)
    self.atributosForma.SetDraggable(False)
    self.Show(1)
    c = self.frame.GetActiveChild().conexion.cursor()
    c.execute("INSERT INTO entidad VALUES ('%s', '%s', '%s')" % (self.id_entidad, self.nombre, self.descripcion))
    c.close()
    self.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad: " + "Id: " + str(self.id_entidad), "Crear Entidad")
    self.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad: " + "Nombre:  " + self.nombreForma.nombre, "Crear Entidad")
    self.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad: " + "Descripcion: " + self.descripcion, "Crear Entidad")
    self.frame.GetActiveChild().conexion.commit()
    self.tree = self.frame.GetActiveChild().tree.AppendItem(self.frame.GetActiveChild().treeEnti, self.nombre, image = self.frame.GetActiveChild().imgEnt, data = wx.TreeItemData(self))
    self.treeAtri = self.frame.GetActiveChild().tree.AppendItem(self.tree, 'Atributos', image = self.frame.GetActiveChild().imgAtrPa, data = wx.TreeItemData(self))
    return self

  def ModificarEntidad(self, canvas, entidadModificar, entidades):
    dlg = Dialogos(canvas.frame, canvas.frame.parent.Idioma(archivo[ENTIDAD_TITULO]))
    dlg.Entidad(entidadModificar.data)
    if dlg.ShowModal() == wx.ID_OK:
      for elemento2 in entidades:
        if elemento2.nombre == entidadModificar.data.get("nombre") and entidadModificar.nombre != entidadModificar.data.get("nombre"):
          validar = entidadModificar.ValidarNombreEntidad(entidades)
          if validar == False:
            entidadModificar.data["nombre"] = entidadModificar.nombre
            return 0
      entidadModificar.nombre = entidadModificar.data.get("nombre")
      entidadModificar.descripcion = entidadModificar.data.get("descripcion")
      entidadModificar.nombreForma.nombre = entidadModificar.data.get("nombre")
      entidadModificar.atributosForma.nombre = entidadModificar.data.get("nombre")
      c = entidadModificar.frame.GetActiveChild().conexion.cursor()
      c.execute("UPDATE entidad SET nombre = ?, descripcion = ? WHERE id = ?", (entidadModificar.nombre, entidadModificar.descripcion, entidadModificar.id_entidad))
      c.close()
      entidadModificar.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad: " + "Nombre:  " + entidadModificar.nombre , "Modificar Entidad")
      entidadModificar.frame.GetActiveChild().conexion.commit()
      entidadModificar.frame.GetActiveChild().tree.SetItemText(entidadModificar.tree, entidadModificar.nombre)
      dc = wx.ClientDC(canvas)
      entidadModificar.nombreForma.FormatText(dc, entidadModificar.nombre, 0)
    else:
      return 0

  def EliminarEntidad(self, canvas, elemento, entidades, frame):
    dlg = wx.MessageDialog(frame, 'Desea remover la entidad %s' % elemento.nombre, 'Eliminar Entidad %s' % elemento.nombre, wx.YES_NO | wx.ICON_QUESTION)
    if dlg.ShowModal() == wx.ID_YES:
      if elemento.nombreForma.Selected():
        dc = wx.ClientDC(canvas)
        elemento.Select(False, dc)
        canvas.Redraw(dc)
      eliminar = []
      for elemento2 in elemento.entidadesHijas:
        for elemento3 in elemento2.relaciones:
          if elemento3.entidadPadre.nombre == elemento.nombre:
            eliminar.append(elemento3)
      for elemento4 in eliminar:
        ejecute = Relacion()
        ejecute.EliminarRelacion(elemento4, canvas, frame, entidades)
      c = frame.conexion.cursor()
      c.execute("DELETE FROM entidad WHERE id = %s" % elemento.id_entidad)
      c.close()
      frame.log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad: " + "Nombre:  " + elemento.nombre, "Eliminar Entidad")
      frame.conexion.commit()
      frame.tree.Delete(elemento.tree)
      canvas.RemoveShape(elemento.atributosForma)
      canvas.RemoveShape(elemento.nombreForma)
      canvas.RemoveShape(elemento)
      return 1
    else:
      return 0

  def ValidarNombreEntidad(self, entidades):
    dial = wx.MessageDialog(entidades[0].frame, "Nombre de la Entidad %s exite!" % self.data.get("nombre"), "Error", wx.OK | wx.ICON_ERROR)
    dial.ShowModal()
    dlg = Dialogos(entidades[0].frame, entidad[0].frame.parent.Idioma("Entity"))
    dlg.Entidad(self.data)
    if dlg.ShowModal() == wx.ID_OK:
      for elemento in entidades:
        if elemento.nombre == self.data.get("nombre") and self.nombre != self.data.get("nombre"):
          validar = self.ValidarNombreEntidad(entidades)
          if validar == False:
            return False
    else:
      return False

  def TipoDeEntidad(self, canvas):
    dc = wx.ClientDC(canvas)
    cont = 0
    for relacion in self.relaciones:
      if relacion.tipoRelacion == "Identificadora":
        cont += 1
    if cont != 0:
      self.tipo = 1
    else:
      self.tipo = 0
    if self.tipo == 0:
      self.atributosForma.SetCornerRadius(0)
      ejecute = Atributo()
      ejecute.ModificarAtributosForma(dc, self)
    else:
      self.atributosForma.SetCornerRadius(10)
      ejecute = Atributo()
      ejecute.ModificarAtributosForma(dc, self)

  def HeredarAtributos(self, entidad, relacionTipo = 0):
    dc = wx.ClientDC(entidad.GetCanvas())
    ver = 1
    for relacion in self.relaciones:
      if relacion.entidadPadre.nombre == entidad.nombre:
        if relacion.tipoRelacion == "No-Identificadora":
          ver = 0
    for atributo in entidad.atributos:
      if atributo.clavePrimaria == True:
        num = 0
        for atributo2 in self.atributos:
          if atributo.nombre == atributo2.nombre:
            num = 2
            if atributo2.claveForanea == True:
              num = 1
        if num != 1:
          addAtributo = Atributo()
          addAtributo.data["nombreAtributo"] = atributo.data["nombreAtributo"]
          addAtributo.data["descripcion"] = atributo.data["descripcion"]
          addAtributo.data["primario"] = atributo.data["primario"]
          addAtributo.data["tipoDeAtributo"] = atributo.data["tipoDeAtributo"]
          if num == 2:
            if atributo.data["nombreColumna"]:
              addAtributo.data["nombreColumna"] = "parent_" + atributo.data["nombreColumna"]
            else:
              addAtributo.data["nombreColumna"] = "parent_" + atributo.data["nombreAtributo"]
          else:
            addAtributo.data["nombreColumna"] = atributo.data["nombreColumna"]
          addAtributo.data["longitud"] = atributo.data["longitud"]
          addAtributo.data["autoIncremento"] = atributo.data["autoIncremento"]
          addAtributo.data["notNull"] = atributo.data["notNull"]
          addAtributo.data["foranea"] = True
          addAtributo.claveForanea = True
          addAtributo.entidadPadre = entidad
          addAtributo.atributoPadre = atributo.id_atributo
          addAtributo.atributoPadreNombre = atributo.nombre
          addAtributo.nombre = addAtributo.data.get("nombreAtributo")
          addAtributo.clavePrimaria = addAtributo.data.get("primario")
          addAtributo.tipo = addAtributo.data.get("tipoDeAtributo")
          addAtributo.descripcion = addAtributo.data.get("descripcion")
          addAtributo.nombreColumna = addAtributo.data.get("nombreColumna")
          addAtributo.longitud = addAtributo.data.get("longitud")
          addAtributo.autoIncremento = addAtributo.data.get("autoIncremento")
          addAtributo.notNull = addAtributo.data.get("notNull")
          addAtributo.id_atributo = self.frame.GetActiveChild().contadorAtributo
          self.frame.GetActiveChild().contadorAtributo += 1
          addAtributo.entidad = self
          addAtributo.id_entidad = self.id_entidad
          if ver == 0:
            addAtributo.clavePrimaria = False
            addAtributo.data["primario"] = False
          for atributo3 in self.relaciones:
            if atributo3.entidadPadre.nombre == entidad.nombre:
              atributo3.atributosHeredados.append(addAtributo)
          self.atributos.append(addAtributo)
          c = self.frame.GetActiveChild().conexion.cursor()
          c.execute("INSERT INTO atributo VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (addAtributo.id_atributo, addAtributo.id_entidad, addAtributo.nombre, addAtributo.nombreColumna, addAtributo.descripcion, addAtributo.tipo, addAtributo.longitud, addAtributo.clavePrimaria, addAtributo.claveForanea, addAtributo.notNull))
          c.close()
          addAtributo.tree = self.frame.GetActiveChild().tree.AppendItem(self.treeAtri, addAtributo.nombre, image = self.frame.GetActiveChild().imgAtr, data = wx.TreeItemData(addAtributo))
          a = self.nombreForma.GetHeight()
          a += 18
          self.nombreForma.SetSize(100, a)
          b = self.atributosForma.GetHeight()
          b += 18
          self.atributosForma.SetSize(100, b)
          ejecute = Atributo()
          ejecute.ModificarAtributosForma(dc, self)
    if self.nombre != entidad.nombre and relacionTipo:
      for entidadHija in self.entidadesHijas:
        continuar = 0
        for relacion in entidadHija.relaciones:
          if relacion.entidadPadre.nombre == self.nombre:
            if relacion.tipoRelacion == "Identificadora":
              continuar = 1
        entidadHija.HeredarAtributos(self, continuar)

  def ModificarAtributosHeredados(self, dc, atributoModificar):
    for atributo in self.atributos:
      if atributo.claveForanea == True:
        if atributo.atributoPadre == atributoModificar.id_atributo:
          atributo.nombre = atributoModificar.data.get("nombreAtributo")
          atributo.tipo = atributoModificar.data.get("tipoDeAtributo")
          atributo.longitud = atributoModificar.data.get("longitud")
          atributo.autoIncremento = atributoModificar.data.get("autoIncremento")
          atributo.notNull = atributoModificar.data.get("notNull")
          atributo.data["nombreAtributo"] = atributoModificar.data.get("nombreAtributo")
          atributo.data["tipoDeAtributo"] = atributoModificar.data.get("tipoDeAtributo")
          atributo.data["longitud"] = atributoModificar.data.get("longitud")
          atributo.data["autoIncremento"] = atributoModificar.data.get("autoIncremento")
          atributo.data["notNull"] = atributoModificar.data.get("notNull")
          atributo.ModificarAtributosForma(dc, self)
          c = self.frame.GetActiveChild().conexion.cursor()
          c.execute("UPDATE atributo SET nombre = ?, nom_colum = ?,  descripcion = ?, tipo_dato = ?, long_dato = ?, cla_prima = ?, cla_fore = ?, atri_n_null = ? WHERE id = ? AND id_entidad = ?", (atributo.nombre, atributo.nombreColumna, atributo.descripcion, atributo.tipo, atributo.longitud, atributo.clavePrimaria, atributo.claveForanea, atributo.notNull, atributo.id_atributo, atributo.id_entidad))
          c.close()
          self.frame.GetActiveChild().tree.SetItemText(atributo.tree, atributo.nombre)
          for entidadHija in self.entidadesHijas:
            entidadHija.ModificarAtributosHeredados(dc, atributo)

class Atributo():
  
  def __init__(self, nombre = "", columna = "", descripcion = "", tipoAtributo = "",
               longitud = "0", primario = False, notNull = False, foranea = False):
    self.id_atributo = 0
    self.id_entidad = 0
    self.nombre = nombre
    self.nombreColumna = columna
    self.tipo = None
    self.precision = 10
    self.escala = 0
    self.clavePrimaria = primario
    self.claveForanea = foranea
    self.notNull = False
    self.autoIncremento = False
    self.descripcion = None
    self.valorPredeterminado = False
    self.longitud = 0
    self.editar = 0
    self.data = {}
    self.data["nombreAtributo"] = nombre
    self.data["nombreColumna"] = columna
    self.data["descripcion"] = descripcion
    self.data["tipoDeAtributo"] = tipoAtributo
    self.data["longitud"] = longitud
    self.data["primario"] = str2bool(primario)
    self.data["autoIncremento"] = False
    self.data["notNull"] = str2bool(notNull)
    self.data["foranea"] = str2bool(foranea)

  def CrearAtributo (self, canvas, entidad, contador):
    dc = wx.ClientDC(canvas)
    self.nombre = self.data.get("nombreAtributo")
    self.clavePrimaria = self.data.get("primario")
    self.tipo = self.data.get("tipoDeAtributo")
    self.descripcion = self.data.get("descripcion")
    self.nombreColumna = self.data.get("nombreColumna")
    self.longitud = self.data.get("longitud")
    self.autoIncremento = self.data.get("autoIncremento")
    self.notNull = self.data.get("notNull")
    self.entidad = entidad
    self.id_atributo = contador
    self.id_entidad = entidad.id_entidad
    entidad.atributos.append(self)
    a = entidad.nombreForma.GetWidth()
    b = entidad.nombreForma.GetHeight()
    b += 18
    entidad.nombreForma.SetSize(a, b)
    a = entidad.atributosForma.GetWidth()
    b = entidad.atributosForma.GetHeight()
    b += 18
    entidad.atributosForma.SetSize(a, b)
    self.ModificarAtributosForma(dc, entidad)
    c = entidad.frame.GetActiveChild().conexion.cursor()
    c.execute("INSERT INTO atributo VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (self.id_atributo, entidad.id_entidad, self.nombre, self.nombreColumna, self.descripcion, self.tipo, self.longitud, self.clavePrimaria, self.claveForanea, self.notNull))
    c.close()
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Id:  " + str(self.id_atributo), "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Nombre:  " + self.nombre, "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Nombre Columna:  " + self.nombre, "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Descripcion:  " + self.descripcion, "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Tipo:  " + self.tipo, "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Longitud:  " + str(self.longitud), "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Clave Primaria:  " + str(self.clavePrimaria), "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Clave Foranea:  " + str(self.claveForanea), "Crear Atributo")
    entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "No Nulo:  " + str(self.notNull), "Crear Atributo")
    entidad.frame.GetActiveChild().conexion.commit()
    self.tree = entidad.frame.GetActiveChild().tree.AppendItem(entidad.treeAtri, self.nombre, image = entidad.frame.GetActiveChild().imgAtr, data = wx.TreeItemData(self))

  def DlgModificarAtributo(self, canvas, entidad):
    lst = []
    for atributo in entidad.atributos:
      lst.append(atributo.nombre)
    dlg = wx.SingleChoiceDialog(canvas.frame, canvas.frame.parent.Idioma("What attribute you want to change?"), canvas.frame.parent.Idioma("%s Entity") % entidad.nombre, lst)
    if dlg.ShowModal() == wx.ID_OK:
      response = dlg.GetStringSelection()
      for atributo in entidad.atributos:
        if atributo.nombre == response:
          self.ModificarAtributo(canvas, entidad, atributo)

  def ModificarAtributo(self, canvas, entidad, atributoModificar):
    dc = wx.ClientDC(canvas)
    dlg = Dialogos(canvas.frame, canvas.frame.parent.Idioma("Attribute"))
    dlg.Atributo(atributoModificar.data)
    if dlg.ShowModal() == wx.ID_OK:
      for atributo2 in entidad.atributos:
        if atributo2.nombre == atributoModificar.data.get("nombreAtributo") and atributoModificar.data.get("nombreAtributo") != atributoModificar.nombre:
          validar = atributoModificar.ValidarNombreAtributo(canvas.frame, entidad.atributos)
          if validar == False:
            #atributoModificar.data["nombreAtributo"] = listaAtributos.nombre
            return 0
      atributoModificar.nombre = atributoModificar.data.get("nombreAtributo")
      atributoModificar.clavePrimaria = atributoModificar.data.get("primario")
      atributoModificar.tipo = atributoModificar.data.get("tipoDeAtributo")
      atributoModificar.descripcion = atributoModificar.data.get("descripcion")
      atributoModificar.nombreColumna = atributoModificar.data.get("nombreColumna")
      atributoModificar.longitud = atributoModificar.data.get("longitud")
      atributoModificar.autoIncremento = atributoModificar.data.get("autoIncremento")
      atributoModificar.notNull = atributoModificar.data.get("notNull")
      c = entidad.frame.GetActiveChild().conexion.cursor()
      c.execute("UPDATE atributo SET nombre = ?, nom_colum = ?,  descripcion = ?, tipo_dato = ?, long_dato = ?, cla_prima = ?, cla_fore = ?, atri_n_null = ? WHERE id = ? AND id_entidad = ?", (atributoModificar.nombre, atributoModificar.nombreColumna, atributoModificar.descripcion, atributoModificar.tipo, atributoModificar.longitud, atributoModificar.clavePrimaria, atributoModificar.claveForanea, atributoModificar.notNull, atributoModificar.id_atributo, atributoModificar.id_entidad))
      c.close()
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Id:  " + str(atributoModificar.id_atributo), "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Nombre:  " + atributoModificar.nombre, "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Nombre Columna:  " + atributoModificar.nombre, "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Descripcion:  " + atributoModificar.descripcion, "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Tipo:  " + atributoModificar.tipo, "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Longitud:  " + str(atributoModificar.longitud), "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Clave Primaria:  " + str(atributoModificar.clavePrimaria), "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Clave Foranea:  " + str(atributoModificar.claveForanea), "Modificar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "No Nulo:  " + str(atributoModificar.notNull), "Modificar Atributo")
      
      entidad.frame.GetActiveChild().tree.SetItemText(atributoModificar.tree, atributoModificar.nombre)
      if atributoModificar.claveForanea == True:
        for atributo4 in entidad.atributos:
          if atributo4.claveForanea == True:
            atributo4.clavePrimaria = atributoModificar.data.get("primario")
      self.ModificarAtributosForma(dc, entidad)
      for entidadHija in entidad.entidadesHijas:
        entidadHija.ModificarAtributosHeredados(dc, atributoModificar)

  def DlgEliminarAtributo(self, canvas, entidad):
    lst = []
    for elemento in entidad.atributos:
      lst.append(elemento.nombre)
    dlg = wx.SingleChoiceDialog(canvas.frame, canvas.frame.parent.Idioma("What attribute you want to delete?"), canvas.frame.parent.Idioma("%s Entity") % entidad.nombre, lst)
    if dlg.ShowModal() == wx.ID_OK:
      response = dlg.GetStringSelection()
      for elemento in entidad.atributos:
        if elemento.nombre == response:
          dlg = wx.MessageDialog(canvas.frame, canvas.frame.parent.Idioma("Want to remove the attribute %s") % elemento.nombre, canvas.frame.parent.Idioma("Delete Attribute %s") % elemento.nombre, wx.YES_NO | wx.ICON_QUESTION)
          if dlg.ShowModal() == wx.ID_YES:
            self.EliminarAtributo(canvas, entidad, elemento)

  def EliminarAtributo(self, canvas, entidad, atributoEliminar, relacion = 0):
    try:
      dc = wx.ClientDC(canvas)
      entidad.atributos.remove(atributoEliminar)
      a = entidad.nombreForma.GetWidth()
      b = entidad.nombreForma.GetHeight()
      b -= 18
      entidad.nombreForma.SetSize(a, b)
      a = entidad.atributosForma.GetWidth()
      b = entidad.atributosForma.GetHeight()
      b -= 18
      entidad.atributosForma.SetSize(a, b)
      c = entidad.frame.GetActiveChild().conexion.cursor()
      c.execute("DELETE FROM atributo WHERE id = ? AND id_entidad = ?", (atributoEliminar.id_atributo, atributoEliminar.id_entidad))
      c.close()
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Id Atributo:  " + str(atributoEliminar.id_atributo), "Eliminar Atributo")
      entidad.frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo: " + "Id Entidad:  " + str(atributoEliminar.id_entidad), "Eliminar Atributo")
      entidad.frame.GetActiveChild().tree.Delete(atributoEliminar.tree)
      self.ModificarAtributosForma(dc, entidad)
      for entidadHija in entidad.entidadesHijas:
        for atributo in entidadHija.atributos:
          continuar = 1
          relacionEditar = 0
          if relacion != 0:
            if relacion.tipoRelacion == "No-Identificadora":
              continuar = 0
          else:
            for relacion in entidadHija.relaciones:
              if relacion.entidadPadre.nombre == entidad.nombre and relacion.entidadHija.nombre == entidadHija.nombre:
                relacionEditar = relacion
          if atributo.nombre == atributoEliminar.nombre and atributo.claveForanea == True and continuar:
            self.EliminarAtributo(canvas, entidadHija, atributo, relacion)
    except:
      pass
  
  def ValidarNombreAtributo(self, frame, entidades):
    dial = wx.MessageDialog(frame, "Nombre del Atributo %s exite!" % self.data.get("nombreAtributo"), 'Error', wx.OK | wx.ICON_ERROR)
    dial.ShowModal()
    dlg = Dialogos(frame, frame.parent.Idioma("Attribute"))
    dlg.Atributo(self.data)
    if dlg.ShowModal() == wx.ID_OK:
      for elemento in entidades:
        if elemento.nombre == self.data.get("nombreAtributo") and self.data.get("nombreAtributo") != self.nombre:
          validar = self.ValidarNombreAtributo(frame, entidades)
          if validar == False:
            return False
    else:
      return False

  def ModificarAtributosForma(self, dc, entidad):
    escribirPrimari = ""
    escribirNoPrimari = ""
    mover = 0
    moverPrimari = 0
    moverNoPrimari = 0
    for elemento in entidad.atributos:
      sumar = 0
      mover +=1
      if elemento.clavePrimaria == True:
        escribirPrimari += elemento.nombre
        if elemento.claveForanea == True:
          escribirPrimari += " (FK)"
          sumar += 5
        escribirPrimari += "\n"
        moverPrimari +=1
      else:
        escribirNoPrimari += elemento.nombre
        if elemento.claveForanea == True:
          escribirNoPrimari += " (FK)"
          sumar +=5
        escribirNoPrimari += "\n"
        moverNoPrimari +=1
      if entidad.nLetras < (len(elemento.nombre) + sumar):
        valor = (len(elemento.nombre) + sumar + 1) * 8.8
        a = entidad.nombreForma.GetWidth()
        b = entidad.nombreForma.GetHeight()
        a = valor
        entidad.nombreForma.SetSize(a, b)
        a = entidad.atributosForma.GetWidth()
        b = entidad.atributosForma.GetHeight()
        a = valor
        entidad.atributosForma.SetSize(a, b)
        entidad.nLetras = len(elemento.nombre)
    entidad.atributosForma.FormatText(dc, escribirPrimari, 0)
    entidad.atributosForma.FormatText(dc, escribirNoPrimari, 1)
    if mover != 0:
      mover = 1.00 / (mover + 1)
      moverPrimari = mover * moverPrimari
      moverNoPrimari = mover * moverNoPrimari
      mover = mover / 2
      if moverPrimari == 0:
        moverPrimari = 1.00 - moverNoPrimari
        entidad.atributosForma._regions[0].SetProportions(0, moverPrimari)
      else:
        if moverNoPrimari != 0:
          moverPrimari += mover
        entidad.atributosForma._regions[0].SetProportions(0, moverPrimari)
      entidad.atributosForma._regions[1].SetProportions(0, moverNoPrimari)
    else:
      entidad.atributosForma._regions[0].SetProportions(0, 0.50)
      entidad.atributosForma._regions[1].SetProportions(0, 0.50)

class Relacion(ogl.LineShape):

  def __init__(self, padre = "", hijo = "", tipoDeRelacion = "", cardinalidad = 0, cardinalidadExacta = 0):
    ogl.LineShape.__init__(self)
    self.entidadPadre = ""
    self.entidadHija = ""
    self.atributosHeredados = []
    self.tipoRelacion = tipoDeRelacion
    self.cadinalidad = cardinalidad
    self.cardinalidadExacta = cardinalidadExacta
    self.data = {}
    self.data["padre"] = padre
    self.data["hijo"] = hijo
    self.data["tipoDeRelacion"] = tipoDeRelacion
    self.data["cardinalidad"] = cardinalidad
    self.data["cardinalidadExacta"] = cardinalidadExacta
    """
    Cardinalidad:
      Cero, uno o mas = 0
      Uno o mas (P) = 1
      Cero o uno (Z) = 2
      Exactamente = 3
    """

  def DlgCrearRelacion(self, frame, canvas, entidades):
    nombreEntidades = []
    for entidad in entidades:
      nombreEntidades.append(entidad.nombre)
    self.data["nombreEntidades"] = nombreEntidades
    dlg = Dialogos(frame, frame.Idioma("Relationship"))
    dlg.Relacion(self.data)
    if dlg.ShowModal() == wx.ID_OK:
      entidadPadre = Entidad()
      entidadPadre.nombre = self.data["padre"]
      entidadHija = Entidad()
      entidadHija.nombre = self.data["hijo"]
      self.cadinalidad = self.data["cardinalidad"]
      self.cardinalidadExacta = self.data["cardinalidadExacta"]
      self.CrearRelacion(frame, canvas, entidadPadre, entidadHija, self.data["tipoDeRelacion"], entidades, self.data["cardinalidad"], self.data["cardinalidadExacta"])
      frame.GetActiveChild().contadorRelacion += 1

  def CrearRelacion(self, frame, canvas, entidadPadre, entidadHija, tipoRelacion, entidades, cardinalidad = 0, cardinalidadExacta = 0, id = -1):
    self.frame = frame
    self.SetCanvas(canvas)
    self.entidadPadre = entidadPadre
    self.entidadHija = entidadHija
    self.tipoRelacion = tipoRelacion
    self.cardinalidad = cardinalidad
    self.cardinalidadExacta = cardinalidadExacta
    self.data["cardinalidad"] = cardinalidad
    self.data["cardinalidadExacta"] = cardinalidadExacta
    if id == -1:
      self.id_relacion = frame.GetActiveChild().contadorRelacion
    else:
      self.id_relacion = id
    self.nombre = "rela" + str(self.id_relacion)
    if self.tipoRelacion == "Identificadora":
      #if 
      self.SetPen(wx.BLACK_PEN)
      self.SetBrush(wx.BLACK_BRUSH)
      self.AddArrow(ogl.ARROW_FILLED_CIRCLE, end=0)
      self.MakeLineControlPoints(2)
      for padre in entidades:
        if padre.nombre == self.entidadPadre.nombre:
          for hija in entidades:
            if hija.nombre == self.entidadHija.nombre:
              hija.entidadesPadres.append(padre)
              padre.entidadesHijas.append(hija)
              hija.relaciones.append(self)
              hija.nombreForma.AddLine(self, padre.nombreForma)
              hija.TipoDeEntidad(canvas)
              hija.HeredarAtributos(padre, 1)
              c = frame.GetActiveChild().conexion.cursor()
              c.execute("INSERT INTO relacion VALUES ( ?, ?, ?, ?)", (self.id_relacion, padre.id_entidad, hija.id_entidad, self.data["tipoDeRelacion"]))
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion:  " + str(self.id_relacion), "Crear Relacion")
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Padre:  " + str(padre.id_entidad), "Crear Relacion")
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Hija:  " + str(hija.id_entidad), "Crear Relacion")
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Tipo de Relacion:  " + self.data["tipoDeRelacion"], "Crear Relacion")
              c.close()
              frame.GetActiveChild().conexion.commit()
              self.tree = frame.GetActiveChild().tree.AppendItem(self.frame.GetActiveChild().treeRela, self.nombre, image = self.frame.GetActiveChild().imgRel, data = wx.TreeItemData(self))
    elif self.tipoRelacion == "No-Identificadora":
      self.SetPen(wx.Pen(wx.BLACK,1, wx.SHORT_DASH))#wx.DOT_DASH))#wx.LONG_DASH))#
      self.SetBrush(wx.BLACK_BRUSH)
      self.AddArrow(ogl.ARROW_FILLED_CIRCLE, end=0)
      self.MakeLineControlPoints(2)
      for padre in entidades:
        if padre.nombre == self.entidadPadre.nombre:
          for hija in entidades:
            if hija.nombre == self.entidadHija.nombre:
              hija.entidadesPadres.append(padre)
              padre.entidadesHijas.append(hija)
              hija.relaciones.append(self)
              hija.nombreForma.AddLine(self, padre.nombreForma)
              hija.TipoDeEntidad(canvas)
              hija.HeredarAtributos(padre)
              c = frame.GetActiveChild().conexion.cursor()
              c.execute("INSERT INTO relacion VALUES ( ?, ?, ?, ?)", (self.id_relacion, padre.id_entidad, hija.id_entidad, self.data["tipoDeRelacion"]))
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion:  " + str(self.id_relacion), "Crear Relacion")
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Padre:  " + str(padre.id_entidad), "Crear Relacion")
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Hija:  " + str(hija.id_entidad), "Crear Relacion")
              frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Tipo de Relacion:  " + self.data["tipoDeRelacion"], "Crear Relacion")
              c.close()
              frame.GetActiveChild().conexion.commit()
              self.tree = frame.GetActiveChild().tree.AppendItem(self.frame.GetActiveChild().treeRela, self.nombre, image = self.frame.GetActiveChild().imgRel, data = wx.TreeItemData(self))
    else:
      print "No existe desarrollada la relacion"
    self.evthandler = MyEvtHandler()
    self.evthandler.SetShape(self)
    self.evthandler.SetPreviousHandler(self.GetEventHandler())
    self.SetEventHandler(self.evthandler)
    canvas.AddShape(self)
    self.Show(1)
    region = ogl.ShapeRegion()
    self.AddRegion(region)
    self.OnCardinalidad()
    self._regions[1].SetPosition(0, 20)
    frame.GetActiveChild().relaciones.append(self)

  def OnCardinalidad(self):
    cardinalidad = ["", "P", "Z", str(self.cardinalidadExacta)]
    if self.frame.menuVerCard.IsChecked():
      self._regions[1].SetSize(12 * len(cardinalidad[self.cardinalidad]), 12)
      self.FormatText(wx.ClientDC(self.GetCanvas()), cardinalidad[self.cardinalidad], 1)
    else:
      self.FormatText(wx.ClientDC(self.GetCanvas()), "", 1)

  def DrawRegion(self, dc, region, x, y):
    """Format one region at this position."""
    if self.GetDisableLabel():
      return
    w, h = region.GetSize()
    # Get offset from x, y
    xx, yy = region.GetPosition()
    xp = xx + x
    yp = yy + y
    # First, clear a rectangle for the text IF there is any
    if len(region.GetFormattedText()):
      dc.SetPen(self.GetBackgroundPen())
      dc.SetBrush(self.GetBackgroundBrush())
      # Now draw the text
      if region.GetFont():
        dc.SetFont(region.GetFont())
        #Comentado para que solo se muestre una letra
        #dc.DrawRectangle(xp - w / 2.0, yp - h / 2.0, w, h)
        if self._pen:
          dc.SetPen(self._pen)
        dc.SetTextForeground(region.GetActualColourObject())
        self.DrawFormattedText(dc, region.GetFormattedText(), xp, yp, w, h, region.GetFormatMode())

  def DrawFormattedText(self, dc, text_list, xpos, ypos, width, height, formatMode):
    if formatMode & 1:
      xoffset = xpos
    else:
      xoffset = xpos - width / 2.0
    if formatMode & 2:
      yoffset = ypos
    else:
      yoffset = ypos - height / 2.0
    for line in text_list:
      dc.DrawText(line.GetText(), xoffset + line.GetX(), yoffset + line.GetY())

  def Select(self, select, dc = None):
    ogl.Shape.Select(self, select, dc)
    if select:
      for i in range(3):
        if self._regions[i]:
          if self._regions[i].GetText() == '':
            region = self._regions[i]
            if region._formattedText:
              w, h = region.GetSize()
              x, y = region.GetPosition()
              xx, yy = self.GetLabelPosition(i)
              if self._labelObjects[i]:
                self._labelObjects[i].Select(False)
                self._labelObjects[i].RemoveFromCanvas(self._canvas)
              self._labelObjects[i] = self.OnCreateLabelShape(self, region, w, h)
              self._labelObjects[i].AddToCanvas(self._canvas)
              self._labelObjects[i].Show(True)
              if dc:
                self._labelObjects[i].Move(dc, x + xx, y + yy)
              self._labelObjects[i].Select(True, dc)
    else:
      for i in range(3):
        if self._labelObjects[i]:
          self._labelObjects[i].Select(False, dc)
          self._labelObjects[i].Erase(dc)
          self._labelObjects[i].RemoveFromCanvas(self._canvas)
          self._labelObjects[i] = None

  def DlgModificarRelacion(self, relacion, frame, canvas, entidades):
    nombreEntidades = []
    for elemento in entidades:
      nombreEntidades.append(elemento.nombre)
    relacion.data["nombreEntidades"] = nombreEntidades
    dlg = Dialogos(frame, frame.Idioma("Relationship"))
    dlg.Relacion(relacion.data)
    if dlg.ShowModal() == wx.ID_OK:
      self.ModificarRelacion(relacion, frame, canvas, entidades)

  def ModificarRelacion(self, relacion, frame, canvas, entidades ):
    if relacion.data["tipoDeRelacion"] != relacion.tipoRelacion or relacion.data["padre"] != relacion.entidadPadre or relacion.data["hijo"] != relacion.entidadHija:
      if relacion.data["tipoDeRelacion"] == "Identificadora":
        newRelacion = RelacionIdentificadora()
        entidadPadre = Entidad()
        entidadPadre.nombre = relacion.data["padre"]
        entidadHija = Entidad()
        entidadHija.nombre = relacion.data["hijo"]
        self.EliminarRelacion(relacion, canvas, frame.GetActiveChild(), entidades)
        newRelacion.CrearRelacion(frame, canvas, entidadPadre, entidadHija, entidades, relacion.data["cardinalidad"], relacion.data["cardinalidadExacta"])
        frame.GetActiveChild().contadorRelacion += 1
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Entidad Padre:  " + entidadPadre.nombre, "Modificar Relacion")
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Entidad Hija:  " + entidadHija.nombre, "Modificar Relacion")
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Cardinalidad:  " + str(relacion.data["cardinalidad"]), "Modificar Relacion")
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Cardinalidad Exacta:  " + str(relacion.data["cardinalidadExacta"]), "Modificar Relacion")
      elif relacion.data["tipoDeRelacion"] == "No-Identificadora":
        newRelacion = RelacionNoIdentificadora()
        entidadPadre = Entidad()
        entidadPadre.nombre = relacion.data["padre"]
        entidadHija = Entidad()
        entidadHija.nombre = relacion.data["hijo"]
        self.EliminarRelacion(relacion, canvas, frame.GetActiveChild(), entidades)
        newRelacion.CrearRelacion(frame, canvas, entidadPadre, entidadHija, entidades, relacion.data["cardinalidad"], relacion.data["cardinalidadExacta"])
        frame.GetActiveChild().contadorRelacion += 1
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Entidad Padre:  " + entidadPadre.nombre, "Modificar Relacion")
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Entidad Hija:  " + entidadHija.nombre, "Modificar Relacion")
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Cardinalidad:  " + str(relacion.data["cardinalidad"]), "Modificar Relacion")
        frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Cardinalidad Exacta:  " + str(relacion.data["cardinalidadExacta"]), "Modificar Relacion")
      else:
        print "En desarrollo."

  def EliminarRelacion(self, relacion, canvas, frame, entidades):
    if relacion.Selected():
      dc = wx.ClientDC(canvas)
      relacion.Select(False, dc)
      canvas.Redraw(dc)
    for entidad in entidades:
      eliminar = []
      if entidad.nombre == relacion.entidadHija.nombre:
        for atributo in entidad.atributos:
          for atributoHeredado in relacion.atributosHeredados:
            if atributo.nombre ==  atributoHeredado.nombre and atributo.claveForanea == True:
              eliminar.append(atributo)
        for elemento in eliminar:
          ejecute = Atributo()
          ejecute.EliminarAtributo(canvas, entidad, elemento, relacion)
        entidad.relaciones.remove(relacion)
        entidad.TipoDeEntidad(canvas)
        for entidadPadre in entidad.entidadesPadres:
          if entidadPadre.nombre == relacion.entidadPadre.nombre:
            entidad.entidadesPadres.remove(entidadPadre)
      if entidad.nombre == relacion.entidadPadre.nombre:
        for entidadHija in entidad.entidadesHijas:
          if entidadHija.nombre == relacion.entidadHija.nombre:
            entidad.entidadesHijas.remove(entidadHija)
    relacion.Unlink()
    frame.relaciones.remove(relacion)
    frame.tree.Delete(relacion.tree)
    canvas.RemoveShape(relacion)
    canvas.Refresh()
    c = frame.conexion.cursor()
    c.execute("DELETE FROM relacion WHERE id = %s" % relacion.id_relacion)
    c.close()
    frame.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Relacion:  " + str(relacion.id_relacion), "Eliminar Relacion")
    frame.conexion.commit()

  def ComprobarRecursividad(self, entidades, entidadPadre, entidadHija, buscar = 0):
    if buscar:
      for padre in entidades:
        if padre.nombre == entidadPadre.nombre:
          for hija in entidades:
            if hija.nombre == entidadHija.nombre:
              entidadPadre = padre
              entidadHija = hija
    for padreEntidad in entidadHija.entidadesPadres:
      if padreEntidad.nombre == entidadPadre.nombre:
        return 1
      if self.ComprobarRecursividad(entidades, entidadPadre, padreEntidad):
        return 1
    return 0

  def GetTipoRelacion(self):
    return self.tipoRelacion

class RelacionIdentificadora(Relacion):

  def __init__(self):
    Relacion.__init__(self)
    self.tipoRelacion = "Identificadora"

  def CrearRelacion (self, frame, canvas, entidadPadre, entidadHija, entidades, cardinalidad = 0, cardinalidadExacta = 0):
    if entidadPadre.nombre == entidadHija.nombre:
      dial = wx.MessageDialog(frame, 'No se puede crear una Relacion Identificadora Recursiva.\nDesea crear una relacion No-Identificadora?', 'Alerta', style=wx.OK | wx.CANCEL, pos=wx.DefaultPosition)
      dial.ShowModal()
      ejecute = RelacionNoIdentificadora()
      ejecute.CrearRelacion(frame, canvas, entidadPadre, entidadHija, entidades, cardinalidad, cardinalidadExacta)
      return 0
    if self.ComprobarRecursividad(entidades, entidadHija, entidadPadre, buscar = 1):
      dial = wx.MessageDialog(frame, 'No se puede crear una Relacion Identificadora Recursiva.\nDesea crear una relacion No-Identificadora?', 'Alerta', style=wx.OK | wx.CANCEL, pos=wx.DefaultPosition)
      dial.ShowModal()
      ejecute = RelacionNoIdentificadora()
      ejecute.CrearRelacion(frame, canvas, entidadPadre, entidadHija, entidades, cardinalidad, cardinalidadExacta)
      return 0
    self.data["padre"] = entidadPadre.nombre
    self.data["hijo"] = entidadHija.nombre
    self.data["tipoDeRelacion"] = self.tipoRelacion
    self.data["cardinalidad"] = cardinalidad
    self.data["cardinalidadExacta"] = cardinalidadExacta
    self.frame = frame
    self.SetCanvas(canvas)
    self.id_relacion = frame.GetActiveChild().contadorRelacion
    self.nombre = "rela" + str(self.id_relacion)
    self.entidadPadre = entidadPadre
    self.entidadHija = entidadHija
    self.cardinalidad = cardinalidad
    self.cardinalidadExacta = cardinalidadExacta
    self.SetPen(wx.BLACK_PEN)
    self.SetBrush(wx.BLACK_BRUSH)
    self.AddArrow(ogl.ARROW_FILLED_CIRCLE, end=0)
    self.MakeLineControlPoints(2)
    for padre in entidades:
      if padre.nombre == self.entidadPadre.nombre:
        for hija in entidades:
          if hija.nombre == self.entidadHija.nombre:
            hija.entidadesPadres.append(padre)
            padre.entidadesHijas.append(hija)
            hija.relaciones.append(self)
            hija.nombreForma.AddLine(self, padre.nombreForma)
            hija.TipoDeEntidad(canvas)
            hija.HeredarAtributos(padre, 1)
            c = frame.GetActiveChild().conexion.cursor()
            c.execute("INSERT INTO relacion VALUES ( ?, ?, ?, ?)", (self.id_relacion, padre.id_entidad, hija.id_entidad, self.data["tipoDeRelacion"]))
            c.close()
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion:  " + str(self.id_relacion), "Crear Relacion")
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Padre:  " + str(padre.id_entidad), "Crear Relacion")
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Hija:  " + str(hija.id_entidad), "Crear Relacion")
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Tipo de Relacion:  " + self.data["tipoDeRelacion"], "Crear Relacion")
            frame.GetActiveChild().conexion.commit()
            self.tree = frame.GetActiveChild().tree.AppendItem(self.frame.GetActiveChild().treeRela, self.nombre, image = self.frame.GetActiveChild().imgRel, data = wx.TreeItemData(self))
    self.evthandler = MyEvtHandler()
    self.evthandler.SetShape(self)
    self.evthandler.SetPreviousHandler(self.GetEventHandler())
    self.SetEventHandler(self.evthandler)
    canvas.AddShape(self)
    self.Show(1)
    region = ogl.ShapeRegion()
    self.AddRegion(region)
    self.OnCardinalidad()
    self._regions[1].SetPosition(0, 20)
    frame.GetActiveChild().relaciones.append(self)

class RelacionNoIdentificadora(Relacion):

  def __init__(self):
    Relacion.__init__(self)
    self.tipoRelacion = "No-Identificadora"

  def CrearRelacion (self, frame, canvas, entidadPadre, entidadHija, entidades, cardinalidad = 0, cardinalidadExacta = 0):
    self.data["padre"] = entidadPadre.nombre
    self.data["hijo"] = entidadHija.nombre
    self.data["tipoDeRelacion"] = self.tipoRelacion
    self.data["cardinalidad"] = cardinalidad
    self.data["cardinalidadExacta"] = cardinalidadExacta
    self.frame = frame
    self.SetCanvas(canvas)
    self.id_relacion = frame.GetActiveChild().contadorRelacion
    self.nombre = "rela" + str(self.id_relacion)
    self.entidadPadre = entidadPadre
    self.entidadHija = entidadHija
    self.cardinalidad = cardinalidad
    self.cardinalidadExacta = cardinalidadExacta
    self.SetPen(wx.Pen(wx.BLACK,1, wx.SHORT_DASH))
    self.SetBrush(wx.BLACK_BRUSH)
    self.AddArrow(ogl.ARROW_FILLED_CIRCLE, end=0)
    self.MakeLineControlPoints(2)
    for padre in entidades:
      if padre.nombre == self.entidadPadre.nombre:
        for hija in entidades:
          if hija.nombre == self.entidadHija.nombre:
            hija.entidadesPadres.append(padre)
            padre.entidadesHijas.append(hija)
            hija.relaciones.append(self)
            hija.nombreForma.AddLine(self, padre.nombreForma)
            hija.TipoDeEntidad(canvas)
            hija.HeredarAtributos(padre)
            c = frame.GetActiveChild().conexion.cursor()
            c.execute("INSERT INTO relacion VALUES ( ?, ?, ?, ?)", (self.id_relacion, padre.id_entidad, hija.id_entidad, self.data["tipoDeRelacion"]))
            c.close()
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion:  " + str(self.id_relacion), "Crear Relacion")
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Padre:  " + str(padre.id_entidad), "Crear Relacion")
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Id Relacion Hija:  " + str(hija.id_entidad), "Crear Relacion")
            frame.GetActiveChild().log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion: " + "Tipo de Relacion:  " + self.data["tipoDeRelacion"], "Crear Relacion")
            frame.GetActiveChild().conexion.commit()
            self.tree = frame.GetActiveChild().tree.AppendItem(self.frame.GetActiveChild().treeRela, self.nombre, image = self.frame.GetActiveChild().imgRel, data = wx.TreeItemData(self))
    self.evthandler = MyEvtHandler()
    self.evthandler.SetShape(self)
    self.evthandler.SetPreviousHandler(self.GetEventHandler())
    self.SetEventHandler(self.evthandler)
    canvas.AddShape(self)
    self.Show(1)
    region = ogl.ShapeRegion()
    self.AddRegion(region)
    self.OnCardinalidad()
    self._regions[1].SetPosition(0, 20)
    frame.GetActiveChild().relaciones.append(self)

class MyEvtHandler(ogl.ShapeEvtHandler):
  # Overwrite the default event handler to implement some custom features.
  def __init__(self):
    ogl.ShapeEvtHandler.__init__(self)

  def OnLeftClick(self, x, y, keys = 0, attachment = 0):
    #The dragging is done here.
    shape = self.GetShape()
    canvas = shape.GetCanvas()
    dc = wx.ClientDC(canvas)
    canvas.PrepareDC(dc)
    if shape.Selected():
      shape.Select(False, dc)
      canvas.Redraw(dc)
    else:
      redraw = False
      shapeList = canvas.GetDiagram().GetShapeList()
      toUnselect = []
      for s in shapeList:
        if s.Selected():
          toUnselect.append(s)
      shape.Select(True, dc)
      if toUnselect:
        for s in toUnselect:
          s.Select(False, dc)
        canvas.Redraw(dc)
    if canvas.frame.relacion == 1:
      if canvas.frame.click == 0:
        canvas.frame.entidadPadre = shape
        canvas.frame.click = 1
        canvas.SetCursor(wx.CROSS_CURSOR)
      elif canvas.frame.click == 1:
        canvas.frame.entidadHija = shape
        canvas.frame.click = 0
        canvas.frame.relacion = 0
        ejecutar = RelacionIdentificadora()
        ejecutar.CrearRelacion(canvas.frame.entidadPadre.frame, canvas, canvas.frame.entidadPadre, canvas.frame.entidadHija, canvas.frame.entidades)
        canvas.frame.entidadPadre.frame.GetActiveChild().contadorRelacion += 1
        canvas.Refresh()
    elif canvas.frame.relacion == 2:
      if canvas.frame.click == 0:
        canvas.frame.entidadPadre = shape
        canvas.frame.click = 1
        canvas.SetCursor(wx.CROSS_CURSOR)
      elif canvas.frame.click == 1:
        canvas.frame.entidadHija = shape
        canvas.frame.click = 0
        canvas.frame.relacion = 0
        ejecutar = RelacionNoIdentificadora()
        ejecutar.CrearRelacion(canvas.frame.entidadPadre.frame, canvas, canvas.frame.entidadPadre, canvas.frame.entidadHija, canvas.frame.entidades)
        canvas.frame.entidadPadre.frame.GetActiveChild().contadorRelacion += 1
        canvas.Refresh()

  def OnRightClick(self, x, y, *dontcare):
    shape = self.GetShape()
    canvas = shape.GetCanvas()
    dc = wx.ClientDC(canvas)
    canvas.PrepareDC(dc)
    redraw = False
    shapeList = canvas.GetDiagram().GetShapeList()
    toUnselect = []
    for s in shapeList:
      if s.Selected():
        toUnselect.append(s)
    if toUnselect:
      for s in toUnselect:
        s.Select(False, dc)
    shape.Select(True, dc)
    canvas.Redraw(dc)
    frame = shape.frame
    if shape.GetClassName() == "TextShape":
      frame.PopupMenu(frame.menu_entidad)
    elif shape.GetClassName() == "DividedShape":
      frame.PopupMenu(frame.menu_atributo)
    elif shape.GetClassName() == "Relacion":
      frame.PopupMenu(frame.menu_relacion)
    elif shape.GetClassName() ==  "RelacionIdentificadora":
      frame.PopupMenu(frame.menu_relacionIdentificadora)
    elif shape.GetClassName() == "RelacionNoIdentificadora":
      frame.PopupMenu(frame.menu_relacionNoIdentificadora)