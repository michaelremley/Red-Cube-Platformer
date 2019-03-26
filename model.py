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
        self.vx = 0.0
        self.vy = 0.0
        self.onsurfacex = True
        self.onsurfacey = False
        self.screensize = screensize

    def update(self, dt):
        """ update the state of the Avatar """
        self.x += self.vx * dt
        self.y += self.vy * dt
        if self.onsurfacex:
            self.vx *= 0.75
            self.vy = 0
        else:
            self.vx *= 0.90
            self.vy += 0.01 * dt
        if self.y > 870:
            self.onsurfacex = True
            self.y = 870
            self.vy = 0
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
        self.platform_width = 100
        self.platform_height = 20
        self.platform_space = 10
        for x in range(self.platform_space,
                       self.width - self.platform_space - self.platform_width,
                       self.platform_width + self.platform_space):
            for y in range(self.platform_space,
                           self.height//2,
                           self.platform_height + self.platform_space):
                self.platforms.append(Platform(self.platform_height,
                                         self.platform_width,
                                         x,
                                         y))
        self.avatar = Avatar(20, 20, 200, self.height - 30, size)
        self.clock = clock

    def update(self):
        """ Update the game state (currently only tracking the avatar) """
        self.clock.tick()
        self.dt = self.clock.get_time()
        self.avatar.update(self.dt)

    def __str__(self):
        output_lines = []
        # convert each platform to a string for outputting
        for platform in self.platforms:
            output_lines.append(str(platform))
        output_lines.append(str(self.avatar))
        # print one item per line
        return "\n".join(output_lines)
