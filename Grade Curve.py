'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

#GRADE CURVE 

import rhinoscriptsyntax as rs

def scale():
    system = rs.UnitSystem()
    if system == 2 or system == 3 or system == 4:
        scaleFactorDict = {2:1, 3:100, 4:1000}
        scaleFactor = scaleFactorDict[system]
        return scaleFactor

    if system != 2 or system != 3 or system != 4:
        return None


def main():
    #If system is not metric, bail.
    if scale() == None:
        rs.MessageBox("This tool can only be used in mm, cm or m model units")
        return None
    
    #Set Variables
    crv = rs.GetObject(message="Get object to grade", filter=4, preselect=True, select=False, custom_filter=None, subobjects=False)
    if not crv: return
    grade = rs.GetReal(message="Enter grade number", number=20, minimum=0.001, maximum=None)
    if not grade: return
    
    rs.EnableRedraw(False)
    
    #FIND LENGTH OF CURVE AT EACH GRIP POINT
    rs.EnableObjectGrips(crv)
    ctrlPts = rs.ObjectGripLocations(crv)
    crvLengths = []
    startParam = rs.CurveClosestPoint(crv, ctrlPts[0])
    
    for i in ctrlPts:
        paramNum = rs.CurveClosestPoint(crv, i)
        CL = (rs.CurveLength(crv, sub_domain=[startParam ,paramNum]))
        crvLengths.append(CL)
    
    #FIND GRADED Z HEIGHT OF GRIP POINT
    gripHeights = []
    for i in crvLengths:
        rise = i / grade
        gripHeights.append(rise)
    
    #EDIT GRIP POINTS WITH NEW Z VALUE
    newGrips = []
    gripIndex = 0
    for i in ctrlPts:
        newPt = (i.X,i.Y,(i.Z+gripHeights[gripIndex]))
        newGrips.append(newPt)
        gripIndex = gripIndex + 1
    
    #MODIFY CURVE TO ENTERED GRADE
    rs.CopyObject(crv)
    grips = rs.ObjectGripLocations(crv, newGrips)
    rs.EnableObjectGrips(crv, enable=False)
    
    rs.EnableRedraw(True)

#Run Script
main()