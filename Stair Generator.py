# Imports
import System
import Rhino.UI
import Eto.Drawing as drawing
import Eto.Forms as forms
import rhinoscriptsyntax as rs

################################################################################

# SampleEtoRoomNumber dialog class
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
        #Stair gen label
        self.stairGenLabel = forms.Label(Text = 'STAIR GENERATOR')
        
        #Gen Handrail label
        self.genStairLabel = forms.Label(Text = 'Generate Stair?:')
        #Gen Handrail control
        self.genStairBool = forms.CheckBox()
        self.genStairBool.Checked = False
        self.genStairBool.CheckedChanged += self.stairGen
        
        #Number of Steps Label
        self.numStepsLabel = forms.Label(Text = 'Number of steps:')
        #Number of Steps control
        self.numStepsC = forms.NumericStepper()
        self.numStepsC.DecimalPlaces = 0
        self.numStepsC.Increment = 1
        self.numStepsC.MaxValue = 100
        self.numStepsC.MinValue = 2
        self.numStepsC.Value = 3
        self.numStepsC.ValueChanged += self.stairGen
        self.numStepsC.ValueChanged += self.handrailGen

        
        #Tread label
        self.treadLabel = forms.Label(Text = 'Tread (mm):')
        #Tread length control
        self.treadC = forms.NumericStepper()
        self.treadC.DecimalPlaces = 0
        self.treadC.Increment = 1
        self.treadC.MaxValue = 1000
        self.treadC.MinValue = 1
        self.treadC.Value = 300
        self.treadC.ValueChanged += self.stairGen
        self.treadC.ValueChanged += self.handrailGen
        
        #Riser Label
        self.riserLabel = forms.Label(Text = 'Riser (mm):')
        #Tread length control
        self.riserC = forms.NumericStepper()
        self.riserC.DecimalPlaces = 0
        self.riserC.Increment = 1
        self.riserC.MaxValue = 1000
        self.riserC.MinValue = 1
        self.riserC.Value = 150
        self.riserC.ValueChanged += self.stairGen
        self.riserC.ValueChanged += self.handrailGen
        
        #Flip label
        self.flipLabel = forms.Label(Text = 'Flip direction of stairs:')
        #Flip control
        self.flipC = forms.CheckBox()
        self.flipC.CheckedChanged += self.stairGen
        self.flipC.CheckedChanged += self.handrailGen
        
        ###########################################
        #Handrail Gen Label
        self.handrailGenLabel = forms.Label(Text = 'HANDRAIL GENERATOR')
        #self.handrailGenLabel.VerticalAlignment.Center
        
        #Gen Handrail label
        self.genHandrailLabel = forms.Label(Text = 'Generate Handrail?:')
        #Gen Handrail control
        self.genHandrailBool = forms.CheckBox()
        self.genHandrailBool.Checked = False
        self.genHandrailBool.CheckedChanged += self.handrailGen
        
        #Handrail Type Label
        self.handrailTypeLabel = forms.Label(Text = 'Handrail type:')
        #Handrail Type Dropdown
        self.handrailTypeC = forms.DropDown()
        self.handrailTypeC.DataStore = ['180 No Return', '180 Full Return', 'Ground Triangular Return', 'Ground Return', 'Wall Return']
        self.handrailTypeC.SelectedIndex = 0
        self.handrailTypeC.SelectedIndexChanged += self.handrailGen
        
        #Handrail Height Label
        self.handrailHeightLabel = forms.Label(Text = 'Handrail height (mm):')
        #Handrail Height control
        self.handrailHeightC = forms.NumericStepper()
        self.handrailHeightC.DecimalPlaces = 0
        self.handrailHeightC.Increment = 1
        self.handrailHeightC.MaxValue = 5000
        self.handrailHeightC.MinValue = 100
        self.handrailHeightC.Value = 900
        self.handrailHeightC.ValueChanged += self.handrailGen
        
        #Handrail offset label
        self.handrailOffsetLabel = forms.Label(Text = 'Handrail offset from edges (mm):')
        #Handrail offset control
        self.handrailOffsetC = forms.NumericStepper()
        self.handrailOffsetC.DecimalPlaces = 0
        self.handrailOffsetC.Increment = 1
        self.handrailOffsetC.MaxValue = 5000
        self.handrailOffsetC.MinValue = 50
        self.handrailOffsetC.Value = 150
        self.handrailOffsetC.ValueChanged += self.handrailGen
        
        #Handrail extension Label
        self.handrailExtensionLabel = forms.Label(Text = 'Handrail extension (mm):')
        #Handrail extension Control
        self.handrailExtensionC = forms.NumericStepper()
        self.handrailExtensionC.DecimalPlaces = 0
        self.handrailExtensionC.Increment = 1
        self.handrailExtensionC.MaxValue = 5000
        self.handrailExtensionC.MinValue = 300
        self.handrailExtensionC.Value = 300
        self.handrailExtensionC.ValueChanged += self.handrailGen
        
        #Handrail Diameter Label
        self.handrailDiameterLabel = forms.Label(Text = 'Handrail diameter (mm):')
        #Handrail Diameter control
        self.handrailDiameterC = forms.NumericStepper()
        self.handrailDiameterC.DecimalPlaces = 0
        self.handrailDiameterC.Increment = 1
        self.handrailDiameterC.MaxValue = 50
        self.handrailDiameterC.MinValue = 30
        self.handrailDiameterC.Value = 30
        self.handrailDiameterC.ValueChanged += self.handrailGen
        
        # Create the default button
        self.DefaultButton = forms.Button(Text = 'OK')
        self.DefaultButton.Click += self.OnOKButtonClick

        # Create the abort button
        self.AbortButton = forms.Button(Text = 'Cancel')
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

################################################################################

    #Stair Generator Method
    def stairGen(self, sender, e):

        # Variables and defaults
        tread = int(self.treadC.Value) * scale
        riser = int(self.riserC.Value) * scale
        numSteps = int(self.numStepsC.Value)
        flip = self.flipC.Checked
        stairLength = tread * numSteps
        genStair = self.genStairBool.Checked
        curveList = []
        junkList = []

        #get user line for top width of stair
        
        rs.EnableRedraw(False)
        
        if genStair == False:
            iteration = rs.ObjectsByName("GdC9V&^a^rGZZNgiWFH&aTRQLLscu*9AZCmhk8t2!a")
            if iteration:
                rs.DeleteObject(iteration)
                rs.EnableRedraw(True)
                
        if genStair == True:
            #Delete any existing iteration
            iteration = rs.ObjectsByName("GdC9V&^a^rGZZNgiWFH&aTRQLLscu*9AZCmhk8t2!a")
            if iteration:
                rs.DeleteObject(iteration)
            
            topLine = rs.AddLine(line[0],line[1])
            topPoint = line[0]
            stepPoint = topPoint
            
            #get perp line - length of stair
            t = rs.CurveClosestPoint(topLine, topPoint)
            planeNormal = rs.CurveNormal(topLine)
            tangent = rs.CurveTangent(topLine, t)
            curveNormal = rs.VectorCrossProduct(planeNormal, tangent)
            
            # Get vector
            vectorRun = rs.VectorCreate(topPoint, topPoint + curveNormal * tread)
            
            # Bool flip direction of stair (add bool option in GUI)
            if flip == True:
                vector = rs.VectorReverse(vectorRun)
            else:
                vector = vectorRun
                
            # loop through number of steps to gen step curve
            for i in range(numSteps):
                pt01 = rs.AddPoint(stepPoint)
                pt02 = rs.CopyObject(pt01, vector)
                pt03 = rs.CopyObject(pt02, [0,0,riser*-1])
                curve = rs.AddPolyline([pt01,pt02,pt03])
                curveList.append(curve)
                stepPoint = rs.CurveEndPoint(curve)
                rs.DeleteObjects([pt01,pt02,pt03])
            
            # Extrude stair curve to full width
            joinedCurve = rs.JoinCurves(curveList)
            bottomPoint = rs.CopyObject(line[0], [0,0,(riser*numSteps)*-1])
            stairBottom = rs.CurveEndPoint(joinedCurve)
            curve = rs.AddPolyline([line[0],bottomPoint,stairBottom])
            handRailCurve = rs.AddCurve([bottomPoint,stairBottom]) #createhandrail curve and return it
            curveList.append(curve)
            joinedCurves = rs.JoinCurves(curveList)
            stair = rs.ExtrudeCurveStraight(joinedCurves, line[0], line[1])
            rs.CapPlanarHoles(stair)
            #this identifies the generated stair geometry
            rs.ObjectName(stair, "GdC9V&^a^rGZZNgiWFH&aTRQLLscu*9AZCmhk8t2!a") 
            
            # clean up leftover geometry
            junkList.extend([bottomPoint,joinedCurve,joinedCurves, topLine, handRailCurve])
            junkList = junkList + curveList
            rs.DeleteObjects(junkList)
        
            rs.EnableRedraw(True)

    # Handrail Generator Method
    # hType, curve, handrailOffset, tread, riser, numSteps, scale, vectorRun, hHeight, hEndLength, pipeDiameter,
    def handrailGen(self, sender, e):
        
        flip = self.flipC.Checked
        hType = self.handrailTypeC.SelectedIndex
        handrailOffset = int(self.handrailOffsetC.Value) * scale
        tread = int(self.treadC.Value) * scale
        riser = int(self.riserC.Value) * scale
        numSteps = int(self.numStepsC.Value)
        hEndLength = int(self.handrailExtensionC.Value) * scale
        pipeDiameter = int(self.handrailDiameterC.Value) * scale
        hHeight = int(self.handrailHeightC.Value) * scale
        topLine = rs.AddLine(line[0],line[1])
        rs.ObjectName(topLine, "BC6#DT5LCQX*#8r97Tquf5gNF")
        topPoint = line[0]
        genHandrail = self.genHandrailBool.Checked

        rs.EnableRedraw(False)
        if genHandrail == False:
            iteration = rs.ObjectsByName("qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
            if iteration:
                rs.DeleteObjects(iteration)
                rs.EnableRedraw(True)
                
        if genHandrail == True:
            #Delete any existing iteration
            iteration = rs.ObjectsByName("qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
            if iteration:
                rs.DeleteObjects(iteration)
            
            #get perp line - length of stair
            t = rs.CurveClosestPoint(topLine, topPoint)
            planeNormal = rs.CurveNormal(topLine)
            tangent = rs.CurveTangent(topLine, t)
            
            if flip == False:
                curveNormal = rs.VectorCrossProduct(planeNormal, tangent)
            else:
                curveNormal = rs.VectorReverse(rs.VectorCrossProduct(planeNormal, tangent))
            
            # Get guide curve
            scaledV = rs.VectorReverse(rs.VectorScale(curveNormal, tread*numSteps))
            ptGuide1 = rs.AddPoint(line[0])
            ptGuide2 = rs.CopyObject(ptGuide1, scaledV)
            rs.MoveObjects([ptGuide1, ptGuide2], [0,0,(riser*numSteps)*-1])
            curve = rs.AddCurve([ptGuide1, ptGuide2])
            
            #Get vector for step run
            vectorRun = rs.VectorCreate(topPoint, topPoint + curveNormal * tread)
            
            # Setup curves for handrail
            curve1 = curve
            curve2 = rs.MoveObject(rs.CopyObject(curve1, rs.VectorCreate(line[1], 
            rs.CurveStartPoint(curve1))), [0,0,(riser * numSteps)*-1])
            midPoint = rs.CurveMidPoint(userCurve)
            
            # Main slanted handrail curve
            pt1 = rs.MoveObject(rs.MoveObject(rs.CurveStartPoint(curve1), vectorRun), [0,0,hHeight + (riser*numSteps)])
            pt2 = rs.MoveObject(rs.MoveObject(rs.CurveEndPoint(curve1), vectorRun), [0,0,hHeight])
            mainCurve = rs.AddCurve([pt1, pt2])
            
            # Top leveled handrail curve at 300mm standard DDA
            pt3 = rs.CopyObject(pt1, rs.VectorReverse(rs.VectorScale(rs.VectorUnitize(vectorRun), hEndLength)))
            topCurve = rs.AddCurve([pt1, pt3])
            
            # Bottom leveled handrail curve at 300mm standard DDA
            pt4 = rs.CopyObject(pt2, rs.VectorScale(rs.VectorUnitize(vectorRun), hEndLength))
            bottomCurve = rs.AddCurve([pt2, pt4])
            
            # Start list of construction geometry for later cleanup
            hGeoList = [curve1, curve2, pt1, pt2, mainCurve, pt3, topCurve, pt4, bottomCurve, ptGuide1, ptGuide2, curve, topLine]
            
            # IF STATEMENTS FOR HANDRAIL TYPE
            
            # 1 180 degree, no return
            if hType == 0:
                
                # Lower Handrail return
                hpt1 = rs.CopyObject(pt4, [0,0,(pipeDiameter * 2)* -1])
                hpt2 = rs.MoveObject(rs.CopyObject(pt4, [0,0,pipeDiameter * -1]), rs.VectorScale(rs.VectorUnitize(vectorRun), pipeDiameter))
                lowerH = rs.AddArc3Pt(pt4, hpt1, hpt2)
                
                # Upper Handrail return
                hpt3 = rs.CopyObject(pt3, [0,0,(pipeDiameter * 2)* -1])
                hpt4 = rs.MoveObject(rs.CopyObject(pt3, [0,0,pipeDiameter * -1]), rs.VectorReverse(rs.VectorScale(rs.VectorUnitize(vectorRun), pipeDiameter)))
                upperH = rs.AddArc3Pt(pt3, hpt3, hpt4)
                
                # Draw leg upper
                lpt1 = rs.CurveMidPoint(topCurve)
                lpt2 = rs.CopyObject(lpt1, [0,0,hHeight*-1])
                lCurveUpper = rs.AddCurve([lpt1, lpt2])
                
                # Draw leg lower
                lpt3 = rs.CopyObject(pt2, [0,0,hHeight*-1])
                lCurveLower = rs.AddCurve([pt2,lpt3])
                
                # Make vectors to move handrails into place
                moveShort = rs.VectorScale(userVector, handrailOffset)
                moveLong = rs.VectorScale(userVector, rs.CurveLength(userCurve) - (handrailOffset*2))
                
                # Join, offset skeleton
                hCurve = rs.JoinCurves([mainCurve, topCurve, bottomCurve, lowerH, upperH])
                hCurve1 = rs.CopyObject(hCurve, moveShort)
                lCurveUpper1 = rs.CopyObject(lCurveUpper, moveShort)
                lCurveLower1 = rs.CopyObject(lCurveLower, moveShort)
                
                # Pipe skeleton
                pipe1 = rs.AddPipe(hCurve1,0, pipeDiameter/2,blend_type=0, cap = 1)
                pipe2 = rs.AddPipe(lCurveUpper1,0, pipeDiameter/2,blend_type=0, cap = 1)
                pipe3 = rs.AddPipe(lCurveLower1,0, pipeDiameter/2,blend_type=0, cap = 1)
                
                #form list of generated geo
                handrailGeo1 = [pipe1, pipe2, pipe3]

                # Name geo for deletion
                for i in handrailGeo1:
                    rs.ObjectName(i, "qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
                #copy
                handrailGeo2 = rs.CopyObjects(handrailGeo1, moveLong)
                
                # Cleanup construction linework
                hGeoList.extend([hpt1, hpt2, lowerH, hpt3, hpt4, upperH, lpt2, lpt3, lCurveLower, hCurve, hCurve1,
                lCurveUpper1, lCurveLower1, lCurveUpper])
                rs.DeleteObjects(hGeoList)
                
                rs.EnableRedraw(True)
        
            # 2 180 degree, full return
            if hType == 1:
                
                rs.EnableRedraw(False)
                
                # Lower handrail return
                hpt1 = rs.CopyObject(pt4, [0,0,(hEndLength/3)*-2])
                hpt2 = rs.CopyObject(pt2, [0,0,(hEndLength/3)*-2])
                hCurve11 = rs.AddPolyline([pt4, hpt1, hpt2])
                lowerH = rs.JoinCurves([bottomCurve, hCurve11])
                
                # Upper handrail return
                hpt3 = rs.CopyObject(pt3, [0,0,(hEndLength/3)*-2])
                hpt4 = rs.CopyObject(rs.CurveMidPoint(topCurve), [0,0,(hEndLength/3)*-2])
                hCurve2 = rs.AddPolyline([pt3, hpt3, hpt4])
                upperH = rs.JoinCurves([topCurve, hCurve2])
                
                # Draw leg upper
                lpt1 = rs.CurveMidPoint(topCurve)
                lpt2 = rs.CopyObject(lpt1, [0,0,hHeight*-1])
                lCurveUpper = rs.AddCurve([lpt1, lpt2])
                
                # Draw leg lower
                lpt3 = rs.CopyObject(pt2, [0,0,hHeight*-1])
                lCurveLower = rs.AddCurve([pt2,lpt3])
                
                # Make vectors to move handrails into place
                moveShort = rs.VectorScale(userVector, handrailOffset)
                moveLong = rs.VectorScale(userVector, rs.CurveLength(userCurve) - (handrailOffset*2))
                
                # Pipe skeleton move
                hCurve1 = rs.JoinCurves([lowerH, upperH, mainCurve])
                rs.MoveObjects([hCurve1, lCurveUpper, lCurveLower], moveShort)
                
                #Pipe
                pipe1 = rs.AddPipe(hCurve1,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe2 = rs.AddPipe(lCurveUpper,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe3 = rs.AddPipe(lCurveLower,0, pipeDiameter/2, blend_type=0, cap = 1)
                
                handrailGeo1 = [pipe1, pipe2, pipe3]

                # Name geo for deletion
                for i in handrailGeo1:
                    rs.ObjectName(i, "qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
                
                # Move and copy into position
                handrailGeo2 = rs.CopyObjects(handrailGeo1, moveLong)
                
                # Cleanup
                hGeoList.extend([hpt1, hpt2, hCurve11, lowerH, hpt3, hpt4, hCurve2, upperH, lpt2, lCurveUpper, lpt3,
                lCurveLower, hCurve1])
                rs.DeleteObjects(hGeoList)
                
                rs.EnableRedraw(True)
                
            # 3 Ground triangle return
            if hType == 2:
                
                rs.EnableRedraw(False)
                
                # Draw leg upper
                lpt1 = rs.CurveMidPoint(topCurve)
                lpt2 = rs.CopyObject(lpt1, [0,0,hHeight*-1])
                lCurveUpper = rs.AddCurve([lpt1, lpt2])
                
                # Draw leg lower
                lpt3 = rs.CopyObject(pt2, [0,0,hHeight*-1])
                lCurveLower = rs.AddCurve([pt2,lpt3])
                
                # Lower Return
                lowerH = rs.AddCurve([pt4, lpt3])
                
                # Upper Return
                upperH = rs.AddCurve([pt3, lpt2])
                
                # Make vectors to move handrails into place
                moveShort = rs.VectorScale(userVector, handrailOffset)
                moveLong = rs.VectorScale(userVector, rs.CurveLength(userCurve) - (handrailOffset*2))
                
                # Join Curves and move
                hCurve = rs.JoinCurves([mainCurve, topCurve, bottomCurve, lowerH, upperH])
                rs.MoveObjects([hCurve, lCurveUpper, lCurveLower], moveShort)
                
                # pipe
                pipe1 = rs.AddPipe(hCurve,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe2 = rs.AddPipe(lCurveUpper,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe3 = rs.AddPipe(lCurveLower,0, pipeDiameter/2, blend_type=0, cap = 1)
                
                handrailGeo1 = [pipe1, pipe2, pipe3]
                
                # Name geo for deletion
                for i in handrailGeo1:
                    rs.ObjectName(i, "qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
                
                # move and copy into place
                handrailGeo2 = rs.CopyObjects(handrailGeo1, moveLong)
                
                # Cleanup
                hGeoList.extend([lpt2, lCurveUpper, lpt3, lCurveLower, lowerH, upperH, hCurve, topLine])
                rs.DeleteObjects(hGeoList)
                
                rs.EnableRedraw(True)
                
            # 4 Ground return
            
            if hType == 3:
                
                rs.EnableRedraw(False)
                
                # Draw leg upper
                lpt1 = rs.CurveMidPoint(topCurve)
                lpt2 = rs.CopyObject(lpt1, [0,0,hHeight*-1])
                lCurveUpper = rs.AddCurve([lpt1, lpt2])
                
                # Draw leg lower
                lpt3 = rs.CopyObject(pt2, [0,0,hHeight*-1])
                lCurveLower = rs.AddCurve([pt2,lpt3])
                
                # Lower Return
                hpt1 = rs.CopyObject(pt4, [0,0,hHeight*-1])
                hCurve1 = rs.AddCurve([pt4, hpt1])
                
                # Upper Return
                hpt2 = rs.CopyObject(pt3, [0,0,hHeight*-1])
                hCurve2 = rs.AddCurve([pt3, hpt2])
                
                # Join curves
                hCurve = rs.JoinCurves([mainCurve, topCurve, bottomCurve, hCurve1, hCurve2])
                
                # Get Vectors
                moveShort = rs.VectorScale(userVector, handrailOffset)
                moveLong = rs.VectorScale(userVector, rs.CurveLength(userCurve) - (handrailOffset*2))
                
                #move
                rs.MoveObjects([hCurve, lCurveUpper, lCurveLower], moveShort)
                
                # Pipe
                pipe1 = rs.AddPipe(hCurve,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe2 = rs.AddPipe(lCurveUpper,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe3 = rs.AddPipe(lCurveLower,0, pipeDiameter/2, blend_type=0, cap = 1)
                
                handrailGeo1 = [pipe1, pipe2, pipe3]
                
                # Name geo for deletion
                for i in handrailGeo1:
                    rs.ObjectName(i, "qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
                    
                # move and copy into place
                handrailGeo2 = rs.CopyObjects(handrailGeo1, moveLong)
                
                # Clean up
                hGeoList.extend([lpt2, lCurveUpper, lpt3, lCurveLower, hpt1, hCurve1, hpt2, hCurve2, hCurve, topLine])
                rs.DeleteObjects(hGeoList)
                
                rs.EnableRedraw(True)
        
            # 5 Wall return
            if hType == 4:
                
                rs.EnableRedraw(False)
                
                # Draw leg upper
                lpt1 = rs.CurveMidPoint(topCurve)
                lpt2 = rs.CopyObject(lpt1, [0,0,hHeight*-1])
                lCurveUpper = rs.AddCurve([lpt1, lpt2])
                
                # Draw leg lower
                lpt3 = rs.CopyObject(pt2, [0,0,hHeight*-1])
                lCurveLower = rs.AddCurve([pt2,lpt3])
                
                #get vectors
                vector1 =  rs.VectorScale(rs.VectorUnitize(rs.VectorReverse(userVector)), handrailOffset)
                vector2 = rs.VectorScale(userVector, rs.CurveLength(userCurve))
                
                # Lower Return
                hpt1 = rs.CopyObject(pt4, vector1)
                hCurve1 = rs.AddCurve([pt4, hpt1])
                
                # Upper Return
                hpt2 = rs.CopyObject(pt3, vector1)
                hCurve2 = rs.AddCurve([pt3, hpt2])
                
                # Join main curves
                hCurveMain1 = rs.JoinCurves([mainCurve, topCurve, bottomCurve])
                
                # Get Vectors
                moveShort = rs.VectorScale(userVector, handrailOffset)
                moveLong = rs.VectorScale(userVector, rs.CurveLength(userCurve) - handrailOffset)
                
                # Copy hanrail 2
                hCurveMain2 = rs.CopyObject(hCurveMain1, moveLong)
                hCurve3 = rs.CopyObject(hCurve1, vector2)
                hCurve4 = rs.CopyObject(hCurve2, vector2)
                lCurveUpper2 = rs.CopyObject(lCurveUpper, moveLong)
                lCurveLower2 = rs.CopyObject(lCurveLower, moveLong)
                
                # Join curves
                hCurveJoined1 = rs.JoinCurves([hCurve1, hCurve2, hCurveMain1])
                hCurveJoined2 = rs.JoinCurves([hCurveMain2, hCurve3, hCurve4,])
                
                # Pipe
                pipe1 = rs.AddPipe(hCurveJoined1,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe2 = rs.AddPipe(lCurveLower,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe3 = rs.AddPipe(lCurveUpper,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe4 = rs.AddPipe(hCurveJoined2,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe5 = rs.AddPipe(lCurveUpper2,0, pipeDiameter/2, blend_type=0, cap = 1)
                pipe6 = rs.AddPipe(lCurveLower2,0, pipeDiameter/2, blend_type=0, cap = 1)
                
                handrailGeo1 = [pipe1, pipe2, pipe3, pipe3, pipe4, pipe5, pipe6]
                
                # Name geo for deletion
                for i in handrailGeo1:
                    rs.ObjectName(i, "qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
                
                # Move handrail 1 into place
                rs.MoveObjects([pipe1, pipe2, pipe3], moveShort)
                
                # Cleanup
                hGeoList.extend([lpt2, lCurveUpper, lpt3, lCurveLower, hpt1, hCurve1, hpt2, hCurve2, hCurveMain1, hCurveMain2, hCurve3,
                hCurve4, lCurveUpper2, lCurveLower2, hCurveJoined1, hCurveJoined2])
                rs.DeleteObjects(hGeoList)
                
                rs.EnableRedraw(True)

    # Close button click handler
    def OnCloseButtonClick(self, sender, e):
        generatedStair = rs.ObjectsByName("GdC9V&^a^rGZZNgiWFH&aTRQLLscu*9AZCmhk8t2!a")
        generatedHandrail = rs.ObjectsByName("qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
        rs.DeleteObjects(rs.ObjectsByName("xAbJgNV6^bz6azN&6E$Q^WeX$Dd^vygCz5z7Hmynb5"))
        rs.DeleteObjects(rs.ObjectsByName("BC6#DT5LCQX*#8r97Tquf5gNF"))
        if generatedStair:
            rs.DeleteObject(generatedStair)
        if generatedHandrail:
            rs.DeleteObjects(generatedHandrail)
        self.Close(False)

    # close x button handler
    def OnFormClosed(self, sender, e):
        generatedStair = rs.ObjectsByName("GdC9V&^a^rGZZNgiWFH&aTRQLLscu*9AZCmhk8t2!a")
        generatedHandrail = rs.ObjectsByName("qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
        rs.DeleteObjects(rs.ObjectsByName("xAbJgNV6^bz6azN&6E$Q^WeX$Dd^vygCz5z7Hmynb5"))
        rs.DeleteObjects(rs.ObjectsByName("BC6#DT5LCQX*#8r97Tquf5gNF"))
        if generatedStair:
            rs.DeleteObject(generatedStair)
        if generatedHandrail:
            rs.DeleteObjects(generatedHandrail)
        self.Close(False)

    # OK button click handler
    def OnOKButtonClick(self, sender, e):
        #remove object name to avoid deletion
        generatedStair = rs.ObjectsByName("GdC9V&^a^rGZZNgiWFH&aTRQLLscu*9AZCmhk8t2!a")
        generatedHandrail = rs.ObjectsByName("qe7g&G5LzXEvbudtPT8xCxQbisusFVqCPqMsiHK2jc")
        rs.DeleteObjects(rs.ObjectsByName("xAbJgNV6^bz6azN&6E$Q^WeX$Dd^vygCz5z7Hmynb5"))
        rs.DeleteObjects(rs.ObjectsByName("BC6#DT5LCQX*#8r97Tquf5gNF"))
        if generatedStair:
            rs.ObjectName(generatedStair, name="www.landarchtools.com")
        if generatedHandrail:
            rs.ObjectName(generatedHandrail, name="www.landarchtools.com")

        self.Close(True)


################################################################################

#Get scale factor and abort if not in mm cm or m
system = rs.UnitSystem()
if system == 2 or system == 3 or system == 4:
    scaleFactorDict = {2:1, 3:0.1, 4:0.001}
    scaleFactor = scaleFactorDict[system]
    scale = scaleFactor
else:
    rs.MessageBox("change document to use mm, cm or m")
    exit()

#Get stair width
line = rs.GetLine(mode=1,message1="Pick two points to define top step width")
line[1].Z = line[0].Z
userCurve = rs.AddLine([line[0].X, line[0].Y, line[0].Z], [line[1].X, line[1].Y, line[0].Z])
userVector = rs.VectorUnitize(rs.VectorCreate((line[1].X, line[1].Y, line[0].Z), (line[0].X, line[0].Y, line[0].Z)))
rs.ObjectName(userCurve, "xAbJgNV6^bz6azN&6E$Q^WeX$Dd^vygCz5z7Hmynb5")

# The script that will be using the dialog.
def RequestStairGen(): # This will call the eto form and assign it as a daughter window of rhino
    dialog = StairGenDialog(); # sets the ETO form to dialog variable
    rc = dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow) # Launches UI as modal daughter of rhino window


################################################################################

RequestStairGen()