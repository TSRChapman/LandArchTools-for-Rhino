'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import rhinoscriptsyntax as rs


def TurnOffSelectedLayer():
    try:

        obj = rs.GetObjects("select obj Layers to turn off")

        if obj:

            rs.EnableRedraw(False)

            for i in obj:
                layer = rs.ObjectLayer(i)
                rs.LayerVisible(layer, visible=False)

            rs.EnableRedraw(True)

    except:
        print("Failed to execute")
        rs.EnableRedraw(True)
        return


if __name__ == "__main__":
    TurnOffSelectedLayer()
