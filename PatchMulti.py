'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

#Patch Multiple Individual closed polylines
#By Thomas Chapman 04/22/2021

import rhinoscriptsyntax as rs

geo = rs.GetObjects('Select Closed Polylines',preselect=True)

uv1 = rs.GetInteger('enter number of UV divisions',number=1,minimum=1)

rs.EnableRedraw(False)
for objects in geo:
    rs.AddPatch((objects),(uv1,uv1))
rs.EnableRedraw(True)
