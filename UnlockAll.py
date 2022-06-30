import rhinoscriptsyntax as rs
import scriptcontext as sc
import Rhino

def unlockAll():
    try:
        rs.EnableRedraw(False)

        it = Rhino.DocObjects.ObjectEnumeratorSettings()
        it.IncludeLights = True
        it.IncludeGrips = True
        it.NormalObjects = True
        it.LockedObjects = True
        it.HiddenObjects = True
        it.ReferenceObjects = True
        id = sc.doc.Objects.GetObjectList(it)

        for e in id:
            sc.doc.Objects.Unlock(e, True)

        rs.EnableRedraw(True)
        
    except:
        print ("Unable to unlock objects")
        rs.EnableRedraw(True)
        return False

if __name__ == "__main__":
    unlockAll()