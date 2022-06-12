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


def ShowRL():
    try:

        scale, imperial = scaling()

        point = rs.GetPoint("Select point")

        if point:
            pointZ = point.Z
        pointZ = pointZ * scale

        if imperial == False:
            rs.AddTextDot("+RL " + str(round(pointZ, 3)) + " m", point)
        if imperial == True:
            rs.AddTextDot("+RL " + str(round(pointZ, 3)) + " ft", point)

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
            # struct unit system for current file
            unitSystem = System.Enum.ToObject(r.UnitSystem, unitNum)
            # struct unitsystem obj for script use, using feet (9)
            internalSystem = System.Enum.ToObject(r.UnitSystem, 9)
            # Scale units to model units
            scale = r.RhinoMath.UnitScale(unitSystem, internalSystem)
            if scale:
                return scale, imperial
        else:
            imperial = False
            # struct unit system for current file
            unitSystem = System.Enum.ToObject(r.UnitSystem, unitNum)
            # struct unitsystem obj for script use, using meteres (4)
            internalSystem = System.Enum.ToObject(r.UnitSystem, 4)
            # Scale units to model units
            scale = r.RhinoMath.UnitScale(unitSystem, internalSystem)
            if scale:
                return scale, imperial
    except:
        print("Failed to find system scale")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    ShowRL()
