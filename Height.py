"""

Copyright <2022> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""


import rhinoscriptsyntax as rs
import Rhino.Input as ri
import Rhino.Geometry as rg
import Rhino.Commands as rc
import System.Drawing.Color


def Height():
    try:

        def GetPointDynamicDrawFunc(sender, args):
            # draw a line from the first picked point to the current mouse point
            currentPoint = args.CurrentPoint
            projectedPoint = rg.Point3d(currentPoint.X, currentPoint.Y, pt01.Z)
            line01 = rg.Line(pt01, currentPoint)
            line02 = rg.Line(currentPoint, projectedPoint)
            line03 = rg.Line(projectedPoint, pt01)
            midPoint = line02.PointAt(0.5)
            circle = rg.Circle(pt01, line03.Length)

            height = str(round(abs(pt01.Z - currentPoint.Z), 3))

            args.Display.DrawCircle(circle, greyColour, 2)
            args.Display.DrawLine(line01, blueColour, 4)
            args.Display.DrawLine(line02, pinkColour, 5)
            args.Display.DrawLine(line03, blueColour, 4)
            args.Display.DrawDot(midPoint, height, greyColour, pinkColour)

        pinkColour = System.Drawing.Color.FromArgb(255, 0, 133)
        blueColour = System.Drawing.Color.FromArgb(82, 187, 209)
        greyColour = System.Drawing.Color.FromArgb(216, 220, 219)

        gp = ri.Custom.GetPoint()
        gp.Get()
        if gp.CommandResult() == rc.Result.Success:
            pt01 = gp.Point()
            gp.DynamicDraw += GetPointDynamicDrawFunc
            gp.Get()
            if gp.CommandResult() == rc.Result.Success:
                pt02 = gp.Point()
                height = str(round(abs(pt01.Z - pt02.Z), 3))
                print("Height = " + height)
                rs.ClipboardText(height)
            else:
                print("Failed to get Second Point")
                return False
        else:
            print("Failed to get First Point")
            return False

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    Height()
