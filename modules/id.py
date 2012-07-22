#!/usr/bin/python
# -*- coding: windows-1252 -*-

import wxversion
wxversion.select('2.8')
import wx

language = {}
archivo = {}
archivoHelp = {}

TITULO = wx.NewId()
archivo[TITULO] = '..:: Sofia - Data Modeler CUC ::..'
archivoHelp[TITULO] = '..:: Sofia - Data Modeler CUC ::..'

menuBar = ['&File', '&View', 'Tool',  '&Help']

### Menu de Archivo ###

ID_CERRAR_APLICACION = wx.ID_EXIT
archivo[ID_CERRAR_APLICACION] = '&Quit'
archivoHelp[ID_CERRAR_APLICACION] = 'Exit the application'

ID_CREAR_MODELO = wx.ID_NEW
archivo[ID_CREAR_MODELO] = '&New Model'
archivoHelp[ID_CREAR_MODELO] = 'Creating a Model'

ID_ABRIR_MODELO = wx.ID_OPEN
archivo[ID_ABRIR_MODELO] = '&Open'
archivoHelp[ID_ABRIR_MODELO] = 'Open Model'

ID_GUARDAR_MODELO = wx.ID_SAVE
archivo[ID_GUARDAR_MODELO] = '&Save'
archivoHelp[ID_GUARDAR_MODELO] = 'Save Model'

ID_GUARDAR_COMO_MODELO = wx.ID_SAVEAS
archivo[ID_GUARDAR_COMO_MODELO] = 'Save as'
archivoHelp[ID_GUARDAR_COMO_MODELO] = 'Save model as...'

ID_EXPORTAR_MODELO = wx.NewId()
archivo[ID_EXPORTAR_MODELO] = 'Export Model'
archivoHelp[ID_EXPORTAR_MODELO] = 'Export Model'

### Menu Ver ###

ID_MENU_VER_REFRESCAR = wx.NewId()
archivo[ID_MENU_VER_REFRESCAR] = 'Refresh\tF5'
archivoHelp[ID_MENU_VER_REFRESCAR] = 'Refresh'

ID_MENU_VER_IDF1X = wx.NewId()
archivo[ID_MENU_VER_IDF1X] = 'IDEF1X Toolbar'
archivoHelp[ID_MENU_VER_IDF1X] = 'View palette helps IDEF1X KIT'

ID_MENU_VER_STANDARD = wx.NewId()
archivo[ID_MENU_VER_STANDARD] = 'Standard Toolbar'
archivoHelp[ID_MENU_VER_STANDARD] = 'Show palette Standard Application'

ID_MENU_VER_NAV = wx.NewId()
archivo[ID_MENU_VER_NAV] = 'Object Browser'
archivoHelp[ID_MENU_VER_NAV] = 'Show Object Browser'

ID_MENU_VER_CARD = wx.NewId()
archivo[ID_MENU_VER_CARD] = 'Cardinality'
archivoHelp[ID_MENU_VER_CARD] = 'Show Cardinality in Relationships'

ID_MENU_VER_BARRA_ESTADO = wx.NewId()
archivo[ID_MENU_VER_BARRA_ESTADO] = 'Status Bar'
archivoHelp[ID_MENU_VER_BARRA_ESTADO] = 'Show Cardinality in Relationships'

### Menu Ayuda ###

ID_MENU_HELP_LANGUAGE = wx.NewId()
archivo[ID_MENU_HELP_LANGUAGE] = 'Language'
archivoHelp[ID_MENU_HELP_LANGUAGE] = 'Language'

ID_MENU_HELP_us_US = wx.NewId()
language[ID_MENU_HELP_us_US] = ''
archivo[ID_MENU_HELP_us_US] = 'English'
archivoHelp[ID_MENU_HELP_us_US] = ''

ID_MENU_HELP_es_ES = wx.NewId()
language[ID_MENU_HELP_es_ES] = 'es_ES'
archivo[ID_MENU_HELP_es_ES] = 'Spanish'
archivoHelp[ID_MENU_HELP_es_ES] = ''

ID_MENU_HELP_fr_FR = wx.NewId()
language[ID_MENU_HELP_fr_FR] = 'fr_FR'

ID_MENU_HELP_AYUDA = wx.ID_HELP
archivo[ID_MENU_HELP_AYUDA] = '&Help'
archivoHelp[ID_MENU_HELP_AYUDA] = 'Help Sofia'

ID_MENU_HELP_LOG = wx.NewId()
archivo[ID_MENU_HELP_LOG] = 'View &Log'
archivoHelp[ID_MENU_HELP_LOG] = ''

ID_MENU_HELP_ACERCA_DE = wx.NewId()
archivo[ID_MENU_HELP_ACERCA_DE] = 'About'
archivoHelp[ID_MENU_HELP_ACERCA_DE] = 'About Sofia'

### Menu Herramienta ###

ID_PUNTERO_MOUSE = wx.NewId()
archivo[ID_PUNTERO_MOUSE] = 'Select'
archivoHelp[ID_PUNTERO_MOUSE] = 'Select Element'

ID_CREAR_ENTIDAD = wx.NewId()
archivo[ID_CREAR_ENTIDAD] = 'New Entity'
archivoHelp[ID_CREAR_ENTIDAD] = 'Create Entity'

ID_MODIFICAR_ENTIDAD = wx.NewId()
archivo[ID_MODIFICAR_ENTIDAD] = 'Edit Entity'
archivoHelp[ID_MODIFICAR_ENTIDAD] = 'Edit Entity'

ID_ELIMINAR_ENTIDAD = wx.NewId()
archivo[ID_ELIMINAR_ENTIDAD] = 'Delete Entity'
archivoHelp[ID_ELIMINAR_ENTIDAD] = 'Delete Entity'

ID_CREAR_ATRIBUTO = wx.NewId()
archivo[ID_CREAR_ATRIBUTO] = 'New Attribute'
archivoHelp[ID_CREAR_ATRIBUTO] = 'New Attribute'

ID_MODIFICAR_ATRIBUTO = wx.NewId()
archivo[ID_MODIFICAR_ATRIBUTO] = 'Edit Attribute'
archivoHelp[ID_MODIFICAR_ATRIBUTO] = 'Edit Attribute'

ID_ELIMINAR_ATRIBUTO = wx.NewId()
archivo[ID_ELIMINAR_ATRIBUTO] = 'Delete Attribute'
archivoHelp[ID_ELIMINAR_ATRIBUTO] = 'Delete Attribute'

ID_TREE_MODIFICAR_ATRIBUTO = wx.NewId()
archivo[ID_TREE_MODIFICAR_ATRIBUTO] = 'Edit Attribute'
archivoHelp[ID_TREE_MODIFICAR_ATRIBUTO] = 'Edit Attribute'

ID_TREE_ELIMINAR_ATRIBUTO = wx.NewId()
archivo[ID_TREE_ELIMINAR_ATRIBUTO] = 'Delete Attribute'
archivoHelp[ID_TREE_ELIMINAR_ATRIBUTO] = 'Delete Attribute'

ID_CREAR_RELACION = wx.NewId()
archivo[ID_CREAR_RELACION] = 'New Relationship'
archivoHelp[ID_CREAR_RELACION] = 'Create Relationship'

ID_RELACION_IDENTIF = wx.NewId()
archivo[ID_RELACION_IDENTIF] = 'New Identifying Relationship'
archivoHelp[ID_RELACION_IDENTIF] = 'Create Identifying Relationship'

ID_RELACION_NO_IDENTIF = wx.NewId()
archivo[ID_RELACION_NO_IDENTIF] = 'New No-Identifying Relationship'
archivoHelp[ID_RELACION_NO_IDENTIF] = 'Create No-Identifying Relationship'

ID_MODIFICAR_RELACION = wx.NewId()
archivo[ID_MODIFICAR_RELACION] = 'Edit Relationship'
archivoHelp[ID_MODIFICAR_RELACION] = 'Edit Relationship'

ID_ELIMINAR_RELACION = wx.NewId()
archivo[ID_ELIMINAR_RELACION] = 'Delete Relationship'
archivoHelp[ID_ELIMINAR_RELACION] = 'Delete Relationship'

ID_GENERAR_SCRIPT= wx.NewId()
archivo[ID_GENERAR_SCRIPT] = 'Gene&rate SQL Script'
archivoHelp[ID_GENERAR_SCRIPT] = 'Generate the SQL script for PostgreSQL'

#ID_GUARDAR_SCRIPT= wx.NewId()

ID_TREE_FRAME = wx.NewId()


#Dialogo de Modelo

ID_MODELO_CREAR_TEXT = wx.NewId()
archivo[ID_MODELO_CREAR_TEXT] = 'Model Name:'

ID_MODELO_CREAR_TITULO = wx.NewId()
archivo[ID_MODELO_CREAR_TITULO] = 'Create Model'

ID_MODELO_ABRIR_ARCHIVO = wx.NewId()
archivo[ID_MODELO_ABRIR_ARCHIVO] = 'File DBD (*.dbd)|*.dbd|All files (*.*)|*.*'

ID_MODELO_ABRIR_TITULO = wx.NewId()
archivo[ID_MODELO_ABRIR_TITULO] = 'Open Model'

ID_MODELO_GUARDAR_ARCHIVO = wx.NewId()
archivo[ID_MODELO_GUARDAR_ARCHIVO] = 'File DBD (*.dbd)|*.dbd'

ID_MODELO_EXPORTAR_TITULO = wx.NewId()
archivo[ID_MODELO_EXPORTAR_TITULO] = 'Save image as'

ID_MODELO_ABRIR_ERROR = wx.NewId()
archivo[ID_MODELO_ABRIR_ERROR] = 'File reading is wrong.'

ID_MODELO_ABRIR_ERROR_TITULO = wx.NewId()
archivo[ID_MODELO_ABRIR_ERROR_TITULO] = 'Error'

# Entidad

ENTIDAD_TITULO = wx.NewId()
archivo[ENTIDAD_TITULO] = 'Entity'

ENTIDAD_NOMBRE = wx.NewId()
archivo[ENTIDAD_NOMBRE] = 'Name Entity:'

ENTIDAD_DESCRIPCION = wx.NewId()
archivo[ENTIDAD_DESCRIPCION] = 'Description:'

#Atributo

ATRIBUTO_TITULO = wx.NewId()
archivo[ATRIBUTO_TITULO] = 'Attribute'

ATRIBUTO_NOMBRE = wx.NewId()
archivo[ATRIBUTO_NOMBRE] = 'Attribute Name:'

ATRIBUTO_COLUMNA = wx.NewId()
archivo[ATRIBUTO_COLUMNA] = 'Column Name:'

ATRIBUTO_DESCRIPCION = wx.NewId()
archivo[ATRIBUTO_DESCRIPCION] = 'Description:'

ATRIBUTO_TIPO_DATO = wx.NewId()
archivo[ATRIBUTO_TIPO_DATO] = 'Data type:'

ATRIBUTO_LONGITUD = wx.NewId()
archivo[ATRIBUTO_LONGITUD] = 'Length:'

ATRIBUTO_PRIMARY = wx.NewId()
archivo[ATRIBUTO_PRIMARY] = 'Primary Key'

ATRIBUTO_NO_NULO = wx.NewId()
archivo[ATRIBUTO_NO_NULO] = 'Not Null'

ATRIBUTO_ELIMINAR_ERROR = wx.NewId()
archivo[ATRIBUTO_ELIMINAR_ERROR] = '%s attribute can not be eliminated \nis Foreign Key!'
