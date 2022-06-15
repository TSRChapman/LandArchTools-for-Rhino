"""

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# Get Coordinates

import rhinoscriptsyntax as rs
import Rhino.Input as ri
import scriptcontext
import Rhino.Geometry as rg
import Rhino.UI as ui
import Rhino.Commands as rc


def GetCoordinate():
    try:

        def GetPointDynamicDrawFunc(sender, args):
            # draw a line from the first picked point to the current mouse point
            point = args.CurrentPoint
            pointX = round(point.X, 3)
            pointY = round(point.Y, 3)
            pointZ = round(point.Z, 3)
            # store string in variable
            coord = "E " + str(pointX) + " N " + str(pointY) + " Z " + str(pointZ)
            ui.MouseCursor.SetToolTip(coord)

        # Create an instance of a GetPoint class and add a delegate
        # for the DynamicDraw event
        gp = ri.Custom.GetPoint()
        gp.DynamicDraw += GetPointDynamicDrawFunc
        gp.Get()
        if gp.CommandResult() == rc.Result.Success:
            pt = gp.Point()

            pointX = round(pt.X, 3)
            pointY = round(pt.Y, 3)
            pointZ = round(pt.Z, 3)

            rs.AddTextDot(
                "E " + str(pointX) + " N " + str(pointY) + " Z " + str(pointZ), pt
            )
            coord = "E " + str(pointX) + " N " + str(pointY) + " Z " + str(pointZ)
            rs.ClipboardText(coord)
            scriptcontext.doc.Views.Redraw()

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    GetCoordinate()
