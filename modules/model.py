#!/usr/bin/python
# -*- coding: windows-1252 -*-

import wxversion
wxversion.select('2.8')
import wx
import wx.lib.ogl as ogl

from id import *
from dialog import *
from graphic import *
from log import *
import config

import os
import codecs
import sqlite3
from xml.dom import minidom

def str2bool(string):
  return string == 'True'

class Modelo(wx.aui.AuiMDIChildFrame):

  def __init__(self, parent):
    wx.aui.AuiMDIChildFrame.__init__(self, parent, -1, "")
    self.parent = parent

  def CrearModelo(self, parent):
    dlg = wx.TextEntryDialog(parent, parent.Idioma(archivo[ID_MODELO_CREAR_TEXT]), parent.Idioma(archivo[ID_MODELO_CREAR_TITULO]), '')
    if dlg.ShowModal() == wx.ID_OK:
      self.nombre = dlg.GetValue()
      self.nombreArchivo = dlg.GetValue()
      self.log = Log(self)
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Modelo: " + self.nombreArchivo, "Crear Tablas temporales / Crear Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Modelo'", "Crear Tablas temporales del Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Entidad'", "Crear Tablas temporales del Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Atributo'", "Crear Tablas temporales del Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Relacion'", "Crear Tablas temporales del Modelo")
      self.SetTitle('%s *' % self.nombre)
      if not os.path.exists("%s/db" % config.GetDataDir()):
        os.makedirs("%s/db" % config.GetDataDir())
      self.conexion = sqlite3.connect(os.path.join("%s/db" % config.GetDataDir(), "%s.db" % self.nombre))
      c = self.conexion.cursor()
      try:
        c.execute("CREATE TABLE modelo (id NUMERIC, nombre TEXT, contEntidad NUMERIC, contAtributo NUMERIC, contRelacion NUMERIC)")
        c.execute("CREATE TABLE entidad (id INTEGER PRIMARY KEY, nombre TEXT, descripcion TEXT)")
        c.execute("""CREATE TABLE atributo (id INTEGER PRIMARY KEY, id_entidad NUMERIC,
                  nombre TEXT, nom_colum TEXT, descripcion TEXT, tipo_dato TEXT,
                  long_dato NUMERIC, cla_prima NUMERIC, cla_fore NUMERIC, atri_n_null NUMERIC)""")
        c.execute("""CREATE TABLE relacion (id INTEGER PRIMARY KEY, ent_padre NUMERIC,
                ent_hija NUMERIC, tipo TEXT);""")
      except:
        c.execute("DROP TABLE modelo")
        c.execute("DROP TABLE entidad")
        c.execute("DROP TABLE atributo")
        c.execute("DROP TABLE relacion")
        c.execute("CREATE TABLE modelo (id NUMERIC, nombre TEXT, contEntidad NUMERIC, contAtributo NUMERIC, contRelacion NUMERIC)")
        c.execute("CREATE TABLE entidad (id INTEGER PRIMARY KEY, nombre TEXT, descripcion TEXT)")
        c.execute("""CREATE TABLE atributo (id INTEGER PRIMARY KEY, id_entidad NUMERIC,
                  nombre TEXT, nom_colum TEXT, descripcion TEXT, tipo_dato TEXT,
                  long_dato NUMERIC, cla_prima NUMERIC, cla_fore NUMERIC, atri_n_null NUMERIC)""")
        c.execute("""CREATE TABLE relacion (id INTEGER PRIMARY KEY, ent_padre NUMERIC,
                ent_hija NUMERIC, tipo TEXT);""")
      c.close()
      self.log = Log(self)
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Modelo: " + self.nombreArchivo, "Crear Tablas temporales / Crear Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Modelo'", "Crear Tablas temporales del Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Entidad'", "Crear Tablas temporales del Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Atributo'", "Crear Tablas temporales del Modelo")
      self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Relacion'", "Crear Tablas temporales del Modelo")
      self.conexion.commit()
      ico = wx.Icon('images/mini_logo_cuc_trans.ico', wx.BITMAP_TYPE_ICO)
      self.SetIcon(ico)
      vbox = wx.BoxSizer(wx.VERTICAL)
      self._mgr = wx.aui.AuiManager(self)
      self.panel = wx.Panel(self, id=wx.ID_ANY, pos=(0, 0), size=(162, 162))
      self.canvas = OGLCanvas(self, self)
      self._mgr.AddPane(self.canvas, wx.aui.AuiPaneInfo().
                        Name("Lienzo").Caption(self.parent.Idioma("Canvas")).
                        Center().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))
      self._mgr.AddPane(self.panel, wx.aui.AuiPaneInfo().
                        Name("Nav").Caption(self.parent.Idioma("Object Browser")).
                        Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
      self.nav = self._mgr.GetPane("Nav")
      self.lienzo = self._mgr.GetPane("Lienzo")
      self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
      il = wx.ImageList(16,16)
      self.imgEntPa = il.Add(wx.Image('images/entidadMiniPa.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
      self.imgEnt = il.Add(wx.Image('images/entidadMini.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
      self.imgAtrPa = il.Add(wx.Image('images/atributoMiniPa.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
      self.imgAtr = il.Add(wx.Image('images/atributoMini.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
      self.imgRelPa = il.Add(wx.Image('images/relacionMiniPa.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
      self.imgRel = il.Add(wx.Image('images/relacionMini.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
      self.tree = wx.TreeCtrl(self.panel, ID_TREE_FRAME, wx.DefaultPosition, wx.DefaultSize, wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
      self.tree.AssignImageList(il)
      self.root = self.tree.AddRoot('Modelo')
      self.treeEnti = self.tree.AppendItem(self.root, 'Entidades', image = self.imgEntPa)
      self.treeRela = self.tree.AppendItem(self.root, 'Relaciones', image = self.imgRelPa)
      self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnSelChangedRight, id=ID_TREE_FRAME)
      self.tree.Bind(wx.EVT_TREE_ITEM_MIDDLE_CLICK, self.OnSelChangedRight, id=ID_TREE_FRAME)
      self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChangedLeft, id=ID_TREE_FRAME)
      self.panel.SetSizer(vbox)
      vbox.Add(self.tree, 1, wx.EXPAND)
      self._mgr.Update()
      self.Show()
      self.contadorEntidad = 0
      self.entidades = []
      self.contadorAtributo = 0
      self.contadorRelacion = 0
      self.relaciones = []
      self.relacion = 0
      self.click = 0
      c = self.conexion.cursor()
      c.execute("INSERT INTO modelo VALUES (1, '%s', 0, 0, 0)" % self.nombre)
      c.close()
      self.conexion.commit()
      self.time = wx.Timer(self)
      self.Bind(wx.EVT_TIMER, self.HiloGuardar, self.time)
      self.Bind(wx.EVT_CLOSE, self.Cerrar)
      self.time.Start(5000)
      
      if not os.path.exists("%s/temp" % config.GetDataDir()):
        os.makedirs("%s/temp" % config.GetDataDir())
      file = codecs.open(os.path.join("%s/temp" % config.GetDataDir(), "%s.dbd" % self.nombreArchivo), encoding='UTF-8', mode='w+')
      modelArchivo = minidom.Document()
      modelArchivoTotal = modelArchivo.createElement("sofia-model")
      modelo = modelArchivo.createElement("model")
      modelo.setAttribute("name", self.nombre)
      modelo.setAttribute("entityCount", str(self.contadorEntidad))
      modelo.setAttribute("attributeCount", str(self.contadorAtributo))
      modelo.setAttribute("relationshipCount", str(self.contadorRelacion))
      modelArchivoTotal.appendChild(modelo)
      modelArchivo.appendChild(modelArchivoTotal)
      textoArchivo = modelArchivo.toprettyxml(indent="  ", newl="\n")
      file.write(textoArchivo.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8" ?>'))
      file.close()
      self.file = os.path.join("%s/temp" % config.GetDataDir(), "%s.dbd" % self.nombreArchivo)
      
      parent.menuFile.Enable(ID_GUARDAR_MODELO, True)
      parent.menuFile.Enable(ID_GUARDAR_COMO_MODELO, True)
      parent.menuFile.Enable(ID_EXPORTAR_MODELO, True)
      parent.menuVer.Enable(ID_MENU_VER_REFRESCAR, True)
      parent.menuVer.Enable(ID_MENU_VER_NAV, True)
      parent.menuVer.Enable(ID_MENU_VER_CARD, True)
      parent.menuTool.Enable(ID_CREAR_ENTIDAD, True)
      parent.menuTool.Enable(ID_RELACION_IDENTIF, True)
      parent.menuTool.Enable(ID_RELACION_NO_IDENTIF, True)
      parent.menuTool.Enable(ID_GENERAR_SCRIPT, True)
      parent.menuHelp.Enable(ID_MENU_HELP_LOG, True)
      parent.toolBarStandard.EnableTool(ID_GUARDAR_MODELO, True)
      parent.toolBarIdef1x.EnableTool(ID_CREAR_ENTIDAD, True)
      parent.toolBarIdef1x.EnableTool(ID_RELACION_IDENTIF, True)
      parent.toolBarIdef1x.EnableTool(ID_RELACION_NO_IDENTIF, True)
      parent.toolBarStandard.EnableTool(ID_GENERAR_SCRIPT, True)
      self.num = 0
      #self.parent = parent
    else:
      self.num = 1
      dlg.Close(True)
  
  def GuardarModelo(self, forzar = 0):
    self.log = Log(self)
    self.log.ConstruirStringModelo(str(datetime.datetime.now()), self.nombreArchivo, " Guardar Modelo ")
    fileTemporal = self.file
    nombreArchivoTemporal = self.nombreArchivo
    if self.file == os.path.join("%s/temp" % config.GetDataDir(), "%s.dbd" % self.nombreArchivo) or forzar:
      tempFile = wx.FileDialog(self, message=self.parent.Idioma(archivoHelp[ID_GUARDAR_MODELO]), defaultDir=os.path.expanduser("~"), defaultFile=self.nombre, wildcard=archivo[ID_MODELO_GUARDAR_ARCHIVO], style=wx.FD_SAVE|wx.FD_OVERWRITE_PROMPT)
      if tempFile.ShowModal() == wx.ID_OK:
        fileTemporal = "%s.dbd" % tempFile.GetPath()
        nombreArchivoTemporal = tempFile.GetFilename()
    try:
      file = codecs.open(fileTemporal, encoding='UTF-8', mode = 'w+')
      #file = open(fileTemporal, 'w+')
      modelArchivo = minidom.Document()
      modelArchivoTotal = modelArchivo.createElement("sofia-model")
      modelo = modelArchivo.createElement("model")
      modelo.setAttribute("name", self.nombre)
      modelo.setAttribute("entityCount", str(self.contadorEntidad))
      modelo.setAttribute("attributeCount", str(self.contadorAtributo))
      modelo.setAttribute("relationshipCount", str(self.contadorRelacion))
      for entidad in self.entidades:
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad.Id: " + str(entidad.id_entidad), " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad.Nombre: " + entidad.nombre, " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad.Descripcion: " + entidad.descripcion, " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad.posX: " + str(entidad.GetX()), " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad.posY: " + str(entidad.GetY()), " Guardar Modelo ")             
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Entidad.Tipo: " + str(entidad.tipo), " Guardar Modelo ")      
        elementEntity = modelArchivo.createElement("entity")
        elementEntity.setAttribute("id", str(entidad.id_entidad))
        elementEntity.setAttribute("name", entidad.nombre)
        elementEntity.setAttribute("description", entidad.descripcion)
        elementEntity.setAttribute("posX", str(entidad.GetX()))
        elementEntity.setAttribute("posY", str(entidad.GetY()))
        elementEntity.setAttribute("type", str(entidad.tipo))
        for atributo in entidad.atributos:
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.Nombre: " + atributo.nombre, " Guardar Modelo ")
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.Nombre columna: " + atributo.nombreColumna, " Guardar Modelo ")
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.Clave primaria: " + str(atributo.clavePrimaria), " Guardar Modelo ")
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.No Nulo: " + str(atributo.notNull), " Guardar Modelo ")             
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.Descripcion: " + atributo.descripcion, " Guardar Modelo ")
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.Longitud: " + str(atributo.longitud), " Guardar Modelo ")
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.Id: " + str(atributo.id_atributo), " Guardar Modelo ")
          self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Atributo.Clave Foranea: " + str(atributo.claveForanea), " Guardar Modelo ")
          elementAttribute = modelArchivo.createElement("attribute")
          elementAttribute.setAttribute("name", atributo.nombre)
          elementAttribute.setAttribute("columnName", atributo.nombreColumna)
          elementAttribute.setAttribute("primary", str(atributo.clavePrimaria))
          elementAttribute.setAttribute("notNull", str(atributo.notNull))
          elementAttribute.setAttribute("dataType", atributo.tipo)
          elementAttribute.setAttribute("description", atributo.descripcion)
          elementAttribute.setAttribute("length", str(atributo.longitud))
          elementAttribute.setAttribute("id", str(atributo.id_atributo))
          elementAttribute.setAttribute("foreignKey", str(atributo.claveForanea))
          elementEntity.appendChild(elementAttribute)
        modelo.appendChild(elementEntity)
      for relacion in self.relaciones:
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Id: " + str(relacion.id_relacion), " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Entidad Padre: " + relacion.entidadPadre.nombre, " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Entidad Hija: " + relacion.entidadHija.nombre, " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Tipo: " + relacion.tipoRelacion, " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Nombre: " + relacion.nombre, " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Nombre Columna: " + relacion.nombre, " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Cardinalidad: " + str(relacion.cardinalidad), " Guardar Modelo ")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Relacion.Cardinalidad Exacta: " + str(relacion.cardinalidadExacta), " Guardar Modelo ")
        elementRelationship = modelArchivo.createElement("relationship")
        elementRelationship.setAttribute("id", str(relacion.id_relacion))
        elementRelationship.setAttribute("entityFather", relacion.entidadPadre.nombre)
        elementRelationship.setAttribute("entityChild", relacion.entidadHija.nombre)
        elementRelationship.setAttribute("type", relacion.tipoRelacion)
        elementRelationship.setAttribute("name", relacion.nombre)
        elementRelationship.setAttribute("nameColumn", relacion.nombre)
        elementRelationship.setAttribute("cardinality", str(relacion.cardinalidad))
        elementRelationship.setAttribute("cardinalityExactly", str(relacion.cardinalidadExacta))
        modelo.appendChild(elementRelationship)
      modelArchivoTotal.appendChild(modelo)
      modelArchivo.appendChild(modelArchivoTotal)
      textoArchivo = modelArchivo.toprettyxml(indent = '  ', newl = '\n')
      file.write(textoArchivo.replace('<?xml version="1.0" ?>', '<?xml version="1.0" encoding="UTF-8" ?>'))
      file.close()
      if not self.file == fileTemporal:
        os.remove(self.file)
        self.file = fileTemporal
        self.nombreArchivo = nombreArchivoTemporal
    except IOError, e:
      if e.errno == 13:
        dial = wx.MessageDialog(self, "Permiso denegado al guardar en el directorio.", 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
      else:
        dial = wx.MessageDialog(self, "Error al guardar el archivo.", 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
    except:
      dial = wx.MessageDialog(self, "Error al guardar el archivo.", 'Error', wx.OK | wx.ICON_ERROR)
      dial.ShowModal()
  
  def GetXMLTag(self, xmlFile, xmlTag):
    try:
      textoArchivo = codecs.open(xmlFile, encoding = 'UTF-8', mode = 'r')
      textoArchivo = textoArchivo.read()
      dom = minidom.parseString(textoArchivo.encode('UTF-8'))
      elements = dom.getElementsByTagName(xmlTag)
      if len(elements) != 0:
        return elements
      else:
        return [0]
    except IOError:
      dom = minidom.parseString(xmlFile)
      elements = dom.getElementsByTagName(xmlTag)
      if len(elements) != 0:
        return elements
      else:
        return [0]
    except:
      print xmlTag
      print 'El fichero no existe o está mal formado.'
      return [0]

  def AbrirModelo(self, parent, file, nameFile):
    try:
      model = self.GetXMLTag(file, 'model')[0]
      if model:
        self.nombre = model.getAttribute("name")
        self.nombreArchivo = nameFile
        self.file = file
        self.SetTitle('%s *' % self.nombre)
        self.log = Log(self)
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Modelo: " + self.nombreArchivo, "Crear Tablas temporales / Abrir Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Modelo'", "Crear Tablas temporales del Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Entidad'", "Crear Tablas temporales del Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Atributo'", "Crear Tablas temporales del Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Relacion'", "Crear Tablas temporales del Modelo")
        if not os.path.exists("%s/db" % config.GetDataDir()):
          os.makedirs("%s/db" % config.GetDataDir())
        self.conexion = sqlite3.connect(os.path.join("%s/db" % config.GetDataDir(), "%s.db" % self.nombre))
        c = self.conexion.cursor()
        try:
          c.execute("CREATE TABLE modelo (id NUMERIC, nombre TEXT, contEntidad NUMERIC, contAtributo NUMERIC, contRelacion NUMERIC)")
          c.execute("CREATE TABLE entidad (id INTEGER PRIMARY KEY, nombre TEXT, descripcion TEXT)")
          c.execute("""CREATE TABLE atributo (id INTEGER PRIMARY KEY, id_entidad NUMERIC,
                    nombre TEXT, nom_colum TEXT, descripcion TEXT, tipo_dato TEXT,
                    long_dato NUMERIC, cla_prima NUMERIC, cla_fore NUMERIC, atri_n_null NUMERIC)""")
          c.execute("""CREATE TABLE relacion (id INTEGER PRIMARY KEY, ent_padre NUMERIC,
                  ent_hija NUMERIC, tipo TEXT);""")
        except:
          c.execute("DROP TABLE modelo")
          c.execute("DROP TABLE entidad")
          c.execute("DROP TABLE atributo")
          c.execute("DROP TABLE relacion")
          c.execute("CREATE TABLE modelo (id NUMERIC, nombre TEXT, contEntidad NUMERIC, contAtributo NUMERIC, contRelacion NUMERIC)")
          c.execute("CREATE TABLE entidad (id INTEGER PRIMARY KEY, nombre TEXT, descripcion TEXT)")
          c.execute("""CREATE TABLE atributo (id INTEGER PRIMARY KEY, id_entidad NUMERIC,
                    nombre TEXT, nom_colum TEXT, descripcion TEXT, tipo_dato TEXT,
                    long_dato NUMERIC, cla_prima NUMERIC, cla_fore NUMERIC, atri_n_null NUMERIC)""")
          c.execute("""CREATE TABLE relacion (id INTEGER PRIMARY KEY, ent_padre NUMERIC,
                  ent_hija NUMERIC, tipo TEXT);""")        
        c.close()
        self.log = Log(self)
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Modelo: " + self.nombreArchivo, "Crear Tablas temporales / Crear Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Modelo'", "Crear Tablas temporales del Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Entidad'", "Crear Tablas temporales del Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Atributo'", "Crear Tablas temporales del Modelo")
        self.log.ConstruirStringModelo(str(datetime.datetime.now()), "'Tabla Relacion'", "Crear Tablas temporales del Modelo")
        self.conexion.commit()
        ico = wx.Icon('images/mini_logo_cuc_trans.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        vbox = wx.BoxSizer(wx.VERTICAL)
        self._mgr = wx.aui.AuiManager(self)
        self.panel = wx.Panel(self, id=wx.ID_ANY, pos=(0, 0), size=(162, 162))
        self.canvas = OGLCanvas(self, self)
        self._mgr.AddPane(self.canvas, wx.aui.AuiPaneInfo().
                          Name("Lienzo").Caption(self.parent.Idioma("Canvas")).
                          Center().Layer(1).Position(1).CloseButton(False).MaximizeButton(True))
        self._mgr.AddPane(self.panel, wx.aui.AuiPaneInfo().
                          Name("Nav").Caption(self.parent.Idioma("Object Browser")).
                          Left().Layer(1).Position(1).CloseButton(True).MaximizeButton(True))
        self.nav = self._mgr.GetPane("Nav")
        self.lienzo = self._mgr.GetPane("Lienzo")
        self.Bind(wx.aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
        il = wx.ImageList(16,16)
        self.imgEntPa = il.Add(wx.Image('images/entidadMiniPa.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imgEnt = il.Add(wx.Image('images/entidadMini.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imgAtrPa = il.Add(wx.Image('images/atributoMiniPa.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imgAtr = il.Add(wx.Image('images/atributoMini.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imgRelPa = il.Add(wx.Image('images/relacionMiniPa.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.imgRel = il.Add(wx.Image('images/relacionMini.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.tree = wx.TreeCtrl(self.panel, ID_TREE_FRAME, wx.DefaultPosition, wx.DefaultSize, wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        self.tree.AssignImageList(il)
        self.root = self.tree.AddRoot('Modelo')
        self.treeEnti = self.tree.AppendItem(self.root, 'Entidades', image = self.imgEntPa)
        self.treeRela = self.tree.AppendItem(self.root, 'Relaciones', image = self.imgRelPa)
        self.tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.OnSelChangedRight, id=ID_TREE_FRAME)
        self.tree.Bind(wx.EVT_TREE_ITEM_MIDDLE_CLICK, self.OnSelChangedRight, id=ID_TREE_FRAME)
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChangedLeft, id=ID_TREE_FRAME)
        self.panel.SetSizer(vbox)
        vbox.Add(self.tree, 1, wx.EXPAND)
        self._mgr.Update()
        self.Show()
        self.contadorEntidad = int(model.getAttribute("entityCount"))
        self.entidades = []
        self.contadorAtributo = int(model.getAttribute("attributeCount"))
        self.atributos = []
        entidades = self.GetXMLTag(file, 'entity')
        if entidades[0] != 0:
          for entidad in entidades:
            ejecute = Entidad(entidad.getAttribute("name"), entidad.getAttribute("description"), entidad.getAttribute("type"))
            ejecute.CrearEntidad(parent, self.canvas, int(entidad.getAttribute("id")), float(entidad.getAttribute("posX")), float(entidad.getAttribute("posY")))
            self.entidades.append(ejecute)
            atributos = self.GetXMLTag(entidad.toxml("UTF-8"), 'attribute')
            if atributos:
              for atributo in atributos:
                if atributo != 0:
                  if not str2bool(atributo.getAttribute("foreignKey")):
                    ejecuteAtributo = Atributo(
                      atributo.getAttribute("name"),
                      atributo.getAttribute("columnName"),
                      atributo.getAttribute("description"),
                      atributo.getAttribute("dataType"),
                      atributo.getAttribute("length"),
                      atributo.getAttribute("primary"),
                      atributo.getAttribute("notNull"),
                      atributo.getAttribute("foreignKey")
                      )
                    ejecuteAtributo.CrearAtributo(self.canvas, ejecute, int(atributo.getAttribute("id")))
        self.contadorRelacion = int(model.getAttribute("relationshipCount"))
        self.relaciones = []
        for relacion in self.GetXMLTag(file, 'relationship'):
          if relacion != 0:
            ejecutar = Relacion(
              relacion.getAttribute("entityFather"),
              relacion.getAttribute("entityChild"),
              relacion.getAttribute("type"))
            entidadPadre = Entidad()
            entidadPadre.nombre = ejecutar.data["padre"]
            entidadHija = Entidad()
            entidadHija.nombre = ejecutar.data["hijo"]
            ejecutar.CrearRelacion(
              parent,
              self.canvas,
              entidadPadre,
              entidadHija,
              relacion.getAttribute("type"),
              self.entidades,
              cardinalidad = int(relacion.getAttribute("cardinality")),
              cardinalidadExacta = int(relacion.getAttribute("cardinalityExactly")),
              id = relacion.getAttribute("id"),
              directo = 0)
        self.relacion = 0
        self.click = 0
        c = self.conexion.cursor()
        c.execute("INSERT INTO modelo VALUES (1, '%s', 0, 0, 0)" % self.nombre)
        c.close()
        self.conexion.commit()
        self.time = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.HiloGuardar, self.time)
        self.Bind(wx.EVT_CLOSE, self.Cerrar)
        self.time.Start(5000)
        parent.menuFile.Enable(ID_GUARDAR_MODELO, True)
        parent.menuFile.Enable(ID_GUARDAR_COMO_MODELO, True)
        parent.menuFile.Enable(ID_EXPORTAR_MODELO, True)
        parent.menuVer.Enable(ID_MENU_VER_REFRESCAR, True)
        parent.menuVer.Enable(ID_MENU_VER_NAV, True)
        parent.menuVer.Enable(ID_MENU_VER_CARD, True)
        parent.menuTool.Enable(ID_CREAR_ENTIDAD, True)
        parent.menuTool.Enable(ID_RELACION_IDENTIF, True)
        parent.menuTool.Enable(ID_RELACION_NO_IDENTIF, True)
        parent.menuTool.Enable(ID_GENERAR_SCRIPT, True)
        parent.menuHelp.Enable(ID_MENU_HELP_LOG, True)
        parent.toolBarStandard.EnableTool(ID_GUARDAR_MODELO, True)
        parent.toolBarIdef1x.EnableTool(ID_CREAR_ENTIDAD, True)
        parent.toolBarIdef1x.EnableTool(ID_RELACION_IDENTIF, True)
        parent.toolBarIdef1x.EnableTool(ID_RELACION_NO_IDENTIF, True)
        parent.toolBarStandard.EnableTool(ID_GENERAR_SCRIPT, True)
        self.num = 0
        self.parent = parent
        self.canvas.Refresh()
      else:
        self.num = 1
    except:
      self.num = 1

  def ExportarModelo(self):
    BITMAP_TYPE = {
      "bmp": wx.BITMAP_TYPE_BMP,      # Save a Windows bitmap file.
      "eps": False,
      "gif": wx.BITMAP_TYPE_GIF,      # Save a GIF file.
      "jpg": wx.BITMAP_TYPE_JPEG,     # Save a JPG file.
      "pcx": wx.BITMAP_TYPE_PCX,      # Save a PCX file.
      "png": wx.BITMAP_TYPE_PNM,      # Save a PNG file.
      "pnm": wx.BITMAP_TYPE_PNM,      # Save a PNM file.
      "tif": wx.BITMAP_TYPE_TIF,      # Save a TIF file.
      "xbm": wx.BITMAP_TYPE_XBM,      # Save an X bitmap file.
      "xpm": wx.BITMAP_TYPE_XPM      # Save an XPM bitmap file.
    }
    
    ARRAY_BITMAP_TYPE = [
      "bmp",
      "eps",
      "gif",
      "jpg",
      "pcx",
      "png",
      "pnm",
      "tif",
      "xbm",
      "xpm"
    ]
    
    fileTypes = BITMAP_TYPE.keys()
    fileTypes.sort()
    ext = "png"
    if ext in fileTypes:
      dlg1 = wx.FileDialog(self, message = self.parent.Idioma(archivo[ID_MODELO_EXPORTAR_TITULO]), defaultDir = os.path.expanduser("~"), defaultFile = self.nombre, wildcard = "|".join(["%s files (*.%s)|*.%s"%(t.upper(), t, t) for t in fileTypes]), style=wx.SAVE|wx.OVERWRITE_PROMPT)
      try:
        while 1:
          if dlg1.ShowModal() == wx.ID_OK:
            fileName = dlg1.GetPath()
            index = dlg1.GetFilterIndex()
            # Check for proper exension
            ext = ARRAY_BITMAP_TYPE[index]
            if ext not in fileTypes:
              dlg2 = wx.MessageDialog(self, 'File name extension\n'
                                      'must be one of %s'%(", ".join(fileTypes)),
                                      'File Name Error', wx.OK | wx.ICON_ERROR)
              try:
                dlg2.ShowModal()
              finally:
                dlg2.Destroy()
            else:
              break # now save file
          else: # exit without saving
            return False
      finally:
        dlg1.Destroy()
      tp = BITMAP_TYPE[ext]
      fileName = fileName + "." + ext
      # Save...
      w, h = self.canvas.GetVirtualSize()
      if tp:
        dc = wx.MemoryDC()
        bitmap = wx.EmptyBitmap(self.GetSize()[0], self.GetSize()[1])
        dc.SelectObject(bitmap)
        x, y = self.canvas.CalcScrolledPosition(self.canvas.GetViewStart())
        dc.SetClippingRegion(x, y, self.GetSize()[0], self.GetSize()[1])
        dc.SetBackground(wx.WHITE_BRUSH)
        dc.Clear()
        self.canvas.GetDiagram().Redraw(dc)
        
        """print self.canvas.GetViewStart()
        print self.canvas.GetScaleX()
        print self.canvas.GetScaleY()
        print self.canvas.GetVirtualSize()
        print self.canvas.CalcScrolledPosition(self.canvas.GetViewStart())"""
        
        bitmap.SaveFile(fileName, tp)
      else:
        #... as postscript
        printData   = wx.PrintData()
        printData.SetFilename(fileName)
        dc = wx.PostScriptDC(printData)
        if dc.Ok():
          dc.StartDoc('Salvado como Postscript')
          #doPrint(dc, self.canvas)
          maxX, maxY = self.GetSize()
          # Let's have at least 50 device units margin
          marginX = 50
          marginY = 50
          # Add the margin to the graphic size
          maxX = maxX + (2 * marginX)
          maxY = maxY + (2 * marginY)
          # Get the size of the DC in pixels
          (w, h) = dc.GetSizeTuple()
          # Calculate a suitable scaling factor
          scaleX = float(w) / maxX
          scaleY = float(h) / maxY
          # Use x or y scaling factor, whichever fits on the DC
          actualScale = min(scaleX, scaleY)
          # Calculate the position on the DC for centering the graphic
          posX = (w - (maxX * actualScale)) / 2.0
          posY = (h - (maxY * actualScale)) / 2.0
          # Set the scale and origin
          dc.SetUserScale(actualScale, actualScale)
          dc.SetDeviceOrigin(int(posX), int(posY))
          dc.DrawText("Drawn by SPE [http://pythonide.stani.be]", marginX/2, maxY-marginY)
          self.canvas.Redraw(dc)

  def OnSelChangedRight(self, event):
    frame = self.parent
    item =  event.GetItem()
    data = self.tree.GetItemData(item)
    if self.tree.GetItemText(event.GetItem()) == 'Entidades':
      frame.PopupMenu(frame.menu_tree_entidad)
      return
    if self.tree.GetItemText(event.GetItem()) == 'Atributos':
      shape = data.GetData().atributosForma
      self.SelectShape(shape)
      frame.PopupMenu(frame.menu_atributo)
      return
    if self.tree.GetItemText(event.GetItem()) == 'Relaciones':
      frame.PopupMenu(frame.menu_tree_relacion)
      return
    try:
      shape = data.GetData().entidad.atributosForma
      self.SelectShape(shape)
      frame.atributoAcc = data.GetData()
      frame.PopupMenu(frame.menu_tree_atributo)
      return
    except:
      pass
    try:
      if data.GetData().tipoRelacion:
        shape = data.GetData()
        self.SelectShape(shape)
        frame.PopupMenu(frame.menu_relacion)
        return
    except:
      pass
    for entidad in self.entidades:
      if self.tree.GetItemText(event.GetItem()) == entidad.nombre:
        frame.PopupMenu(frame.menu_entidad)
        return

  def OnSelChangedLeft(self, event):
    item =  event.GetItem()
    data = self.tree.GetItemData(item)
    shape = 0
    try:
      if self.tree.GetItemText(event.GetItem()) != 'Atributos':
        shape = data.GetData().nombreForma
    except:
      pass
    if (type(shape).__name__ == 'TextShape' or type(shape).__name__ == ''):
      self.SelectShape(shape)

  def HiloGuardar(self, evt):
    c = self.conexion.cursor()
    c.execute("UPDATE modelo SET contEntidad = ?, contAtributo = ?, contRelacion = ? WHERE nombre = ?", (self.contadorEntidad, self.contadorAtributo, self.contadorRelacion, self.nombre))
    c.close()
    self.conexion.commit()

  def SelectShape(self, shape):
    canvas = shape.GetCanvas()
    dc = wx.ClientDC(canvas)
    canvas.PrepareDC(dc)
    if shape.Selected():
      pass
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

  def Cerrar(self, evt):
    self.log = Log(self)
    self.log.ConstruirStringModelo(str(datetime.datetime.now()), "Modelo: " + self.nombreArchivo, "Cerrar Modelo")
    self.OnCloseWindow(evt)
    if self.GetMDIParentFrame().GetActiveChild() == None:
      self.parent.menuFile.Enable(ID_GUARDAR_MODELO, False)
      self.parent.menuFile.Enable(ID_GUARDAR_COMO_MODELO, False)
      self.parent.menuFile.Enable(ID_EXPORTAR_MODELO, False)
      self.parent.menuTool.Enable(ID_CREAR_ENTIDAD, False)
      self.parent.menuVer.Enable(ID_MENU_VER_REFRESCAR, False)
      self.parent.menuVer.Enable(ID_MENU_VER_NAV, False)
      self.parent.menuVer.Enable(ID_MENU_VER_CARD, False)
      self.parent.menuTool.Enable(ID_CREAR_ENTIDAD, False)
      self.parent.menuTool.Enable(ID_RELACION_IDENTIF, False)
      self.parent.menuTool.Enable(ID_RELACION_NO_IDENTIF, False)
      self.parent.menuTool.Enable(ID_GENERAR_SCRIPT, False)
      self.parent.menuHelp.Enable(ID_MENU_HELP_LOG, False)
      self.parent.toolBarStandard.EnableTool(ID_GUARDAR_MODELO, False)
      self.parent.toolBarIdef1x.EnableTool(ID_CREAR_ENTIDAD, False)
      self.parent.toolBarIdef1x.EnableTool(ID_RELACION_IDENTIF, False)
      self.parent.toolBarIdef1x.EnableTool(ID_RELACION_NO_IDENTIF, False)
      self.parent.toolBarStandard.EnableTool(ID_GENERAR_SCRIPT, False)

  def OnPaneClose(self, event):
    if event.GetPane().name == 'Nav':
      self.parent.NavVer('1')

def doPrint(dc,canvas):
  # One possible method of setting scaling factors...
  maxX, maxY = canvas.GetVirtualSize()
  # Let's have at least 50 device units margin
  marginX = 50
  marginY = 50
  # Add the margin to the graphic size
  maxX = maxX + (2 * marginX)
  maxY = maxY + (2 * marginY)
  # Get the size of the DC in pixels
  (w, h) = dc.GetSizeTuple()
  # Calculate a suitable scaling factor
  scaleX = float(w) / maxX
  scaleY = float(h) / maxY
  # Use x or y scaling factor, whichever fits on the DC
  actualScale = min(scaleX, scaleY)
  # Calculate the position on the DC for centering the graphic
  posX = (w - (maxX * actualScale)) / 2.0
  posY = (h - (maxY * actualScale)) / 2.0
  # Set the scale and origin
  dc.SetUserScale(actualScale, actualScale)
  dc.SetDeviceOrigin(int(posX), int(posY))
  canvas.Redraw(dc)
  dc.DrawText("Drawn by SPE [http://pythonide.stani.be]", marginX/2, maxY-marginY)
  
class OGLCanvas(ogl.ShapeCanvas):
  
  def __init__ (self, parent, frame):
   
    ogl.ShapeCanvas.__init__(self, parent)
    self.EnableScrolling(True, True)
    PAGE_WIDTH = 1000
    PAGE_HEIGHT = 1000
    self.SetScrollbars(100, 100, PAGE_WIDTH/20, PAGE_HEIGHT/20)
    self.frame = frame
    self.SetBackgroundColour("White")
    self.diagrama = ogl.Diagram()
    self.SetDiagram(self.diagrama)
    self.diagrama.SetCanvas(self)