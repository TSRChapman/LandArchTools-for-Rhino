"""

Copyright <2022> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# Calculate grade between two given points
# By Thomas Chapman on 11/01/2021
# Update Thomas Chapman on 31/07/2021

import rhinoscriptsyntax as rs
import math as m
import scriptcontext as sc
import System
import Rhino as r
import Rhino.Input as ri
import Rhino.Commands as rc
import Rhino.Geometry as rg


# Determine Unit system and scale m input to unit system scale and close if not mm, cm, m


def CalcGrade():

    try:
        scale, imperial = scaling()

        # Colours
        pinkColour = System.Drawing.Color.FromArgb(255, 0, 133)
        blueColour = System.Drawing.Color.FromArgb(82, 187, 209)
        greyColour = System.Drawing.Color.FromArgb(216, 220, 219)
        blackColour = System.Drawing.Color.FromArgb(0, 0, 0)

        def GetPointDynamicDrawFunc(sender, args):
            # draw a line from the first picked point to the current mouse point
            currentPoint = args.CurrentPoint

            if currentPoint.Z == 0:
                projectedPoint = rg.Point3d(currentPoint.X, currentPoint.Y, pt1.Z)
                line01 = rg.Line(pt1, currentPoint)
                line02 = rg.Line(currentPoint, projectedPoint)
                line03 = rg.Line(projectedPoint, pt1)
                midPoint01 = line01.PointAt(0.5)
                circle = rg.Circle(pt1, line03.Length)
                args.Display.DrawCircle(circle, blackColour, 2)
                args.Display.DrawLine(line01, blueColour, 4)
                args.Display.DrawDot(midPoint01, "No Grade", greyColour, blackColour)

            else:
                projectedPoint = rg.Point3d(currentPoint.X, currentPoint.Y, pt1.Z)
                line01 = rg.Line(pt1, currentPoint)
                line02 = rg.Line(currentPoint, projectedPoint)
                line03 = rg.Line(projectedPoint, pt1)
                midPoint01 = line01.PointAt(0.5)
                circle = rg.Circle(pt1, line03.Length)

                # Calculate grade
                hypotenuse = rs.Distance(pt1, currentPoint)

                # Find the rise of given points in any order
                if pt1.Z > currentPoint.Z:  # this is the negative direction
                    rise = pt1.Z - currentPoint.Z
                elif pt1.Z < currentPoint.Z:
                    rise = currentPoint.Z - pt1.Z  # this is the positive direction

                # Find the run of given points
                run = m.sqrt(hypotenuse**2 - rise**2)

                # Detect model units and scale to mm, if mm do nothing
                rise = rise * scale
                run = run * scale

                grade = run / rise
                if imperial == True:
                    grade = (1 / grade) * 100
                    gradeText = str(abs(round(grade, 2))) + "%"
                else:
                    gradeText = "1:" + str(abs(round(grade, 2)))
                rs.EnableRedraw(True)

                args.Display.DrawCircle(circle, blackColour, 2)
                args.Display.DrawLine(line01, blueColour, 4)
                args.Display.DrawLine(line02, pinkColour, 5)
                args.Display.DrawLine(line03, blueColour, 4)
                args.Display.DrawDot(midPoint01, gradeText, greyColour, blackColour)

        # Get first point
        gp = ri.Custom.GetPoint()
        gp.Get()
        if gp.CommandResult() == rc.Result.Success:
            pt1 = gp.Point()
            gp.DynamicDraw += GetPointDynamicDrawFunc
            gp.Get()
            if gp.CommandResult() == rc.Result.Success:
                pt2 = gp.Point()
            else:
                print("Failed to get Second Point")
                return False
        else:
            print("Failed to get First Point")
            return False

        if pt1:
            if pt2:
                rs.EnableRedraw(False)
                hypotenuse = rs.Distance(pt1, pt2)

                # Find the rise of given points in any order
                if pt1.Z == pt2.Z:
                    rs.EnableRedraw(True)
                    print("No Grade Found")
                    return
                if pt1.Z > pt2.Z:
                    rise = pt1.Z - pt2.Z
                elif pt1.Z < pt2.Z:
                    rise = pt2.Z - pt1.Z

                # Find the run of given points
                run = m.sqrt(hypotenuse**2 - rise**2)

                # Detect model units and scale to mm, if mm do nothing
                rise = rise * scale
                run = run * scale
                # Calculate grade based on rise and run
                try:
                    grade = run / rise

                except ZeroDivisionError:
                    print("No Grade Found")
                    rs.EnableRedraw(True)
                    exit()

                # Print text dot to screen
                curve = rs.AddCurve([pt1, pt2])
                midpoint = rs.CurveMidPoint(curve)
                rs.DeleteObject(curve)
                if imperial == True:
                    grade = (1 / grade) * 100
                    rs.AddTextDot(str(abs(round(grade, 2))) + "%", midpoint)
                else:
                    rs.AddTextDot("1:" + str(abs(round(grade, 2))), midpoint)
                rs.EnableRedraw(True)

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return

def scaling():
    try:
        unitNum = int(sc.doc.ModelUnitSystem)
        # check to see if using metric
        if (
            unitNum != 1
            and unitNum != 2
            and unitNum != 3
            and unitNum != 4
            and unitNum != 5
        ):
            imperial = True
        else:
            imperial = False
        # struct unit system for current file
        unitSystem = System.Enum.ToObject(r.UnitSystem, unitNum)
        # struct unitsystem obj for script use, using mm (2)
        internalSystem = System.Enum.ToObject(r.UnitSystem, 2)
        # Scale units to model units
        scale = r.RhinoMath.UnitScale(internalSystem, unitSystem)
        if scale:
            return scale, imperial
    except:
        print("Failed to find system scale")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    CalcGrade()
