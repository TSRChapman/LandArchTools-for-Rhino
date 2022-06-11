import Rhino as r
import rhinoscriptsyntax as rs
import scriptcontext as sc
import sys

def main():

    ###############################################################################
    
    def StairCode(startCrv, steps, riser, tread):
    
        startCrvRef = startCrv
    
        #create loop to offset curve and loft between them
        for i in range(steps):
            #Top Riser
            offsetCrv1 = startCrv.Offset(worldXY, tread, tol, r.Geometry.CurveOffsetCornerStyle.Sharp)
            loft1 = r.Geometry.Brep.CreateFromLoftRefit((startCrv, offsetCrv1[0]), r.Geometry.Point3d.Unset, r.Geometry.Point3d.Unset, r.Geometry.LoftType.Normal, False, tol)
    
            #Check if multiple Lofts were made an abort if so
            if len(loft1) != 1:
                print ("Curve is incompatible")
                return
            #New Step
            offsetCrv1Copy = (offsetCrv1[0]).Duplicate() #RhinoCommon .Transform edits the original geometry so a copy of the original is made to be edited
            (offsetCrv1[0]).Transform(xformRiser) #Transform effects the original and only returns a bool, very confusing!
    
    
            # Note, offsetCrv1Copy is now Crv1 and offsetCrv1 is now crv 2, effectively.
            loft2 = r.Geometry.Brep.CreateFromLoftRefit((offsetCrv1Copy, offsetCrv1[0]), r.Geometry.Point3d.Unset, r.Geometry.Point3d.Unset, r.Geometry.LoftType.Normal, False, tol)
    
            #Check if multiple Lofts were made an abort if so
            if len(loft2) != 1:
                print ("Curve is incompatible")
                return
    
            #Check if last loft and add curve to new list
            if i == (steps - 1):
                endCrv.append(offsetCrv1[0])
                offsetCrv3 = (offsetCrv1[0]).Offset(worldXY, -abs(tread * steps), tol, r.Geometry.CurveOffsetCornerStyle.Sharp)
                loft3 = r.Geometry.Brep.CreateFromLoftRefit((offsetCrv1[0], offsetCrv3[0]), r.Geometry.Point3d.Unset, r.Geometry.Point3d.Unset, r.Geometry.LoftType.Normal, False, tol)
                loft4 = r.Geometry.Brep.CreateFromLoftRefit((offsetCrv3[0], startCrvRef), r.Geometry.Point3d.Unset, r.Geometry.Point3d.Unset, r.Geometry.LoftType.Normal, False, tol)
                stairLofts.extend((loft3[0], loft4[0]))
    
            #Add Lofts to list
            stairLofts.extend((loft1[0],loft2[0]))
    
            #Start new step and repeat
            print offsetCrv1[0]
            startCrv = offsetCrv1[0]
    
        #join breps together
        joinedBrep = r.Geometry.Brep.JoinBreps(stairLofts, tol)
        #Cap ends
        stairs = (joinedBrep[0]).CapPlanarHoles(tol)

        #Add to document
        docObj = sc.doc.Objects.AddBrep(stairs)


        
        #sc.doc.Objects.AddBrep(brep[0])
        sc.doc.Views.Redraw()
    
    def crvCheck(startCrv):
        # Curve health checks
        isValid = startCrv.IsValid #add return statement if False
        isIntersected = (r.Geometry.Intersect.Intersection.CurveSelf(startCrv, 0.001)).Count #add a return statement if >0
        if isValid == False:
            print ("Curve is not valid")
            return False
        if isIntersected > 0:
            print ("Curve cannot be intersecting")
            return False
        #Evaluate Height of Curve
        pt1 = (startCrv.PointAtEnd).Z
        pt2 = (startCrv.PointAtStart).Z
        evalPts = max([pt1, pt2])
        # Project Crv to world plane to flatten
        xformWorld = r.Geometry.Transform.PlanarProjection(r.Geometry.Plane.WorldXY)
        startCrv.Transform(xformWorld)
        # Move Crv back to heighest point it was before
        xformOrigin = r.Geometry.Transform.Translation(0,0,evalPts)
        startCrv.Transform(xformOrigin)
    
    ###############################################################################
    
    # Get User Curve for starting point of Stairs
    startCrv = rs.coercecurve(rs.GetObject(message="Select the curve to used at the top level step", filter=4, preselect=True, select=False, custom_filter=None, subobjects=False))
    
    crvBool = crvCheck(startCrv)
    if crvBool == False:
        return False
    
    #Variables to link to GUI
    steps = 3
    riser = 0.15
    tread = 0.30
    
    # System Variables
    #tolerance = rs.UnitAbsoluteTolerance()
    tol = sc.doc.ModelAbsoluteTolerance
    xformRiser = r.Geometry.Transform.Translation(r.Geometry.Vector3d(0,0,-abs(riser)))
    
    #Init Lists
    stairLofts = []
    endCrv = []
    
    #Plane to offset along world
    worldXY = r.Geometry.Plane.WorldXY

    
    StairCode(startCrv, steps, riser, tread)
    
    ###############################################################################

if __name__ == "__main__":
    main()
    