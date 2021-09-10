'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
#Rotate picture frames to face camera

import rhinoscriptsyntax as rs

frames = rs.GetObjects("Select Picture Frames",filter=8,preselect=True)


#rotate surfaces around z axis towards camera point
if frames:

    cam = rs.ViewCamera()
    camz = (cam.X,cam.Y,0)
    world = rs.WorldXYPlane()
    angle = 1

    rs.EnableRedraw(False)

    for i in frames:
        angle = 1
        while angle >= 1:
            
            #get mid point of surface and move to z 0
            pointmid = rs.SurfaceAreaCentroid(i)
            pointmidz = (pointmid[0].X,pointmid[0].Y,0)
            #Get center UV of surface
            domainU = rs.SurfaceDomain(i, 0)
            domainV = rs.SurfaceDomain(i, 1)
            u = domainU[1]/2.0
            v = domainV[1]/2.0
            #Get normal vector of surface and cam vector
            vec1 = rs.SurfaceNormal(i,(u,v))
            vec1 = vec1.X,vec1.Y,0
            vec2 = rs.VectorCreate(camz,pointmidz)
            #find angle difference between the two vectors
            angle = rs.VectorAngle(vec1,vec2)
            angle = round(angle)
            #Rotate Object
            rs.RotateObject(i,pointmidz,angle)
        continue

    rs.EnableRedraw(True)