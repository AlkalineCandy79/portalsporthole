#-------------------------------------------------------------------------------
# Name:        Portal's Porthole
# Purpose:  This script pulls the entire inventory of REST endpoints used by
#           Web Maps from ArcGIS Online and/or ArcGIS Portal.  SAML and OATH
#           logon capabilities are not compatible yet with the most current
#           version of the ArcGIS Python API.  Must have ArcGIS Pro installed
#           to even run this script.  More documentation will be provided as
#           Pro adds some interesting complexity when you try to customize at
#           a later date.
#
# Author:      John Spence
#
# Created:     3/9/2019
# Modified:
# Modification Purpose:
#
#-------------------------------------------------------------------------------

# 888888888888888888888888888888888888888888888888888888888888888888888888888888
# ------------------------------- Configuration --------------------------------
#
#  Configurations pending.
#
# ------------------------------- Dependencies ---------------------------------
#
#  Dependency attribution pending.
#
# 888888888888888888888888888888888888888888888888888888888888888888888888888888

import arcgis
import collections
from arcgis.gis import GIS
import pandas as pd
import xlsxwriter

gis = GIS("https://cobgis.maps.arcgis.com/","","") #non-saml or ADFS user name, #password

layer = []
baselayer = []
exceptions = []

search_results = gis.content.search(query="",item_type="Web Map",max_items=100000)
for result in search_results:
    print (result)
    wmo = arcgis.mapping.WebMap(result)
    print (wmo)
    ops_layers = wmo.definition['operationalLayers']
    print (ops_layers)
    for op_layer in ops_layers:
        try:
            itemURL = '=HYPERLINK("http://YOURPORTAL.maps.arcgis.com/home/item.html?id={0}","Launch Map")'.format(result.itemid)
            a = collections.OrderedDict()
            a["Web Map Name"] = result.title
            a["Web Map Owner"] = result.owner
            a["Web Map Item ID"] = itemURL
            a["Layer Title"] =  "{0}".format (op_layer["title"])
            a["Layer Type"] = "{0}".format (op_layer["layerType"])
            #a["Layer WKID"] = "{0}".format (op_layer["wkid"])
            a["Layer URL"] = op_layer["url"]
            layer.append(a)
        except:
            print ('Unable to add')
            itemURL = '=HYPERLINK("http://YOURPORTAL.maps.arcgis.com/home/item.html?id={0}","Launch Map")'.format(result.itemid)
            a = collections.OrderedDict()
            a["Item Name"] = result.title
            a["Item Owner"] = result.owner
            a["Item Item ID"] = itemURL
            #a["Layer Title"] =  "{0}".format (op_layer["title"])
            exceptions.append(a)

    basemap_layers = wmo.definition['baseMap']['baseMapLayers']
    print (basemap_layers)
    for base_layer in basemap_layers:
        try:
            itemURL = '=HYPERLINK("http://YOURPORTAL.maps.arcgis.com/home/item.html?id={0}","Launch Map")'.format(result.itemid)
            b = collections.OrderedDict()
            b["Web Map Name"] = result.title
            b["Web Map Owner"] = result.owner
            b["Web Map Item ID"] = itemURL
            b["Layer Title"] =  "{0}".format (base_layer["title"])
            b["Layer Type"] = "{0}".format (base_layer["layerType"])
            #b["Layer WKID"] = "{0}".format (base_layer["wkid"])
            b["Layer URL"] = base_layer["url"]
            baselayer.append(b)
        except:
            print ('Unable to add')
            itemURL = '=HYPERLINK("http://YOURPORTAL.maps.arcgis.com/home/item.html?id={0}","Launch Map")'.format(result.itemid)
            b = collections.OrderedDict()
            b["Item Name"] = result.title
            b["Item Owner"] = result.owner
            b["Item Item ID"] = itemURL
            #b["Layer Title"] =  "{0}".format (base_layer["title"])
            exceptions.append(b)

df_l = pd.DataFrame(layer)
df_b = pd.DataFrame(baselayer)
df_e = pd.DataFrame(exceptions)

writer = pd.ExcelWriter ('D:\\YourFile.xlsx', engine='xlsxwriter')
df_l.to_excel (writer, sheet_name='Operational Layers')
df_b.to_excel (writer, sheet_name='Basemap Layers')
df_e.to_excel (writer, sheet_name='Retrieval Errors')
writer.save()