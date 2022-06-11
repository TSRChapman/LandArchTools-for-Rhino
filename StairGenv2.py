# Imports
import System
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import rhinoscriptsyntax as rs
import Rhino as r
import scriptcontext as sc

################################################################################



def StairGen():

    class StairGenDialog(forms.Dialog[bool]):

        # Dialog box Class initializer
        def __init__(self):
            # Initialize dialog box
            self.Title = 'LandArchTools: Stair Generator'
            self.Padding = drawing.Padding(10)
            self.Resizable = False
            self.Closing += self.OnFormClosed
            ################################################################################

            # Create controls for the dialog
            # Stair gen label
            self.stairGenLabel = forms.Label(Text='STAIR GENERATOR')

            # Gen Handrail label
            self.genStairLabel = forms.Label(Text='Generate Stair?:')
            # Gen Handrail control
            self.genStairBool = forms.CheckBox()
            self.genStairBool.Checked = False
            self.genStairBool.CheckedChanged += self.stairGen

            # Number of Steps Label
            self.numStepsLabel = forms.Label(Text='Number of steps:')
            # Number of Steps control
            self.numStepsC = forms.NumericStepper()
            self.numStepsC.DecimalPlaces = 0
            self.numStepsC.Increment = 1
            self.numStepsC.MaxValue = 50
            self.numStepsC.MinValue = 1
            self.numStepsC.Value = 3
            self.numStepsC.ValueChanged += self.stairGen
            self.numStepsC.ValueChanged += self.handrailGen

            # Tread label
            self.treadLabel = forms.Label(Text='Tread (mm):')
            # Tread length control
            self.treadC = forms.NumericStepper()
            self.treadC.DecimalPlaces = 0
            self.treadC.Increment = 1
            self.treadC.MaxValue = 10000
            self.treadC.MinValue = 1
            self.treadC.Value = 300
            self.treadC.ValueChanged += self.stairGen
            self.treadC.ValueChanged += self.handrailGen

            # Riser Label
            self.riserLabel = forms.Label(Text='Riser (mm):')
            # Tread length control
            self.riserC = forms.NumericStepper()
            self.riserC.DecimalPlaces = 0
            self.riserC.Increment = 1
            self.riserC.MaxValue = 10000
            self.riserC.MinValue = 1
            self.riserC.Value = 150
            self.riserC.ValueChanged += self.stairGen
            self.riserC.ValueChanged += self.handrailGen

            # Flip label
            self.flipLabel = forms.Label(Text='Flip direction of stairs:')
            # Flip control
            self.flipC = forms.CheckBox()
            self.flipC.CheckedChanged += self.flipChecked
            self.flipC.CheckedChanged += self.handrailGen
            self.flipC.CheckedChanged += self.stairGen

            ###########################################
            # Handrail Gen Label
            self.handrailGenLabel = forms.Label(Text='HANDRAIL GENERATOR')
            # self.handrailGenLabel.VerticalAlignment.Center

            # Gen Handrail label
            self.genHandrailLabel = forms.Label(Text='Generate Handrail?:')
            # Gen Handrail control
            self.genHandrailBool = forms.CheckBox()
            self.genHandrailBool.Checked = False
            self.genHandrailBool.CheckedChanged += self.handrailGen

            # Handrail Type Label
            self.handrailTypeLabel = forms.Label(Text='Handrail type:')
            # Handrail Type Dropdown
            self.handrailTypeC = forms.DropDown()
            self.handrailTypeC.DataStore = [
                '180 No Return', '180 Full Return', 'Ground Triangular Return', 'Ground Return', 'Wall Return']
            self.handrailTypeC.SelectedIndex = 0
            self.handrailTypeC.SelectedIndexChanged += self.handrailGen

            # Handrail Height Label
            self.handrailHeightLabel = forms.Label(
                Text='Handrail height (mm):')
            # Handrail Height control
            self.handrailHeightC = forms.NumericStepper()
            self.handrailHeightC.DecimalPlaces = 0
            self.handrailHeightC.Increment = 1
            self.handrailHeightC.MaxValue = 5000
            self.handrailHeightC.MinValue = 100
            self.handrailHeightC.Value = 900
            self.handrailHeightC.ValueChanged += self.handrailGen

            # Handrail offset label
            self.handrailOffsetLabel = forms.Label(
                Text='Handrail offset from edges (mm):')
            # Handrail offset control
            self.handrailOffsetC = forms.NumericStepper()
            self.handrailOffsetC.DecimalPlaces = 0
            self.handrailOffsetC.Increment = 1
            self.handrailOffsetC.MaxValue = 5000
            self.handrailOffsetC.MinValue = 50
            self.handrailOffsetC.Value = 150
            self.handrailOffsetC.ValueChanged += self.handrailGen

            # Handrail extension Label
            self.handrailExtensionLabel = forms.Label(
                Text='Handrail extension (mm):')
            # Handrail extension Control
            self.handrailExtensionC = forms.NumericStepper()
            self.handrailExtensionC.DecimalPlaces = 0
            self.handrailExtensionC.Increment = 1
            self.handrailExtensionC.MaxValue = 5000
            self.handrailExtensionC.MinValue = 300
            self.handrailExtensionC.Value = 300
            self.handrailExtensionC.ValueChanged += self.handrailGen

            # Handrail Diameter Label
            self.handrailDiameterLabel = forms.Label(
                Text='Handrail diameter (mm):')
            # Handrail Diameter control
            self.handrailDiameterC = forms.NumericStepper()
            self.handrailDiameterC.DecimalPlaces = 0
            self.handrailDiameterC.Increment = 1
            self.handrailDiameterC.MaxValue = 50
            self.handrailDiameterC.MinValue = 30
            self.handrailDiameterC.Value = 30
            self.handrailDiameterC.ValueChanged += self.handrailGen

            # Create the default button
            self.DefaultButton = forms.Button(Text='OK')
            self.DefaultButton.Click += self.OnOKButtonClick

            # Create the abort button
            self.AbortButton = forms.Button(Text='Cancel')
            self.AbortButton.Click += self.OnCloseButtonClick

            ################################################################################

            # Create a table layout and add all the controls
            layout = forms.DynamicLayout()
            layout.Spacing = drawing.Size(5, 5)

            layout.AddRow(None)
            layout.AddRow(self.stairGenLabel)
            layout.AddRow(None)
            layout.AddRow(None)
            layout.AddRow(self.genStairLabel, self.genStairBool)
            layout.AddRow(self.numStepsLabel, self.numStepsC)
            layout.AddRow(self.treadLabel, self.treadC)
            layout.AddRow(self.riserLabel, self.riserC)
            layout.AddRow(self.flipLabel, self.flipC)
            layout.AddRow(None)
            layout.AddRow(None)
            layout.AddRow(None)
            layout.AddRow(None)
            layout.AddRow(self.handrailGenLabel)
            layout.AddRow(None)
            layout.AddRow(None)
            layout.AddRow(self.genHandrailLabel, self.genHandrailBool)
            layout.AddRow(self.handrailTypeLabel, self.handrailTypeC)
            layout.AddRow(self.handrailHeightLabel, self.handrailHeightC)
            layout.AddRow(self.handrailOffsetLabel, self.handrailOffsetC)
            layout.AddRow(self.handrailExtensionLabel, self.handrailExtensionC)
            layout.AddRow(self.handrailDiameterLabel, self.handrailDiameterC)
            layout.AddRow(self.DefaultButton, self.AbortButton)

            # Set the dialog content
            self.Content = layout

        #########################################################################################

        # GEOMETRY GENERATION METHODS

        def stairGen(self, sender, e):
            rs.EnableRedraw(False)
            
            global startCrv
            

            
            # CHECK FOR PREVIOUS GENERATIONS
            pRev = rs.ObjectsByName("37DNW&T8BWXmZG^$g&Qjfrciv2E495opp@PzZYQhbBYgjsD4Gs")
            if len(pRev) > 0:
                for i in pRev:
                    rs.DeleteObject(i)
            
            # INHERITED VARIABLES
            tread = int(self.treadC.Value) * scale
            riser = int(self.riserC.Value) * scale
            steps = int(self.numStepsC.Value)
            


            
            # LOCAL VARIABLES
            tol = sc.doc.ModelAbsoluteTolerance
            xformRiser = r.Geometry.Transform.Translation(r.Geometry.Vector3d(0,0,-abs(riser)))
            stairLofts = []
            endCrv = []
            worldXY = r.Geometry.Plane.WorldXY
            
            ###########
            
            

                 
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
                startCrv = offsetCrv1[0]
        
            #join breps together
            joinedBrep = r.Geometry.Brep.JoinBreps(stairLofts, tol)
            #Cap ends
            stairs = (joinedBrep[0]).CapPlanarHoles(tol)

            #Add to document
            docObj = sc.doc.Objects.AddBrep(stairs)
            rs.ObjectName(docObj, "37DNW&T8BWXmZG^$g&Qjfrciv2E495opp@PzZYQhbBYgjsD4Gs")
            #sc.doc.Objects.AddBrep(brep[0])
            startCrv = startCrvRef
            rs.EnableRedraw(True)

        def handrailGen(self, sender, e):
            
            rs.EnableRedraw(False)
            
            
            # Variables
            global startCrv
            worldXY = r.Geometry.Plane.WorldXY
            tol = sc.doc.ModelAbsoluteTolerance
            angTol = sc.doc.ModelAngleToleranceRadians
            sideOffset01 = self.handrailOffsetC.Value * scale
            sideOffset02 = (startCrv.GetLength()) - ((self.handrailOffsetC.Value) * scale)
            lowXForm = r.Geometry.Transform.Translation(r.Geometry.Vector3d(0,0,(-abs((self.riserC.Value * self.numStepsC.Value)* scale))))
            
            
            #Calc distance between upper and lower upright for handrail
            handrailLengthOuter = ((self.treadC.Value) * ((self.numStepsC.Value) + 1)) * scale
            handrailLengthInner = ((self.treadC.Value) * .5) * scale
            handrailExt = self.handrailExtensionC.Value * scale

            offsetCrvLow = startCrv.Offset(worldXY, handrailLengthOuter, tol, r.Geometry.CurveOffsetCornerStyle.Sharp)
            offsetCrvLow[0].Transform(lowXForm) #Moving lower line to lower ground position
            offsetCrvLowH = offsetCrvLow[0].Offset(worldXY, handrailExt, tol, r.Geometry.CurveOffsetCornerStyle.Sharp)
            
            offsetCrvHigh = startCrv.Offset(worldXY, handrailLengthInner, tol, r.Geometry.CurveOffsetCornerStyle.Sharp)
            offsetCrvHigh1 = offsetCrvHigh[0].Offset(worldXY, ((self.treadC.Value / 2) * scale), tol, r.Geometry.CurveOffsetCornerStyle.Sharp)
            
            
            # Creat Lower Points for handrail uprights
            pt01 = offsetCrvLow[0].PointAtLength(sideOffset01)
            pt03 = offsetCrvHigh[0].PointAtLength(sideOffset01)
            pt031 = offsetCrvHigh1[0].PointAtLength(sideOffset01)
            
            
            # Create upper points fir handrail uprights
            pt11 = pt01 + (r.Geometry.Vector3d(0,0,((self.handrailHeightC.Value) * scale)))
            pt33 = pt03 + (r.Geometry.Vector3d(0,0,((self.handrailHeightC.Value) * scale)))
            pt031 = pt031 + (r.Geometry.Vector3d(0,0,((self.handrailHeightC.Value) * scale)))
            
            # Handrail Points
            ptH01 = offsetCrvLowH[0].PointAtLength(sideOffset01) + (r.Geometry.Vector3d(0,0,((self.handrailHeightC.Value) * scale)))
            ptH02 = startCrv.PointAtLength(sideOffset01) + (r.Geometry.Vector3d(0,0,((self.handrailHeightC.Value) * scale)))
            vecH01 = (r.Geometry.Vector3d((ptH01 - pt11)))
            vecH01.Unitize()
   
            # Build handril bone curve
            cPts = (pt01, pt11, pt031, pt33, pt03)
            handrailBone = r.Geometry.Curve.CreateControlPointCurve(cPts, 1)
            botHandExt = r.Geometry.Curve.CreateControlPointCurve((pt11, ptH01),1)
            topHandExt = r.Geometry.Curve.CreateControlPointCurve((pt33, ptH02),1)
            
            sc.doc.Objects.AddCurve(handrailBone)



            
            
            
            ############ HANDRAIL END MODIFIERS ###################
            
            modSel = self.handrailTypeC.SelectedIndex
            vecHandrailCopy = (r.Geometry.Vector3d((startCrv.PointAtEnd + startCrv.PointAtEnd)))
            vecHandrailCopy.Unitize()
            print vecHandrailCopy

 
            # HANDRAIL 00
            def handrail00(pt01, pt02, botCrv, topCrv):
                pt03 = pt01 + (r.Geometry.Vector3d(0,0,((-abs(self.handrailDiameterC.Value * 2)) * scale)))
                pt04 = (pt01 + (vecH01 * ((self.handrailDiameterC.Value) * scale)))
                pt04 = pt04 - r.Geometry.Vector3d(0, 0, (self.handrailDiameterC.Value * scale))
                HCurve01 = r.Geometry.ArcCurve(r.Geometry.Arc(pt01, pt04, pt03))
                joined01 = r.Geometry.Curve.JoinCurves((botCrv, HCurve01), tol)
                sc.doc.Objects.AddCurve(joined01[0])
                
                vecH01.Reverse()
                
                pt05 = pt02 + (r.Geometry.Vector3d(0,0,((-abs(self.handrailDiameterC.Value * 2)) * scale)))
                pt06 = (pt02 + (vecH01 * ((self.handrailDiameterC.Value) * scale)))
                pt06 = pt06 - r.Geometry.Vector3d(0, 0, (self.handrailDiameterC.Value * scale))
                HCurve02 = r.Geometry.ArcCurve(r.Geometry.Arc(pt02, pt06, pt05))
                joined02 = r.Geometry.Curve.JoinCurves((topCrv, HCurve02), tol)
                
                sc.doc.Objects.AddCurve(joined02[0])
                
                return joined01, joined02
#                
#                
#            def handrail01(hCurve):
#                
#            def handrail02(hCurve):
#                
#            def handrail03(hCurve):
            if modSel == 0:
                hCrv1, hCrv2 = handrail00(ptH01, ptH02, botHandExt, topHandExt)
                pipe1 = r.Geometry.Brep.CreatePipe(handrailBone, (((self.handrailDiameterC.Value) / 2) * scale), True, r.Geometry.PipeCapMode.Flat, True, 0.001, angTol)
                pipe2 = r.Geometry.Brep.CreatePipe(hCrv1[0], (((self.handrailDiameterC.Value) / 2) * scale), True, r.Geometry.PipeCapMode.Flat, True, 0.001, angTol)
                pipe3 = r.Geometry.Brep.CreatePipe(hCrv2[0], (((self.handrailDiameterC.Value) / 2) * scale), True, r.Geometry.PipeCapMode.Flat, True, 0.001, angTol)
                
                pipes01 = (pipe1[0], pipe2[0], pipe3[0])
                
                pipes02 = (pipe1[0].Duplicate, pipe2[0].Duplicate, pipe3[0].Duplicate)
                for i in pipes02:
                    translation = r.Geometry.Transform.Translation(vecHandrailCopy)
                    i.Transform(translation)
                    sc.doc.Objects.AddBrep(i)
                
                
#            if modSel == 1:
#                handrail01()
#            if modSel == 2:
#                handrail02()
#            if modsel == 3:
#                handrail03()
#            
#           
            
            
            rs.EnableRedraw(True)
            
            
            return

        ##########################################################################################

        # Close button click handler
        def OnCloseButtonClick(self, sender, e):
            pRev = rs.ObjectsByName("37DNW&T8BWXmZG^$g&Qjfrciv2E495opp@PzZYQhbBYgjsD4Gs")
            if len(pRev) > 0:
                for i in pRev:
                    rs.DeleteObject(i)
            self.Close(False)

        # close x button handler
        def OnFormClosed(self, sender, e):
            pRev = rs.ObjectsByName("37DNW&T8BWXmZG^$g&Qjfrciv2E495opp@PzZYQhbBYgjsD4Gs")
            if len(pRev) > 0:
                for i in pRev:
                    rs.DeleteObject(i)
            self.Close(False)

        # OK button click handler
        def OnOKButtonClick(self, sender, e):
            pRev = rs.ObjectsByName("37DNW&T8BWXmZG^$g&Qjfrciv2E495opp@PzZYQhbBYgjsD4Gs")
            if len(pRev) > 0:
                for i in pRev:
                    rs.ObjectName(i, "www.landarchtools.com")
            self.Close(True)
            
        #Flip Button handler
        def flipChecked(self, sender, e):
            flip = self.flipC.Checked
            if flip == True: #Defulat is always off so this doesnt require further logic
                startCrv.Reverse()
            if flip == False:
                startCrv.Reverse()
                


    ################################################################################
    
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
    
    ##################################################################################################
    
    # GLOBAL VARIABLES
    
    #Scale System
    def scaling():
        unitNum= int(sc.doc.ModelUnitSystem)
        unitSystem = System.Enum.ToObject(r.UnitSystem, unitNum) # struct unit system for current file
        internalSystem = System.Enum.ToObject(r.UnitSystem, 2) # struct unitsystem obj for script use
        scale = r.RhinoMath.UnitScale(internalSystem, unitSystem)# Scale units to model units
        return scale
    scale = scaling()
    
    # CURVE HEALTH CHECK
    global startCrv
    crvBool = crvCheck(startCrv)
    if crvBool == False:
        return False
    
    # The script that will be using the dialog.
    def RequestStairGen():  # This will call the eto form and assign it as a daughter window of rhino
        dialog = StairGenDialog()  # sets the ETO form to dialog variable
        rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow) # Launches UI as modal daughter of rhino window

    ################################################################################

    RequestStairGen()

# GLOBAL VALUES
startCrv = rs.coercecurve(rs.GetObject(message="Select the curve to used at the top level step", filter=4, preselect=True, select=False, custom_filter=None, subobjects=False))

if __name__ == "__main__":
    StairGen()
