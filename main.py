from pathlib import Path

import pygame


WIDTH, HEIGHT = 1600, 600
FPS = 60
ROAD_TOP = 485
GROUND_Y = ROAD_TOP - 66
SKY = (123, 202, 235)
ROAD = (48, 52, 58)
RUN_FRAME_PATHS = (
    Path(__file__).with_name("dinoa.png"),
    Path(__file__).with_name("dinob.png"),
)
CROUCH_FRAME_PATH = Path(__file__).with_name("couching.png")


class Background:
    def draw(self, screen):
        screen.fill(SKY)
        self._draw_mountains(screen)
        self._draw_bridge(screen)
        pygame.draw.rect(screen, ROAD, (0, ROAD_TOP, WIDTH, HEIGHT - ROAD_TOP))
        pygame.draw.rect(screen, (215, 222, 226), (0, ROAD_TOP, WIDTH, 7))

        for marker_x in range(-80, WIDTH + 80, 80):
            pygame.draw.rect(screen, (244, 202, 72), (marker_x, 540, 42, 5))

    def _draw_mountains(self, screen):
        for base_x in range(-500, WIDTH + 500, 500):
            position_x = base_x
            points = [(position_x, ROAD_TOP), (position_x + 210, 275), (position_x + 430, ROAD_TOP)]
            pygame.draw.polygon(screen, (107, 143, 149), points)
            pygame.draw.polygon(screen, (92, 127, 132), [(position_x + 190, ROAD_TOP), (position_x + 350, 330), (position_x + 540, ROAD_TOP)])

    def _draw_bridge(self, screen):
        for base_x in range(-360, WIDTH + 360, 360):
            pylon_x = base_x
            pylon_top = 130
            pygame.draw.rect(screen, (179, 187, 190), (pylon_x - 13, pylon_top, 26, ROAD_TOP - pylon_top))
            pygame.draw.rect(screen, (136, 148, 153), (pylon_x - 18, pylon_top, 36, 14))
            for deck_x in range(int(pylon_x - 180), int(pylon_x + 181), 45):
                pygame.draw.line(screen, (217, 224, 225), (pylon_x, pylon_top + 14), (deck_x, ROAD_TOP), 2)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 145.0
        self.velocity_y = 0.0
        self.gravity = 1800
        self.jump_strength = -690
        self.move_speed = 330
        self.ducking = False
        self.on_ground = True
        self.is_moving = False
        self.facing_left = False
        self.animation_time = 0.0
        self.run_frames = self._load_run_frames()
        self.left_run_frames = [pygame.transform.flip(frame, True, False) for frame in self.run_frames]
        self.crouch_frame = self._load_frame(CROUCH_FRAME_PATH, 58)
        self.left_crouch_frame = pygame.transform.flip(self.crouch_frame, True, False)
        self.rect = pygame.Rect(int(self.x), GROUND_Y, 68, 66)

    @staticmethod
    def _load_frame(image_path, target_height):
        image = pygame.image.load(image_path).convert_alpha()
        target_width = round(image.get_width() * target_height / image.get_height())
        return pygame.transform.smoothscale(image, (target_width, target_height))

    @classmethod
    def _load_run_frames(cls):
        frames = []
        for image_path in RUN_FRAME_PATHS:
            frames.append(cls._load_frame(image_path, 78))
        return frames

    def update(self, delta_time, keys, active):
        if not active:
            return
        self.ducking = bool(keys[pygame.K_DOWN]) and self.on_ground
        self.is_moving = bool(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])
        if keys[pygame.K_LEFT]:
            self.rect.x -= round(self.move_speed * delta_time)
            self.facing_left = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += round(self.move_speed * delta_time)
            self.facing_left = False
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, ROAD_TOP))

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.ducking = False

        target_size = (84, 48) if self.ducking else (68, 66)
        if self.rect.size != target_size:
            bottom = self.rect.bottom
            self.rect.size = target_size
            self.rect.bottom = bottom

        self.velocity_y += self.gravity * delta_time
        self.rect.y += int(self.velocity_y * delta_time)
        if self.rect.bottom >= ROAD_TOP:
            self.rect.bottom = ROAD_TOP
            self.velocity_y = 0
            self.on_ground = True

        if self.is_moving:
            self.animation_time += delta_time

    def draw(self, screen):
        if self.ducking:
            image = self.left_crouch_frame if self.facing_left else self.crouch_frame
            image_rect = image.get_rect(midbottom=self.rect.midbottom)
            screen.blit(image, image_rect)
            return

        if self.on_ground and self.is_moving and not self.ducking:
            stride_frame = int(self.animation_time * 12) % 2
        else:
            stride_frame = 0
        frames = self.left_run_frames if self.facing_left else self.run_frames
        image_rect = frames[stride_frame].get_rect(midbottom=self.rect.midbottom)
        screen.blit(frames[stride_frame], image_rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("T-Rex on the Rio-Antirrio Bridge")
        self.clock = pygame.time.Clock()
        self.background = Background()
        self.player = Player()
        self.running = True

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.update(delta_time, keys, True)

            self.background.draw(self.screen)
            self.player.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()