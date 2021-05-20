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

obj = rs.GetObjects('Select objects',preselect=True)

if obj:
    current = rs.GetPoint('Select point')
    
    if current: 
        rl = rs.GetString('RL to move to?')
        rl = float(rl)
        
        if rs.UnitSystem() == 3: #if model is in cm scale by 100
            rl = rl*100
        elif rs.UnitSystem() == 2: #if model is in mm scale by 1000
            rl = rl*1000
        
        if rl == 0.000: #move objects to the 0 coord
            target3 = current.Z
            if target3:
                target3 = target3 *-1
                target4 = geo.Point3d(0,0,target3)
                rs.MoveObject(obj, target4)

        elif rl > 0.000:
            target = rl - current.Z #+ or - number to target location
            target2 = geo.Point3d(0,0,target) #translated vector needed to hit target
            rs.MoveObject(obj, target2)