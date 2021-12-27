# dependencies
# import bpy
# import bmesh

def backLeftBottomVertex(listOfVerts):
	s = sorted(listOfVerts, key = lambda vert: (vert.co[0], vert.co[1], vert.co[2]))
	vertex = s[0]
	return vertex
	
def bmBackLeftBottomVertex(bm):
	bm.verts.ensure_lookup_table()
	verts = list(bm.verts)
	vertex = backLeftBottomVertex(listOfVerts)
	if not isFirstVertexOnEveryAxis(bm, vertex):
		raise ValueError('Error:  has no unique vertex simultaneously at furthest back, left and bottom sides')
	return vertex
	
def isFirstVertexOnAxis(bm, vertex, axis):
	bm.verts.ensure_lookup_table()
	verts = list(bm.verts)
	#axis x = 0, y = 1, z = 2
	s = sorted(verts, key = lambda vert: (vert.co[axis]))
	return s[0].co[axis] == vertex.co[axis]

def isFirstVertexOnEveryAxis(bm, vertex):
	return all(isFirstVertexOnAxis(bm, vertex, axis) for axis in range(0,3))

def rotateMesh(bm, matrix):
	bmesh.rotate(bm, verts = bm.verts, matrix = matrix)


def get_vertices_in_group(a,index):
    # a is a Blender object
    # index is an integer representing the index of the vertex group in a
    vlist = []
    for v in a.data.vertices:
        for g in v.groups:
            if g.group == index:
                vlist.append(v.index)
    return vlist




# p = bpy.data.objects[1]
# bm = bmesh.new()
# bm.from_mesh(p.data)

# print(p)
# v = backLeftBottomVertex(bm)
# print(v)

# print(v.co)