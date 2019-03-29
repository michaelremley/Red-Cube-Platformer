"""
Platformer model code
"""

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
            if not 'LEFT' in self.collisions:
                self.vx = -self.sensitivity
            else:
                self.vy = self.vy * 0.75
        elif 'RIGHT' in self.inputs:
            if not 'RIGHT' in self.collisions:
                self.vx = self.sensitivity
            else:
                self.vy = self.vy * 0.75
        else:
            self.vx = 0
        if 'JUMP' in self.inputs:
            if 'BOTTOM' in self.collisions:
                self.collisions.remove('BOTTOM')
                self.vy = -1.25
            elif 'LEFT' in self.collisions:
                self.collisions.remove('LEFT')
                self.vy = -1.25
                self.vx = self.sensitivity * 2
            elif 'RIGHT' in self.collisions:
                self.collisions.remove('RIGHT')
                self.vy = -1.25
                self.vx = -self.sensitivity * 2

    def check_collisions(self, dt, platforms):
        for p in platforms:
            if p.x <= self.x+self.width+self.vx*dt and self.x+self.vx*dt <= p.x+p.width:
                if self.y+self.height+self.vy*dt >= p.y and p.y >= self.y+self.vy*dt:
                    self.collisions.append('BOTTOM')
                    self.ynew = p.y-self.height
                    self.vx = 0
                elif self.y+self.vy*dt <= p.y+p.height and p.y+p.height <= self.y+self.height+self.vy*dt:
                    self.collisions.append('TOP')
                    self.ynew = p.y+p.height
            if p.y < self.y+self.height+self.vy*dt and self.y+self.vy*dt < p.y+p.height:
                if self.x+self.vx*dt <= p.x+p.width and p.x+p.width <= self.x+self.width+self.vx*dt:
                    self.collisions.append('LEFT')
                    self.xnew = p.x+p.width
                    self.vx = 0
                elif self.x+self.width+self.vx*dt >= p.x and p.x >= self.x+self.vx*dt:
                    self.collisions.append('RIGHT')
                    self.xnew = p.x-self.width
                    self.vx = 0

    def resolve_collisions(self):
        if 'LEFT' in self.collisions or 'RIGHT' in self.collisions:
            self.x = self.xnew
        if 'TOP' in self.collisions or 'BOTTOM' in self.collisions:
            self.y = self.ynew
            self.vy = 0


    def update(self, dt, platforms):
        """ update the state of the Avatar """
        self.collisions = []
        self.check_collisions(dt, platforms)
        self.controls()
        self.resolve_collisions()
        if self.y > 870:
            self.collisions.append('BOTTOM')
            self.y = 870
            self.vy = 0
        elif ('LEFT' in self.collisions and 'LEFT' in self.inputs) or ('RIGHT' in self.collisions and 'RIGHT' in self.inputs):
            self.vy += 0.0002 * dt
        else:
            self.vy += 0.002 * dt
        self.x += self.vx*dt
        self.y += self.vy*dt
        if self.x < 0:
            self.x = 0
        if self.x > self.screensize[0]-self.width:
            self.x = self.screensize[0]-self.width


    def __str__(self):
        return "Avatar height=%f, width=%f, x=%f, y=%f" % (self.height,
                                                           self.width,
                                                           self.x,
                                                           self.y)

class PlatformerModel(object):
    """ Encodes a model of the game state """
    def __init__(self, size, clock):
        self.platforms = []
        self.width = size[0]
        self.height = size[1]
        self.dt = 0
        self.platform_width = 200
        self.platform_height = 200
        self.platform_space = 200
        for x in range(self.platform_space,
                       self.width - self.platform_space - self.platform_width,
                       self.platform_width + self.platform_space):
            for y in range(self.platform_space,
                           self.height - 100,
                           self.platform_height + self.platform_space):
                self.platforms.append(Platform(self.platform_height,
                                         self.platform_width,
                                         x,
                                         y))
        self.avatar = Avatar(20, 20, 300, self.height - 550, size)
        self.clock = clock

    def update(self):
        """ Update the game state (currently only tracking the avatar) """
        self.clock.tick()
        self.dt = self.clock.get_time()
        self.avatar.update(self.dt, self.platforms)

    def __str__(self):
        output_lines = []
        # convert each platform to a string for outputting
        for platform in self.platforms:
            output_lines.append(str(platform))
        output_lines.append(str(self.avatar))
        # print one item per line
        return "\n".join(output_lines)
