import bpy
import bmesh

class Utilities:
	@staticmethod
	def backLeftBottomVertex(listOfVerts):
		s = sorted(listOfVerts, key = lambda vert: (vert.co[0], vert.co[1], vert.co[2]))
		vertex = s[0]
		return vertex

	@staticmethod
	def bmBackLeftBottomVertex(bm):
		bm.verts.ensure_lookup_table()
		verts = list(bm.verts)
		vertex = Utilities.backLeftBottomVertex(listOfVerts)
		if not Utilities.isFirstVertexOnEveryAxis(bm, vertex):
			raise ValueError('Error:  has no unique vertex simultaneously at furthest back, left and bottom sides')
		return vertex

	@staticmethod
	def isFirstVertexOnAxis(bm, vertex, axis):
		bm.verts.ensure_lookup_table()
		verts = list(bm.verts)
		#axis x = 0, y = 1, z = 2
		s = sorted(verts, key = lambda vert: (vert.co[axis]))
		return s[0].co[axis] == vertex.co[axis]

	@staticmethod
	def isFirstVertexOnEveryAxis(bm, vertex):
		return all(Utilities.isFirstVertexOnAxis(bm, vertex, axis) for axis in range(0,3))
		

p = bpy.data.objects[1]
bm = bmesh.new()
bm.from_mesh(p.data)

print(p)
v = Utilities.backLeftBottomVertex(bm)
print(v)

print(v.co)