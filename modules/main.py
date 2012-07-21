#!/usr/bin/python
# -*- coding: windows-1252 -*-

import wxversion
wxversion.select('2.8')
import wx

import wx.aui
import sqlite3

from id import *
from model import *
from graphic import *
from sql import *

from xml.dom import minidom

class MainFrame(wx.aui.AuiMDIParentFrame):
  
  def __init__(self, app, posx, posy, sizex, sizey):
    self.app = app
#--Iniciar el padre con las posiciones y titulo del Frame--#
    wx.aui.AuiMDIParentFrame.__init__(self, None, -1, "..:: Sofia - Modelador de Datos del CUC ::..", pos = (posx, posy), size = (sizex, sizey))
#--Imbuir el logo del CUC en la caja de control de la ventana--#
    ico = wx.Icon('images/mini_logo_cuc_trans.ico', wx.BITMAP_TYPE_ICO)
    self.SetIcon(ico)
#--Inicializamos la libreria OGL de wxPython--#
    ogl.OGLInitialize()
#--MENU--#
#Menu de Archivo
    self.menuFile = wx.Menu()
    self.menuFile.Append(ID_CREAR_MODELO, "&Nuevo Modelo", "Crear un Modelo")
    self.menuFile.Append(ID_ABRIR_MODELO, "&Abrir", "Abrir Modelo")
    self.menuFile.AppendSeparator()
    self.menuFile.Append(ID_GUARDAR_MODELO, "&Guardar", "Guardar Modelo")
    self.menuFile.Enable(ID_GUARDAR_MODELO, False)
    self.menuFile.Append(ID_GUARDAR_COMO_MODELO, "Guardar como", "Guardar Modelo como...")
    self.menuFile.Enable(ID_GUARDAR_COMO_MODELO, False)
    self.menuFile.Append(ID_EXPORTAR_MODELO, "Exportar Modelo", "Exportar Modelo")
    self.menuFile.Enable(ID_EXPORTAR_MODELO, False)
    self.menuFile.AppendSeparator()
    self.menuFile.Append(ID_CERRAR_APLICACION, "&Salir", "Salir de la Aplicación")
#Menu Ver
    self.menuVer = wx.Menu()
    self.refrescar = self.menuVer.Append(ID_MENU_VER_REFRESCAR, "Refrescar\tF5", "Refrescar")
    wx.EVT_MENU(self, ID_MENU_VER_REFRESCAR, self.Actualizar)
    self.menuVer.AppendSeparator()
    self.menuVerStandard = self.menuVer.Append(ID_MENU_VER_STANDARD, "Barra Estandar", "Mostrar paleta Estandar de aplicaciones", kind=wx.ITEM_CHECK)
    self.menuVerIdef1x = self.menuVer.Append(ID_MENU_VER_IDF1X, "Barra IDEF1X", "Mostrar paleta de ayuda IDEF1X KIT", kind=wx.ITEM_CHECK)
    self.menuVer.AppendSeparator()
    self.menuVerNav = self.menuVer.Append(ID_MENU_VER_NAV, "Navegador de Objeto", "Mostrar Navegador de Objeto", kind=wx.ITEM_CHECK)
    self.menuVerCard = self.menuVer.Append(ID_MENU_VER_CARD, "Cardinalidad", "Mostrar Cardinalidad en las Relaciones", kind=wx.ITEM_CHECK)
    self.menuVer.AppendSeparator()
    self.barraStatus = self.menuVer.Append(ID_MENU_VER_BARRA_ESTADO, 'Barra de Estado', "Mostrar Barra de Estado", kind=wx.ITEM_CHECK)
    if app.tool:
      idf1x, standard, navegador = eval(app.tool)
    else:
      idf1x, standard, navegador = (True, True, True)
      app.config.Write("tool", str( (True, True, True) ))
      app.config.Flush()
    self.menuVer.Check(ID_MENU_VER_STANDARD, standard)
    self.menuVer.Check(ID_MENU_VER_IDF1X, idf1x)
    self.menuVer.Check(ID_MENU_VER_BARRA_ESTADO, True)
    self.menuVer.Enable(ID_MENU_VER_REFRESCAR, False)
    self.menuVer.Enable(ID_MENU_VER_NAV, False)
    self.menuVer.Enable(ID_MENU_VER_CARD, False)
#Menu Herramientas
    self.menuTool = wx.Menu()
    self.menuTool.Append(ID_CREAR_ENTIDAD, "Nueva Entidad", "Crear una Entidad")
    self.menuTool.Enable(ID_CREAR_ENTIDAD, False)
    self.menuTool.AppendSeparator()
    self.menuTool.Append(ID_RELACION_IDENTIF, "Nueva Relación Identificadora", "Crear una Relación Identificadora")
    self.menuTool.Enable(ID_RELACION_IDENTIF, False)
    self.menuTool.Append(ID_RELACION_NO_IDENTIF, "Nueva Relación No Identificadora", "Crear una Relación No Identificadora")
    self.menuTool.Enable(ID_RELACION_NO_IDENTIF, False)
    self.menuTool.AppendSeparator()
    self.menuTool.Append(ID_GENERAR_SCRIPT, "Gene&rar Script SQL", "Genera el Script SQL del modelo para PostgreSQL")
    self.menuTool.Enable(ID_GENERAR_SCRIPT, False)
#Menu de Ayuda
    self.menuHelp = wx.Menu()
    self.menuHelp.Append(ID_MENU_HELP_AYUDA, "A&yuda")
    self.menuHelp.AppendSeparator()
    self.menuHelp.Append(ID_MENU_HELP_LOG, "Ver &Log")
    self.menuHelp.Enable(ID_MENU_HELP_LOG, False)
    self.menuHelp.AppendSeparator()
    self.menuHelp.Append(ID_MENU_HELP_ACERCA_DE, "Acerca de", "Acerca de Sofia")
#--Se adicionan los menues a la barra de menu--#
    self.menuBar = wx.MenuBar()
    self.menuBar.Append(self.menuFile, "&Archivo")
    self.menuBar.Append(self.menuVer, "&Ver")
    self.menuBar.Append(self.menuTool, "Herramientas")
    self.menuBar.Append(self.menuHelp, "A&yuda")
#--Se adiciona la barra de menu al frame--#
    self.SetMenuBar(self.menuBar)
    if not posx:
      self.Centre()
#--MENU ToolBar--#
    self._mgr = wx.aui.AuiManager()
    self._mgr.SetManagedWindow(self)
    self._perspectives = []
    self.n = 0
    self.x = 0
    
    self.toolBarIdef1x = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                                    wx.TB_FLAT | wx.TB_NODIVIDER)
    self.toolBarIdef1x.SetToolBitmapSize((8, 8))
    self.toolBarIdef1x.AddLabelTool(ID_PUNTERO_MOUSE, "Puntero", wx.Bitmap('images/Puntero.png'))
    self.toolBarIdef1x.AddLabelTool(ID_CREAR_ENTIDAD, "Entidad", wx.Bitmap('images/Entidad.png'))
    self.toolBarIdef1x.EnableTool(ID_CREAR_ENTIDAD, False)
    self.toolBarIdef1x.AddLabelTool(ID_RELACION_IDENTIF, "Relacion Identificadora", wx.Bitmap('images/R-identificadora.png'))
    self.toolBarIdef1x.EnableTool(ID_RELACION_IDENTIF, False)
    self.toolBarIdef1x.AddLabelTool(ID_RELACION_NO_IDENTIF, "Relacion No-Identificadora", wx.Bitmap('images/R-No-identificadora.png'))
    self.toolBarIdef1x.EnableTool(ID_RELACION_NO_IDENTIF, False)
    self.toolBarIdef1x.Realize()
    
    self._mgr.AddPane(self.toolBarIdef1x, wx.aui.AuiPaneInfo().
                      Name("toolBarIdef1x").Caption("IDEF1X-Kit").
                      ToolbarPane().Top().Row(1).
                      LeftDockable(True).RightDockable(True).CloseButton(False))

    if not idf1x:
      panelIdef1x = self._mgr.GetPane("toolBarIdef1x");
      panelIdef1x.Hide()
    
    self.toolBarStandard = wx.ToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                              wx.TB_FLAT | wx.TB_NODIVIDER)
    self.toolBarStandard.SetToolBitmapSize(wx.Size(32, 32))
    self.toolBarStandard.AddLabelTool(ID_CREAR_MODELO, "Nuevo", wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR))
    self.toolBarStandard.AddLabelTool(ID_ABRIR_MODELO, "Abrir", wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR))
    self.toolBarStandard.AddSeparator()
    self.toolBarStandard.AddLabelTool(ID_GUARDAR_MODELO, "Guardar", wx.ArtProvider.GetBitmap(wx.ART_FLOPPY, wx.ART_TOOLBAR))
    self.toolBarStandard.EnableTool(ID_GUARDAR_MODELO, False)
    self.toolBarStandard.AddSeparator()
    self.toolBarStandard.AddLabelTool(ID_GENERAR_SCRIPT, 'Script SQL', wx.Bitmap('images/2_sqlLogo.png') )
    self.toolBarStandard.EnableTool(ID_GENERAR_SCRIPT, False)
    self.toolBarStandard.Realize()
    
    self._mgr.AddPane(self.toolBarStandard, wx.aui.AuiPaneInfo().
                      Name("toolBarStandard").Caption("Estandar").
                      ToolbarPane().Top().Row(1).
                      LeftDockable(True).RightDockable(True).CloseButton(False))
    
    if not standard:
      panelStandard = self._mgr.GetPane("toolBarStandard");
      panelStandard.Hide()
    
    self._mgr.Update()
    
#--Barra de Estado--#
    self.statusBar = self.CreateStatusBar()
    self.SetStatusText("Listo!")
#--MENU click derecho en el Tree --#
    self.menu_tree_entidad = wx.Menu()
    self.menu_tree_entidad.Append(ID_CREAR_ENTIDAD, "Nueva")
    self.menu_tree_atributo = wx.Menu()
    self.menu_tree_atributo.Append(ID_TREE_MODIFICAR_ATRIBUTO, "Modificar")
    self.menu_tree_atributo.Append(ID_TREE_ELIMINAR_ATRIBUTO, "Eliminar")
    self.menu_tree_relacion = wx.Menu()
    self.menu_tree_relacion.Append(ID_CREAR_RELACION, "Nueva")
#--MENU click derecho en las formas--#
    self.menu_entidad = wx.Menu()
    self.menu_entidad.Append(ID_MODIFICAR_ENTIDAD, "Modificar")
    self.menu_entidad.Append(ID_ELIMINAR_ENTIDAD, "Eliminar")
    self.menu_atributo = wx.Menu()
    self.menu_atributo.Append(ID_CREAR_ATRIBUTO, "Agregar Atributo")
    self.menu_atributo.Append(ID_MODIFICAR_ATRIBUTO, "Modificar Atributo")
    self.menu_atributo.Append(ID_ELIMINAR_ATRIBUTO, "Eliminar Atributo")
    self.menu_relacion = wx.Menu()
    self.menu_relacion.Append(ID_MODIFICAR_RELACION, "Modificar Relación")
    self.menu_relacion.Append(ID_ELIMINAR_RELACION, "Eliminar Relación")
    self.menu_relacionIdentificadora = wx.Menu()
    self.menu_relacionIdentificadora.Append(ID_MODIFICAR_RELACION, "Modificar Relación")
    self.menu_relacionIdentificadora.Append(ID_ELIMINAR_RELACION, "Eliminar Relación")
    self.menu_relacionNoIdentificadora = wx.Menu()
    self.menu_relacionNoIdentificadora.Append(ID_MODIFICAR_RELACION, "Modificar Relación")
    self.menu_relacionNoIdentificadora.Append(ID_ELIMINAR_RELACION, "Eliminar Relación")
#--Eventos para todos los botones segun su ID--#
    self.Bind(wx.EVT_MENU, self.CrearModelo, id=ID_CREAR_MODELO)
    self.Bind(wx.EVT_MENU, self.GuardarModelo, id=ID_GUARDAR_MODELO)
    self.Bind(wx.EVT_MENU, self.GuardarModeloComo, id=ID_GUARDAR_COMO_MODELO)
    self.Bind(wx.EVT_MENU, self.AbrirModelo, id=ID_ABRIR_MODELO)
    self.Bind(wx.EVT_MENU, self.ExportarModelo, id=ID_EXPORTAR_MODELO)
    self.Bind(wx.EVT_MENU, self.OnExit, id=ID_CERRAR_APLICACION )
    self.Bind(wx.EVT_MENU, self.ToolBarIdef1xVer, id=ID_MENU_VER_IDF1X)
    self.Bind(wx.EVT_MENU, self.NavVer, id=ID_MENU_VER_NAV)
    self.Bind(wx.EVT_MENU, self.NavCard, id=ID_MENU_VER_CARD)
    self.Bind(wx.EVT_MENU, self.ToolBarStandardVer, id=ID_MENU_VER_STANDARD)
    self.Bind(wx.EVT_MENU, self.ToggleStatusBar, id=ID_MENU_VER_BARRA_ESTADO)
    self.Bind(wx.EVT_MENU, self.Puntero, id = ID_PUNTERO_MOUSE)
    self.Bind(wx.EVT_MENU, self.CrearEntidad, id = ID_CREAR_ENTIDAD)
    self.Bind(wx.EVT_MENU, self.ModificarEntidad, id= ID_MODIFICAR_ENTIDAD)
    self.Bind(wx.EVT_MENU, self.EliminarEntidad, id= ID_ELIMINAR_ENTIDAD)
    self.Bind(wx.EVT_MENU, self.CrearAtributo, id = ID_CREAR_ATRIBUTO)
    self.Bind(wx.EVT_MENU, self.ModificarAtributo, id = ID_MODIFICAR_ATRIBUTO)
    self.Bind(wx.EVT_MENU, self.EliminarAtributo, id = ID_ELIMINAR_ATRIBUTO)
    self.Bind(wx.EVT_MENU, self.TreeModificarAtributo, id = ID_TREE_MODIFICAR_ATRIBUTO)
    self.Bind(wx.EVT_MENU, self.TreeEliminarAtributo, id = ID_TREE_ELIMINAR_ATRIBUTO)
    self.Bind(wx.EVT_MENU, self.CrearRelacion, id = ID_CREAR_RELACION)
    self.Bind(wx.EVT_MENU, self.RelacionIdentificadora, id = ID_RELACION_IDENTIF)
    self.Bind(wx.EVT_MENU, self.RelacionNoIdentificadora, id = ID_RELACION_NO_IDENTIF)
    self.Bind(wx.EVT_MENU, self.ModificarRelacion, id = ID_MODIFICAR_RELACION)
    self.Bind(wx.EVT_MENU, self.EliminarRelacion, id = ID_ELIMINAR_RELACION)
    self.Bind(wx.EVT_MENU, self.GenerarScriptSql, id = ID_GENERAR_SCRIPT)
    self.Bind(wx.EVT_MENU, self.VerLog, id=ID_MENU_HELP_LOG )
    self.Bind(wx.EVT_MENU, self.OnAboutBox, id=ID_MENU_HELP_ACERCA_DE )
    
#--Hilo para verificar y guardar la posicion del Frame--#
    self.time = wx.Timer(self)
    self.Bind(wx.EVT_TIMER, app.SaveConfig, self.time)
    self.time.Start(5000)
  
  def CrearModelo(self, evt):
    ejecute = Modelo(self)
    ejecute.CrearModelo(self)
    if ejecute.num == 1:
      ejecute.Close(True)

  def GuardarModelo(self, evt):
    self.GetActiveChild().GuardarModelo()

  def GuardarModeloComo(self, evt):
    self.GetActiveChild().GuardarModelo(1)

  def AbrirModelo(self, evt):
    file = wx.FileDialog(self, message="Abrir Modelo", defaultDir=os.path.expanduser("~"), wildcard="Archivos DBD (*.dbd)|*.dbd|Todos los archivos (*.*)|*.*", style=0)
    if file.ShowModal() == wx.ID_OK:
      ejecute = Modelo(self)
      ejecute.AbrirModelo(self, file.GetPath(), file.GetFilename())
      if ejecute.num == 1:
        dial = wx.MessageDialog(self, "Archivo de lectura se encuentra erroneo.", 'Error', wx.OK | wx.ICON_ERROR)
        dial.ShowModal()
        ejecute.Close(True)

  def AbrirModeloDirecto(self, file):
    ejecute = Modelo(self)
    ejecute.AbrirModelo(self, file.strip(), "ver")
    if ejecute.num == 1:
      dial = wx.MessageDialog(self, "Archivo de lectura se encuentra erroneo.", 'Error', wx.OK | wx.ICON_ERROR)
      dial.ShowModal()
      ejecute.Close(True)
  
  def ExportarModelo(self, evt):
    self.GetActiveChild().ExportarModelo()
  
  #--Permite salir de la aplicacion--#
  def OnExit(self, evt):
    self.Close(True)

  def Actualizar(self, evt):
    dc = wx.ClientDC(self.GetActiveChild().canvas)
    self.GetActiveChild().canvas.PrepareDC(dc)
    self.GetActiveChild().canvas.Redraw(dc)
    self.GetActiveChild().canvas.Refresh()
    self.Refresh()
  
  def ToolBarIdef1xVer(self, event):
    panelIdef1x = self._mgr.GetPane("toolBarIdef1x");
    if self.menuVerIdef1x.IsChecked():
      panelIdef1x.Show()
      mos = True
    else:
      panelIdef1x.Hide()
      mos = False
    self.app.config.Write("tool", str((mos, self.menuVerStandard.IsChecked(), self.menuVerNav.IsChecked())))
    self.app.config.Flush()
    self._mgr.Update()

  def NavVer(self, event):
    panelNav = self.GetActiveChild().nav;
    if self.menuVerNav.IsChecked() and not panelNav.IsShown():
      panelNav.Show()
      mos = True
    else:
      panelNav.Hide()
      mos = False
    self.menuVer.Check(ID_MENU_VER_NAV, mos)
    self.app.config.Write("tool", str((self.menuVerIdef1x.IsChecked(), self.menuVerStandard.IsChecked() , mos)))
    self.app.config.Flush()
    self.GetActiveChild()._mgr.Update()

  def NavCard(self, event):
    if self.menuVerCard.IsChecked():
      mos = True
    else:
      mos = False
    self.menuVer.Check(ID_MENU_VER_CARD, mos)
    for relacion in self.GetActiveChild().relaciones:
      relacion.OnCardinalidad()
    self.GetActiveChild().canvas.Refresh()

  def ToolBarStandardVer(self, event):
    panelStandard = self._mgr.GetPane("toolBarStandard");
    if self.menuVerStandard.IsChecked():
      panelStandard.Show()
      mos = True
    else:
      panelStandard.Hide()
      mos = False
    self.app.config.Write("tool", str((self.menuVerIdef1x.IsChecked(), mos, self.menuVerNav.IsChecked())))
    self.app.config.Flush()
    self._mgr.Update()

  def ToggleStatusBar(self, event):
    if self.barraStatus.IsChecked():
      self.statusBar.Show()
    else:
      self.statusBar.Hide()

  def CrearEntidad(self, evt):
    ejecute = Entidad()
    #validar = ejecute.CrearEntidad(self, self.GetActiveChild().canvas, self.GetActiveChild().contadorEntidad)
    dlg = Dialogos(self, "Entidad")
    dlg.Entidad(ejecute.data)
    if dlg.ShowModal() == wx.ID_OK:
      for elemento in self.GetActiveChild().entidades:
        if elemento.nombre == ejecute.data.get("nombre"):
          validar = ejecute.ValidarNombreEntidad(self.GetActiveChild().entidades)
          if validar == False:
            return 0
    else:
      return 0
    ejecute.CrearEntidad(self, self.GetActiveChild().canvas, self.GetActiveChild().contadorEntidad)
    self.GetActiveChild().contadorEntidad += 1
    self.GetActiveChild().entidades.append(ejecute)
    self.GetActiveChild().canvas.Refresh()

  def ModificarEntidad(self, evt):
    ejecute = Entidad()
    for elemento in self.GetActiveChild().entidades:
      if elemento.nombreForma.Selected():
        ejecute.editar = 1
        ejecute.elemento = elemento
    if ejecute.editar == 1:
      ejecute.ModificarEntidad(self.GetActiveChild().canvas, ejecute.elemento, self.GetActiveChild().entidades)
    """else:
      dlg = wx.TextEntryDialog(None, "cual entidad quiere modificar?", 'Modificar Entidad', '')
      if dlg.ShowModal() == wx.ID_OK:
        response = dlg.GetValue()
        for elemento in self.GetActiveChild().entidades:
          if elemento.nombre == response:
            ejecute.ModificarEntidad(self.GetActiveChild().canvas, elemento, self.GetActiveChild().entidades)"""
    self.GetActiveChild().canvas.Refresh()
    
  def EliminarEntidad(self, evt):
    ejecute = Entidad()
    for elemento in self.GetActiveChild().entidades:
      if elemento.nombreForma.Selected():
        ejecute.editar = 1
        ejecute.elemento = elemento
    if ejecute.editar == 1:
      respuesta = ejecute.EliminarEntidad(self.GetActiveChild().canvas, ejecute.elemento, self.GetActiveChild().entidades, self.GetActiveChild())
      if respuesta == 1:
        self.GetActiveChild().entidades.remove(ejecute.elemento)
    """else:
      dlg = wx.TextEntryDialog(None, "cual entidad quiere eliminar?", 'Eliminar Entidad', '')
      dlg.SetIcon=(icon)
      if dlg.ShowModal() == wx.ID_OK:
        response = dlg.GetValue()
        for elemento in self.GetActiveChild().entidades:
          if elemento.nombre == response:
            respuesta = ejecute.EliminarEntidad(self.GetActiveChild().canvas, elemento, self.GetActiveChild().entidades, self.GetActiveChild())
            if respuesta == 1:
              self.GetActiveChild().entidades.remove(elemento)"""
    self.GetActiveChild().canvas.Refresh()

  def CrearAtributo(self, evt):
    ejecute = Atributo()
    for elemento in self.GetActiveChild().entidades:
      if elemento.atributosForma.Selected():
        ejecute.editar = 1
        ejecute.elemento = elemento
    if ejecute.editar == 1:
      dlg = Dialogos(self.GetActiveChild().canvas.frame, "Atributo")
      dlg.Atributo(ejecute.data)
      if dlg.ShowModal() == wx.ID_OK:
        for elemento in ejecute.elemento.atributos:
          if elemento.nombre == ejecute.data.get("nombreAtributo"):
            validar = ejecute.ValidarNombreAtributo(self.GetActiveChild().canvas.frame, ejecute.elemento.atributos)
            if validar == False:
              return 0
      else:
        return 0
      ejecute.CrearAtributo(self.GetActiveChild().canvas, ejecute.elemento, self.GetActiveChild().contadorAtributo)
      self.GetActiveChild().contadorAtributo += 1
      for entidadHija in ejecute.elemento.entidadesHijas:
        entidadHija.HeredarAtributos(ejecute.elemento)
    """else:
      dlg = wx.TextEntryDialog(None, "cual entidad agregar un atributo?", 'Agregar Atributo', '')
      if dlg.ShowModal() == wx.ID_OK:
        response = dlg.GetValue()
        for elemento in self.GetActiveChild().entidades:
          if elemento.nombre == response:
            ejecute.CrearAtributo(self.GetActiveChild().canvas, elemento, self.GetActiveChild().contadorAtributo)"""
    self.GetActiveChild().canvas.Refresh()

  def ModificarAtributo(self, evt):
    ejecute = Atributo()
    for elemento in self.GetActiveChild().entidades:
      if elemento.atributosForma.Selected():
        ejecute.editar = 1
        ejecute.elemento = elemento
    if ejecute.editar == 1:
      ejecute.DlgModificarAtributo(self.GetActiveChild().canvas, ejecute.elemento)
    """else:
      dlg = wx.TextEntryDialog(None, "cuall entidad agregar un atributo?", 'Agregar Atributo', '')
      if dlg.ShowModal() == wx.ID_OK:
        response = dlg.GetValue()
        for elemento in self.GetActiveChild().entidades:
          if elemento.nombre == response:
            ejecute.ModificarAtributo(self.GetActiveChild().canvas, elemento)"""
    dc = wx.ClientDC(self.GetActiveChild().canvas)
    for elemento in self.GetActiveChild().entidades:
      ejecute.ModificarAtributosForma(dc, elemento)
    self.GetActiveChild().canvas.Refresh()

  def EliminarAtributo(self, evt):
    ejecute = Atributo()
    for elemento in self.GetActiveChild().entidades:
      if elemento.atributosForma.Selected():
        ejecute.editar = 1
        ejecute.elemento = elemento
    if ejecute.editar == 1:
      ejecute.DlgEliminarAtributo(self.GetActiveChild().canvas, ejecute.elemento)
    """else:
      dlg = wx.TextEntryDialog(None, "cual entidad remover un atributo?", 'Eliminar Atributo', '')
      if dlg.ShowModal() == wx.ID_OK:
        response = dlg.GetValue()
        for elemento in self.GetActiveChild().entidades:
          if elemento.nombre == response:
            ejecute.DlgEliminarAtributo(self.GetActiveChild().canvas, elemento)"""
    self.GetActiveChild().canvas.Refresh()

  def CrearRelacion(self, evt):
    ejecute = Relacion()
    ejecute.DlgCrearRelacion(self, self.GetActiveChild().canvas, self.GetActiveChild().entidades)
    self.GetActiveChild().contadorRelacion += 1
    self.GetActiveChild().canvas.Refresh()

  def TreeModificarAtributo(self, evt):
    ejecute = Atributo()
    ejecute.ModificarAtributo(self.GetActiveChild().canvas, self.atributoAcc.entidad, self.atributoAcc)
    self.GetActiveChild().canvas.Refresh()

  def TreeEliminarAtributo(self, evt):
    if self.atributoAcc.claveForanea == True:
      dial = wx.MessageDialog(self, "Atributo %s no se puede eliminar \nes Clave Foranea!" % self.atributoAcc.nombre, 'Error', wx.OK | wx.ICON_ERROR)
      dial.ShowModal()
      return
    dlg = wx.MessageDialog(self.GetActiveChild().canvas, 'Desea remover el atributo %s' % self.atributoAcc.nombre, 'Eliminar Atributo %s' % self.atributoAcc.nombre, wx.YES_NO | wx.ICON_QUESTION)
    if dlg.ShowModal() == wx.ID_YES:
      ejecute = Atributo()
      ejecute.EliminarAtributo(self.GetActiveChild().canvas, self.atributoAcc.entidad, self.atributoAcc)
    self.GetActiveChild().canvas.Refresh()

  def RelacionIdentificadora(self, evt):
    self.GetActiveChild().canvas.SetCursor(wx.CROSS_CURSOR)
    self.GetActiveChild().relacion = 1

  def RelacionNoIdentificadora(self, evt):
    self.GetActiveChild().canvas.SetCursor(wx.CROSS_CURSOR)
    self.GetActiveChild().relacion = 2

  def ModificarRelacion(self, evt):
    ejecute = Relacion()
    for elemento in self.GetActiveChild().relaciones:
      if elemento.Selected():
        ejecute.DlgModificarRelacion(elemento, self, self.GetActiveChild().canvas, self.GetActiveChild().entidades)

  def EliminarRelacion(self, evt):
    ejecute = Relacion()
    for elemento in self.GetActiveChild().relaciones:
      if elemento.Selected():
        ejecute.EliminarRelacion(elemento, self.GetActiveChild().canvas, self.GetActiveChild(), self.GetActiveChild().entidades)

  def GenerarScriptSql(self, evt):
    script = SQL().ScriptPostgreSQL(self.GetActiveChild())
    dlg = Dialogos(self, "Script SQL")
    dlg.ScriptSql(script)
    dlg.ShowModal()
  
  def VerLog(self, event):
    dlg = Dialogos(self, "Eventos")
    dlg.VerLog(self.GetActiveChild().log.VerEventos())
    dlg.ShowModal()
  
#--Permite desplegar el cuadro de About--#
  def OnAboutBox(self, event):
    description = """Sofia es una herramienta desarrollada con el lenguaje de programación Python para la modelación de datos, genera el Script SQL para PostgreSQL en esta versión. Es un proyecto de Investigación y Desarrollo del Centro de Investigación en Informatica Aplicada (CENIIA) del Colegio Universitario de Caracas. Creado y dirigido por el Prof. Alejandro Amaro."""
    licence = """Aplicación liberada bajo la licencia GPL, para el uso."""
    info = wx.AboutDialogInfo()
    info.SetIcon(wx.Icon("images/sofia.png", wx.BITMAP_TYPE_PNG))
    info.SetName('Sofia')
    info.SetVersion('0.0.7')
    info.SetDescription(description)
    info.SetCopyright('(C) 2011 Colegio Universitario de Caracas')
    info.SetWebSite('http://www.cuc.edu.ve')
    info.SetLicence(licence)
    info.AddDeveloper('Prof. Alejandro Amaro - Autor - Tutor')
    info.AddDeveloper("Estudiantes de Proyecto Socio-Tecnológico:")
    info.AddDeveloper('    Junio 2011 Mayo 2012 - Versión 0.0.7')
    info.AddDeveloper('        T.S.U. Arturo Delgado  ')
    info.AddDeveloper('        T.S.U. Maximo Gonzales ')
    info.AddDeveloper('        T.S.U. Alexis Canchica ')
    info.AddDeveloper('    Mayo 2010 Mayo 2011 - Versión 0.0.4')
    info.AddDeveloper('        Br. Arturo Delgado  ')
    info.AddDeveloper('        Br. Ruben Rosas     ')
    info.AddDeveloper('        Br. Carolina Machado')
    info.AddDeveloper('        Br. Erik Mejias     ')
    info.AddDeveloper('Estudiantes Tesistas:')
    info.AddDeveloper('    Abril 2009 Junio 2009 - Versión 0.0.1')
    info.AddDeveloper('        Br. Dorian Machado  ')
    info.AddDeveloper('        Br. Daglis Campos   ')
    info.AddDeveloper('        Br. Felix Rodriguez ')
    info.AddDocWriter('Estudiantes de Proyecto Socio-Tecnológico:')
    info.AddDocWriter('    Junio 2011 Mayo 2012 - Versión 0.0.7')
    info.AddDocWriter('        T.S.U. Arturo Delgado  ')
    info.AddDocWriter('        T.S.U. Maximo Gonzales ')
    info.AddDocWriter('        T.S.U. Alexis Canchica ')
    info.AddDocWriter('    Mayo 2010 Mayo 2011 - Versión 0.0.4')
    info.AddDocWriter('        Br. Arturo Delgado  ')
    info.AddDocWriter('        Br. Ruben Rosas     ')
    info.AddDocWriter('        Br. Carolina Machado')
    info.AddDocWriter('        Br. Erik Mejias     ')
    info.AddArtist('Alumnos del Colegio Universitario de Caracas')
    info.AddTranslator('Anonimo')
    wx.AboutBox(info)
    #dlg = Dialogos(self, "Script SQL")
    #dlg.AboutBox()
    #dlg.ShowModal()

  def Puntero(self, evt):
    self.GetActiveChild().canvas.SetCursor(wx.STANDARD_CURSOR)
    self.GetActiveChild().click = 0
    self.GetActiveChild().relacion = 0