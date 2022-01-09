'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# DROP OBJECTS TO SELECTED SRF


import rhinoscriptsyntax as rs

obj = rs.GetObjects('Select Objects', rs.filter.curve | rs.filter.instance | rs.filter.mesh |
                    rs.filter.surface | rs.filter.subd | rs.filter.light | rs.filter.polysurface, preselect=True)
srf = rs.GetObject('Select Surface')

if obj:
    if srf:

        rs.EnableRedraw(False)

        # Check if srf is a mesh, if so convert to Nurb
        isMesh = rs.IsMesh(srf)
        if isMesh == True:
            srf = rs.MeshToNurb(srf)

        # For each object send test rays up and down in Z coord
        # Move each object to the ray test that hits a srf
        for i in obj:
            bndBox = rs.BoundingBox(i)
            pt1 = bndBox[0]
            pt2 = bndBox[2]
            crv = rs.AddLine(pt1, pt2)

            if crv:
                midcrv = rs.CurveMidPoint(crv)
                rs.DeleteObject(crv)

            ray_pt_up = rs.ShootRay(srf, midcrv, (0, 0, 1), reflections=1)
            ray_pt_down = rs.ShootRay(srf, midcrv, (0, 0, -1), reflections=1)

            if ray_pt_up:
                vector = rs.VectorCreate(ray_pt_up[1], midcrv)
                rs.MoveObject(i, vector)

            if ray_pt_down:
                vector = rs.VectorCreate(ray_pt_down[1], midcrv)
                rs.MoveObject(i, vector)

        # deleate any created srf
        if isMesh == True:
            rs.DeleteObject(srf)
        rs.EnableRedraw(True)
