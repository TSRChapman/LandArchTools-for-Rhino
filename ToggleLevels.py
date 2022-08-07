"""

Copyright <2022> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""

# Toggle visibility of levels
# By Thomas Chapman on 06/08/2022



import scriptcontext as sc
import Rhino as r
import itertools


def ToggleLevels():

    # Get list of relevent objects
    it = r.DocObjects.ObjectEnumeratorSettings()
    it.IncludeLights = False
    it.IncludeGrips = False
    it.NormalObjects = True
    it.LockedObjects = True
    it.HiddenObjects = True
    it.ReferenceObjects = False
    it.ObjectTypeFilter = r.DocObjects.ObjectType.TextDot  # get textdots only
    textdotList = sc.doc.Objects.GetObjectList(it)

    # Loop through all textdots in document, check userdata and check if visible, toggle visibility
    visiList = []
    tdl1, tdl2 = itertools.tee(textdotList, 2)

    #in case some rl textdots are already hidden, check and turn all on
    for i in tdl1:
        visiList.append(i.IsHidden)
    if sum(visiList) == 0:
        hidden = False
    else:
        hidden = True
    
    for i in tdl2:
        stringCheck = i.Geometry.UserStringCount
        if stringCheck > 0:
            string = i.Geometry.GetUserString("LandArchTools")
            if string == "RLTextDot":
                if hidden == True:
                    sc.doc.Objects.Show(i, True)
                elif hidden == False:
                    sc.doc.Objects.Hide(i, True)

    sc.doc.Views.Redraw()

if __name__ == "__main__":
    ToggleLevels()
