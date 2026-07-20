import random
from pathlib import Path

import pygame


WIDTH, HEIGHT = 1200, 600
BRIDGE_WORLD_WIDTH = 3600
NAFPAKTOS_WORLD_WIDTH = BRIDGE_WORLD_WIDTH * 2
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
MEAT_IMAGE_PATH = Path(__file__).with_name("meat.png")
BOTTLE_IMAGE_PATH = Path(__file__).with_name("bottle.png")
WEAPON_IMAGE_PATH = Path(__file__).with_name("weapon.png")
RESOURCE_TARGETS = {"meat": 3, "water": 3, "weapon": 3}
RESOURCE_WIDTHS = {"meat": 40, "water": 52, "weapon": 45}
RESOURCE_IMAGE_PATHS = {
    "meat": MEAT_IMAGE_PATH,
    "water": BOTTLE_IMAGE_PATH,
    "weapon": WEAPON_IMAGE_PATH,
}


class BridgeBackground:
    def __init__(self):
        self.clouds = [
            [180.0, 95, 1.0, 14],
            [720.0, 170, 0.7, 10],
            [1100.0, 65, 1.25, 17],
        ]
        self.sign_font = pygame.font.Font(None, 28)

    def update(self, delta_time):
        for cloud in self.clouds:
            cloud[0] -= cloud[3] * delta_time
            if cloud[0] < -180 * cloud[2]:
                cloud[0] = WIDTH + 80

    def draw(self, screen, camera_x):
        screen.fill(SKY)
        self._draw_clouds(screen)
        self._draw_mountains(screen, camera_x)
        self._draw_bridge(screen, camera_x)
        pygame.draw.rect(screen, ROAD, (0, ROAD_TOP, WIDTH, HEIGHT - ROAD_TOP))
        pygame.draw.rect(screen, (215, 222, 226), (0, ROAD_TOP, WIDTH, 7))

        first_marker_x = int(camera_x // 80) * 80 - 80
        for marker_x in range(first_marker_x, int(camera_x + WIDTH + 80), 80):
            pygame.draw.rect(screen, (244, 202, 72), (marker_x - camera_x, 540, 42, 5))

        self._draw_patras_sign(screen, camera_x)
        self._draw_nafpaktos_sign(screen, camera_x)

    def _draw_patras_sign(self, screen, camera_x):
        sign_x = 5 - camera_x
        sign_y = ROAD_TOP - 105
        sign_width = 140
        sign_height = 64
        sign_color = (24, 91, 166)
        border_color = (238, 245, 250)

        pygame.draw.rect(screen, (104, 110, 113), (sign_x + 78, sign_y + sign_height, 10, ROAD_TOP - sign_y - sign_height))
        points = [
            (sign_x, sign_y + sign_height // 2),
            (sign_x + 25, sign_y),
            (sign_x + sign_width, sign_y),
            (sign_x + sign_width, sign_y + sign_height),
            (sign_x + 25, sign_y + sign_height),
        ]
        pygame.draw.polygon(screen, sign_color, points)
        pygame.draw.lines(screen, border_color, True, points, 3)
        label = self.sign_font.render("Πάτρα", True, border_color)
        label_rect = label.get_rect(center=(sign_x + 87, sign_y + sign_height // 2))
        screen.blit(label, label_rect)

    def _draw_nafpaktos_sign(self, screen, camera_x):
        sign_width = 160
        sign_height = 64
        sign_x = BRIDGE_WORLD_WIDTH - sign_width - camera_x
        sign_y = ROAD_TOP - 105
        sign_color = (24, 91, 166)
        border_color = (238, 245, 250)

        pygame.draw.rect(screen, (104, 110, 113), (sign_x + 70, sign_y + sign_height, 10, ROAD_TOP - sign_y - sign_height))
        points = [
            (sign_x, sign_y),
            (sign_x + sign_width - 25, sign_y),
            (sign_x + sign_width, sign_y + sign_height // 2),
            (sign_x + sign_width - 25, sign_y + sign_height),
            (sign_x, sign_y + sign_height),
        ]
        pygame.draw.polygon(screen, sign_color, points)
        pygame.draw.lines(screen, border_color, True, points, 3)
        label = self.sign_font.render("Ναύπακτος", True, border_color)
        label_rect = label.get_rect(center=(sign_x + 70, sign_y + sign_height // 2))
        screen.blit(label, label_rect)

    def _draw_clouds(self, screen):
        for position_x, position_y, scale, _ in self.clouds:
            width = round(105 * scale)
            height = round(34 * scale)
            cloud_color = (245, 250, 252)
            pygame.draw.ellipse(screen, cloud_color, (position_x, position_y + height // 2, width, height))
            pygame.draw.circle(screen, cloud_color, (round(position_x + width * 0.3), round(position_y + height * 0.6)), round(height * 0.7))
            pygame.draw.circle(screen, cloud_color, (round(position_x + width * 0.55), round(position_y + height * 0.45)), round(height * 0.9))
            pygame.draw.circle(screen, cloud_color, (round(position_x + width * 0.75), round(position_y + height * 0.65)), round(height * 0.65))

    def _draw_mountains(self, screen, camera_x):
        first_mountain_x = int(camera_x // 500) * 500 - 500
        for base_x in range(first_mountain_x, int(camera_x + WIDTH + 500), 500):
            position_x = base_x - camera_x
            points = [(position_x, ROAD_TOP), (position_x + 210, 275), (position_x + 430, ROAD_TOP)]
            pygame.draw.polygon(screen, (107, 143, 149), points)
            pygame.draw.polygon(screen, (92, 127, 132), [(position_x + 190, ROAD_TOP), (position_x + 350, 330), (position_x + 540, ROAD_TOP)])

    def _draw_bridge(self, screen, camera_x):
        first_pylon_x = int(camera_x // 360) * 360 - 360
        for base_x in range(first_pylon_x, int(camera_x + WIDTH + 360), 360):
            pylon_x = base_x - camera_x
            pylon_top = 130
            pygame.draw.rect(screen, (179, 187, 190), (pylon_x - 13, pylon_top, 26, ROAD_TOP - pylon_top))
            pygame.draw.rect(screen, (136, 148, 153), (pylon_x - 18, pylon_top, 36, 14))
            for deck_x in range(int(pylon_x - 180), int(pylon_x + 181), 45):
                pygame.draw.line(screen, (217, 224, 225), (pylon_x, pylon_top + 14), (deck_x, ROAD_TOP), 2)


class NafpaktosBackground:
    def __init__(self):
        self.clouds = [[210.0, 80, 0.9, 10], [710.0, 130, 1.2, 13], [1080.0, 55, 0.7, 8]]
        self.sign_font = pygame.font.Font(None, 28)

    def update(self, delta_time):
        for cloud in self.clouds:
            cloud[0] -= cloud[3] * delta_time
            if cloud[0] < -180 * cloud[2]:
                cloud[0] = WIDTH + 80

    def draw(self, screen, camera_x):
        screen.fill((121, 202, 232))
        self._draw_clouds(screen)
        self._draw_hills(screen, camera_x)
        pygame.draw.rect(screen, (52, 155, 190), (0, 330, WIDTH, HEIGHT - 330))
        self._draw_sailboats(screen, camera_x)
        self._draw_cafes(screen, camera_x)
        self._draw_souvenir_shops(screen, camera_x)
        self._draw_castle(screen, camera_x)
        pygame.draw.rect(screen, (190, 166, 127), (0, ROAD_TOP, WIDTH, HEIGHT - ROAD_TOP))
        pygame.draw.rect(screen, (229, 214, 181), (0, ROAD_TOP, WIDTH, 7))
        for stone_x in range(int(camera_x // 55) * 55 - 55, int(camera_x + WIDTH + 55), 55):
            pygame.draw.line(screen, (154, 134, 103), (stone_x - camera_x, 545), (stone_x - camera_x + 35, 545), 3)
        self._draw_bridge_sign(screen, camera_x)
        self._draw_kravara_sign(screen, camera_x)

    def _draw_bridge_sign(self, screen, camera_x):
        sign_x = 5 - camera_x
        sign_y = ROAD_TOP - 105
        sign_width = 140
        sign_height = 64
        sign_color = (24, 91, 166)
        border_color = (238, 245, 250)
        pygame.draw.rect(screen, (104, 110, 113), (sign_x + 78, sign_y + sign_height, 10, ROAD_TOP - sign_y - sign_height))
        points = [
            (sign_x, sign_y + sign_height // 2),
            (sign_x + 25, sign_y),
            (sign_x + sign_width, sign_y),
            (sign_x + sign_width, sign_y + sign_height),
            (sign_x + 25, sign_y + sign_height),
        ]
        pygame.draw.polygon(screen, sign_color, points)
        pygame.draw.lines(screen, border_color, True, points, 3)
        label = self.sign_font.render("Γεφυρα", True, border_color)
        screen.blit(label, label.get_rect(center=(sign_x + 87, sign_y + sign_height // 2)))

    def _draw_kravara_sign(self, screen, camera_x):
        sign_width = 160
        sign_height = 64
        sign_x = NAFPAKTOS_WORLD_WIDTH - sign_width - camera_x
        sign_y = ROAD_TOP - 105
        sign_color = (24, 91, 166)
        border_color = (238, 245, 250)
        pygame.draw.rect(screen, (104, 110, 113), (sign_x + 70, sign_y + sign_height, 10, ROAD_TOP - sign_y - sign_height))
        points = [
            (sign_x, sign_y),
            (sign_x + sign_width - 25, sign_y),
            (sign_x + sign_width, sign_y + sign_height // 2),
            (sign_x + sign_width - 25, sign_y + sign_height),
            (sign_x, sign_y + sign_height),
        ]
        pygame.draw.polygon(screen, sign_color, points)
        pygame.draw.lines(screen, border_color, True, points, 3)
        label = self.sign_font.render("Κράβαρα", True, border_color)
        screen.blit(label, label.get_rect(center=(sign_x + 70, sign_y + sign_height // 2)))

    def _draw_clouds(self, screen):
        for position_x, position_y, scale, _ in self.clouds:
            width, height = round(105 * scale), round(34 * scale)
            color = (247, 251, 252)
            pygame.draw.ellipse(screen, color, (position_x, position_y + height // 2, width, height))
            pygame.draw.circle(screen, color, (round(position_x + width * .35), round(position_y + height * .6)), round(height * .7))
            pygame.draw.circle(screen, color, (round(position_x + width * .6), round(position_y + height * .48)), round(height * .85))

    def _draw_hills(self, screen, camera_x):
        first_hill_x = int(camera_x // 700) * 700 - 700
        for world_x in range(first_hill_x, int(camera_x + WIDTH + 700), 700):
            position_x = world_x - camera_x
            pygame.draw.polygon(screen, (102, 147, 134), [(position_x, 330), (position_x + 280, 160), (position_x + 620, 330)])

    def _draw_sailboats(self, screen, camera_x):
        for world_x in range(380, NAFPAKTOS_WORLD_WIDTH, 760):
            position_x = world_x - camera_x
            water_y = 390 + (world_x // 160 % 3) * 18
            pygame.draw.polygon(screen, (245, 247, 241), [(position_x - 35, water_y), (position_x + 40, water_y), (position_x + 20, water_y + 12), (position_x - 23, water_y + 12)])
            pygame.draw.line(screen, (84, 73, 59), (position_x, water_y), (position_x, water_y - 74), 3)
            pygame.draw.polygon(screen, (250, 245, 226), [(position_x + 3, water_y - 68), (position_x + 3, water_y - 7), (position_x + 42, water_y - 7)])
            pygame.draw.polygon(screen, (54, 112, 151), [(position_x - 3, water_y - 53), (position_x - 3, water_y - 6), (position_x - 34, water_y - 6)])

    def _draw_cafes(self, screen, camera_x):
        cafe_positions = (420, 1220, 2050, 2940, 3830, 4720, 5700, 6420)
        for index, world_x in enumerate(cafe_positions):
            position_x = world_x - camera_x
            wall_color = ((246, 233, 205), (239, 223, 194), (248, 238, 215))[index % 3]
            roof_color = ((205, 85, 61), (193, 106, 57), (180, 77, 70))[index % 3]
            pygame.draw.rect(screen, wall_color, (position_x, 360, 150, 125))
            pygame.draw.polygon(screen, roof_color, [(position_x - 12, 360), (position_x + 75, 318), (position_x + 162, 360)])
            pygame.draw.rect(screen, (69, 109, 137), (position_x + 28, 405, 32, 45))
            pygame.draw.rect(screen, (69, 109, 137), (position_x + 92, 392, 35, 27))
            pygame.draw.rect(screen, (255, 248, 225), (position_x + 18, 435, 115, 11))

    def _draw_souvenir_shops(self, screen, camera_x):
        shop_positions = (790, 1660, 2550, 3460, 4380, 5400, 6250)
        for index, world_x in enumerate(shop_positions):
            position_x = world_x - camera_x
            wall_color = ((236, 224, 193), (227, 213, 184), (242, 229, 203))[index % 3]
            awning_color = ((54, 121, 167), (201, 91, 69), (61, 146, 126))[index % 3]
            pygame.draw.rect(screen, wall_color, (position_x, 385, 112, 100))
            pygame.draw.rect(screen, (91, 73, 53), (position_x + 15, 425, 34, 60))
            pygame.draw.rect(screen, (73, 117, 144), (position_x + 65, 422, 30, 28))
            for stripe_x in range(position_x - 4, position_x + 116, 18):
                pygame.draw.polygon(screen, awning_color, [(stripe_x, 386), (stripe_x + 10, 386), (stripe_x + 16, 410), (stripe_x + 6, 410)])
            pygame.draw.circle(screen, (226, 181, 48), (position_x + 82, 443), 7)
            pygame.draw.circle(screen, (213, 97, 66), (position_x + 72, 455), 6)
            pygame.draw.circle(screen, (70, 151, 129), (position_x + 91, 457), 6)

    def _draw_castle(self, screen, camera_x):
        castle_width = 540
        castle_height = 125
        castle_x = NAFPAKTOS_WORLD_WIDTH - castle_width - 180 - camera_x
        castle_y = ROAD_TOP - castle_height
        pygame.draw.rect(screen, (157, 142, 113), (castle_x, castle_y, castle_width, castle_height))
        for tower_x in (castle_x, castle_x + 240, castle_x + 488):
            pygame.draw.rect(screen, (139, 124, 97), (tower_x, castle_y - 35, 52, castle_height + 35))
            pygame.draw.polygon(screen, (116, 102, 80), [(tower_x - 5, castle_y - 35), (tower_x + 26, castle_y - 60), (tower_x + 57, castle_y - 35)])
        for window_x in range(castle_x + 28, castle_x + castle_width - 24, 48):
            pygame.draw.rect(screen, (72, 79, 77), (window_x, castle_y + 50, 14, 24))


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

    def update(self, delta_time, keys, active, platforms, world_width):
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
        self.rect.clamp_ip(pygame.Rect(0, 0, world_width, ROAD_TOP))

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
        elif self.rect.bottom >= ROAD_TOP:
            self.rect.bottom = ROAD_TOP
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False

        if self.is_moving:
            self.animation_time += delta_time

    def draw(self, screen, camera_x):
        if self.ducking:
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
    def __init__(self, position_x, position_y, width):
        self.rect = pygame.Rect(position_x, position_y, width, 24)

    def draw(self, screen, camera_x):
        draw_rect = self.rect.move(-camera_x, 0)
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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("T-Rex on the Rio-Antirrio Bridge")
        self.clock = pygame.time.Clock()
        self.background = BridgeBackground()
        self.player = Player()
        self.level_name = "Rio–Antirrio Bridge"
        self.world_width = BRIDGE_WORLD_WIDTH
        self.platforms = self._create_bridge_platforms()
        self.resources = self._create_resources()
        self.collected = {resource_type: 0 for resource_type in RESOURCE_TARGETS}
        self.hud_font = pygame.font.Font(None, 32)
        self.hud_icons = self._load_hud_icons()
        self.camera_x = 0.0
        self.running = True

    @staticmethod
    def _create_bridge_platforms():
        return [
            Platform(560, ROAD_TOP - 75, 190),
            Platform(940, ROAD_TOP - 125, 180),
            Platform(1320, ROAD_TOP - 70, 220),
            Platform(1870, ROAD_TOP - 110, 210),
            Platform(2310, ROAD_TOP - 155, 180),
            Platform(2780, ROAD_TOP - 80, 230),
        ]

    @staticmethod
    def _create_nafpaktos_platforms():
        return [
            Platform(680, ROAD_TOP - 80, 220),
            Platform(1480, ROAD_TOP - 125, 250),
            Platform(2350, ROAD_TOP - 95, 210),
            Platform(3260, ROAD_TOP - 150, 230),
            Platform(4180, ROAD_TOP - 105, 240),
            Platform(5120, ROAD_TOP - 175, 280),
            Platform(6080, ROAD_TOP - 90, 240),
        ]

    def _create_resources(self):
        resource_types = ["meat"] * RESOURCE_TARGETS["meat"]
        resource_types += ["water"] * RESOURCE_TARGETS["water"]
        resource_types += ["weapon"] * RESOURCE_TARGETS["weapon"]
        random.shuffle(resource_types)

        resources = []
        platform_resource_count = (len(resource_types) + 1) // 2
        for resource_type in resource_types[:platform_resource_count]:
            platform = random.choice(self.platforms)
            resource_width = RESOURCE_WIDTHS[resource_type]
            position_x = random.randint(platform.rect.left + 12, platform.rect.right - resource_width - 12)
            resources.append(Resource(resource_type, position_x, platform.rect.top))

        ground_positions = random.sample(range(350, BRIDGE_WORLD_WIDTH - 350, 340), len(resource_types) - platform_resource_count)
        for resource_type, position_x in zip(resource_types[platform_resource_count:], ground_positions):
            resources.append(Resource(resource_type, position_x))
        return resources

    @staticmethod
    def _load_hud_icons():
        icons = {}
        for resource_type, image_path in RESOURCE_IMAGE_PATHS.items():
            image = pygame.image.load(image_path).convert_alpha()
            target_height = 26
            target_width = round(image.get_width() * target_height / image.get_height())
            icons[resource_type] = pygame.transform.smoothscale(image, (target_width, target_height))
        return icons

    def _collect_resources(self):
        for resource in self.resources[:]:
            if self.player.rect.colliderect(resource.rect):
                self.collected[resource.resource_type] += 1
                self.resources.remove(resource)

    def _draw_hud(self):
        panel = pygame.Surface((155, 120), pygame.SRCALPHA)
        panel.fill((16, 27, 36, 185))
        panel_x = WIDTH - panel.get_width() - 18
        panel_y = 18
        self.screen.blit(panel, (panel_x, panel_y))
        for index, (resource_type, target) in enumerate(RESOURCE_TARGETS.items()):
            row_y = panel_y + 10 + index * 37
            icon = self.hud_icons[resource_type]
            icon_rect = icon.get_rect(midleft=(panel_x + 14, row_y + 13))
            self.screen.blit(icon, icon_rect)
            counter_surface = self.hud_font.render(f"{self.collected[resource_type]}/{target}", True, (255, 255, 255))
            self.screen.blit(counter_surface, (panel_x + 70, row_y))

        if self.level_name == "Rio–Antirrio Bridge" and not self.resources:
            complete_surface = self.hud_font.render("Η πίστα ολοκληρώθηκε!", True, (255, 245, 158))
            self.screen.blit(complete_surface, complete_surface.get_rect(center=(WIDTH // 2, 82)))

    def update_camera(self):
        target_x = self.player.rect.centerx - WIDTH // 2
        self.camera_x = max(0, min(target_x, self.world_width - WIDTH))

    def _start_nafpaktos_level(self):
        self.level_name = "Nafpaktos"
        self.world_width = NAFPAKTOS_WORLD_WIDTH
        self.background = NafpaktosBackground()
        self.platforms = self._create_nafpaktos_platforms()
        self.resources = []
        self.player = Player()
        self.camera_x = 0.0

    def _return_to_bridge_level(self):
        self.level_name = "Rio–Antirrio Bridge"
        self.world_width = BRIDGE_WORLD_WIDTH
        self.background = BridgeBackground()
        self.platforms = self._create_bridge_platforms()
        self.player = Player()
        self.player.rect.centerx = BRIDGE_WORLD_WIDTH - 300
        self.camera_x = BRIDGE_WORLD_WIDTH - WIDTH

    def _check_level_transition(self):
        has_reached_nafpaktos_sign = self.player.rect.right >= BRIDGE_WORLD_WIDTH - 160
        if self.level_name == "Rio–Antirrio Bridge" and not self.resources and has_reached_nafpaktos_sign:
            self._start_nafpaktos_level()
        elif self.level_name == "Nafpaktos" and self.player.rect.left <= 0:
            self._return_to_bridge_level()

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            keys = pygame.key.get_pressed()
            self.player.update(delta_time, keys, True, self.platforms, self.world_width)
            self._collect_resources()
            self._check_level_transition()
            self.update_camera()
            self.background.update(delta_time)

            self.background.draw(self.screen, self.camera_x)
            for platform in self.platforms:
                platform.draw(self.screen, self.camera_x)
            for resource in self.resources:
                resource.draw(self.screen, self.camera_x)
            self.player.draw(self.screen, self.camera_x)
            self._draw_hud()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()