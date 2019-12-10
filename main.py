import numpy as np
import os
from PIL import Image

im1name = "a.png"
im2name = "b.png"

im1 = np.array(Image.open(im1name))[:, :, 0] <= 128
im2 = np.array(Image.open(im2name))[:, :, 0] <= 128

assert im1.shape[0] == im2.shape[1], "Images non-equal in height"

out = np.full((
    im1.shape[1], #Width
    im1.shape[0], #Height
    im2.shape[1]  #Depth
), True)

def carve(dirc, a3d, a2d):
    for x in range(a2d.shape[0]):
        for y in range(a2d.shape[1]):
            if not a2d[im1.shape[0]-1-y][(im2.shape[1]-1-x if dirc else x)]:
                if not dirc:
                    a3d[x, y, :] = False
                else:
                    a3d[:, y, x] = False

carve(False, out, im1)
carve(True, out, im2)

f = open("out.html", "w+")
f.write("""<html>
  <head>
    <script src="https://aframe.io/releases/0.9.2/aframe.min.js"></script>
  </head>
  <body>
    <a-scene background="color: #00FFFF">
      """)
height_bump = 1.4 - (out.shape[1] / 100)
for x in range(out.shape[0]):
    for y in range(out.shape[1]):
        for z in range(out.shape[2]):
            if out[x][y][z]:
                f.write("<a-box position='%s %s %s' scale='0.02 0.02 0.02' color='#ff0000'></a-box>" % (x/50,y/50+height_bump,z/50))
f.write("""
        <a-plane position="0 0 0" rotation="-90 0 0" width="4" height="4" color="#7BC8A4"></a-plane>
        <a-sky color="#ECECEC"></a-sky>
    </a-scene>
  </body>
</html>""")
f.close()
