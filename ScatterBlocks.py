'''

Copyright <2022> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# SCATTER BLOCKS

import rhinoscriptsyntax as rs
import random
import math
import Rhino
import scriptcontext as sc

# r1 = vector 01 of triangle from origin (this will be randomised between 0,1)
# r2 = vector 02 of triangle from origin (this will be randomised between 0,1)
# a = origin corner of triangle (this should be picked as largest radius)
# b, c = other corners of triangle


def ScatterBlocks():

    ################################################################################
    #                             GET OBJECTS AND VARIABLE                         #
    ################################################################################

    obj = rs.GetObject(message="Select surface to scatter on", filter=8 | 16 |
                       32, preselect=False, select=False, custom_filter=None, subobjects=False)
    if not obj:
        return
    blocks = rs.GetObjects(message="Select blocks to scatter", filter=4096, group=True, preselect=False,
                           select=False, objects=None, minimum_count=1, maximum_count=0, custom_filter=None)
    if not blocks:
        return
    scatterNum = rs.GetInteger(
        message="Enter scatter amount", number=100, minimum=1, maximum=10000)
    if not scatterNum:
        return
    userScale = rs.GetReal(
        "enter scale multiplyer (0 for no scaling)", number=0, minimum=None, maximum=None)

    userRotation = rs.GetBoolean(
        "random rotation of blocks?", ("Rotation", "No", "Yes"), (True))
    if not userRotation:
        return

    isMesh = rs.IsMesh(obj)
    ptBucket = 0
    pointList = []
    blockList = []
    worldZVector = (rs.WorldXYPlane()).ZAxis

    rs.EnableRedraw(False)

    def MeshBrep(brep_id, params):
        brep = rs.coercebrep(brep_id)
        if brep:
            mesh = Rhino.Geometry.Mesh()
            mesh_parts = Rhino.Geometry.Mesh.CreateFromBrep(brep, params)
            for mesh_part in mesh_parts:
                mesh.Append(mesh_part)
            mesh.Compact()
            return mesh

    def TestMeshBrep():
        mesh_params = Rhino.Geometry.MeshingParameters.Coarse
        mesh_brep = MeshBrep(obj, mesh_params)
        if mesh_brep:
            mesh = sc.doc.Objects.AddMesh(mesh_brep)
        return mesh

    def chunks(lst, n):  # list split generator
        for i in xrange(0, len(lst), n):
            yield lst[i:i + n]

    if isMesh == False:
        mesh = TestMeshBrep()
    else:
        mesh = obj

    # Get and format vertex points in mesh, format from point3d object to float list
    meshVerts = rs.MeshFaces(mesh, face_type=False)
    totalArea = rs.MeshArea(mesh)
    meshFaceCount = rs.MeshFaceCount(mesh)

    PT01 = meshVerts[0::3]
    PT01S = []
    for i in PT01:
        i = (i.X, i.Y, i.Z)
        PT01S.append(i)

    PT02 = meshVerts[1::3]
    PT02S = []
    for i in PT02:
        i = (i.X, i.Y, i.Z)
        PT02S.append(i)

    PT03 = meshVerts[2::3]
    PT03S = []
    for i in PT03:
        i = (i.X, i.Y, i.Z)
        PT03S.append(i)

    # format list together in order to loop through
    triangleList = zip(PT01S, PT02S, PT03S)

    ################################################################################
    #                             POINT SCATTER LOOP                               #
    ################################################################################

    # loop through the three vertexes forming individual triangles
    for i in triangleList:
        a = i[0]  # triangle vert 1
        b = i[1]  # triangle vert 2
        c = i[2]  # triangle vert 3

    # Find area of triangle
        dist01 = rs.Distance(a, b)
        dist02 = rs.Distance(a, c)
        dist03 = rs.Distance(b, c)
        # Herons formula to find area of triangle by sides
        s = (dist01 + dist02 + dist03) / 2
        tArea = math.sqrt(s*(s-dist01)*(s-dist02)*(s-dist03))

    # assign portion of points base on area of triangle, if assignment of points is lower then one, add that to the next assignment
        numPtsPerUnit = totalArea[1] / scatterNum
        ptAllocation = tArea / numPtsPerUnit
        ptBucket = ptBucket + ptAllocation

        if ptBucket < 1:
            continue
        else:
            pointShare = int(math.floor(ptBucket))
            ptBucket = 0

    # Vectors from origin to either corner of triangle
        ac = rs.VectorCreate(c, a)
        ab = rs.VectorCreate(b, a)
        originVector = rs.VectorCreate(a, (0, 0, 0))

    # Generate random numbers between 0,1. Random scatter onto triangle
        for i in range(pointShare):
            r1 = random.random()
            r2 = random.random()
            if r1 + r2 < 1:
                p = r1 * ac + r2 * ab
            else:
                p = (1 - r1) * ac + (1 - r2) * ab

            points = rs.AddPoint(p)
            pointList.append(points)
            rs.MoveObjects(points, originVector)

    ################################################################################
    #                 MOVE BLOCKS TO POINTS WITH ROTATION / SCALE                  #
    ################################################################################

    # shuffle point list then split list by the number of blocks to scatter. Copy blocks to split lists
    random.shuffle(pointList)
    ptDivision = int(len(pointList) / len(blocks))
    genList = chunks(pointList, ptDivision)
    blockIndex = 0

    for pts in genList:  # looping through split point list and blocks and copying blocks to scatter
        blockPt = rs.BlockInstanceInsertPoint(blocks[blockIndex])
        for pt in pts:
            vector = rs.VectorCreate(pt, blockPt)
            newBlock = rs.CopyObject(blocks[blockIndex], vector)
            # create list of blocks for later modification
            blockList.append(newBlock)
        if blockIndex < (len(blocks) - 1):
            blockIndex += 1

    # apply random scaling and rotation to blocks
    if userRotation[0] == True:
        for block in blockList:
            centerPt = rs.BlockInstanceInsertPoint(block)
            angle = random.randint(0, 360)
            rs.RotateObject(block, centerPt, angle, worldZVector)

    for block in blockList:
        centerPt = rs.BlockInstanceInsertPoint(block)
        scale = random.uniform((userScale/4), userScale)
        rs.ScaleObject(block, centerPt, (scale, scale, scale))

    # If a mesh was created, delete it, general cleanup
    if isMesh == False:
        rs.DeleteObject(mesh)
    rs.DeleteObjects(pointList)

    rs.EnableRedraw(True)


if __name__ == "__main__":
    ScatterBlocks()
