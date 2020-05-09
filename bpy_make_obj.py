import bpy, numpy

data = numpy.load(input("Path to .npy file?"))

def strVector3( v3 ):
    return str(v3.x) + "," + str(v3.y) + "," + str(v3.z)

# create a new cube
for x in range(data.shape[0]):
    for y in range(data.shape[1]):
        for z in range(data.shape[2]):
            if data[x][y][z] == False:
                continue
    
            bpy.ops.mesh.primitive_cube_add()

            # newly created cube will be automatically selected
            cube = bpy.context.selected_objects[0]
            # change name
            cube.name = strVector3(cube.location)

            # change its location
            cube.location = (x/5, z/5, y/5)
            cube.scale = (0.1,0.1,0.1)
