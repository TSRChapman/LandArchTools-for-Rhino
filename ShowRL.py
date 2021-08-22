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

point = rs.GetPoint('Select point')

if point:
    pointZ = point.Z

    if rs.UnitSystem() == 3: #if doc is in CM
        pointZ = pointZ *0.01
    if rs.UnitSystem() == 2:#if doc is in MM
         pointZ = pointZ *0.001

    rs.AddTextDot('+RL ' + str(round(pointZ,3)),point)

    #Copy RL to Clipboard

    RL = str(round(pointZ,3))

    rs.ClipboardText(RL)

