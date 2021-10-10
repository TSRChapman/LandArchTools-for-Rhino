import struct
import imghdr
import rhinoscriptsyntax as rs

'''
Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

#Check document units

#Determin Unit system and scale m input to unit system scale and close if not mm, cm, m
def scale():
    system = rs.UnitSystem()
    if system == 2 or system == 3 or system == 4:
        scaleFactorDict = {2:1000, 3:100, 4:1}
        scaleFactor = scaleFactorDict[system]
        return scaleFactor

    if system != 2 or system != 3 or system != 4:
        return None

def get_image_size(fname):
    '''Determine the image type of fhandle and return its size.
    from draco'''
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0) # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception: #IGNORE:W0703
                return
        else:
            return
        return width, height

def main():
    if scale() == None:
        rs.MessageBox("This tool is can only be used in mm, cm or m model units")
        return None
    
    factor = scale()
    
    #Find and open jgw file, extract scalefactor and x and y coordinates
    
    jgw = rs.OpenFileName(title= 'Select .JGW file',filter="JGW Files (*.JGW)|*.JGW||" )
    
    with open(jgw,'rt') as f:
        numslist = f.read().splitlines()
    
    scaleFactor01 = numslist[0]
    
    worldx = float(numslist[4])*int(factor)
    worldy = float(numslist[5])*int(factor)
    
    #Find and open jpg file, extract pixel size
    
    jpg = rs.OpenFileName(title= 'Select .JPG image File',filter="JPG Files (*.JPG)|*.JPG||")
    
    size = get_image_size(jpg)
    
    scaleFactor02 = (float(size[0])*int(factor))
    scaleFactor03 = (float(size[1])*int(factor))
    
    # Calculate scale factor
    
    scaleFactorWidth = (float(scaleFactor01))*(float(scaleFactor02))
    scaleFactorHeight = (float(scaleFactor01))*(float(scaleFactor03))
    
    origin = (float(worldx), (float(worldy) - float(scaleFactorHeight)), 0)
    
    picturePlane = rs.PlaneFromFrame(origin,(1,0,0),(0,1,0))
    
    rs.AddPictureFrame(picturePlane,jpg,width=(float(scaleFactorWidth)), height=(float(scaleFactorHeight)))

main()