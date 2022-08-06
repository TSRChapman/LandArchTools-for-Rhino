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
    for i in textdotList:
        stringCheck = i.Geometry.UserStringCount
        if stringCheck > 0:
            string = i.Geometry.GetUserString("LandArchTools")
            if string == "RLTextDot":
                if i.IsHidden == True:
                    sc.doc.Objects.Show(i, True)
                elif i.IsHidden == False:
                    sc.doc.Objects.Hide(i, True)


if __name__ == "__main__":
    ToggleLevels()
