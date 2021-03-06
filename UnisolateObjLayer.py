'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Unisolate All objects
# By Thomas Chapman 21/05/01

import rhinoscriptsyntax as rs


def UnisolateObjLayer():
    try:
        rs.EnableRedraw(False)
        obj = rs.HiddenObjects()

        if obj:

            rs.ShowObjects(obj)
        rs.EnableRedraw(True)

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    UnisolateObjLayer()
