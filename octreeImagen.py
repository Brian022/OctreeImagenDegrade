import cv2

class Color(object):

    def __init__(self, red=0, green=0, blue=0):

        self.red = red
        self.green = green
        self.blue = blue
        
class OctreeNode(object):

    def __init__(self, level, parent):

        self.color = Color(0, 0, 0)
        self.pixel_count = 0
        self.children = [None for _ in range(8)]

        if level < Octree.niveles - 1:
            parent.add_level_node(level, self)

    def es_hoja(self):
        return self.pixel_count>0

    def agregar_color(self, color, level, parent):
        if level >= Octree.niveles:
            self.color.red += color.red
            self.color.green += color.green
            self.color.blue += color.blue
            self.pixel_count += 1
            return
        posicion = self.get_posicion_color(color, level)
        if not self.children[posicion]:
            self.children[posicion] = OctreeNode(level, parent)
        self.children[posicion].agregar_color(color, level + 1, parent)
        
    def get_posicion_color(self, color, level):

        posicion = 0
        mask = 0x80 >> level
        if color.red & mask:
            posicion |= 4
        if color.green & mask:
            posicion |= 2
        if color.blue & mask:
            posicion |= 1
        return posicion

class Octree(object):

    niveles = 8

    def __init__(self):
        self.levels = {i: [] for i in range(Octree.niveles)}
        self.root = OctreeNode(0, self)

    def add_level_node(self, level, node):
        self.levels[level].append(node)

    def fill(self, color):
        self.root.agregar_color(color, 0, self)


##Inicia el MAIN
img = cv2.imread('/Imagenes/Memes/pfp.png', 1)
cv2.imshow('imagen', img)
##dimension = img.shape
height = img.shape[0]
width = img.shape[1]

octree = Octree()

for i in range(height):
    for j in range(width):
        b,g,r = (img[i, j])
        octree.fill(Color(r,g,b))
     

# =============================================================================
#         b,g,r = (img[i, j])
#         print(r,g,b)
# =============================================================================

cv2.waitKey(0)
cv2.destroyAllWindows()
#plt.imshow(img, cmap='gray')
# =============================================================================
# b,g,r = (img[0, 0])
# print (r)
# print (g)
# print (b)
# =============================================================================