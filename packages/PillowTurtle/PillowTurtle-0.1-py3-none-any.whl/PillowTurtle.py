from math import cos, sin, radians as rad
from PIL import ImageDraw

class Turtle(object):
    def __init__(self, pos=[0,0], rot=0, typ="line", width=1, color=(255,255,255)):
        self.pos = pos.copy()
        self.rot = rot
        self.type = typ
        self.width = width
        self.color = color

        self._visible = True
        self._path = []
        self._stacks = {
            "default": []
        }
        self._changed = False

    def move(self, dist):
        if self._visible:
            if self._path == [] or self._changed or self._props_changed():
                self._path.append({
                    "type": self.type,
                    "width": self.width,
                    "color": self.color,
                    "points": [
                        tuple(self.pos)
                    ]
                })
                self._changed = False
                
        # Calculate new position
        rad_rot = rad(self.rot)
        self.x += cos(rad_rot) * dist
        self.y += sin(rad_rot) * dist

        if self._visible:
            self._path[len(self._path)-1]["points"].append(tuple(self.pos))

    def forward(self, dist):
        self.move(dist)
    
    def backward(self, dist):
        self.move(-dist)

    def rotate(self, degrees):
        self.rot += degrees
    
    def right(self, degrees):
        self.rotate(-degrees)

    def left(self, degrees):
        self.rotate(degrees)

    def up(self):
        self.visible = False
    
    def down(self):
        self.visible = True
    
    def push(self, name="default"):
        if name not in self._stacks:
            self._stacks[name] = []
        
        self._stacks[name].append([self.x, self.y])
        self._stacks[name].append(self.rot)

    def pop(self, name="default"):
        prev_visible = self._visible

        self.up()

        self.rot = self._stacks[name].pop()
        self.pos = self._stacks[name].pop()
        self._visible = prev_visible

    def polygon(self):
        self.type = "polygon" if self.type == "line" else "line"
    
    def draw(self, canvas):
        draw = ImageDraw.Draw(canvas)
        for seg in self._path:
            if seg["type"]=="line":
                draw.line(seg["points"], seg["color"], seg["width"])
            elif seg["type"]=="polygon":
                draw.polygon(seg["points"], seg["color"])
    
    def _props_changed(self):
        if self._path != []:
            curr = self._path[len(self._path)-1]

            return curr["type"] != self.type or (curr["width"] != self.width and curr["type"] == "line") or curr["color"] != self.color
        return False

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, x):
        if x is False and self._visible is True:
            self._changed = True
        self._visible = x

    @property
    def x(self):
        return self.pos[0]

    @x.setter
    def x(self, x):
        self.pos[0] = x

    @property
    def y(self):
        return self.pos[1]

    @y.setter
    def y(self, y):
        self.pos[1] = y

