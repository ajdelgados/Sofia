#!/usr/bin/python
# -*- coding: windows-1252 -*-

import wxversion
wxversion.select('2.8')
import wx
import wx.lib.intctrl as intCtrl

from sql import *

class Dialogos(wx.Dialog):

  def __init__(self, frame, nombre):
    wx.Dialog.__init__(self, frame, -1, nombre)

  def Entidad(self, data):
    nombre_l = wx.StaticText(self, -1, "Nombre de la Entidad:")
    descripcion_l = wx.StaticText(self, -1, "Descripcion:")
    nombre_t = wx.TextCtrl(self, validator=DataXferValidator(data, "nombre"))
    descripcion_t = wx.TextCtrl(self, size= (200, 100), style = wx.TE_MULTILINE, validator=DataXferValidator(data, "descripcion"))
    okay = wx.Button(self, wx.ID_OK)
    okay.SetDefault()
    cancel = wx.Button(self, wx.ID_CANCEL)
    sizer = wx.BoxSizer(wx.VERTICAL)
    fgs = wx.FlexGridSizer(2, 2, 10, 10)
    fgs.Add(nombre_l, 0, wx.ALIGN_RIGHT)
    fgs.Add(nombre_t, 0, wx.EXPAND)
    fgs.Add(descripcion_l, 0, wx.ALIGN_RIGHT)
    fgs.Add(descripcion_t, 0, wx.EXPAND)
    fgs.AddGrowableCol(1)
    sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
    sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    btns = wx.StdDialogButtonSizer()
    btns.AddButton(okay)
    btns.AddButton(cancel)
    btns.Realize()
    sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
    self.SetSizer(sizer)
    sizer.Fit(self)

  def Atributo(self, data):
    self.data = data
    tipos = []
    for t in SQL().variablePostgreSQL:
      tipos.append(t[0])
    nombre_l = wx.StaticText(self, -1, "Nombre del Atributo:")
    nombre_c_l = wx.StaticText(self, -1, "Nombre de la Columna:")
    descripcion_l = wx.StaticText(self, -1, "Descripcion:")
    tipo_l = wx.StaticText(self, -1, "Tipo de dato:")
    longitud_l = wx.StaticText(self, -1, "Longitud:")
    nombre_t = wx.TextCtrl(self, validator=DataXferValidator(data, "nombreAtributo"))
    nombre_c_t = wx.TextCtrl(self, validator=DataXferValidator(data, "nombreColumna"))
    descripcion_t = wx.TextCtrl(self, size= (200, 100), style = wx.TE_MULTILINE, validator=DataXferValidator(data, "descripcion"))
    tipo_t = wx.Choice(self, -1, (85, 18), choices = tipos, validator=DataXferValidator(data, "tipoDeAtributo"))
    self.longitud_t = intCtrl.IntCtrl(self, validator=DataXferValidator(data, "longitud"))
    if SQL().ActivarLongitud(data["tipoDeAtributo"]) == False:
      self.longitud_t.Enable(False)
    self.Bind(wx.EVT_CHOICE, self.EnableTextCtrl, tipo_t)
    primario = wx.CheckBox(self, -1, "Clave Primaria", (35, 40), (150, 20), validator=DataXferValidator(data, "primario"))
    #autoIncremento = wx.CheckBox(self, -1, "Auto Incrementar", (35, 40), (150, 20), validator=DataXferValidator(data, "autoIncremento"))
    notNull = wx.CheckBox(self, -1, "No Nulo", (35, 40), (150, 20), validator=DataXferValidator(data, "notNull"))
    if data["foranea"] == True:
      tipo_t.Enable(False)
      self.longitud_t.Enable(False)
      primario.Enable(False)
      notNull.Enable(False)
    okay = wx.Button(self, wx.ID_OK)
    okay.SetDefault()
    cancel = wx.Button(self, wx.ID_CANCEL)
    sizer = wx.BoxSizer(wx.VERTICAL)
    fgs = wx.FlexGridSizer(2, 2, 10, 10)
    fgs.Add(nombre_l, 0, wx.ALIGN_RIGHT)
    fgs.Add(nombre_t, 0, wx.EXPAND)
    fgs.Add(nombre_c_l, 0, wx.ALIGN_RIGHT)
    fgs.Add(nombre_c_t, 0, wx.EXPAND)
    fgs.Add(descripcion_l, 0, wx.ALIGN_RIGHT)
    fgs.Add(descripcion_t, 0, wx.EXPAND)
    fgs.Add(tipo_l, 0, wx.ALIGN_RIGHT)
    fgs.Add(tipo_t, 0, wx.EXPAND)
    fgs.Add(longitud_l, 0, wx.ALIGN_RIGHT)
    fgs.Add(self.longitud_t, 0, wx.EXPAND)
    fgs.Add(primario, 0, wx.EXPAND)
    #fgs.Add(autoIncremento, 0, wx.EXPAND)
    fgs.Add(notNull, 0, wx.EXPAND)
    fgs.AddGrowableCol(1)
    sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
    sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    btns = wx.StdDialogButtonSizer()
    btns.AddButton(okay)
    btns.AddButton(cancel)
    btns.Realize()
    sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
    self.SetSizer(sizer)
    sizer.Fit(self)

  def EnableTextCtrl(self, event):
    tipo_t = event.GetEventObject()
    if SQL().ActivarLongitud(tipo_t.GetStringSelection()):
      self.longitud_t.Enable(True)
    else:
      self.longitud_t.SetValue(0)
      self.longitud_t.Enable(False)
      self.data["longitud"] = self.longitud_t.GetValue()

  def Relacion(self, data):
    self.data = data
    tiposDeRelacion = ["Identificadora", "No-Identificadora"]
    tipoDeRelacion_t = wx.StaticText(self, -1, "Tipo de Relación:")
    tipoDeRelacion = wx.ComboBox(self, -1, "default value", (15, 30), wx.DefaultSize, tiposDeRelacion, wx.CB_READONLY, validator=DataXferValidator(data, "tipoDeRelacion"))
    entidadPadre_t = wx.StaticText(self, -1, "Entidad Padre:")
    entidadPadre = wx.ComboBox(self, -1, "default value", (15, 30), wx.DefaultSize, data["nombreEntidades"], wx.CB_READONLY, validator=DataXferValidator(data, "padre"))
    entidadHija_t = wx.StaticText(self, -1, "Entidad Hija:")
    entidadHija = wx.ComboBox(self, -1, "default value", (15, 30), wx.DefaultSize, data["nombreEntidades"], wx.CB_READONLY, validator=DataXferValidator(data, "hijo"))
    cardinalidadBox = wx.StaticBox(self, -1, "Cardinalidad: ")
    cardinalidad = wx.StaticBoxSizer(cardinalidadBox, wx.HORIZONTAL)
    cardinalidadPanel = wx.Panel(self)
    cardinalidadPanel.data = data
    fgs = wx.FlexGridSizer(2, 2, 10, 10)
    cardinalidad_0 = wx.RadioButton(cardinalidadPanel, 0, "Cero, uno o mas", name="cardinalidad")
    cardinalidad_1 = wx.RadioButton(cardinalidadPanel, 1, "Uno o mas (P)", name="cardinalidad")
    cardinalidad_2 = wx.RadioButton(cardinalidadPanel, 2, "Cero o uno (Z)", name="cardinalidad")
    cardinalidad_3 = wx.RadioButton(cardinalidadPanel, 3, "Exactamente:", name="cardinalidad")
    #self.cardinalidadExacta = intCtrl.IntCtrl(self, -1, pos = (129, 193), size = (150, 25), validator=DataXferValidator(data, "cardinalidadExacta"))
    self.cardinalidadExacta = intCtrl.IntCtrl(self, -1, pos = (155, 230), size = (150, 25), validator=DataXferValidator(data, "cardinalidadExacta"))
    cardinalidadPanel.SetSizer(fgs)
    self.cardinalidadExacta.Enable(False)
    for radio in [cardinalidad_0, cardinalidad_1, cardinalidad_2, cardinalidad_3]:
      if data["cardinalidad"] == radio.GetId():
        radio.SetValue(True)
        if data["cardinalidad"] == 3:
          self.cardinalidadExacta.Enable(True)
      else:
        radio.SetValue(False)
    #cardinalidadNoExacta = wx.StaticText(self, -1, "                                ")
    cardinalidadNoExacta = wx.StaticText(self, -1, "                                        ")
    for elemento in [cardinalidad_0, cardinalidad_1, cardinalidad_2, cardinalidad_3]:
      self.Bind(wx.EVT_RADIOBUTTON, self.EnableTextCtrlRadio, elemento)
    fgs.Add(cardinalidad_0, 0, wx.ALIGN_LEFT)
    fgs.Add(cardinalidadNoExacta, 0, wx.ALIGN_LEFT)
    fgs.Add(cardinalidad_1, 0, wx.ALIGN_LEFT)
    fgs.Add(cardinalidadNoExacta, 0, wx.ALIGN_LEFT)
    fgs.Add(cardinalidad_2, 0, wx.ALIGN_LEFT)
    fgs.Add(cardinalidadNoExacta, 0, wx.ALIGN_LEFT)
    fgs.Add(cardinalidad_3, 0, wx.ALIGN_LEFT)
    fgs.AddGrowableCol(1)
    cardinalidad.Add(cardinalidadPanel, wx.EXPAND|wx.ALL)
    #relacionTipoBox = wx.StaticBox(self, -1, "Tipo de Relacion: ")
    #relacionTipo = wx.StaticBoxSizer(relacionTipoBox, wx.VERTICAL)
    #relacionPanel = wx.Panel(self)
    #fgs = wx.FlexGridSizer(2, 1, 10, 10)
    #relacionPanel.SetSizer(fgs)
    #relacionIdentificadora = wx.RadioButton(relacionPanel, -1, "Identificadora", name="relacionTipo")
    #relacionNoIdentificadora = wx.RadioButton(relacionPanel, -1, "No identificadora", name="relacionTipo")
    #fgs.Add(relacionIdentificadora, 0, wx.ALIGN_LEFT)
    #fgs.Add(relacionNoIdentificadora, 0, wx.ALIGN_LEFT)
    #fgs.AddGrowableCol(1)
    #relacionTipo.Add(relacionPanel)
    okay = wx.Button(self, wx.ID_OK)
    okay.SetDefault()
    cancel = wx.Button(self, wx.ID_CANCEL)
    sizer = wx.BoxSizer(wx.VERTICAL)
    #fgs = wx.FlexGridSizer(2, 4, 10, 10)
    fgs = wx.FlexGridSizer(2, 2, 10, 10)
    fgs.Add(tipoDeRelacion_t, 0, wx.ALIGN_RIGHT)
    fgs.Add(tipoDeRelacion, 0, wx.EXPAND)
    fgs.Add(entidadPadre_t, 0, wx.ALIGN_RIGHT)
    fgs.Add(entidadPadre, 0, wx.EXPAND)
    fgs.Add(entidadHija_t, 0 , wx.ALIGN_RIGHT)
    fgs.Add(entidadHija, 0 , wx.EXPAND)
    fgs.AddGrowableCol(1)
    sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
    fgs = wx.FlexGridSizer(2, 2, 10, 10)
    fgs.Add(cardinalidad, 0, wx.EXPAND|wx.ALL|wx.ALIGN_CENTER)
    #fgs.Add(relacionTipo, 0, wx.EXPAND|wx.ALL)
    fgs.AddGrowableCol(1)
    sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
    sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    btns = wx.StdDialogButtonSizer()
    btns.AddButton(okay)
    btns.AddButton(cancel)
    btns.Realize()
    sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
    self.SetSizer(sizer)
    sizer.Fit(self)

  def EnableTextCtrlRadio(self, event):
    self.data["cardinalidad"] = event.GetEventObject().GetId()
    if self.data["cardinalidad"] == 3:
      self.cardinalidadExacta.Enable(True)
    else:
      self.cardinalidadExacta.Enable(False)
      self.cardinalidadExacta.SetValue(0)
    self.data["cardinalidadExacta"] = self.cardinalidadExacta.GetValue()

  def ScriptSql(self, text):
    script_t = wx.StaticText(self, -1, "Script SQL:")
    script_l = wx.TextCtrl(self, -1, text, pos = (0, 0), size = (750, 400), style = wx.TE_MULTILINE|wx.TE_RICH2)
    script_l.SetEditable(False)
    okay = wx.Button(self, wx.ID_OK)
    okay.SetDefault()
    sizer = wx.BoxSizer(wx.VERTICAL)
    fgs = wx.FlexGridSizer(2, 1, 10, 10)
    fgs.Add(script_t, 0, wx.ALIGN_CENTER_HORIZONTAL)
    fgs.Add(script_l, 0, wx.ALIGN_CENTER_HORIZONTAL)
    fgs.AddGrowableCol(1)
    sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
    sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    btns = wx.StdDialogButtonSizer()
    btns.AddButton(okay)
    btns.Realize()
    sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
    self.SetSizer(sizer)
    sizer.Fit(self)
    self.MoveXY(100, 100)
  
  def VerLog(self, text):
    script_t = wx.StaticText(self, -1, "Eventos Registrados:")
    script_l = wx.TextCtrl(self, -1, text, pos = (0, 0), size = (750, 400), style = wx.TE_MULTILINE|wx.TE_RICH2)
    script_l.SetEditable(False)
    okay = wx.Button(self, wx.ID_OK)
    okay.SetDefault()
    sizer = wx.BoxSizer(wx.VERTICAL)
    fgs = wx.FlexGridSizer(2, 1, 10, 10)
    fgs.Add(script_t, 0, wx.ALIGN_CENTER_HORIZONTAL)
    fgs.Add(script_l, 0, wx.ALIGN_CENTER_HORIZONTAL)
    fgs.AddGrowableCol(1)
    sizer.Add(fgs, 0, wx.EXPAND|wx.ALL, 5)
    sizer.Add(wx.StaticLine(self), 0, wx.EXPAND|wx.ALL, 5)
    btns = wx.StdDialogButtonSizer()
    btns.AddButton(okay)
    btns.Realize()
    sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
    self.SetSizer(sizer)
    sizer.Fit(self)
    self.MoveXY(100, 100)
  
  def AboutBox(self):
    bmp = wx.Image("images/sofia.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    icon = wx.StaticBitmap(self, wx.ID_ANY, bmp)
    close = wx.Button(self, wx.ID_EXIT)
    self.Bind(wx.EVT_BUTTON, self.OnExit, close)

  def OnExit(self, evt):
    self.Close(True)

class DataXferValidator(wx.PyValidator):

  def __init__(self, data, key):
    wx.PyValidator.__init__(self)
    self.data = data
    self.key = key

  def Clone(self):
    return DataXferValidator(self.data, self.key)

  def Validate(self, win):
    return True

  def TransferToWindow(self):
    textCtrl = self.GetWindow()
    if textCtrl.GetClassName() == 'wxChoice':
      textCtrl.SetStringSelection(self.data.get(self.key))
    else:
      textCtrl.SetValue(self.data.get(self.key))
    return True

  def TransferFromWindow(self):
    textCtrl = self.GetWindow()
    if textCtrl.GetClassName() == 'wxChoice':
      self.data[self.key] = textCtrl.GetStringSelection()
    else:
      self.data[self.key] = textCtrl.GetValue()
    return True
