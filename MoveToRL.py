'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# MOVE OBJECT TO SPECIFIED RL
# BY THOMAS CHAPMAN ON 01/10/2021

import rhinoscriptsyntax as rs
import Rhino.Geometry as geo


def MoveToRL():
    try:
        # Determine Unit system and scale m input to unit system scale and close if not mm, cm, m
        def scale():
            system = rs.UnitSystem()
            if system == 2 or system == 3 or system == 4:
                scaleFactorDict = {2: 1000, 3: 100, 4: 1}
                scaleFactor = scaleFactorDict[system]
                return scaleFactor

            if system != 2 or system != 3 or system != 4:
                return None

        if scale() == None:
            rs.MessageBox(
                "This tool is can only be used in mm, cm or m model units")
            return None

        obj = rs.GetObjects('Select objects', preselect=True)
        if obj:
            current = rs.GetPoint('Select point')

            if current:
                rl = rs.GetString('RL to move to?')
                rl = float(rl)
                rl = rl*scale()

                if rl == 0:  # move objects to the 0 coord
                    target3 = current.Z
                    if target3:
                        target3 = target3 * -1
                        target4 = geo.Point3d(0, 0, target3)
                        rs.MoveObject(obj, target4)

                elif rl < 0:
                    target5 = rl - current.Z
                    target6 = geo.Point3d(0, 0, target5)
                    rs.MoveObject(obj, target6)

                elif rl > 0:
                    target = rl - current.Z  # + or - number to target location
                    # translated vector needed to hit target
                    target2 = geo.Point3d(0, 0, target)
                    rs.MoveObject(obj, target2)

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    MoveToRL()
