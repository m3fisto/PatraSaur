import pygame

from config import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 145.0
        self.velocity_y = 0.0
        self.gravity = 1800
        self.jump_strength = -690
        self.move_speed = 330
        self.ducking = False
        self.resting = False
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

    def update(self, delta_time, keys, active, platforms, world_width, ground_y=ROAD_TOP):
        if not active or self.resting:
            return
        self.ducking = bool(keys[pygame.K_DOWN]) and self.on_ground
        self.is_moving = bool(keys[pygame.K_LEFT] or keys[pygame.K_RIGHT])
        if keys[pygame.K_LEFT]:
            self.rect.x -= round(self.move_speed * delta_time)
            self.facing_left = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += round(self.move_speed * delta_time)
            self.facing_left = False
        self.rect.left = max(0, min(self.rect.left, world_width - self.rect.width))

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP]) and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False
            self.ducking = False

        target_size = (84, 48) if self.ducking else (68, 66)
        if self.rect.size != target_size:
            bottom = self.rect.bottom
            self.rect.size = target_size
            self.rect.bottom = bottom

        previous_bottom = self.rect.bottom
        self.velocity_y += self.gravity * delta_time
        self.rect.y += int(self.velocity_y * delta_time)
        landing_platform = None
        if self.velocity_y >= 0:
            for platform in platforms:
                is_above_platform = previous_bottom <= platform.rect.top
                has_crossed_platform = self.rect.bottom >= platform.rect.top
                is_over_platform = self.rect.right > platform.rect.left and self.rect.left < platform.rect.right
                if is_above_platform and has_crossed_platform and is_over_platform:
                    landing_platform = platform
                    break

        if landing_platform:
            self.rect.bottom = landing_platform.rect.top
            self.velocity_y = 0
            self.on_ground = True
        elif ground_y is not None and self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if self.is_moving:
            self.animation_time += delta_time

    def draw(self, screen, camera_x):
        if self.ducking or self.resting:
            image = self.left_crouch_frame if self.facing_left else self.crouch_frame
            image_rect = image.get_rect(midbottom=(self.rect.centerx - camera_x, self.rect.bottom))
            screen.blit(image, image_rect)
            return

        if self.on_ground and self.is_moving and not self.ducking:
            stride_frame = int(self.animation_time * 12) % 2
        else:
            stride_frame = 0
        frames = self.left_run_frames if self.facing_left else self.run_frames
        image_rect = frames[stride_frame].get_rect(midbottom=(self.rect.centerx - camera_x, self.rect.bottom))
        screen.blit(frames[stride_frame], image_rect)


class Platform:
    def __init__(self, position_x, position_y, width, style="stone"):
        self.rect = pygame.Rect(position_x, position_y, width, 24)
        self.style = style

    def draw(self, screen, camera_x):
        draw_rect = self.rect.move(-camera_x, 0)
        if self.style == "invisible":
            return
        if self.style == "log":
            bark_color = (96, 57, 30)
            wood_color = (157, 98, 52)
            cut_color = (207, 151, 84)
            pygame.draw.rect(screen, bark_color, draw_rect, border_radius=11)
            pygame.draw.rect(screen, wood_color, (draw_rect.x + 10, draw_rect.y + 2, draw_rect.width - 20, draw_rect.height - 4), border_radius=9)
            pygame.draw.circle(screen, cut_color, draw_rect.midleft, 10)
            pygame.draw.circle(screen, cut_color, draw_rect.midright, 10)
            pygame.draw.circle(screen, (157, 105, 59), draw_rect.midleft, 4)
            pygame.draw.circle(screen, (157, 105, 59), draw_rect.midright, 4)
            for grain_x in range(draw_rect.x + 28, draw_rect.right - 20, 34):
                pygame.draw.line(screen, (116, 68, 35), (grain_x, draw_rect.y + 6), (grain_x + 12, draw_rect.bottom - 6), 2)
            return
        if self.style == "car":
            body_color = (184, 62, 55) if (self.rect.x // 100) % 2 else (48, 105, 169)
            pygame.draw.rect(screen, (25, 30, 36), (draw_rect.x + 8, draw_rect.bottom - 6, draw_rect.width - 16, 12), border_radius=5)
            pygame.draw.rect(screen, body_color, (draw_rect.x, draw_rect.y + 8, draw_rect.width, 20), border_radius=7)
            pygame.draw.polygon(screen, body_color, [(draw_rect.x + 28, draw_rect.y + 8), (draw_rect.x + 46, draw_rect.y - 12), (draw_rect.right - 38, draw_rect.y - 12), (draw_rect.right - 18, draw_rect.y + 8)])
            pygame.draw.polygon(screen, (145, 199, 220), [(draw_rect.x + 50, draw_rect.y + 5), (draw_rect.x + 58, draw_rect.y - 8), (draw_rect.centerx - 4, draw_rect.y - 8), (draw_rect.centerx - 4, draw_rect.y + 5)])
            pygame.draw.circle(screen, (17, 21, 25), (draw_rect.x + 28, draw_rect.bottom), 9)
            pygame.draw.circle(screen, (17, 21, 25), (draw_rect.right - 28, draw_rect.bottom), 9)
            return
        pygame.draw.rect(screen, (105, 114, 121), draw_rect, border_radius=4)
        pygame.draw.rect(screen, (211, 220, 223), (draw_rect.x, draw_rect.y, draw_rect.width, 6), border_radius=3)
        pygame.draw.rect(screen, (73, 81, 87), (draw_rect.x + 8, draw_rect.bottom - 6, draw_rect.width - 16, 3))


class Resource:
    def __init__(self, resource_type, position_x, ground_y=ROAD_TOP):
        self.resource_type = resource_type
        self.image = None
        if resource_type == "meat":
            self.rect = pygame.Rect(position_x, ground_y - 31, 40, 31)
            image = pygame.image.load(MEAT_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.smoothscale(image, self.rect.size)
        elif resource_type == "water":
            self.rect = pygame.Rect(position_x, ground_y - 46, RESOURCE_WIDTHS["water"], 46)
            image = pygame.image.load(BOTTLE_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.smoothscale(image, self.rect.size)
        else:
            self.rect = pygame.Rect(position_x, ground_y - 52, RESOURCE_WIDTHS["weapon"], 52)
            image = pygame.image.load(WEAPON_IMAGE_PATH).convert_alpha()
            self.image = pygame.transform.smoothscale(image, self.rect.size)

    def draw(self, screen, camera_x):
        draw_rect = self.rect.move(-camera_x, 0)
        if self.resource_type == "meat":
            screen.blit(self.image, draw_rect)
        elif self.resource_type == "water":
            screen.blit(self.image, draw_rect)
        else:
            screen.blit(self.image, draw_rect)


class SickApatosaurus:
    def __init__(self):
        self.rect = pygame.Rect(SICK_APATOSAURUS_X, ROAD_TOP - 168, 308, 195)
        self.sleeping_image = self._load_image(SLEEPING_APATOSAURUS_IMAGE_PATH)
        self.awake_image = self._load_image(AWAKE_APATOSAURUS_IMAGE_PATH)
        self.healed = False

    def _load_image(self, image_path):
        image = pygame.image.load(image_path).convert_alpha()
        return pygame.transform.smoothscale(image, self.rect.size)

    def draw(self, screen, camera_x):
        image = self.awake_image if self.healed else self.sleeping_image
        screen.blit(image, self.rect.move(-camera_x, 0))


class Velociraptor:
    def __init__(self, position_x=NAFPAKTOS_CASTLE_X + 300):
        self.frames = self._load_frames()
        self.left_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.rect = pygame.Rect(position_x, ROAD_TOP - 78, 121, 78)
        self.speed = 155
        self.animation_time = 0.0
        self.awake = False
        self.dead = False
        self.hits = 0

    @staticmethod
    def _load_frames():
        frames = []
        for image_path in VELOCIRAPTOR_FRAME_PATHS:
            image = pygame.image.load(image_path).convert_alpha()
            target_height = 78
            target_width = round(image.get_width() * target_height / image.get_height())
            frames.append(pygame.transform.smoothscale(image, (target_width, target_height)))
        return frames

    def update(self, delta_time, player, camera_x):
        if self.dead:
            return
        is_visible = self.rect.right >= camera_x and self.rect.left <= camera_x + WIDTH
        self.awake = self.awake or is_visible
        if self.awake:
            if self.rect.centerx < player.rect.centerx:
                self.rect.x += round(self.speed * delta_time)
            elif self.rect.centerx > player.rect.centerx:
                self.rect.x -= round(self.speed * delta_time)
            self.animation_time += delta_time

    def take_hit(self):
        self.hits += 1
        if self.hits >= 2:
            self.dead = True

    def draw(self, screen, camera_x, player_x):
        if self.dead:
            return
        moving_left = self.rect.centerx > player_x
        frames = self.left_frames if moving_left else self.frames
        frame_index = int(self.animation_time * 8) % len(frames) if self.awake else 0
        image_rect = frames[frame_index].get_rect(midbottom=(self.rect.centerx - camera_x, self.rect.bottom))
        screen.blit(frames[frame_index], image_rect)


class ThrownWeapon:
    def __init__(self, position_x, position_y, moving_left):
        image = pygame.image.load(WEAPON_IMAGE_PATH).convert_alpha()
        target_height = 32
        target_width = round(image.get_width() * target_height / image.get_height())
        self.image = pygame.transform.smoothscale(image, (target_width, target_height))
        self.rect = self.image.get_rect(center=(position_x, position_y))
        self.speed = -620 if moving_left else 620

    def update(self, delta_time):
        self.rect.x += round(self.speed * delta_time)

    def draw(self, screen, camera_x):
        screen.blit(self.image, self.rect.move(-camera_x, 0))


