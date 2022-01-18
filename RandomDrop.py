
'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import rhinoscriptsyntax as rs
import random as r


def RandomDrop():
    try:
        obj = rs.GetObjects('Pick blocks to drop randomly',
                            filter=4096, preselect=True)
        dropnum = rs.GetReal("Enter max drop distance")

        if obj:
            rs.EnableRedraw(False)

            for object in obj:
                num = r.uniform((-abs(dropnum)), 0)
                vec = rs.VectorCreate([0, 0, num], [0, 0, 0])
                point = rs.BlockInstanceInsertPoint(object)
                rs.MoveObject(object, vec)

            rs.EnableRedraw(True)

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    RandomDrop()
