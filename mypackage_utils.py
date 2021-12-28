# dependencies
# import bpy
import bmesh


# dev environment para o modulo
# from importlib import reload  # Python 3.4+
# from mypackage_utils import mypackage_utils as u
# reload(u)


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


def duplicate_object_unlinked(obj):
	collection = obj.users_collection[0]
	newCopy = obj.copy()
	newCopy.data = obj.data.copy()
	collection.objects.link(newCopy)
	return newCopy

def duplicate_object_linked(obj):
	collection = obj.users_collection[0]
	newCopy = obj.copy()
	collection.objects.link(newCopy)
	return newCopy

def plug_object_to_socket(plug, face):
	socketNormal = face.normal

def place_copy_of_obj2_to_obj1_mesh_vertex(obj1, obj2, vertex, merge = True):
	# obj2 origin will to vertex
	bm1 = bmesh.new()
	bm1.from_mesh(obj1.data)
	bmesh.ops.translate(bm1, verts = bm1.verts, vec = -vertex.co)
	bm1.from_mesh(obj2.data)
	bmesh.ops.translate(bm1, verts = bm1.verts, vec = vertex.co)
	if merge:
		bmesh.ops.remove_doubles(bm1, verts = bm1.verts, dist = 0.000001)
	bm1.to_mesh(obj1.data)
	bm1.free()


def get_faces_from_facemap_index(bm, facemap_index):
	fm = bm.faces.layers.face_map.verify()
	faces = []
	for face in bm.faces:
		face_idx = face.index
		map_idx = face[fm]
		if map_idx == facemap_index:
			faces.append(face)
	return faces

def get_normal_from_first_face_in_facemap(obj, facemap_name):
	bm = bmesh.new()
	bm.from_mesh(obj.data)
	facemap_index = obj.face_maps[facemap_name].index
	faces = get_faces_from_facemap_index(bm, facemap_index)
	first_face = faces[0]
	normal = first_face.normal
	bm.free()
	return normal

# p = bpy.data.objects[1]
# bm = bmesh.new()
# bm.from_mesh(p.data)

# print(p)
# v = backLeftBottomVertex(bm)
# print(v)

# print(v.co)