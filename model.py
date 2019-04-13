"""
Platformer model code
"""
import copy
import random

class Platform(object):
    """ Encodes the state of a platform in the game """
    def __init__(self,height,width,x,y):
        self.height = height
        self.width = width
        self.x = x
        self.y = y

    def __str__(self):
        return "Platform height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                          self.width,
                                                          self.x,
                                                          self.y)

class Stage(object):
    def __init__(self, size, platforms):
        self.platforms = platforms
        self.width = size[0]
        self.height = size[1]
        self.platform_width = 200
        self.platform_height = 20
        self.platform_space = 200
        #self.generate_platforms()

    def generate_platforms(self):
        self.platforms.append(Platform(self.platform_height,
                                    self.width,
                                     0,
                                     self.height-self.platform_height))

size = (1920, 1080)
screenbottom = 1020
thickness = 60
pit1 = Stage(size,
[Platform(thickness,size[0]/2,0,screenbottom),
Platform(thickness,size[0]/2,1200,screenbottom)]
)

pit2 = Stage(size,
[Platform(thickness,300,400,screenbottom),
Platform(thickness,300,1000,screenbottom),
Platform(thickness,320,1600,screenbottom)]
)

pit3 = Stage(size,
[Platform(thickness,200,0,screenbottom),
Platform(thickness,200,400,screenbottom-300),
Platform(300,thickness,600,screenbottom-700),
Platform(thickness,300,900,screenbottom-700),
#Platform(100,thickness,600,screenbottom-900),
Platform(800,thickness,1200,screenbottom-700),
Platform(thickness,400,1200,screenbottom)]
)

ceiling1 = Stage(size,
[Platform(thickness,200,0,screenbottom),
Platform(800,1600,0,0),
Platform(thickness,200,1600,screenbottom)]
)

ceiling2 = Stage(size,
[Platform(thickness,200,0,screenbottom),
Platform(400,1200,0,0),
Platform(500,thickness,200,screenbottom-440),
Platform(200,thickness,0,screenbottom-640),
Platform(thickness,200,1600,screenbottom),
Platform(thickness,200,1000,screenbottom-400),
Platform(thickness,200,1200,screenbottom-200),
Platform(thickness,200,1400,screenbottom-100)]
)

class Avatar(object):
    """ Encodes the state of the player's Avatar in the game """
    def __init__(self, height, width, x, y, screensize):
        """ Initialize an Avatar with the specified height, width,
            and position (x,y) """
        self.height = height
        self.width = width
        self.x = x
        self.y = y
        self.xnew = x
        self.ynew = y
        self.vx = 0.0
        self.vy = 0.0
        self.sensitivity = 0.33
        self.inputs = []
        self.collisions = []
        self.screensize = screensize


    def addinput(self, input):
        if not input in self.inputs:
            self.inputs.append(input)

    def removeinput(self, input):
        if input in self.inputs:
            self.inputs.remove(input)

    def controls(self):
        if 'LEFT' in self.inputs and 'RIGHT' in self.inputs:
            self.vx = 0
        elif 'LEFT' in self.inputs:
            if 'RIGHT' in self.collisions:
                self.collisions[:] = (value for value in self.collisions if value != 'RIGHT')
            if not 'LEFT' in self.collisions:
                self.vx = -self.sensitivity
            else:
                self.vy = self.vy * 0.75
        elif 'RIGHT' in self.inputs:
            if 'LEFT' in self.collisions:
                self.collisions[:] = (value for value in self.collisions if value != 'LEFT')
            if not 'RIGHT' in self.collisions:
                self.vx = self.sensitivity
            else:
                self.vy = self.vy * 0.75
        else:
            self.vx = 0
        if 'JUMP' in self.inputs:

            if 'BOTTOM' in self.collisions:
                #self.collisions.remove('BOTTOM')
                self.collisions[:] = (value for value in self.collisions if value != 'BOTTOM')
                self.vy = -1.25
                self.y -= 10

            if 'LEFT' in self.collisions:
                self.collisions.remove('LEFT')
                self.vy = -1.25
                self.vx = self.sensitivity * 2
            if 'RIGHT' in self.collisions:
                self.collisions.remove('RIGHT')
                self.vy = -1.25
                self.vx = -self.sensitivity * 2
            if 'TOP' in self.collisions:
                #self.collisions.remove('TOP')
                self.collisions[:] = (value for value in self.collisions if value != 'TOP')

    def check_collisions(self, dt, platforms):
        self.xnew = self.x + self.vx*dt
        self.ynew = self.y + self.vy*dt
        for p in platforms:
            if p.x <= self.xnew+self.width and self.width+self.xnew <= p.x+p.width:
                if self.ynew+self.height >= p.y and p.y >= self.ynew:
                    self.collisions.append('BOTTOM')
                    self.ynew = p.y-self.height
                    self.vx = 0
                    self.vy = 0
                elif self.ynew <= p.y+p.height and p.y+p.height <= self.ynew+self.height:
                    self.collisions.append('TOP')
                    self.ynew = p.y+p.height
                    self.vx = 0
                    self.vy = 0
            if p.y < self.ynew+self.height+self.vy*dt and self.ynew+self.vy*dt < p.y+p.height:
                if self.x+self.vx*dt <= p.x+p.width and p.x+p.width <= self.x+self.width+self.vx*dt:
                    self.collisions.append('LEFT')
                    self.xnew = p.x+p.width
                    self.vx = 0
                    self.vy = 0
                elif self.x+self.width+self.vx*dt >= p.x and p.x >= self.x+self.vx*dt:
                    self.collisions.append('RIGHT')
                    self.xnew = p.x-self.width
                    self.vx = 0
                    self.vy = 0

    def resolve_collisions(self):
        if 'LEFT' in self.collisions or 'RIGHT' in self.collisions:
            self.x = self.xnew
            self.vx = 0
        if 'TOP' in self.collisions or 'BOTTOM' in self.collisions:
            self.y = self.ynew
            self.vy = 0


    def update(self, dt, platforms):
        """ update the state of the Avatar """
        self.collisions = []
        self.check_collisions(dt, platforms)
        if self.y+self.vy*dt > 1080-self.height:
            self.collisions.append('BOTTOM')
            self.ynew = 1080-self.height
            self.vy = 0
        self.x = self.xnew
        self.y = self.ynew
        self.controls()
        self.resolve_collisions()
        # Set terminal velocity to prevent collision bugs
        self.vy = min(self.vy,1)


        if ('LEFT' in self.collisions and 'LEFT' in self.inputs) or ('RIGHT' in self.collisions and 'RIGHT' in self.inputs):
            self.vy += 0.0002 * dt
        elif not ('TOP' in self.collisions or 'BOTTOM' in self.collisions):
            self.vy += 0.002 * dt


        if self.x < 0:
            self.x = 0
        if self.x > self.screensize[0]*4-self.width:
            self.x = self.screensize[0]*4-self.width



    def __str__(self):
        return "Avatar height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                           self.y)

class PlatformerModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size, clock):
        self.platforms = []
        self.view_width = size[0]
        self.view_height = size[1]
        self.stages = [pit1, pit2, pit3, ceiling1, ceiling2]
        for i in [0,1]:
            for p in self.stages[i].platforms:
                p_new = copy.deepcopy(p)
                p_new.x = p_new.x+i*self.view_width# +p_new.x%self.view_width
                self.platforms.append(p_new)
        #self.update_platforms()
        for platform in self.platforms:
            if platform.x < -platform.width:
                self.platforms.remove(platform)
        self.left_edge = 0
        self.autoscrollspeed = 0.1
        self.dt = 0

        self.avatar = Avatar(20, 20, 400, self.view_height - 400, size)
        self.clock = clock

    def update_platforms(self):
        for platform in self.platforms:
            if platform.x < -platform.width:
                self.platforms.remove(platform)

    def append_stage(self):
        for p in random.choice(self.stages).platforms:
            p_new = copy.deepcopy(p)
            p_new.x = p_new.x + self.view_width
            self.platforms.append(p_new)

    def update(self):
        """ Update the game state (currently only tracking the avatar) """
        self.clock.tick()
        self.dt = self.clock.get_time()
        self.left_edge += self.dt * self.autoscrollspeed

        self.update_platforms()

        if self.left_edge >= 1920:
            self.left_edge -= 1920
            for platform in self.platforms:
                platform.x -= 1920
            self.avatar.x -= 1920
            self.append_stage()
        self.avatar.update(self.dt, self.platforms)
        if 'QUIT' in self.avatar.inputs:
            return True

    def __str__(self):
        output_lines = []
        # convert each platform to a string for outputting
        for platform in self.platforms:
            output_lines.append(str(platform))
        output_lines.append(str(self.avatar))
        # print one item per line
        return "\n".join(output_lines)
