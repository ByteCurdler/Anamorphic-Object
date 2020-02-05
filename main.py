import numpy as np
import os
from PIL import Image

im1name = "a.png"
im2name = "b.png"

im1 = np.array(Image.open(im1name))[:, :, 0] <= 128
im2 = np.array(Image.open(im2name))[:, :, 0] <= 128

assert im1.shape[0] == im2.shape[0], "Images non-equal in height"

for i in range(im1.shape[0]):
    assert (True in im1[i, :]) == (True in im2[i, :]), (
        "Images take up different rows, this would "
        "cause an unwanted gap in the final product")

def efficient(a, b):
    out = np.full((
        a.shape[1], #Width
        a.shape[0], #Height
        b.shape[1]  #Depth
    ), False)
    for i in range(out.shape[1]):
        rows = [j for j in range(a.shape[1]) if a[a.shape[0]-1-i, j]]
        cols = [j for j in range(b.shape[1]) if b[b.shape[0]-1-i, j]]
        for j in range(max(len(rows), len(cols))):
            out[rows[j] if j<len(rows) else rows[-1]][i
              ][cols[j] if j<len(cols) else cols[-1]] = True
    return out

print("Carving...")

out = efficient(im1, im2)

print("Writing files...")
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

np.save('out.npy', out)

print("Done!")
