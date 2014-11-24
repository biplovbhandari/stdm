# -*- coding: utf-8 -*-
"""
/***************************************************************************
 stdm
                                 A QGIS plugin
 Securing land and property rights for all
                              -------------------
        begin                : 2014-03-30
        copyright            : (C) 2014 by GLTN
        email                : njoroge.solomon@yahoo.com
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
from stdm.data import XMLTableElement, tableColumns, tableRelations,lookupTable,lookupColumn,profiles,\
tableLookUpCollection,lookupData,lookupData2List,geometryColumns,writeSQLFile, writeHTML,setLookupValue,updateSQL,\
listEntityViewer, EntityColumnModel,FilePaths


from stdm.settings import RegistryConfig, PATHKEYS


class ConfigTableReader(object):
    def __init__(self,parent=None, args=None):
        
        self._doc=''
        self.args=args
        self.fileHandler=FilePaths()
        self.config = RegistryConfig()   
   
    def tableListModel(self,profile):
        '''pass the table list to a listview model'''
        tData=self.tableNames(profile)
        if tData!= None:
            model=listEntityViewer(tData)
            return model
        else:
            return None
    
    def tableNames(self,profile):
        tData=XMLTableElement(profile)
        if tData is not None:
#            if "social_tenure" in tData:
#                tData.remove('social_tenure')
            return tData
    
    def fulltableList(self):
        tbList=tableLookUpCollection()
        if tbList is not None:
            return tbList
        
    def STDMProfiles(self):
        pfList=profiles()
        return pfList
    
    def lookupTableModel(self):
        model=listEntityViewer(self.lookupTable())
        return model
    
    def lookupTable(self):
        return lookupTable()
        
    
    def lookupColumns(self,lookupName):
        columnModel=None
        tableAttrib=lookupColumn(lookupName)
        if len(tableAttrib)>0:
            colHeaders=tableAttrib[0].keys()
            colVals=[]
            for item in tableAttrib:
                colVals.append(item.values())
            columnModel=EntityColumnModel(colHeaders,colVals)
            return columnModel
        else: 
            return None
    
    def columns(self,profile,tableName):
        '''Functions to read columns details from the config for the given table''' 
        columnModel = None
        tableAttrib = tableColumns(profile,tableName)
        if len(tableAttrib) > 0:
            colHeaders = tableAttrib[0].keys()
            colVals = []
            for item in tableAttrib:
                colVals.append(item.values())
            columnModel = EntityColumnModel(colHeaders, colVals)
            return columnModel
        else: 
            return None
    
    def tableRelation(self,tableName):
        '''Method to read all defined table relationship in the config file'''
        relationModel = None
        tableAttrib = tableRelations(tableName,"relations")
        if tableAttrib is None:
            return tableAttrib
        if len(tableAttrib)>0:
            colHeaders = tableAttrib[0].keys()
            colVals = []
            for item in tableAttrib:
                colVals.append(item.values())
            relationModel = EntityColumnModel(colHeaders,colVals)
            return relationModel
        
    def geometryData(self,tableName):
        '''Method to read all defined table relationship in the config file'''
        geometryModel = None
        geomAttrib = geometryColumns(tableName, 'constraints')
        if geomAttrib == None:
            return geomAttrib
        if len(geomAttrib) > 0:
            colHeaders = geomAttrib[0].keys()
            colVals = []
            for item in geomAttrib:
                colVals.append(item.values())
            geometryModel = EntityColumnModel(colHeaders, colVals)
            return geometryModel

    def sqlTableDefinition(self):
        '''load the table definition info in html file'''
        docfile = self.fileHandler.SQLFile()
        return docfile
    
    def htmlTableDefinition(self):
        '''load the table definition info in html file'''
        docfile = self.fileHandler.HtmlFile()
        return docfile
    
    def userProfileDir(self):
        return self.fileHandler.STDMSettingsPath()

    def updateDir(self, path):
        return  self.fileHandler.userConfigPath(path)
        
    def saveXMLchanges(self):
        writeSQLFile()
        writeHTML()
                
    def upDateSQLSchema(self):
        #To be implemented to allow updating of schema
        updateSQL()
        
        
    def setProfileSettings(self,profileData):
        '''write the current profile in Qsettings'''            
        self.config.write(profileData) 
    
    def settingsKeys(self):
        '''
        Keys used to store directory paths in the database
        '''
        return PATHKEYS
    
    def pathSettings(self):
        pathKeys = self.settingsKeys()
        pathSetting = self.config.read(pathKeys)
        return pathKeys, pathSetting
    
    def createDir(self, paths):
        if paths != None:
            for fPath in paths:
                self.fileHandler.createDir(fPath)
    
    def addLookupValue(self,table,valueText):
        setLookupValue(table,valueText)
        
    def readLookupList(self,table):
        lookupList=[]
        try:
            lookupList=lookupData(table)
        except:
            pass
        return lookupList
        
    def setDocumentationPath(self):
        '''get the help contents available to user'''
        helpFile=self.fileHandler.HelpContents()
        return helpFile
    
    def trackXMLChanges(self):
        self.fileHandler.createBackup()
    
