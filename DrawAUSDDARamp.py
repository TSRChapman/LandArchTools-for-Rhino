'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

# Model Standard Australian DDA Ramps

import rhinoscriptsyntax as rs
import math as m

# Determin Unit system and scale m input to unit system scale and close if not mm, cm, m


def scale():
    system = rs.UnitSystem()
    if system == 2 or system == 3 or system == 4:
        scaleFactorDict = {2: 1000, 3: 100, 4: 1}
        scaleFactor = scaleFactorDict[system]
        return scaleFactor

    if system != 2 or system != 3 or system != 4:
        return None


def main():
    if scale() == None:
        rs.MessageBox(
            "This tool is can only be used in mm, cm or m model units")
        return None

    Mult = scale()
    pt00 = rs.GetPoint('Pick insertion point')

    if pt00:

        pt01 = rs.CreatePoint(pt00.X, pt00.Y)
        RampOptions = 'Step Ramp', 'Kerb Ramp', 'Ramp', 'Walkway'
        RampType = rs.PopupMenu(RampOptions)

        rs.EnableRedraw(False)

        if RampType == -1:
            exit()

        if RampType == 0:  # Step Ramp
            Curve = rs.AddPolyline(
                [(pt01), (pt01.X, pt01.Y, (0.190*Mult)), ((pt01.X+1.9*Mult), pt01.Y, pt01.Z), (pt01)])
            Surface = rs.ExtrudeCurveStraight(
                Curve, (pt01), (pt01.X, (pt01.Y+1*Mult), pt01.Z))
            rs.CapPlanarHoles(Surface)
            rs.DeleteObject(Curve)

        if RampType == 1:  # Kerb Ramp
            # main ramp portion
            Curve = rs.AddPolyline(
                [(pt01), (pt01.X, pt01.Y, (0.190*Mult)), ((pt01.X+1.52*Mult), pt01.Y, pt01.Z), (pt01)])
            Surface = rs.ExtrudeCurveStraight(
                Curve, (pt01), (pt01.X, (pt01.Y+1*Mult), pt01.Z))
            rs.CapPlanarHoles(Surface)
            rs.DeleteObject(Curve)

        if RampType == 2:  # Ramp
            Grade = '1:19', '1:18', '1:17', '1:16', '1:15', '1:14'
            Index = rs.PopupMenu(Grade)
            GradeNum = [19, 18, 17, 16, 15, 14]
            if Index == 5:
                Rise = 9/(GradeNum[Index])
                Curve = rs.AddPolyline(
                    [(pt01), (pt01.X, pt01.Y, (Rise*Mult)), ((pt01.X+9*Mult), pt01.Y, pt01.Z), (pt01)])
                Surface = rs.ExtrudeCurveStraight(
                    Curve, (pt01), (pt01.X, (pt01.Y+1*Mult), pt01.Z))
                rs.CapPlanarHoles(Surface)
                rs.DeleteObject(Curve)
            elif Index != 5:
                Rise = 15/(GradeNum[Index])
                Curve = rs.AddPolyline(
                    [(pt01), (pt01.X, pt01.Y, (Rise*Mult)), ((pt01.X+15*Mult), pt01.Y, pt01.Z), (pt01)])
                Surface = rs.ExtrudeCurveStraight(
                    Curve, (pt01), (pt01.X, (pt01.Y+1*Mult), pt01.Z))
                rs.CapPlanarHoles(Surface)
                rs.DeleteObject(Curve)

        if RampType == 3:  # Walkway
            Grade = '1:33', '1:32', '1:31', '1:30', '1:29', '1:28', '1:27', '1:26', '1:25', '1:24', '1:23', '1:22', '1:21', '1:20'
            Index = rs.PopupMenu(Grade)
            GradeNum = [33, 32, 31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20]
            if Index == 0:
                Rise = 25/(GradeNum[Index])
                Curve = rs.AddPolyline(
                    [(pt01), (pt01.X, pt01.Y, (Rise*Mult)), ((pt01.X+25*Mult), pt01.Y, pt01.Z), (pt01)])
                Surface = rs.ExtrudeCurveStraight(
                    Curve, (pt01), (pt01.X, (pt01.Y+1*Mult), pt01.Z))
                rs.CapPlanarHoles(Surface)
                rs.DeleteObject(Curve)
            if Index == 13:
                Rise = 15/(GradeNum[Index])
                Curve = rs.AddPolyline(
                    [(pt01), (pt01.X, pt01.Y, (Rise*Mult)), ((pt01.X+15*Mult), pt01.Y, pt01.Z), (pt01)])
                Surface = rs.ExtrudeCurveStraight(
                    Curve, (pt01), (pt01.X, (pt01.Y+1*Mult), pt01.Z))
                rs.CapPlanarHoles(Surface)
                rs.DeleteObject(Curve)
            elif Index != 0 or Index != 13:
                # Linear interpolation of landing distance - DDA requirement...Srsly?
                Interp = m.floor(
                    ((GradeNum[Index] - 20)*(25 - 15)/(33 - 20))+15)
                Rise = Interp/(GradeNum[Index])
                Curve = rs.AddPolyline(
                    [(pt01), (pt01.X, pt01.Y, (Rise*Mult)), ((pt01.X+Interp*Mult), pt01.Y, pt01.Z), (pt01)])
                Surface = rs.ExtrudeCurveStraight(
                    Curve, (pt01), (pt01.X, (pt01.Y+1*Mult), pt01.Z))
                rs.CapPlanarHoles(Surface)
                rs.DeleteObject(Curve)

        rs.EnableRedraw(True)


main()
