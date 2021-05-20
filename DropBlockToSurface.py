'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

#Drop objects to surface

#By Thomas Chapman on 17/01/2021
#24/04/2021 revision to capture most error messages

import rhinoscriptsyntax as rs
import itertools

def main():

    # prompt user for obj and surface
    obj = rs.GetObjects('Pick objects',preselect=True,filter=(8+16+32+4096+1073741824))
    surface = rs.GetObjects('Pick Surface/Mesh')
    
    #Check selects are valid
    
    if obj == None:
        return
    if surface == None:
        return
    
    
    meshCheck = rs.IsMesh(surface[0])
    indexnum = []
    surfacetypes = []
    
    
    
    #Check if mixed surface types
    for thing in surface:
        result = rs.IsMesh(thing)
        surfacetypes.append(str(result))
    
    if ('True' in surfacetypes) and ('False' in surfacetypes):
        print ('Please select only one surface type')
        return
    
    
    
    #Turn off redraw to speed up script
    rs.EnableRedraw(False)
    
    # Generate bounding box around obj and find distance between obj and surface
    for objects in obj:
        ptlist = []
    
        # Get bounding box and make a square on lower half and find centroid
        bounds = rs.BoundingBox(objects)
        pl = rs.AddPolyline((bounds[0:4]+[bounds[0]]))
        centroid = rs.CurveAreaCentroid(pl)
    
        # Add three points at the centroid and move them in both z direction
        pt00 = rs.AddPoint(centroid[0])
        pt000 = rs.AddPoint(centroid[0])
        lowpoint = rs.AddPoint(centroid[0])
        pt01 = rs.MoveObject(pt00, (0,0,100000))
        pt02 = rs.MoveObject(pt000, (0,0,-100000))
    
        #Check if Mesh else use nurb instersect
        if meshCheck is True:
            curve = rs.AddCurve((pt01, pt02))
            for plane in surface:
                intersection = rs.CurveMeshIntersection(curve, plane)
                if intersection is None:
                    continue
                ptlist.append(list(filter(None,intersection)))
            merged = list(itertools.chain(*ptlist))
            merged = list(itertools.chain(*merged))
    
        # Create curve to intersect with surface to find distance from obj
        elif meshCheck is False:
            curve = rs.AddCurve((pt01, pt02))
            for plane in surface:
                intersection = rs.CurveBrepIntersect(curve, plane)
                if intersection is None:
                    continue
                ptlist.append(list(filter(None,intersection)))
            merged = list(itertools.chain(*ptlist))
            merged = list(itertools.chain(*merged))
    
        if merged is not None and merged != []:
            # Find the highest Z value and use that to target
            sorted = rs.SortPoints((rs.coerce3dpointlist(merged)), ascending=False, order=4)
            inter = (sorted[0])
            dist = rs.Distance(lowpoint, inter)
    
            # Convert Guid to point list
            intCon = rs.coerce3dpoint(inter)
            lowCon = rs.coerce3dpoint(lowpoint)
    
            # Find if obj is below or above surface and change dist to + or - accordingly
            if lowCon[2] < intCon[2]:
                distCon = abs(dist)
            if lowCon[2] > intCon[2]:
                distCon = (dist)*-1
            elif lowCon[2] == intCon[2]:
                rs.DeleteObjects([curve, pt01, pt02, pl, lowpoint]+merged)
                continue
    
            # Move obj to intersection
            rs.MoveObject(objects, (0,0,distCon))
    
            #deleate construction geo
            try:
               rs.DeleteObjects([curve, pt01, pt02, pl, lowpoint]+merged)
            except:
                continue
    
    
    
            #Clear list values for second run through loop
            del intersection
            del merged
            del ptlist
    
    
    
    #delete any polysurfaces created
    if isinstance(indexnum, int):
        rs.DeleteObjects(surface[indexnum])
    
    # Enable redraw to show results
    rs.EnableRedraw(True)


main()