"""

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# MOVE OBJECT TO SPECIFIED RL
# BY THOMAS CHAPMAN ON 12/06/2022

import rhinoscriptsyntax as rs
import Rhino.Geometry as geo
import Rhino as r
import System
import scriptcontext as sc


def MoveToRL():
    try:

        scale, imperial = scaling()

        obj = rs.GetObjects("Select objects", preselect=True)
        if obj:
            current = rs.GetPoint("Select point")

            if current:

                if imperial == False:
                    rl = rs.GetString("RL (m) to move to?")
                if imperial == True:
                    rl = rs.GetString("RL (ft) to move to?")
                rl = float(rl)
                rl = rl * scale

                if rl == 0:  # move objects to the 0 coord
                    target3 = current.Z
                    if target3:
                        target3 = target3 * -1
                        target4 = r.Geometry.Point3d(0, 0, target3)
                        rs.MoveObject(obj, target4)

                elif rl < 0:
                    target5 = rl - current.Z
                    target6 = r.Geometry.Point3d(0, 0, target5)
                    rs.MoveObject(obj, target6)

                elif rl > 0:
                    target = rl - current.Z  # + or - number to target location
                    # translated vector needed to hit target
                    target2 = r.Geometry.Point3d(0, 0, target)
                    rs.MoveObject(obj, target2)

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
    MoveToRL()
