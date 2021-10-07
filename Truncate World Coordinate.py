'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

#Truncate World Coordinate

import rhinoscriptsyntax as rs


#Get setout point
point = rs.GetPoint("Pick Point for World Coordinate value")

if point:
    rs.EnableRedraw(False)
    northing = round(point.Y,5)
    easting = round(point.X,5)

    #Add origin layer and lock it
    rs.AddLayer("_ORIGIN_",(255,0,0),visible=True,locked=True)
    originPoint = rs.AddPoint(point)

    #Move all objects to origin
    allObj = rs.AllObjects()
    vector = rs.VectorCreate((0,0,0),point)
    rs.MoveObjects(allObj,vector)

    #Draw origin marker
    circle = rs.AddCircle(originPoint,1)
    quads = rs.EllipseQuadPoints(circle)
    line1 = rs.AddLine(quads[0],quads[1])
    line2 = rs.AddLine(quads[2],quads[3])

    #Draw text marker and designate a name
    text = rs.AddText((" E "+ str(easting) + " N " + str(northing)), originPoint, 0.5)
    rs.ObjectName(text, "_ORIGIN_TEXT_")
    rs.ObjectName(originPoint, "_ORIGIN_POINT_")

    #Move geometry to locked origin layer
    rs.ObjectLayer([circle, line1, line2, originPoint, text], "_ORIGIN_")
    
    rs.EnableRedraw(True)