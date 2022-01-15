'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Get Coordinates

import rhinoscriptsyntax as rs


def GetCoordinate():

    # Get point from user and round to nearest 3 decimal points
    point = rs.GetPoint("Pick point to find Coordinate information")
    pointX = round(point.X, 3)
    pointY = round(point.Y, 3)
    pointZ = round(point.Z, 3)

    # store string in variable
    coord = ("E " + str(pointX) + " N " + str(pointY) + " Z " + str(pointZ))

    # Create textdot
    rs.AddTextDot("E " + str(pointX) + " N " +
                  str(pointY) + " Z " + str(pointZ), point)

    # copy to clipboard
    rs.ClipboardText(coord)


if __name__ == "__main__":
    GetCoordinate()
