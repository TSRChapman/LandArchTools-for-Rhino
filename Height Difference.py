'''

Copyright <2021> <Thomas Chapman>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import rhinoscriptsyntax as rs

pt01 = rs.GetPoint('Select first point to measure from')
pt02 = rs.GetPoint('Select second point to measure to')

pt01Z = pt01.Z
pt02Z = pt02.Z

height = abs(pt01Z-pt02Z)
height = round(height, 3)

rs.ClipboardText(height)

rs.MessageBox(height, buttons=0, title="Height difference - Value copied to clipboard")