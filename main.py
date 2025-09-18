from pygame_template import *
import colorsys
from noise import pnoise1

class Circle(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((720, 720), pygame.SRCALPHA)
        self.rect = self.image.get_frect(center=(APP.HW, APP.HH))
        self.time = 0.0
        self.color = (255, 255, 255, 255)

    def update(self, dt):
        self.time += dt * 0.2
        hue = pnoise1(self.time) * 0.5 + 0.5
        r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
        self.color = (int(r * 255), int(g * 255), int(b * 255), 255)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(
            self.image,
            self.color,
            V2(self.rect.center) - V2(self.rect.topleft),
            self.rect.centerx - self.rect.x,
            10
        )

class Ball(Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.radius = 20
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, Color.white, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_frect(center=(APP.HW, APP.HH - 50))

        self.pos = V2(self.rect.center)
        self.vel = V2(400, 400)
        self.acc = V2(0, 800)

        self.circle_center = V2(APP.HW, APP.HH)
        self.circle_radius = 360
        self.contact_points = []

    def update(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt

        to_center = self.pos - self.circle_center
        dist = to_center.length()
        max_dist = self.circle_radius - self.radius

        if dist > max_dist:
            normal = to_center.normalize()
            self.pos -= normal * (dist - max_dist)
            self.vel = self.vel.reflect(normal)
            self.contact_points.append(self.pos + normal * self.radius)
            print(len(self.contact_points))

        self.rect.center = self.pos

class run(APP):
    def setup(self):
        self.circle = Circle()
        self.ball = Ball()
        self.group = Group(self.circle, self.ball)
        self.dt_speed_factor = 1

    def update(self):
        self.group.update(self.dt)

    def draw(self):
        for point in self.ball.contact_points:
            pygame.draw.line(
                self.circle.image,
                (255, 255, 255, 100),
                self.ball.pos - V2(self.circle.rect.topleft),
                point - V2(self.circle.rect.topleft),
                2
            )
        self.group.draw()
run()
