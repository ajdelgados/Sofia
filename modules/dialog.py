#!/usr/bin/python
# -*- coding: windows-1252 -*-

import wxversion
wxversion.select('2.8')
import wx
import wx.lib.intctrl as intCtrl

from sql import *
from id import *

from decimal import *

class Dialogos(wx.Dialog):

  def __init__(self, frame, nombre):
    wx.Dialog.__init__(self, frame, -1, nombre)
    self.frame = frame

  def Entidad(self, data):
    if self.frame.GetClassName() == 'wxAuiMDIParentFrame':
      nombre_l = wx.StaticText(self, -1, self.frame.Idioma(archivo[ENTIDAD_NOMBRE]))
      descripcion_l = wx.StaticText(self, -1, self.frame.Idioma(archivo[ENTIDAD_DESCRIPCION]))
    else:
      nombre_l = wx.StaticText(self, -1, self.frame.parent.Idioma(archivo[ENTIDAD_NOMBRE]))
      descripcion_l = wx.StaticText(self, -1, self.frame.parent.Idioma(archivo[ENTIDAD_DESCRIPCION]))
    nombre_t = wx.TextCtrl(self, validator=DataXferValidator(data, "nombre", required = True))
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
    if self.frame.GetClassName() == 'wxAuiMDIParentFrame':
      nombre_l = wx.StaticText(self, -1, self.frame.Idioma(archivo[ATRIBUTO_NOMBRE]))
      nombre_c_l = wx.StaticText(self, -1, self.frame.Idioma(archivo[ATRIBUTO_COLUMNA]))
      descripcion_l = wx.StaticText(self, -1, self.frame.Idioma(archivo[ATRIBUTO_DESCRIPCION]))
      tipo_l = wx.StaticText(self, -1, self.frame.Idioma(archivo[ATRIBUTO_TIPO_DATO]))
      longitud_l = wx.StaticText(self, -1, self.frame.Idioma(archivo[ATRIBUTO_LONGITUD]))
      primario = wx.CheckBox(self, -1, self.frame.Idioma(archivo[ATRIBUTO_PRIMARY]), (35, 40), (150, 20), validator=DataXferValidator(data, "primario"))
      self.notNull = wx.CheckBox(self, -1, self.frame.Idioma(archivo[ATRIBUTO_NO_NULO]), (35, 40), (150, 20), validator=DataXferValidator(data, "notNull"))
    else:
      nombre_l = wx.StaticText(self, -1, self.frame.parent.Idioma(archivo[ATRIBUTO_NOMBRE]))
      nombre_c_l = wx.StaticText(self, -1, self.frame.parent.Idioma(archivo[ATRIBUTO_COLUMNA]))
      descripcion_l = wx.StaticText(self, -1, self.frame.parent.Idioma(archivo[ATRIBUTO_DESCRIPCION]))
      tipo_l = wx.StaticText(self, -1, self.frame.parent.Idioma(archivo[ATRIBUTO_TIPO_DATO]))
      longitud_l = wx.StaticText(self, -1, self.frame.parent.Idioma(archivo[ATRIBUTO_LONGITUD]))
      primario = wx.CheckBox(self, -1, self.frame.parent.Idioma(archivo[ATRIBUTO_PRIMARY]), (35, 40), (150, 20), validator=DataXferValidator(data, "primario"))
      self.notNull = wx.CheckBox(self, -1, self.frame.parent.Idioma(archivo[ATRIBUTO_NO_NULO]), (35, 40), (150, 20), validator=DataXferValidator(data, "notNull"))
    nombre_t = wx.TextCtrl(self, validator=DataXferValidator(data, "nombreAtributo", required = True))
    nombre_c_t = wx.TextCtrl(self, validator=DataXferValidator(data, "nombreColumna"))
    descripcion_t = wx.TextCtrl(self, size= (200, 100), style = wx.TE_MULTILINE, validator=DataXferValidator(data, "descripcion"))
    tipo_t = wx.Choice(self, -1, (85, 18), choices = tipos, validator=DataXferValidator(data, "tipoDeAtributo"))
    self.longitud_t = wx.TextCtrl(self, validator=DataXferValidator(data, "longitud", required = True, decimal = True))
    if SQL().ActivarLongitud(data["tipoDeAtributo"]) == False:
      self.longitud_t.Enable(False)
    self.Bind(wx.EVT_CHOICE, self.EnableTextCtrl, tipo_t)
    self.Bind(wx.EVT_CHECKBOX, self.EnableCheckBox, primario)
    #autoIncremento = wx.CheckBox(self, -1, "Auto Incrementar", (35, 40), (150, 20), validator=DataXferValidator(data, "autoIncremento"))
    if data["foranea"] == True:
      tipo_t.Enable(False)
      self.longitud_t.Enable(False)
      primario.Enable(False)
      self.notNull.Enable(False)
    if data["primario"] == True:
      self.notNull.Enable(False)
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
    fgs.Add(self.notNull, 0, wx.EXPAND)
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
      self.longitud_t.SetValue("0")
      self.longitud_t.Enable(False)
      self.data["longitud"] = self.longitud_t.GetValue()

  def EnableCheckBox(self, event):
    primario = event.GetEventObject()
    if primario.IsChecked() == False:
      self.notNull.Enable(True)
    else:
      self.notNull.SetValue(0)
      self.notNull.Enable(False)
      self.data["notNull"] = False

  def Relacion(self, data):
    self.data = data
    tiposDeRelacion = ["Identificadora", "No-Identificadora"]
    tipoDeRelacion = wx.ComboBox(self, -1, "default value", (15, 30), wx.DefaultSize, tiposDeRelacion, wx.CB_READONLY, validator=DataXferValidator(data, "tipoDeRelacion"))
    entidadPadre = wx.ComboBox(self, -1, "default value", (15, 30), wx.DefaultSize, data["nombreEntidades"], wx.CB_READONLY, validator=DataXferValidator(data, "padre"))
    entidadHija = wx.ComboBox(self, -1, "default value", (15, 30), wx.DefaultSize, data["nombreEntidades"], wx.CB_READONLY, validator=DataXferValidator(data, "hijo"))
    cardinalidadPanel = wx.Panel(self)
    cardinalidadPanel.data = data
    fgs = wx.FlexGridSizer(2, 2, 10, 10)
    if self.frame.GetClassName() == 'wxAuiMDIParentFrame':
      tipoDeRelacion_t = wx.StaticText(self, -1, self.frame.Idioma("Type of Relationship:"))
      entidadPadre_t = wx.StaticText(self, -1, self.frame.Idioma("Parent:"))
      entidadHija_t = wx.StaticText(self, -1, self.frame.Idioma("Child:"))
      cardinalidadBox = wx.StaticBox(self, -1, self.frame.Idioma("Cardinality:"))
      cardinalidad_0 = wx.RadioButton(cardinalidadPanel, 0, self.frame.Idioma("Zero, One o More"), name="cardinalidad")
      cardinalidad_1 = wx.RadioButton(cardinalidadPanel, 1, self.frame.Idioma("One o More (P)"), name="cardinalidad")
      cardinalidad_2 = wx.RadioButton(cardinalidadPanel, 2, self.frame.Idioma("Zero o One (Z)"), name="cardinalidad")
      cardinalidad_3 = wx.RadioButton(cardinalidadPanel, 3, self.frame.Idioma("Exactly:"), name="cardinalidad")
    else:
      tipoDeRelacion_t = wx.StaticText(self, -1, self.frame.parent.Idioma("Type of Relationship:"))
      entidadPadre_t = wx.StaticText(self, -1, self.frame.parent.Idioma("Parent Entity:"))
      entidadHija_t = wx.StaticText(self, -1, self.frame.parent.Idioma("Child:"))
      cardinalidadBox = wx.StaticBox(self, -1, self.frame.parent.Idioma("Cardinality:"))
      cardinalidad_0 = wx.RadioButton(cardinalidadPanel, 0, self.frame.parent.Idioma("Zero, One o More"), name="cardinalidad")
      cardinalidad_1 = wx.RadioButton(cardinalidadPanel, 1, self.frame.parent.Idioma("One o More (P)"), name="cardinalidad")
      cardinalidad_2 = wx.RadioButton(cardinalidadPanel, 2, self.frame.parent.Idioma("Zero o One (Z)"), name="cardinalidad")
      cardinalidad_3 = wx.RadioButton(cardinalidadPanel, 3, self.frame.parent.Idioma("Exactly:"), name="cardinalidad")
    #self.cardinalidadExacta = intCtrl.IntCtrl(self, -1, pos = (129, 193), size = (150, 25), validator=DataXferValidator(data, "cardinalidadExacta"))
    cardinalidad = wx.StaticBoxSizer(cardinalidadBox, wx.HORIZONTAL)
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
    save = wx.Button(self, wx.ID_CANCEL, label= "Guardar SQL", name="Guardar SQL")
    self.Bind(wx.EVT_BUTTON, self.GetParent().GuardarScriptSql, save)
    save.SetDefault()
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
    btns.AddButton(save)
    btns.Realize()
    sizer.Add(btns, 0, wx.EXPAND|wx.ALL, 5)
    self.SetSizer(sizer)
    sizer.Fit(self)
    self.MoveXY(100, 100)
  
  def Configuracion(self, data):
    tiposDeIdioma = [archivo[ID_MENU_HELP_us_US], archivo[ID_MENU_HELP_es_ES]]
    tipoDeRelacion = wx.ComboBox(self, -1, "", (15, 30), wx.DefaultSize, tiposDeIdioma, wx.CB_READONLY, validator=DataXferValidator(data, "idioma", comboBox = True, idCombox = data["idioma"], arrayId = language, arrayText = archivo))
    tipoDeRelacion_t = wx.StaticText(self, -1, self.frame.Idioma("Language:"))
    okay = wx.Button(self, wx.ID_OK)
    okay.SetDefault()
    cancel = wx.Button(self, wx.ID_CANCEL)
    sizer = wx.BoxSizer(wx.VERTICAL)
    fgs = wx.FlexGridSizer(2, 2, 10, 10)
    fgs.Add(tipoDeRelacion_t, 0, wx.ALIGN_RIGHT)
    fgs.Add(tipoDeRelacion, 0, wx.EXPAND)
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
  
  def __init__(self, data, key, required = False, decimal = False, comboBox = False, idCombox = -1, arrayId = -1, arrayText = -1):
    wx.PyValidator.__init__(self)
    self.data = data
    self.key = key
    self.required = required
    self.decimal = decimal
    self.comboBox = comboBox
    self.idCombox = idCombox
    self.arrayId = arrayId
    self.arrayText = arrayText
  
  def Clone(self):
    return DataXferValidator(self.data, self.key, self.required, self.decimal, self.comboBox, self.idCombox, self.arrayId, self.arrayText)
  
  def Validate(self, win):
    if(self.required):
      textCtrl = self.GetWindow()
      text = textCtrl.GetValue()
      if len(text) == 0:
        wx.MessageBox("Este campo debe contener algun texto!", "Error")
        textCtrl.SetFocus()
        textCtrl.Refresh()
        return False
    if(self.decimal):
      textCtrl = self.GetWindow()
      text = textCtrl.GetValue()
      try:
        Decimal(textCtrl.GetValue().replace(',', '.'))
      except:
        wx.MessageBox("Este campo debe contener un numero, las decimas se expresan en \",\"!", "Error")
        textCtrl.SetFocus()
        textCtrl.Refresh()
        return False
    return True
  
  def TransferToWindow(self):
    textCtrl = self.GetWindow()
    if textCtrl.GetClassName() == 'wxChoice':
      textCtrl.SetStringSelection(self.data.get(self.key))
    elif self.comboBox:
      textCtrl.SetValue(self.arrayText[self.data.get(self.key)])
    else:
      textCtrl.SetValue(self.data.get(self.key))
    return True
  
  def TransferFromWindow(self):
    textCtrl = self.GetWindow()
    if textCtrl.GetClassName() == 'wxChoice':
      self.data[self.key] = textCtrl.GetStringSelection()
    elif self.comboBox:
      for k, v in self.arrayText.iteritems():
        if v == textCtrl.GetValue():
          self.data[self.key] = k
    else:
      self.data[self.key] = textCtrl.GetValue()
    return True
