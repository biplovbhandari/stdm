<<<<<<< HEAD
# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : column_editor
Description          : Editor to create/edit entity columns
Date                 : 24/January/2016
copyright            : (C) 2015 by UN-Habitat and implementing partners.
                       See the accompanying file CONTRIBUTORS.txt in the root
email                : stdm@unhabitat.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import collections
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from collections import OrderedDict

from ui_column_editor import Ui_ColumnEditor

from stdm.data.configuration.columns import BaseColumn
from stdm.data.configuration.entity_relation import EntityRelation

from varchar_property import VarcharProperty
from bigint_property import BigintProperty
from double_property import DoubleProperty
from date_property import DateProperty
from dtime_property import DTimeProperty
from geometry_property import GeometryProperty
from fk_property import FKProperty
from lookup_property import LookupProperty
from multi_select_property import MultiSelectProperty

from datetime import (
    date,
    datetime
)

class ColumnEditor(QDialog, Ui_ColumnEditor):
    """
    Form to add/edit entity columns
    """
    def __init__(self, parent, **kwargs):
        """
        :param parent: Owner of this dialog
        :type parent: QWidget
        :param kwargs: Keyword dictionary of the following params;
         column - Column you editting, None if its a new column
         entity - Entity you are adding the column
         profile - Current profile
        """
        QDialog.__init__(self, parent)
        self.form_parent = parent

        self.FK_EXCLUDE = [u'supporting_document', u'admin_spatial_unit_set']

        self.EX_TYPE_INFO =  ['SUPPORTING_DOCUMENT', 'SOCIAL_TENURE', 
                'ADMINISTRATIVE_SPATIAL_UNIT', 'ENTITY_SUPPORTING_DOCUMENT',
                'VALUE_LIST']

        self.setupUi(self)
        self.dtypes = {}

        self.column  = kwargs.get('column', None)
        self.entity  = kwargs.get('entity', None)
        self.profile = kwargs.get('profile', None)

        self.type_info = ''
        
        # dictionary to hold default attributes for each data type
        self.type_attribs = {}
        self.init_type_attribs()

        # dictionary to act as a work area for the form fields.
        self.form_fields = {}
        self.init_form_fields()

        self.fk_entities     = []
        self.lookup_entities = []

        # the current entity should not be part of the foreign key parent table, add it to the exclusion list
        self.FK_EXCLUDE.append(self.entity.short_name)

        self.cboDataType.currentIndexChanged.connect(self.change_data_type)

        #self.btnTableList.clicked.connect(self.lookupDialog)
        self.btnColProp.clicked.connect(self.data_type_property)

        self.type_names = \
                [str(name) for name in BaseColumn.types_by_display_name().keys()]

        self.init_controls()

    def init_controls(self):
        self.popuplate_type_cbo()

        name_regex = QtCore.QRegExp('^[a-z][a-z0-9_]*$')
        name_validator = QtGui.QRegExpValidator(name_regex)
        self.edtColName.setValidator(name_validator)

        if self.column:
            self.column_to_form(self.column)
            self.column_to_wa(self.column)

        self.edtColName.setFocus()

    def column_to_form(self, column):
        """
        Initialize form controls with column data when editting a column.
        :param column: Column to edit
        :type column: BaseColumn
        """
        self.edtColName.setText(column.name)
        self.edtColDesc.setText(column.description)
        self.edtUserTip.setText(column.user_tip)
        self.cbMandt.setCheckState(self.bool_to_check(column.mandatory))
        self.cbSearch.setCheckState(self.bool_to_check(column.searchable))
        self.cbUnique.setCheckState(self.bool_to_check(column.unique))
        self.cbIndex.setCheckState(self.bool_to_check(column.index))

        self.cboDataType.setCurrentIndex( \
                self.cboDataType.findText(column.display_name()))

    def column_to_wa(self, column):
        """
        Initialize 'work area' form_fields with column data.
        Used when editing a column
        :param column: Column to edit
        :type column: BaseColumn
        """
        self.form_fields['colname'] = column.name
        self.form_fields['value']  = None
        self.form_fields['mandt']  = column.mandatory
        self.form_fields['search'] = column.searchable
        self.form_fields['unique'] = column.unique
        self.form_fields['index']  = column.index

        if hasattr(column, 'minimum'):
            self.form_fields['minimum'] = column.minimum
            self.form_fields['maximum'] = column.maximum

        if hasattr(column, 'srid'):
            self.form_fields['srid'] = column.srid
            self.form_fields['geom_type'] = column.geom_type

        if hasattr(column, 'entity_relation'):
            self.form_fields['entity_relation'] = column.entity_relation

        if hasattr(column, 'association'):
            self.form_fields['first_parent'] = column.association.first_parent
            self.form_fields['second_parent'] = column.association.second_parent

    def bool_to_check(self, state):
        """
        Converts a boolean to a Qt checkstate.
        :param state: True/False
        :type state: boolean
        :rtype: Qt.CheckState
        """
        if state:
            return Qt.Checked
        else:
            return Qt.Unchecked

    def init_form_fields(self):
        """
        Initializes work area 'form_fields' dictionary with default values.
        Used when creating a new column.
        """
        self.form_fields['colname'] = ''
        self.form_fields['value']  = None
        self.form_fields['mandt']  = False
        self.form_fields['search'] = False
        self.form_fields['unique'] = False
        self.form_fields['index']  = False
        self.form_fields['minimum'] = self.type_attribs.get('minimum', 0) 
        self.form_fields['maximum'] = self.type_attribs.get('maximum', 0)
        self.form_fields['srid'] = self.type_attribs.get('srid', "")
        self.form_fields['geom_type'] = self.type_attribs.get('geom_type', 0)

        self.form_fields['entity_relation'] = \
                self.type_attribs.get('entity_relation', None)

        self.form_fields['first_parent'] = \
                self.type_attribs.get('first_parent', None)

        self.form_fields['second_parent'] = \
                self.type_attribs.get('second_parent', None)

    def init_type_attribs(self):
        """
        Initializes data type attributes. The attributes are used to
        set the form controls state when a particular data type is selected.
        mandt - enables/disables checkbox 'mandatory field'
        search - enables/disables checkbox 'is searchable'
        unique - enables/disables checkbox 'is unique'
        index - enables/disables checkbox 'column index'
        *property - function to execute when a data type is selected.
        """
        self.type_attribs['VARCHAR'] = {
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':True, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':True},
                'index':{'check_state':False, 'enabled_state':True},
                'maximum':30,'property': self.varchar_property }

        self.type_attribs['BIGINT'] = {
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':True, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':True},
                'index':{'check_state':False, 'enabled_state':True},
                'minimum':0, 'maximum':0,
                'property':self.bigint_property }

        self.type_attribs['TEXT'] = {
                'mandt':{'check_state':False, 'enabled_state':False},
                'search':{'check_state':False, 'enabled_state':False},
                'unique':{'check_state':False, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                } 

        self.type_attribs['DOUBLE' ] = {
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':True, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':True},
                'index':{'check_state':False, 'enabled_state':True},
                'minimum':0.0, 'maximum':0.0,
                'property':self.double_property }

        self.type_attribs['DATE'] =  {
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':False, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                'minimum':QtCore.QDate.currentDate(),
                'maximum':QtCore.QDate.currentDate(),
                'property':self.date_property }
               
        self.type_attribs['DATETIME'] = {
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':False, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                'minimum':QtCore.QDateTime.currentDateTime(),
                'maximum':QtCore.QDateTime.currentDateTime(),
                'property':self.dtime_property }

        self.type_attribs['FOREIGN_KEY'] = {
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':False, 'enabled_state':False},
                'unique':{'check_state':False, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                'entity_relation':None,
                'property':self.fk_property, 'prop_set':False }

        self.type_attribs['LOOKUP'] = {
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':True, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                'entity_relation':{},
                'property':self.lookup_property, 'prop_set':False }

        self.type_attribs['GEOMETRY'] ={
                'mandt':{'check_state':False, 'enabled_state':False},
                'search':{'check_state':False, 'enabled_state':False},
                'unique':{'check_state':True, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                'srid':"", 'geom_type':0,
                'property':self.geometry_property, 'prop_set':False }


        self.type_attribs['ADMIN_SPATIAL_UNIT'] ={
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':True, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                'entity_relation':None}

        self.type_attribs['MULTIPLE_SELECT'] ={
                'mandt':{'check_state':False, 'enabled_state':True},
                'search':{'check_state':False, 'enabled_state':True},
                'unique':{'check_state':False, 'enabled_state':False},
                'index':{'check_state':False, 'enabled_state':False},
                'first_parent':None, 'second_parent':self.entity,
                'property':self.multi_select_property, 'prop_set':False }
	
    def data_type_property(self):
        """
        Executes the relevant function assigned to the property attribute of 
        the current selected data type.
        """
        self.type_attribs[self.current_type_info()]['property']()

    def varchar_property(self):
        """
        Opens the property editor for the Varchar data type.
        If successfull, set a minimum column in work area 'form fields'
        """
        editor = VarcharProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['maximum'] = editor.max_len()

    def bigint_property(self):
        """
        Opens a property editor for the BigInt data type.
        """
        editor = BigintProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def double_property(self):
        """
        Opens a property editor for the Double data type.
        """
        editor = DoubleProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def date_property(self):
        """
        Opens a property editor for the Date data type.
        """
        editor = DateProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def dtime_property(self):
        """
        Opens a property editor for the DateTime data type.
        """
        editor = DTimeProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def geometry_property(self):
        """
        Opens a property editor for the Geometry data type.
        If successfull, set the srid(projection), geom_type (LINE, POLYGON...)
        and prop_set which is boolean flag to verify that all the geometry
        properties are set.  If prop_set is false you are not allowed to save
        the column.
        """
        editor = GeometryProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['srid'] = editor.coord_sys()
            self.form_fields['geom_type'] = editor.geom_type()
            self.type_attribs[self.type_info]['prop_set'] = True

    def admin_spatial_unit_property(self):
        """
        Sets entity relation property used when creating column of type
        ADMIN_SPATIAL_UNIT
        """
        er_fields = {}
        er_fields['parent'] = self.entity
        er_fields['parent_column'] = None
        er_fields['display_columns'] = []
        er_fields['child'] = None
        er_fields['child_column'] = None
        self.form_fields['entity_relation'] = EntityRelation(self.profile, **er_fields)

    def fk_property(self):
        """
        Opens a property editor for the ForeignKey data type.
        """
        if len(self.edtColName.displayText())==0:
            self.error_message("Please enter column name!")
            return

        # filter list of lookup tables, don't show internal 
        # tables in list of lookups
        fk_ent = [entity for entity in self.profile.entities.items() \
                if entity[1].TYPE_INFO not in self.EX_TYPE_INFO]

        fk_ent = [entity for entity in fk_ent if unicode(entity[0]) \
                not in self.FK_EXCLUDE]

        relation = {}
        relation['entity_relation'] = self.form_fields['entity_relation']
        relation['fk_entities'] = fk_ent
        relation['profile'] = self.profile
        relation['entity'] = self.entity
        relation['column_name'] = unicode(self.edtColName.text())

        editor = FKProperty(self, relation)
        result = editor.exec_()
        if result == 1:
            self.form_fields['entity_relation'] = editor.entity_relation()
            self.type_attribs[self.type_info]['prop_set'] = True

    def lookup_property(self):
        """
        Opens a lookup type property editor
        """
        er = self.form_fields['entity_relation']
        editor = LookupProperty(self, er, profile=self.profile) 
        result = editor.exec_()
        if result == 1:
            self.form_fields['entity_relation'] = editor.entity_relation()
            self.type_attribs[self.type_info]['prop_set'] = True

    def multi_select_property(self):
        """
        Opens a multi select property editor
        """
        if len(self.edtColName.displayText())==0:
           self.error_message("Please enter column name!")
           return
       
        first_parent = self.form_fields['first_parent']
        editor = MultiSelectProperty(self, first_parent, self.entity, self.profile) 
        result = editor.exec_()
        if result == 1:
            self.form_fields['first_parent'] = editor.lookup()
            self.form_fields['second_parent'] = self.entity
            self.type_attribs[self.type_info]['prop_set'] = True

    def create_column(self):
        """
        Creates a new BaseColumn.
        """
        column = None
        if self.type_info:
            if self.type_info == 'ADMIN_SPATIAL_UNIT':
                self.admin_spatial_unit_property()
                column = BaseColumn.registered_types[self.type_info] \
                        (self.entity, **self.form_fields)
                return column

            if self.is_property_set(self.type_info):
                column = BaseColumn.registered_types[self.type_info] \
                        (self.form_fields['colname'], self.entity, 
                                self.form_fields['geom_type'],
                                self.entity, **self.form_fields)
            else:
                self.error_message('Please set column properties.')
        else:
            raise "No type to create!"

        return column

    def is_property_set(self, ti):
        """
        Checks if column property is set by reading the value of
        attribute 'prop_set'
        :param ti: Type info to check for prop set
        :type ti: BaseColumn.TYPE_INFO
        :rtype: boolean
        """
        if not self.type_attribs[ti].has_key('prop_set'):
            return True

        return self.type_attribs[ti]['prop_set']

    def property_by_name(self, ti, name):
        try:
                return self.dtype_property(ti)['property'][name]
        except:
                return None

    def popuplate_type_cbo(self):
        """
        Fills the data type combobox widget with BaseColumn type names
        """
        self.cboDataType.clear()
        self.cboDataType.insertItems(0, BaseColumn.types_by_display_name().keys())
        self.cboDataType.setCurrentIndex(0)

    def change_data_type(self):
        """
        Called by type combobox when you select a different data type.
        """
        ti = self.current_type_info()
        if ti=='':
            return
        self.btnColProp.setEnabled(self.type_attribs[ti].has_key('property'))
        self.type_info = ti
        opts = self.type_attribs[ti]
        self.set_optionals(opts)
        self.set_min_max_defaults(ti)

    def set_optionals(self, opts):
        """
        Enable/disables form controls by selected data type attribute
        param opts: Dictionary of selected column type properties
        type: dictionary
        """
        self.cbMandt.setEnabled(opts['mandt']['enabled_state'])
        self.cbSearch.setEnabled(opts['search']['enabled_state'])
        self.cbUnique.setEnabled(opts['unique']['enabled_state'])
        self.cbIndex.setEnabled(opts['index']['enabled_state'])

        self.cbMandt.setCheckState(self.bool_to_check(opts['mandt']['check_state']))
        self.cbSearch.setCheckState(self.bool_to_check(opts['search']['check_state']))
        self.cbUnique.setCheckState(self.bool_to_check(opts['unique']['check_state']))
        self.cbIndex.setCheckState(self.bool_to_check(opts['index']['check_state']))

    def set_min_max_defaults(self, type_info):
        """
        sets the work area 'form_fields' defaults(minimum/maximum)
        from the column attribute dictionary
        :param type_info: BaseColumn.TYPE_INFO
        :type type_info: str
        """
        self.form_fields['minimum'] = \
                self.type_attribs[type_info].get('minimum', 0)

        self.form_fields['maximum'] = \
                self.type_attribs[type_info].get('maximum', 0)

    def current_type_info(self):
        """
        Returns a TYPE_INFO of a data type
        :rtype: BaseColumn.TYPE_INFO
        """
        text = self.cboDataType.itemText(self.cboDataType.currentIndex())
        try:
                return BaseColumn.types_by_display_name()[text].TYPE_INFO
        except:
                return ''

    def fill_work_area(self):
        """
        Sets work area 'form_fields' with form control values
        """
        self.form_fields['colname']    = unicode(self.edtColName.text())
        self.form_fields['description']= unicode(self.edtColDesc.text())
        self.form_fields['index']      = self.cbIndex.isChecked()
        self.form_fields['mandatory']  = self.cbMandt.isChecked()
        self.form_fields['searchable'] = self.cbSearch.isChecked()
        self.form_fields['unique']     = self.cbUnique.isChecked()
        self.form_fields['user_tip']   = unicode(self.edtUserTip.text())

    def error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(QApplication.translate("AttributeEditor", "STDM"))
        msg.setText(message)
        msg.exec_()  

    def accept(self):
        col_name = unicode(self.edtColName.text()).strip()

        # column name is not empty
        if len(col_name)==0:
            self.error_message('Please enter the column name!')
            return False

        # check if another column with the same name exist in the current entity
        if self.entity.columns.has_key(col_name):
            self.error_message(QApplication.translate("ColumnEditor",
                "Column with the same name already exist!"))
            return 

        # if column is initialized, this is an edit
        # delete old one then add a new one
        if self.column:
            self.entity.remove_column(self.column.name)

        self.fill_work_area()
        self.column = self.create_column()

        if self.column:
            self.entity.add_column(self.column)
            self.done(1)
        else:
            return

    def rejectAct(self):
        self.done(0)

=======
# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : column_editor
Description          : Editor to create/edit entity columns
Date                 : 24/January/2016
copyright            : (C) 2015 by UN-Habitat and implementing partners.
                       See the accompanying file CONTRIBUTORS.txt in the root
email                : stdm@unhabitat.org
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import collections
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from collections import OrderedDict

from ui_column_editor import Ui_ColumnEditor

from stdm.data.configuration.columns import BaseColumn
from stdm.data.configuration.entity_relation import EntityRelation

from varchar_property import VarcharProperty
from bigint_property import BigintProperty
from double_property import DoubleProperty
from date_property import DateProperty
from dtime_property import DTimeProperty
from geometry_property import GeometryProperty
from fk_property import FKProperty
from lookup_property import LookupProperty
from multi_select_property import MultiSelectProperty

from datetime import (
    date,
    datetime
)

class ColumnEditor(QDialog, Ui_ColumnEditor):
    """
    Form to add/edit entity columns
    """
    def __init__(self, parent, **kwargs):
        """
        :param parent: Owner of this dialog
        :type parent: QWidget
        :param kwargs: Keyword dictionary of the following params;
         column - Column you editting, None if its a new column
         entity - Entity you are adding the column
         profile - Current profile
        """
        QDialog.__init__(self, parent)
        self.form_parent = parent

        self.FK_EXCLUDE = [u'supporting_document', u'admin_spatial_unit_set']

        self.EX_TYPE_INFO =  ['SUPPORTING_DOCUMENT', 'SOCIAL_TENURE', 
                'ADMINISTRATIVE_SPATIAL_UNIT', 'ENTITY_SUPPORTING_DOCUMENT',
                'VALUE_LIST']

        self.setupUi(self)
        self.dtypes = {}

        self.column  = kwargs.get('column', None)
        self.entity  = kwargs.get('entity', None)
        self.profile = kwargs.get('profile', None)

        self.type_info = ''
        
        # dictionary to hold default attributes for each data type
        self.type_attribs = {}
        self.init_type_attribs()

        # dictionary to act as a work area for the form fields.
        self.form_fields = {}
        self.init_form_fields()

        self.fk_entities     = []
        self.lookup_entities = []

        # the current entity should not be part of the foreign key parent table, add it to the exclusion list
        self.FK_EXCLUDE.append(self.entity.short_name)

        self.cboDataType.currentIndexChanged.connect(self.change_data_type)

        #self.btnTableList.clicked.connect(self.lookupDialog)
        self.btnColProp.clicked.connect(self.data_type_property)

        self.type_names = \
                [str(name) for name in BaseColumn.types_by_display_name().keys()]

        self.init_controls()

    def init_controls(self):
        self.popuplate_type_cbo()

        name_regex = QtCore.QRegExp('^[a-z][a-z0-9_]*$')
        name_validator = QtGui.QRegExpValidator(name_regex)
        self.edtColName.setValidator(name_validator)

        if self.column:
            self.column_to_form(self.column)
            self.column_to_wa(self.column)

        self.edtColName.setFocus()

    def column_to_form(self, column):
        """
        Initializes form controls with column data when editting a column.
        :param column: Column to edit
        :type column: BaseColumn
        """
        self.edtColName.setText(column.name)
        self.edtColDesc.setText(column.description)
        self.edtUserTip.setText(column.user_tip)
        self.cbMandt.setCheckState(self.bool_to_check(column.mandatory))
        self.cbSearch.setCheckState(self.bool_to_check(column.searchable))
        self.cbUnique.setCheckState(self.bool_to_check(column.unique))
        self.cbIndex.setCheckState(self.bool_to_check(column.index))

        #self.cboDataType.setCurrentIndex(cbo_id)

        self.cboDataType.setCurrentIndex( \
                self.cboDataType.findText(column.display_name()))

    def column_to_wa(self, column):
        """
        Initializes work area 'form_fields' with column data.
        Used when editing a column
        :param column: Column to edit
        :type column: BaseColumn
        """
        self.form_fields['colname'] = column.name
        self.form_fields['value']  = None
        self.form_fields['mandt']  = column.mandatory
        self.form_fields['search'] = column.searchable
        self.form_fields['unique'] = column.unique
        self.form_fields['index']  = column.index

        if hasattr(column, 'minimum'):
            self.form_fields['minimum'] = column.minimum
            self.form_fields['maximum'] = column.maximum

        if hasattr(column, 'srid'):
            self.form_fields['srid'] = column.srid
            self.form_fields['geom_type'] = column.geom_type

        if hasattr(column, 'entity_relation'):
            self.form_fields['entity_relation'] = column.entity_relation

        if hasattr(column, 'association'):
            self.form_fields['first_parent'] = column.association.first_parent
            self.form_fields['second_parent'] = column.association.second_parent

    def bool_to_check(self, state):
        """
        Converts a boolean to a Qt checkstate.
        :param state: True/False
        :type state: boolean
        :rtype: Qt.CheckState
        """
        if state:
            return Qt.Checked
        else:
            return Qt.Unchecked

    def init_form_fields(self):
        """
        Initializes work area 'form_fields' dictionary with default values.
        Used when creating a new column.
        """
        self.form_fields['colname'] = ''
        self.form_fields['value']  = None
        self.form_fields['mandt']  = False
        self.form_fields['search'] = False
        self.form_fields['unique'] = False
        self.form_fields['index']  = False
        self.form_fields['minimum'] = self.type_attribs.get('minimum', 0) 
        self.form_fields['maximum'] = self.type_attribs.get('maximum', 0)
        self.form_fields['srid'] = self.type_attribs.get('srid', "")
        self.form_fields['geom_type'] = self.type_attribs.get('geom_type', 0)

        self.form_fields['entity_relation'] = \
                self.type_attribs.get('entity_relation', None)

        self.form_fields['first_parent'] = \
                self.type_attribs.get('first_parent', None)

        self.form_fields['second_parent'] = \
                self.type_attribs.get('second_parent', None)

    def init_type_attribs(self):
        """
        Initializes data type attributes. The attributes are used to
        set the form controls state when a particular data type is selected.
        mandt - enables/disables checkbox 'mandatory field'
        search - enables/disables checkbox 'is searchable'
        unique - enables/disables checkbox 'is unique'
        index - enables/disables checkbox 'column index'
        *property - function to execute when a data type is selected.
        """
        self.type_attribs['VARCHAR'] = {
                'mandt':False,'search': True,
                'unique': False, 'index': False,
                'maximum':30,'property': self.varchar_property }

        self.type_attribs['INT'] = {
                'mandt':False, 'search': False,
                'unique': False, 'index': False,
                'minimum':0, 'maximum':0,
                'property':self.bigint_property }

        self.type_attribs['TEXT'] = {'mandt':False, 'search': False, 
                'unique': False, 'index': False } 

        self.type_attribs['DOUBLE' ] = {'mandt':False, 'search': False, 
                'unique': False, 'index': False, 
                'minimum':0.0, 'maximum':0.0,
                'property':self.double_property }

        self.type_attribs['DATE'] =  {'mandt':False, 'search': False,
                'unique': False, 'index': False,
                'minimum':QtCore.QDate.currentDate(),
                'maximum':QtCore.QDate.currentDate(),
                'property':self.date_property }
               
        self.type_attribs['DATETIME'] = {'mandt':False, 'search': False,
                'unique': False, 'index': False,
                'minimum':QtCore.QDateTime.currentDateTime(),
                'maximum':QtCore.QDateTime.currentDateTime(),
                'property':self.dtime_property }

        self.type_attribs['FOREIGN_KEY'] = {'mandt':False, 'search': False, 
                'unique': False, 'index': False,
                'entity_relation':None,
                'property':self.fk_property, 'prop_set':False }

        self.type_attribs['LOOKUP'] = {'mandt':False, 'search': False,
                'unique': False, 'index': False,
                'entity_relation':{},
                'property':self.lookup_property, 'prop_set':False }

        self.type_attribs['GEOMETRY'] ={'mandt':False, 'search': False, 
                'unique': False, 'index': False,
                'srid':"", 'geom_type':0,
                'property':self.geometry_property, 'prop_set':False }


        self.type_attribs['ADMIN_SPATIAL_UNIT'] ={'mandt':False, 'search': False,
                'entity_relation':None, 'unique': False, 'index': False}

        self.type_attribs['MULTIPLE_SELECT'] ={'mandt':False, 'search': False, 
                'unique': False, 'index': False,
                'first_parent':None, 'second_parent':self.entity,
                'property':self.multi_select_property, 'prop_set':False }
	
    def data_type_property(self):
        """
        Executes the relevant function assigned to the property attribute of 
        the current selected data type.
        """
        self.type_attribs[self.current_type_info()]['property']()

    def varchar_property(self):
        """
        Opens the property editor for the Varchar data type.
        If successfull, set a minimum column in work area 'form fields'
        """
        editor = VarcharProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['maximum'] = editor.max_len()

    def bigint_property(self):
        """
        Opens a property editor for the BigInt data type.
        """
        editor = BigintProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def double_property(self):
        """
        Opens a property editor for the Double data type.
        """
        editor = DoubleProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def date_property(self):
        """
        Opens a property editor for the Date data type.
        """
        editor = DateProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def dtime_property(self):
        """
        Opens a property editor for the DateTime data type.
        """
        editor = DTimeProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['minimum'] = editor.min_val()
            self.form_fields['maximum'] = editor.max_val()

    def geometry_property(self):
        """
        Opens a property editor for the Geometry data type.
        If successfull, set the srid(projection), geom_type (LINE, POLYGON...)
        and prop_set which is boolean flag to verify that all the geometry
        properties are set.  If prop_set is false you are not allowed to save
        the column.
        """
        editor = GeometryProperty(self, self.form_fields)
        result = editor.exec_()
        if result == 1:
            self.form_fields['srid'] = editor.coord_sys()
            self.form_fields['geom_type'] = editor.geom_type()
            self.type_attribs[self.type_info]['prop_set'] = True

    def admin_spatial_unit_property(self):
        """
        Sets entity relation property used when creating column of type
        ADMIN_SPATIAL_UNIT
        """
        er_fields = {}
        er_fields['parent'] = self.entity
        er_fields['parent_column'] = None
        er_fields['display_columns'] = []
        er_fields['child'] = None
        er_fields['child_column'] = None
        self.form_fields['entity_relation'] = EntityRelation(self.profile, **er_fields)

    def fk_property(self):
        """
        Opens a property editor for the ForeignKey data type.
        """
        if len(self.edtColName.displayText())==0:
            self.error_message("Please enter column name!")
            return

        # filter list of lookup tables, don't show internal 
        # tables in list of lookups
        fk_ent = [entity for entity in self.profile.entities.items() \
                if entity[1].TYPE_INFO not in self.EX_TYPE_INFO]

        fk_ent = [entity for entity in fk_ent if unicode(entity[0]) \
                not in self.FK_EXCLUDE]

        relation = {}
        relation['entity_relation'] = self.form_fields['entity_relation']
        relation['fk_entities'] = fk_ent
        relation['profile'] = self.profile
        relation['entity'] = self.entity
        relation['column_name'] = unicode(self.edtColName.text())

        editor = FKProperty(self, relation)
        result = editor.exec_()
        if result == 1:
            self.form_fields['entity_relation'] = editor.entity_relation()
            self.type_attribs[self.type_info]['prop_set'] = True

    def lookup_property(self):
        """
        Opens a lookup type property editor
        """
        er = self.form_fields['entity_relation']
        editor = LookupProperty(self, er, profile=self.profile) 
        result = editor.exec_()
        if result == 1:
            self.form_fields['entity_relation'] = editor.entity_relation()
            self.type_attribs[self.type_info]['prop_set'] = True

    def multi_select_property(self):
        """
        Opens a multi select property editor
        """
        if len(self.edtColName.displayText())==0:
           self.error_message("Please enter column name!")
           return
       
        first_parent = self.form_fields['first_parent']
        editor = MultiSelectProperty(self, first_parent, self.entity, self.profile) 
        result = editor.exec_()
        if result == 1:
            self.form_fields['first_parent'] = editor.lookup()
            self.form_fields['second_parent'] = self.entity
            self.type_attribs[self.type_info]['prop_set'] = True

    def create_column(self):
        """
        Creates a new BaseColumn.
        """
        column = None
        if self.type_info:
            if self.type_info == 'ADMIN_SPATIAL_UNIT':
                self.admin_spatial_unit_property()
                column = BaseColumn.registered_types[self.type_info] \
                        (self.entity, **self.form_fields)
                return column

            if self.is_property_set(self.type_info):
                column = BaseColumn.registered_types[self.type_info] \
                        (self.form_fields['colname'], self.entity, 
                                self.form_fields['geom_type'],
                                self.entity, **self.form_fields)
            else:
                self.error_message('Please set column properties.')
        else:
            raise "No type to create!"

        return column

    def is_property_set(self, ti):
        """
        Checks if column property is set by reading the value of
        attribute 'prop_set'
        :param ti: Type info to check for prop set
        :type ti: BaseColumn.TYPE_INFO
        :rtype: boolean
        """
        if not self.type_attribs[ti].has_key('prop_set'):
            return True

        return self.type_attribs[ti]['prop_set']

    def property_by_name(self, ti, name):
        try:
                return self.dtype_property(ti)['property'][name]
        except:
                return None

    def popuplate_type_cbo(self):
        """
        Fills the data type combobox widget with BaseColumn type names
        """
        self.cboDataType.clear()
        self.cboDataType.insertItems(0, BaseColumn.types_by_display_name().keys())
        self.cboDataType.setCurrentIndex(0)

    def change_data_type(self):
        """
        Called by type combobox when you select a different data type.
        """
        ti = self.current_type_info()
        if ti=='':
            return
        self.btnColProp.setEnabled(self.type_attribs[ti].has_key('property'))
        self.type_info = ti
        opts = self.type_attribs[ti]
        self.set_optionals(opts)
        self.set_min_max_defaults(ti)

    def set_optionals(self, opts):
        """
        Enable/disables form controls by selected data type attribute
        param opts: Dictionary of selected column type properties
        type: dictionary
        """
        self.cbMandt.setEnabled(opts['mandt'])
        self.cbSearch.setEnabled(opts['search'])
        self.cbUnique.setEnabled(opts['unique'])
        self.cbIndex.setEnabled(opts['index'])

        self.cbMandt.setCheckState(self.bool_to_check(opts['mandt']))
        self.cbSearch.setCheckState(self.bool_to_check(opts['search']))
        self.cbUnique.setCheckState(self.bool_to_check(opts['unique']))
        self.cbIndex.setCheckState(self.bool_to_check(opts['index']))

    def set_min_max_defaults(self, type_info):
        """
        sets the work area 'form_fields' defaults(minimum/maximum)
        from the column attribute dictionary
        :param type_info: BaseColumn.TYPE_INFO
        :type type_info: str
        """
        self.form_fields['minimum'] = \
                self.type_attribs[type_info].get('minimum', 0)

        self.form_fields['maximum'] = \
                self.type_attribs[type_info].get('maximum', 0)

    def current_type_info(self):
        """
        Returns a TYPE_INFO of a data type
        :rtype: BaseColumn.TYPE_INFO
        """
        text = self.cboDataType.itemText(self.cboDataType.currentIndex())
        try:
                return BaseColumn.types_by_display_name()[text].TYPE_INFO
        except:
                return ''

    def fill_work_area(self):
        """
        Sets work area 'form_fields' with form control values
        """
        self.form_fields['colname']    = unicode(self.edtColName.text())
        self.form_fields['description']= unicode(self.edtColDesc.text())
        self.form_fields['index']      = self.cbIndex.isChecked()
        self.form_fields['mandatory']  = self.cbMandt.isChecked()
        self.form_fields['searchable'] = self.cbSearch.isChecked()
        self.form_fields['unique']     = self.cbUnique.isChecked()
        self.form_fields['user_tip']   = unicode(self.edtUserTip.text())

    def error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(QApplication.translate("AttributeEditor", "STDM"))
        msg.setText(message)
        msg.exec_()  

    def accept(self):
        col_name = unicode(self.edtColName.text()).strip()

        # column name is not empty
        if len(col_name)==0:
            self.error_message('Please enter the column name!')
            return False

        # check if another column with the same name exist in the current entity
        if self.entity.columns.has_key(col_name):
            self.error_message(QApplication.translate("ColumnEditor",
                "Column with the same name already exist!"))
            return 

        # if column is initialized, this is an edit
        # delete old one then add a new one
        if self.column:
            self.entity.remove_column(self.column.name)

        self.fill_work_area()
        self.column = self.create_column()

        if self.column:
            self.entity.add_column(self.column)
            self.done(1)
        else:
            return

    def rejectAct(self):
        self.done(0)

>>>>>>> 7a93a8f25be0e7eb5a3ce57e948518321a34068d
