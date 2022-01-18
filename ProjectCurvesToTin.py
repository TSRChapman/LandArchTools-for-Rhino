'''

Copyright <2022> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE 
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR 
THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Project Curves to TIN

from rhinoscript.object import FlashObject
import rhinoscriptsyntax as rs


def ProjectCurvesToTIN():
    try:
        crvs = rs.GetObjects(message="Select curves to project", filter=4, group=True, preselect=False,
                             select=False, objects=None, minimum_count=1, maximum_count=0,
                             custom_filter=None)
        if not crvs:
            return
        obj = rs.GetObject("Select the TIN to project onto", 8 | 16 | 32)
        if not obj:
            return
        isMesh = rs.IsMesh(obj)
        zUpList = []
        zDownList = []

        rs.EnableRedraw(False)

        # Convert Mesh to Nurbs for ShootRay compatibility
        if isMesh == True:
            srf = rs.MeshToNurb(obj)
        if isMesh == False:
            srf = obj

        # Shoot ray from each grip point and move grips to reflection point
        for crv in crvs:
            rs.EnableObjectGrips(crv)
            grips = rs.ObjectGripLocations(crv)
            for grip in grips:

                zUp = rs.ShootRay(srf, grip, (0, 0, 1), 1)
                # if zUp != None:
                if zUp == None:
                    zUpList.append(False)
                else:
                    zUpList.append(zUp[1])

                zDown = rs.ShootRay(srf, grip, (0, 0, -1), 1)
                # if zDown != None:
                if zDown == None:
                    zDownList.append(False)
                else:
                    zDownList.append(zDown[1])

            rs.CopyObject(crv)  # Copy Existing curve

            # Find the right list to iterate over and insert existing points for any falses
            if all(x is False for x in zUpList):
                falseindex = [i for i, val in enumerate(zDownList) if not val]
                for i in falseindex:
                    # Replace False with existing grip location and closest Z value
                    closestPt = rs.BrepClosestPoint(srf, grips[i])
                    zDownList[i] = (grips[i].X, grips[i].Y, closestPt[0].Z)
                rs.ObjectGripLocations(crv, zDownList)
            else:
                falseindex = [i for i, val in enumerate(zUpList) if not val]
                for i in falseindex:
                    # Replace False with existing grip location and closest Z value
                    closestPt = rs.BrepClosestPoint(srf, grips[i])
                    zUpList[i] = (grips[i].X, grips[i].Y, closestPt[0].Z)
                rs.ObjectGripLocations(crv, zUpList)

            del zDownList[:]
            del zUpList[:]
            rs.EnableObjectGrips(crv, False)

        if isMesh == True:
            rs.DeleteObject(srf)

        rs.EnableRedraw(True)

    except:
        rs.EnableObjectGrips(crv, False)
        rs.DeleteObject(crv)
        rs.EnableRedraw()


if __name__ == "__main__":
    ProjectCurvesToTIN()
