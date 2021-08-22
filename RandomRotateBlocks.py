'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

#RANDOM ROTATE BLOCK INSTANCES AROUND INSERTION POINT
#BY THOMAS CHAPMAN ON 01/09/2021

import rhinoscriptsyntax as rs
import random as r

vec = rs.VectorCreate([0,0,1],[0,0,0])
obj = rs.GetObjects('pick Blocks to rotate randomly', filter=4096, preselect=True)

if obj:
    rs.EnableRedraw(False)

    for object in obj:
        num = r.randrange(-180,180)
        point = rs.BlockInstanceInsertPoint(object)
        rs.RotateObject(object, point, num, vec)

    rs.EnableRedraw(True)