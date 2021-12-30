# dependencies
import bpy
import bmesh

# Principal dica: OBJECT, MESH e BMESH são coisas diferente!

# dev environment para o modulo
# from importlib import reload  # Python 3.4+
# from mypackage_utils import mypackage_utils as u
# reload(u)

# Falta ainda:
# [ ] criar novo objeto, definir altura e largura aleatoriamente e posicionar ao lado
# [ ] criar modificador array
# [ ] criar aleatoriamente (com parametros de minimo e maximo) janelas na face, linkando ao facemap
# [ ] excluir a face do socket
# [ ] ajustar o tamanho do socket ao tamanho do plug
# [ ] criar diferentes tipos de janelas
# [ ] criar diferentes tipos de coberturas
# [ ] criar diferentes tipos de bases
# [ ] criar sockets para bases, coberturas e ar condicionado
# [ ] criar diferentes materiais para cada tipo de facemap (janela (vidros, frames, venesianas), concretos (cor e textura), etc)
# [ ] juntar tudo para criar multiplos predios


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

# def place_copy_of_obj2_to_obj1_mesh_vertex(obj1, obj2, vertex, merge = True):
# 	# obj2 origin will to vertex
# 	bm1 = bmesh.new()
# 	bm1.from_mesh(obj1.data)
# 	bmesh.ops.translate(bm1, verts = bm1.verts, vec = -vertex.co)
# 	bm1.from_mesh(obj2.data)
# 	bmesh.ops.translate(bm1, verts = bm1.verts, vec = vertex.co)
# 	if merge:
# 		bmesh.ops.remove_doubles(bm1, verts = bm1.verts, dist = 0.000001)
# 	bm1.to_mesh(obj1.data)
# 	bm1.free()

def place_copy_of_obj2_to_obj1_mesh_vertex(obj1, obj2, vertex, *, merge = True, copyFaceMaps = True, copyMaterials = True):
	# obj2 origin will to vertex
	tempMesh = obj2.data.copy()
	bm1 = bmesh.new()
	bm2 = bmesh.new()
	
	bm1.from_mesh(obj1.data)
	bmesh.ops.translate(bm1, verts = bm1.verts, vec = -vertex.co)
	if copyFaceMaps:
		registerTable = copy_facemaps_from_obj2_to_obj1(obj1, obj2)
		bm2.from_mesh(tempMesh)
		set_new_facemap_index_into_bmesh(bm2, registerTable)
		bm2.to_mesh(tempMesh)
		bm2.clear()
	if copyMaterials:
		registerTable = copy_materials_from_obj2_to_obj1(obj1, obj2)
		bm2.from_mesh(tempMesh)
		set_new_material_index_into_bmesh(bm2, registerTable)
		bm2.to_mesh(tempMesh)
		bm2.clear()

	bm1.from_mesh(tempMesh)
	bmesh.ops.translate(bm1, verts = bm1.verts, vec = vertex.co)
	if merge:
		bmesh.ops.remove_doubles(bm1, verts = bm1.verts, dist = 0.000001)
	bm1.to_mesh(obj1.data)
	bpy.data.meshes.remove(tempMesh)
	bm1.free()
	bm2.free()

def copy_facemaps_from_obj2_to_obj1(obj1, obj2):
	facemapsList = list(map(lambda facemap: (facemap.name, facemap.index), obj2.face_maps))
	for name, _ in facemapsList:
		if obj1.face_maps.find(name) == -1:
			obj1.face_maps.new(name = name)
	registerTable = []
	for name, oldIndex in facemapsList:
		index = obj1.face_maps.find(name)
		reg = {
			'name': name,
			'oldIndex': oldIndex,
			'newIndex': index,
		}
		registerTable.append(reg)
	return registerTable

def set_new_facemap_index_into_bmesh(bm, registerTable):
	fm = bm.faces.layers.face_map.active
	for face in bm.faces:
		index = face[fm]
		reg = next((reg for reg in registerTable if reg['oldIndex'] == index), None)
		if reg:
			face[fm] = reg['newIndex']

def copy_materials_from_obj2_to_obj1(obj1, obj2):
	l = list(obj2.data.materials)
	materialList = list((material, index) for index, material in enumerate(l))
	for material, _ in materialList:
		if obj1.data.materials.find(material.name) == -1:
			obj1.data.materials.append(material)
	registerTable = []
	for material, oldIndex in materialList:
		index = obj1.data.materials.find(material.name)
		reg = {
			'name': material.name,
			'oldIndex': oldIndex,
			'newIndex': index,
		}
		registerTable.append(reg)
	return registerTable

def set_new_material_index_into_bmesh(bm, registerTable):
	for face in bm.faces:
		oldIndex = face.material_index
		reg = next((reg for reg in registerTable if reg['oldIndex'] == oldIndex), None)
		if reg:
			face.material_index = reg['newIndex']

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



# from mypackage_utils import mypackage_utils as u
def tempfunction():
	# passo a passo para colar p no vértice mais a esquerda da face 0 do facemap janelas de c1
	p = D.objects['flecha']
	c1 = D.objects['Cube.003']
	tbm = bmesh.new()
	tbm.from_mesh(c1.data)
	faces = u.get_faces_from_facemap_index(tbm, 0)
	v1 = u.backLeftBottomVertex(list(faces[0].verts))
	u.place_copy_of_obj2_to_obj1_mesh_vertex(c1, p, v1)



# p = bpy.data.objects[1]
# bm = bmesh.new()
# bm.from_mesh(p.data)

# print(p)
# v = backLeftBottomVertex(bm)
# print(v)

# print(v.co)