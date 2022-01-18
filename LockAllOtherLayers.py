'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Lock all objects apart from those on the selected Obj layer
# BY THOMAS CHAPMAN ON 01/10/2021

import rhinoscriptsyntax as rs
import random


def LockAllOtherLayers():
    try:
        obj = rs.GetObject(message="Select the object on the layer you want to stay unlocked", filter=0,
                           preselect=True, select=False, custom_filter=None, subobjects=False)

        rs.EnableRedraw(False)

        groupName = random.random()

        layer = rs.ObjectLayer(obj)
        objs = rs.ObjectsByLayer(layer, select=False)
        allobj = rs.AllObjects(select=True, include_lights=False,
                               include_grips=False, include_references=False)
        rs.UnselectObjects(objs)
        toBeLockedObj = rs.SelectedObjects()
        rs.UnselectAllObjects()

        group = rs.AddGroup(groupName)
        rs.AddObjectsToGroup(toBeLockedObj, group)

        rs.LockGroup(groupName)

        rs.DeleteGroup(groupName)

        rs.EnableRedraw(True)

    except:
        rs.EnableRedraw(True)
        print("Failed to execute")
        return


if __name__ == "__main__":
    LockAllOtherLayers()
