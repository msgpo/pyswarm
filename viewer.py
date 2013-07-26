import sys, os, os.path, soya, soya.cube
from time import sleep

PAUSE = False
STOP  = False
FPS   = 10

class MovableCamera(soya.Camera):
    def __init__(self, parent):
        soya.Camera.__init__(self, parent)

        self.speed = soya.Vector(self)
        self.rotation_x_speed = 0.0
        self.rotation_y_speed = 0.0
        self.rotation_z_speed = 0.0

    def begin_round(self):
        global PAUSE, STOP, FPS
        soya.Camera.begin_round(self)

        for event in soya.process_event():
            if event[0] == soya.sdlconst.KEYDOWN:
                if   event[1] == soya.sdlconst.K_w     : self.speed.z = -0.1
                elif event[1] == soya.sdlconst.K_s     : self.speed.z =  0.1
                elif event[1] == soya.sdlconst.K_e     : self.rotation_x_speed =  1.0
                elif event[1] == soya.sdlconst.K_q     : self.rotation_x_speed = -1.0
                elif event[1] == soya.sdlconst.K_a     : self.rotation_y_speed =  1.0
                elif event[1] == soya.sdlconst.K_d     : self.rotation_y_speed = -1.0
                elif event[1] == soya.sdlconst.K_q     : STOP = True
                elif event[1] == soya.sdlconst.K_ESCAPE: STOP = True
                elif event[1] == soya.sdlconst.K_SPACE : PAUSE = not PAUSE
                elif event[1] == soya.sdlconst.K_PLUS  : FPS += 1
                elif event[1] == soya.sdlconst.K_MINUS : FPS -= 1
                else: print event[1]
            if event[0] == soya.sdlconst.KEYUP:
                if   event[1] == soya.sdlconst.K_w  : self.speed.z = 0.0
                elif event[1] == soya.sdlconst.K_s  : self.speed.z = 0.0
                elif event[1] == soya.sdlconst.K_e  : self.rotation_x_speed = 0.0
                elif event[1] == soya.sdlconst.K_q  : self.rotation_x_speed = 0.0
                elif event[1] == soya.sdlconst.K_a  : self.rotation_y_speed = 0.0
                elif event[1] == soya.sdlconst.K_d  : self.rotation_y_speed = 0.0

    def advance_time(self, proportion):
        self.add_mul_vector(proportion, self.speed)
        self.turn_y(self.rotation_y_speed * proportion)
        self.turn_x(self.rotation_x_speed * proportion)

def read_swarms():
    global sys
    swarms = {}
    while True:
        s = sys.stdin.readline().strip()
        if s == 'done':
            break
        s = s.split()
        swarms[s[0]] = map(float, s[1:])
    return swarms


soya.init()
soya.path.append(os.path.join(os.path.dirname(sys.argv[0]), "data"))

# Creates the scene.

scene = soya.World()

light = soya.Light(scene)
light.set_xyz(10.0, 10.2, 11.0)

camera = MovableCamera(scene)
camera.set_xyz(-10.0, 4.0, 10.0)
camera.fov = 140.0
soya.set_root_widget(camera)

cube = soya.cube.Cube(None, size=0.08).shapify()

swarms = read_swarms()

cubes = {}
for i,swarm in swarms.items():
    cubes[i] = soya.Body(scene,cube)
    cubes[i].set_xyz(*swarms[i])


# Main loop
class MainLoop(soya.MainLoop):
    def begin_round(self):
        soya.MainLoop.begin_round(self)

ml = MainLoop(scene)
while not STOP:
    if not PAUSE:
        swarms = read_swarms()
        for i,swarm in swarms.items():
            cubes[i].set_xyz(*swarms[i])
        sleep(1/float(FPS))
    ml.update()