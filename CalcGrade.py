
'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Calculate grade between two given points
# By Thomas Chapman on 11/01/2021

import rhinoscriptsyntax as rs
import math as m
import scriptcontext as sc
import System
import Rhino as r


# Determine Unit system and scale m input to unit system scale and close if not mm, cm, m


def CalcGrade():

    try:
        scale = scaling()

        # Get points from user
        pt1 = rs.GetPoint('Pick the first point')
        pt2 = rs.GetPoint('Pick the second point')
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
                rise = rise*scale
                run = run*scale
                # Calculate grade based on rise and run
                try:
                    grade = run / rise

                except ZeroDivisionError:
                    print('No Grade Found')
                    rs.EnableRedraw(True)
                    exit()

                # Print text dot to screen
                curve = rs.AddCurve([pt1, pt2])
                midpoint = rs.CurveMidPoint(curve)
                rs.DeleteObject(curve)
                rs.AddTextDot('1:' + str(abs(round(grade, 2))), midpoint)
                rs.EnableRedraw(True)

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return

def scaling():
    try:
        unitNum= int(sc.doc.ModelUnitSystem)
        unitSystem = System.Enum.ToObject(r.UnitSystem, unitNum) # struct unit system for current file
        internalSystem = System.Enum.ToObject(r.UnitSystem, 2) # struct unitsystem obj for script use
        scale = r.RhinoMath.UnitScale(internalSystem, unitSystem)# Scale units to model units
        if scale:
            return scale
    except:
        print ("Failed to find system scale")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    CalcGrade()
