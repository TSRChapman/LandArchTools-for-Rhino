import Rhino as r
import rhinoscriptsyntax as rs
import scriptcontext as sc
import sys
import os

def addToClipBoard(text):
    command = 'echo ' + text.strip() + '| clip'
    os.system(command)

obj = rs.coercecurve(rs.GetObject(message="Select the curve to used at the top level step",  preselect=True, select=False, custom_filter=None, subobjects=False))

string = obj.ToJSON(r.FileIO.SerializationOptions())

addToClipBoard(string)


#rebuild = r.Runtime.CommonObject.FromJSON(string)


#sc.doc.Objects.AddBrep(rebuild)
#sc.doc.Views.Redraw()

#print rebuild

