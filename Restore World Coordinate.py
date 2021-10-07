'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

#Restore world coordinate

import rhinoscriptsyntax as rs

rs.EnableRedraw(False)

#retreive northing and easting from text object
obj = rs.ObjectsByName("_ORIGIN_TEXT_")
if obj:
    text = rs.TextObjectText(obj)
    textList = text.split()
    easting = float(textList[1])
    northing = float(textList[3])
    
    #create reference coordinates to make vector
    orPoint = (easting,northing,0)
    point = rs.PointCoordinates(rs.ObjectsByName("_ORIGIN_POINT_"))
    vector = rs.VectorCreate(orPoint,point)
    
    #move all objects back to original origin point
    allObj = rs.AllObjects()
    rs.MoveObjects(allObj,vector)
    
    #delete coordinate geometry
    isCurrent = rs.IsLayerCurrent("_ORIGIN_")
    if isCurrent == False:
        rs.PurgeLayer("_ORIGIN_")
    if isCurrent == True:
        defaultCheck = rs.IsLayer("Default")
        if defaultCheck == True:
            rs.CurrentLayer("Default")
            rs.PurgeLayer("_ORIGIN_")
        if defaultCheck == False:
            rs.AddLayer("Default")
            rs.CurrentLayer("Default")
            rs.PurgeLayer("_ORIGIN_")
    
    rs.EnableRedraw(True)