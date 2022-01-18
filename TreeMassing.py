import rhinoscriptsyntax as rs
import math
import random

'''

Copyright <2022> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Calculate Soil requirements


def TreeMassing():
    try:

        litre = rs.GetReal("Enter the root ball litres, max 2000 Litres", 400)
        soilDepth = rs.GetReal('Enter the soil depth available in m', 0.8)
        matureHeight = rs.GetReal('Enter the mature tree height in m', 5)
        dbh = rs.GetReal(
            'Enter the DBH at maturity in m, if unknown hit Enter', 0)
        userPt = rs.GetPoint('Pick a point to place rootball')

        rs.EnableRedraw(False)

        # Dictionery for litre size to pot Rootball Diameter [0] / Rootball Height [1] / Calliper [2] / Height [3] / Spread [4]
        # Figures obtained from https://winterhill.com.au/tree-sizes/
        PotDict = {
            25: [0.300, 0.250, 0.020, 1.000, 0.500],
            45: [0.420, 0.350, 0.025, 2.000, 1.000],
            75: [0.465, 0.500, 0.035, 2.500, 2.000],
            100: [0.520, 0.560, 0.050, 3.500, 2.000],
            200: [0.700, 0.625, 0.070, 4.500, 3.000],
            400: [0.980, 0.715, 0.090, 6.000, 4.000],
            600: [1.200, 0.600, 0.100, 6.000, 5.000],
            800: [1.300, 0.600, 0.120, 7.000, 5.000],
            1000: [1.500, 0.600, 0.150, 8.000, 5.000],
            2000: [2.000, 0.800, 0.200, 9.000, 5.000],
        }

        def closest(lst, K):

            return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-K))]

        def scale():
            system = rs.UnitSystem()
            if system == 2 or system == 3 or system == 4:
                scaleFactorDict = {2: 1000, 3: 100, 4: 1}
                scaleFactor = scaleFactorDict[system]
                return scaleFactor

            if system != 2 or system != 3 or system != 4:
                return None

        s = scale()

        if s == None:
            rs.MessageBox(
                "This tool is can only be used in mm, cm or m model units")
            return None

        # Calc for standard soil requirements as per Australian Standards

        if dbh == 0:
            dbh = ((matureHeight / 100) * 4) * 1000  # Gives a DBH in mm
        # Gives a required soil volume in M3
        reqSoil = (matureHeight * dbh) / 100
        reqSoilRadius = math.sqrt(reqSoil / ((math.pi)*soilDepth))

        # Add soil puck to doc
        reqSoilRadiusCyl = rs.AddCylinder(
            userPt, (soilDepth*s), (reqSoilRadius*s), cap=True)
        rs.ObjectColor(reqSoilRadiusCyl, (150, 75, 0))

        # Calc for size of rootball as per standard pot sizes
        litreMatch = closest(list(PotDict.keys()), litre)
        dia = (PotDict[litreMatch])[0]
        height = (PotDict[litreMatch])[1]

        # Add Rootball to doc
        rootballCyl = rs.AddCylinder(userPt, (height*s), ((dia/2)*s))
        rs.ObjectColor(rootballCyl, (0, 128, 0))
        vec = (0, 0, ((soilDepth*s) - (height*s)))
        rs.MoveObject(rootballCyl, vec)

        # Add Tree model based on Dict
        calliper = (PotDict[litreMatch])[2]
        treeHeight = (PotDict[litreMatch])[3]
        spread = (PotDict[litreMatch])[4]
        vec02 = (0, 0, (((soilDepth*s) - (height*s))) + (height*s))

        treeTrunk = rs.AddCylinder(userPt, (treeHeight*s), (calliper*s))
        rs.ObjectColor(treeTrunk, (101, 67, 33))
        rs.MoveObject(treeTrunk, vec02)
        canopy = rs.AddSphere(userPt, ((spread/2)*s))
        rs.ObjectColor(canopy, (33, 101, 67))
        vec03 = (0, 0, (((soilDepth*s) - (height*s))) +
                 (height*s) + (treeHeight*s) - ((spread/2)*s))
        rs.MoveObject(canopy, vec03)

        # Various Text Annotation
        txt1 = rs.AddText('Rootball ' + 'Height = ' + str(height*s) + ', Diameter = ' + str(dia*s), userPt,
                          height=(.1*s), font="Arial", font_style=0, justification=2)

        txt2 = rs.AddText('Soil Volume Requirement = ' + str(reqSoil) + ' m3', (userPt.X, (userPt.Y - (.2*s)), userPt.Z),
                          height=(.1*s), font="Arial", font_style=0, justification=2)

        block = rs.AddBlock((reqSoilRadiusCyl, rootballCyl, treeTrunk, canopy, txt1, txt2), userPt,
                            ("Rootball and Soil " + (str(random.random()))), delete_input=True)
        rs.BlockDescription(block, 'Rootball ' + 'Height = ' + str(height*s) + ', Diameter = ' + str(dia*s)
                            + ', Soil Volume Requirement = ' + str(reqSoil) + ' m3')

        guid = rs.InsertBlock(block, userPt)
        rs.ObjectName(guid, 'Rootball ' + 'Height = ' + str(height*s) + ', Diameter = ' + str(dia*s)
                            + ', Soil Volume Requirement = ' + str(reqSoil) + ' m3')

        rs.EnableRedraw(True)

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    TreeMassing()
