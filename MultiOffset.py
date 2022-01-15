'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''
# Multi Offset

import rhinoscriptsyntax as rs


def MultiOffset():

    obj = rs.GetObjects('Select Closed Curves for Offset', preselect=True)
    bool = rs.GetBoolean('Offset Direction', ('Direction',
                                              'Inward', 'Outward'), (False))

    if bool:
        bool = bool[0]
        offset = rs.GetReal('Distance to Offset')

        for i in obj:
            if rs.IsCurveClosed(i):
                if bool == False:
                    pt = rs.CurveAreaCentroid(i)
                    pt = pt[0]
                    rs.OffsetCurve(i, pt, offset)
                if bool == True:
                    pt = [1000000, 1000000, 1000000]
                    rs.OffsetCurve(i, pt, offset)


if __name__ == "__main__":
    MultiOffset()
