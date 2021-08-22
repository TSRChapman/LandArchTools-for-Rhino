'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import rhinoscriptsyntax as rs

# Get object and find layer it is on
obj = rs.GetObjects('select an object on the layer to isolate',preselect=True)

if obj:


    rs.EnableRedraw(False)

    # Create list of selected obj layers
    selectedlayers = []
    for i in obj:
        layer = rs.ObjectLayer(i)
        selectedlayers.append(layer)

    # Select all objects on each layer

    for i in selectedlayers:
        rs.ObjectsByLayer(i,True)
    isolate = rs.SelectedObjects()

    allObjects = rs.AllObjects()

    for i in isolate:
        allObjects.remove(i)

    # Hide selected objects

    rs.HideObjects(allObjects)

    rs.UnselectAllObjects()

    rs.EnableRedraw(True)