
'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Create Standard Layers

import rhinoscriptsyntax as rs
import random as r


def CreateStandardLayers():

    # Add Layers to document

    rs.EnableRedraw(False)

    layerList = [
        "L_BLDS",
        "L_BNDY_WRKS",
        "L_EDGE",
        "L_HARD_ROCK",
        "L_HARD_WALL",
        "L_HARD_STEP",
        "L_HARD_RAMP",
        "L_HARD_FNCE",
        "L_HARD_PAV1",
        "L_HARD_PAV2",
        "L_HARD_PAV3",
        "L_HARD_PAV4",
        "L_LGHT",
        "L_ENTO",
        "L_PLAY_EQUI",
        "L_PLNT",
        "L_STRU",
        "L_TEXT",
        "L_TREE_PROP",
        "L_TREE_RETN",
        "L_WALL",
        "_L_WORKING",
        "L_SOFT_GRDN",
        "L_SOFT_MLCH",
        "L_SOFT_LAWN",
        "L_SOFT_PLANT",
        "L_FURN",
        "_L_OFF"


    ]

    layerList.sort()

    parentLayer = rs.AddLayer(name="LANDSCAPE", color=None,
                              visible=True, locked=False, parent=None)

    for layer in layerList:
        rs.AddLayer(layer, (r.randrange(255), r.randrange(255), r.randrange(
            255)), visible=True, locked=False, parent=parentLayer)

    rs.EnableRedraw(True)


if __name__ == "__main__":
    CreateStandardLayers()
