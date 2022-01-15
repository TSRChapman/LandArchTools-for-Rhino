'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


# Show RL of specified point and copy to clipboard
# By Thomas Chapman on 01/10/2021

import rhinoscriptsyntax as rs
import os


def ShowRL():

    def scale():
        system = rs.UnitSystem()
        if system == 2 or system == 3 or system == 4:
            scaleFactorDict = {2: 0.001, 3: 0.01, 4: 1}
            scaleFactor = scaleFactorDict[system]
            return scaleFactor

        if system != 2 or system != 3 or system != 4:
            return None

    if scale() == None:
        rs.MessageBox(
            "This tool is can only be used in mm, cm or m model units")
        return None

    point = rs.GetPoint('Select point')

    if point:
        pointZ = point.Z
    pointZ = pointZ*scale()
    rs.AddTextDot('+RL ' + str(round(pointZ, 3)), point)

    # Copy RL to Clipboard
    RL = str(round(pointZ, 3))
    rs.ClipboardText(RL)


if __name__ == "__main__":
    ShowRL()
