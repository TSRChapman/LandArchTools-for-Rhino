"""

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


# Show RL of specified point and copy to clipboard
# By Thomas Chapman on 01/10/2021

import rhinoscriptsyntax as rs
import scriptcontext as sc
import System
import Rhino as r
import Rhino.Input as ri
import Rhino.Commands as rc
import Rhino.Geometry as rg


def ShowRL():
    try:

        scale, imperial = scaling()
        def GetPointDynamicDrawFunc(sender, args):
            point = args.CurrentPoint

            circle = rg.Circle(point, 1 * scale)
            line01 = rg.Line(point, rg.Point3d(point.X + (1 * scale), point.Y, point.Z))
            line02 = rg.Line(point, rg.Point3d(point.X - (1 * scale), point.Y, point.Z))
            line03 = rg.Line(point, rg.Point3d(point.X, point.Y + (1 * scale), point.Z))
            line04 = rg.Line(point, rg.Point3d(point.X, point.Y - (1 * scale), point.Z))
            midpoint = line03.PointAt(0.5)

            if imperial == False:
                rl = "+RL " + str(round(point.Z * scale, 3)) + " m"
            if imperial == True:
                rl = "+RL " + str(round(point.Z * scale, 3)) + " ft"

            args.Display.DrawLine(line01, blueColour, 4)
            args.Display.DrawLine(line02, blueColour, 4)
            args.Display.DrawLine(line03, blueColour, 4)
            args.Display.DrawLine(line04, blueColour, 4)
            args.Display.DrawCircle(circle, pinkColour, 2)
            args.Display.DrawDot(midpoint, str(rl), greyColour, blackColour)

        pinkColour = System.Drawing.Color.FromArgb(255, 0, 133)
        blueColour = System.Drawing.Color.FromArgb(82, 187, 209)
        greyColour = System.Drawing.Color.FromArgb(216, 220, 219)
        blackColour = System.Drawing.Color.FromArgb(0, 0, 0)

        gp = ri.Custom.GetPoint()
        gp.DynamicDraw += GetPointDynamicDrawFunc
        gp.Get()
        if gp.CommandResult() == rc.Result.Success:
            point = gp.Point()

            if point:
                pointZ = point.Z
            pointZ = pointZ * scale

            if imperial == False:
                textDot = rs.AddTextDot("+RL " + str(round(pointZ, 3)) + " m", point)
            if imperial == True:
                textDot = rs.AddTextDot("+RL " + str(round(pointZ, 3)) + " ft", point)

            # Add user key and value for later identification
            rs.SetUserText(textDot, "LandArchTools", "RLTextDot", True)


            # Copy RL to Clipboard
            RL = str(round(pointZ, 3))
            rs.ClipboardText(RL)

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
            # struct unit system for cu2rrent file
            unitSystem = System.Enum.ToObject(r.UnitSystem, unitNum)
            # struct unitsystem obj for script use, using feet (9)
            internalSystem = System.Enum.ToObject(r.UnitSystem, 9)
            # Scale units to model units
            scale = r.RhinoMath.UnitScale(internalSystem, unitSystem)
            if scale:
                return scale, imperial
        else:
            imperial = False
            # struct unit system for current file
            unitSystem = System.Enum.ToObject(r.UnitSystem, unitNum)
            # struct unitsystem obj for script use, using meteres (4)
            internalSystem = System.Enum.ToObject(r.UnitSystem, 4)
            # Scale units to model units
            scale = r.RhinoMath.UnitScale(internalSystem, unitSystem)
            if scale:
                return scale, imperial
    except:
        print("Failed to find system scale")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    ShowRL()
