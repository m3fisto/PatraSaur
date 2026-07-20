import random
from pathlib import Path

import pygame


WIDTH, HEIGHT = 1200, 600
BRIDGE_WORLD_WIDTH = 3600
NAFPAKTOS_WORLD_WIDTH = BRIDGE_WORLD_WIDTH
NAFPAKTOS_CASTLE_X = NAFPAKTOS_WORLD_WIDTH - 540 - 180
MOUNTAIN_RIVER_WORLD_WIDTH = 3000
FERRY_BOAT_WORLD_WIDTH = 3000
PATRAS_CITY_WORLD_WIDTH = 3300
SCHOOL_WORLD_WIDTH = 2000
CLASSROOM_WORLD_WIDTH = 1500
SICK_APATOSAURUS_X = MOUNTAIN_RIVER_WORLD_WIDTH - 580
ROCKY_BARRIER_X = SICK_APATOSAURUS_X + 308
STONE_BRIDGE_DECK_Y = 272
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
HEART_IMAGE_PATH = Path(__file__).with_name("heart.png")
SLEEPING_APATOSAURUS_IMAGE_PATH = Path(__file__).with_name("apatosaurousSleeping.png")
AWAKE_APATOSAURUS_IMAGE_PATH = Path(__file__).with_name("apatosaurousUp.png")
LOCHNESS_IMAGE_PATH = Path(__file__).with_name("lochness.png")
MONSTER_NECK_IMAGE_PATH = Path(__file__).with_name("monsterneck.png")
VELOCIRAPTOR_FRAME_PATHS = (
    Path(__file__).with_name("velociraptor1.png"),
    Path(__file__).with_name("velociraptor2.png"),
)
RESOURCE_TARGETS = {"meat": 3, "water": 3, "weapon": 3}
RESOURCE_WIDTHS = {"meat": 40, "water": 52, "weapon": 45}
RESOURCE_IMAGE_PATHS = {
    "meat": MEAT_IMAGE_PATH,
    "water": BOTTLE_IMAGE_PATH,
    "weapon": WEAPON_IMAGE_PATH,
    "heart": HEART_IMAGE_PATH,
}
MAX_HEALTH = 3


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
        cafe_positions = (420, 1120, 1820, 2480)
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
        shop_positions = (760, 1500, 2220)
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
        castle_x = NAFPAKTOS_CASTLE_X - camera_x
        castle_y = ROAD_TOP - castle_height
        pygame.draw.rect(screen, (157, 142, 113), (castle_x, castle_y, castle_width, castle_height))
        for tower_x in (castle_x, castle_x + 240, castle_x + 488):
            pygame.draw.rect(screen, (139, 124, 97), (tower_x, castle_y - 35, 52, castle_height + 35))
            pygame.draw.polygon(screen, (116, 102, 80), [(tower_x - 5, castle_y - 35), (tower_x + 26, castle_y - 60), (tower_x + 57, castle_y - 35)])
        for window_x in range(castle_x + 28, castle_x + castle_width - 24, 48):
            pygame.draw.rect(screen, (72, 79, 77), (window_x, castle_y + 50, 14, 24))


class MountainRiverBackground:
    def __init__(self):
        self.water_offset = 0.0
        self.lochness_visible = False
        self.lochness_completed = False
        self.lochness_frame_index = 0
        self.lochness_frame_time = 0.0
        self.lochness_frames = self._load_lochness_frames()
        self.fish = [
            [260.0, 500, 230],
            [700.0, 540, 280],
            [1210.0, 510, 250],
            [1690.0, 550, 300],
            [2200.0, 490, 260],
            [2680.0, 535, 290],
        ]
        self.sign_font = pygame.font.Font(None, 28)

    def update(self, delta_time):
        self.water_offset = (self.water_offset + 90 * delta_time) % 80
        if self.lochness_visible:
            self.lochness_frame_time += delta_time
            if self.lochness_frame_time >= 0.25:
                self.lochness_frame_time = 0.0
                if self.lochness_frame_index < len(self.lochness_frames) - 1:
                    self.lochness_frame_index += 1
                else:
                    self.lochness_visible = False
                    self.lochness_completed = True
        for fish in self.fish:
            fish[0] -= fish[2] * delta_time
            if fish[0] < -45:
                fish[0] = MOUNTAIN_RIVER_WORLD_WIDTH + 45

    def draw(self, screen, camera_x):
        screen.fill((115, 178, 206))
        self._draw_mountains(screen, camera_x)
        self._draw_pines(screen, camera_x)
        pygame.draw.rect(screen, (43, 135, 181), (0, 340, WIDTH, HEIGHT - 340))
        self._draw_water_flow(screen, camera_x)
        self._draw_fish(screen, camera_x)
        if self.lochness_visible:
            self._draw_lochness(screen)
        self._draw_arch_bridge(screen, camera_x)
        self._draw_rocky_barrier(screen, camera_x)
        self._draw_nafpaktos_sign(screen, camera_x)
        self._draw_antirrio_sign(screen, camera_x)

    def _draw_nafpaktos_sign(self, screen, camera_x):
        sign_x = 5 - camera_x
        sign_y = ROAD_TOP - 105
        sign_width = 160
        sign_height = 64
        sign_color = (24, 91, 166)
        border_color = (238, 245, 250)
        pygame.draw.rect(screen, (104, 110, 113), (sign_x + 88, sign_y + sign_height, 10, ROAD_TOP - sign_y - sign_height))
        points = [
            (sign_x, sign_y + sign_height // 2),
            (sign_x + 25, sign_y),
            (sign_x + sign_width, sign_y),
            (sign_x + sign_width, sign_y + sign_height),
            (sign_x + 25, sign_y + sign_height),
        ]
        pygame.draw.polygon(screen, sign_color, points)
        pygame.draw.lines(screen, border_color, True, points, 3)
        label = self.sign_font.render("Ναύπακτος", True, border_color)
        screen.blit(label, label.get_rect(center=(sign_x + 95, sign_y + sign_height // 2)))

    def _draw_antirrio_sign(self, screen, camera_x):
        sign_width = 140
        sign_height = 64
        sign_x = MOUNTAIN_RIVER_WORLD_WIDTH - sign_width - 55 - camera_x
        sign_y = STONE_BRIDGE_DECK_Y - sign_height - 86
        sign_color = (24, 91, 166)
        border_color = (238, 245, 250)
        pygame.draw.rect(screen, (104, 110, 113), (sign_x + 60, sign_y + sign_height, 10, STONE_BRIDGE_DECK_Y - sign_y - sign_height))
        points = [
            (sign_x, sign_y),
            (sign_x + sign_width - 25, sign_y),
            (sign_x + sign_width, sign_y + sign_height // 2),
            (sign_x + sign_width - 25, sign_y + sign_height),
            (sign_x, sign_y + sign_height),
        ]
        pygame.draw.polygon(screen, sign_color, points)
        pygame.draw.lines(screen, border_color, True, points, 3)
        label = self.sign_font.render("Αντίριο", True, border_color)
        screen.blit(label, label.get_rect(center=(sign_x + 60, sign_y + sign_height // 2)))

    def _draw_rocky_barrier(self, screen, camera_x):
        barrier_x = ROCKY_BARRIER_X - camera_x
        rock_base = (89, 86, 80)
        rock_mid = (125, 120, 109)
        rock_light = (163, 157, 142)

        pygame.draw.polygon(screen, rock_base, [
            (barrier_x - 18, ROAD_TOP),
            (barrier_x - 12, 360),
            (barrier_x + 35, 300),
            (barrier_x + 110, 320),
            (barrier_x + 155, 385),
            (barrier_x + 145, ROAD_TOP),
        ])
        pygame.draw.polygon(screen, rock_mid, [
            (barrier_x, ROAD_TOP),
            (barrier_x + 4, 372),
            (barrier_x + 42, 318),
            (barrier_x + 84, 335),
            (barrier_x + 126, 395),
            (barrier_x + 120, ROAD_TOP),
        ])
        pygame.draw.polygon(screen, rock_light, [
            (barrier_x + 25, 392),
            (barrier_x + 47, 338),
            (barrier_x + 75, 350),
            (barrier_x + 67, 416),
        ])
        pygame.draw.polygon(screen, rock_light, [
            (barrier_x + 81, 430),
            (barrier_x + 98, 374),
            (barrier_x + 120, 403),
            (barrier_x + 112, 456),
        ])

    def _draw_mountains(self, screen, camera_x):
        first_mountain_x = int(camera_x // 500) * 500 - 500
        for world_x in range(first_mountain_x, int(camera_x + WIDTH + 500), 500):
            position_x = world_x - camera_x
            pygame.draw.polygon(screen, (72, 111, 99), [(position_x, 360), (position_x + 220, 70), (position_x + 470, 360)])
            pygame.draw.polygon(screen, (92, 133, 111), [(position_x + 190, 360), (position_x + 390, 115), (position_x + 650, 360)])

    def _draw_pines(self, screen, camera_x):
        first_tree_x = int(camera_x // 130) * 130 - 130
        for world_x in range(first_tree_x, int(camera_x + WIDTH + 130), 130):
            position_x = world_x - camera_x
            height = 105 + (world_x // 130 % 3) * 23
            base_y = 410
            pygame.draw.rect(screen, (77, 59, 39), (position_x - 5, base_y - height // 3, 10, height // 3))
            for level, width in enumerate((66, 52, 38)):
                top_y = base_y - height + level * 26
                pygame.draw.polygon(screen, (28, 91, 65), [(position_x, top_y), (position_x - width // 2, top_y + 64), (position_x + width // 2, top_y + 64)])

    def _draw_water_flow(self, screen, camera_x):
        for world_x in range(int(camera_x // 80) * 80 - 80, int(camera_x + WIDTH + 80), 80):
            position_x = world_x - camera_x - self.water_offset
            pygame.draw.line(screen, (137, 211, 229), (position_x, 380), (position_x + 42, 380), 3)
            pygame.draw.line(screen, (112, 199, 224), (position_x + 25, 460), (position_x + 70, 460), 3)
            pygame.draw.line(screen, (146, 218, 235), (position_x + 8, 515), (position_x + 58, 515), 3)
            pygame.draw.line(screen, (104, 193, 220), (position_x + 42, 565), (position_x + 78, 565), 3)

    def _draw_fish(self, screen, camera_x):
        for position_x, position_y, _ in self.fish:
            draw_x = position_x - camera_x
            color = (235, 151, 74)
            pygame.draw.ellipse(screen, color, (draw_x, position_y, 28, 12))
            pygame.draw.polygon(screen, color, [(draw_x + 25, position_y + 6), (draw_x + 38, position_y), (draw_x + 38, position_y + 12)])
            pygame.draw.circle(screen, (30, 47, 57), (round(draw_x + 8), position_y + 4), 2)

    @staticmethod
    def _load_lochness_frames():
        sprite_sheet = pygame.image.load(LOCHNESS_IMAGE_PATH).convert_alpha()
        frame_height = sprite_sheet.get_height() // 5
        frames = []
        for frame_index in range(5):
            frame = sprite_sheet.subsurface((0, frame_index * frame_height, sprite_sheet.get_width(), frame_height))
            frames.append(pygame.transform.smoothscale(frame, (250, 60)))
        return frames

    def _draw_lochness(self, screen):
        position_x = 25 - self.lochness_frame_index * 24
        screen.blit(self.lochness_frames[self.lochness_frame_index], (position_x, HEIGHT - 125))

    def _draw_arch_bridge(self, screen, camera_x):
        bridge_x = MOUNTAIN_RIVER_WORLD_WIDTH - 350 - camera_x
        deck_y = STONE_BRIDGE_DECK_Y - 12
        stone = (151, 145, 129)
        light_stone = (188, 180, 160)
        dark_stone = (104, 103, 96)
        water = (43, 135, 181)

        pygame.draw.rect(screen, dark_stone, (bridge_x - 10, deck_y + 20, 370, 48), border_radius=4)
        pygame.draw.rect(screen, stone, (bridge_x - 10, deck_y + 12, 370, 48), border_radius=4)
        pygame.draw.rect(screen, light_stone, (bridge_x - 10, deck_y + 12, 370, 8), border_radius=3)
        pygame.draw.line(screen, dark_stone, (bridge_x, deck_y + 43), (bridge_x + 350, deck_y + 43), 3)

        for rail_x in range(int(bridge_x), int(bridge_x + 350), 38):
            pygame.draw.rect(screen, stone, (rail_x, deck_y - 30, 11, 45))
            pygame.draw.rect(screen, light_stone, (rail_x - 3, deck_y - 34, 17, 7))
        pygame.draw.line(screen, stone, (bridge_x, deck_y - 10), (bridge_x + 350, deck_y - 10), 7)

        arch_center = (bridge_x + 175, 455)
        pygame.draw.circle(screen, stone, arch_center, 165)
        pygame.draw.rect(screen, stone, (bridge_x + 8, 410, 334, 75))
        pygame.draw.circle(screen, water, arch_center, 126)
        pygame.draw.rect(screen, water, (bridge_x + 49, 455, 252, 30))
        pygame.draw.rect(screen, dark_stone, (bridge_x + 8, 432, 40, 53))
        pygame.draw.rect(screen, dark_stone, (bridge_x + 302, 432, 40, 53))

        for row_y in (310, 338, 366, 394):
            offset = 18 if row_y % 2 == 0 else 0
            for stone_x in range(int(bridge_x + offset), int(bridge_x + 350), 44):
                pygame.draw.line(screen, dark_stone, (stone_x, row_y), (stone_x + 26, row_y), 2)


class FerryBoatBackground:
    def __init__(self):
        self.wave_offset = 0.0
        self.rain_offset = 0.0
        self.storm_active = False
        self.lightning_time = 0.0
        self.lightning_cooldown = 0.0
        self.monster_window_index = -1
        self.monster_image = self._load_monster_image()
        self.sign_font = pygame.font.Font(None, 28)

    def update(self, delta_time):
        self.wave_offset = (self.wave_offset + 110 * delta_time) % 120
        if self.storm_active:
            self.rain_offset = (self.rain_offset + 420 * delta_time) % 36
            self.lightning_time = max(0.0, self.lightning_time - delta_time)
            self.lightning_cooldown -= delta_time
            if self.lightning_cooldown <= 0:
                self._trigger_lightning()

    def start_storm(self):
        if not self.storm_active:
            self.storm_active = True
            self._trigger_lightning()

    @staticmethod
    def _load_monster_image():
        image = pygame.image.load(MONSTER_NECK_IMAGE_PATH).convert_alpha()
        return pygame.transform.smoothscale(image, (38, 58))

    def _trigger_lightning(self):
        window_count = FERRY_BOAT_WORLD_WIDTH // 300
        self.monster_window_index = (self.monster_window_index + 1) % window_count
        self.lightning_time = 0.22
        self.lightning_cooldown = random.uniform(1.8, 3.2)

    def draw(self, screen, camera_x):
        screen.fill((8, 16, 35))
        pygame.draw.rect(screen, (19, 31, 52), (0, 80, WIDTH, 315))
        self._draw_stars(screen)
        self._draw_ship_margin(screen)
        pygame.draw.rect(screen, (50, 63, 77), (0, 390, WIDTH, 20))
        pygame.draw.rect(screen, (83, 96, 107), (0, 410, WIDTH, 16))
        self._draw_ship_walls(screen, camera_x)
        self._draw_waves(screen, camera_x)
        if self.storm_active:
            self._draw_rain(screen)
            self._draw_lightning(screen)
        self._draw_exit_sign(screen, camera_x)

    @staticmethod
    def _draw_stars(screen):
        for star_x, star_y in ((45, 106), (105, 154), (180, 120), (260, 92), (340, 145), (430, 112), (520, 164), (610, 96), (700, 138), (795, 108), (885, 158), (970, 94), (1060, 135), (1150, 105)):
            pygame.draw.circle(screen, (215, 226, 236), (star_x, star_y), 2)

    @staticmethod
    def _draw_ship_margin(screen):
        pygame.draw.line(screen, (107, 122, 137), (0, 190), (WIDTH, 190), 5)
        pygame.draw.line(screen, (173, 189, 199), (0, 193), (WIDTH, 193), 2)

    def _draw_ship_walls(self, screen, camera_x):
        first_wall_x = int(camera_x // 300) * 300 - 300
        for world_x in range(first_wall_x, int(camera_x + WIDTH + 300), 300):
            position_x = world_x - camera_x
            pygame.draw.rect(screen, (75, 88, 99), (position_x + 12, 220, 90, 10))
            pygame.draw.rect(screen, (130, 177, 196), (position_x + 30, 250, 52, 72), border_radius=5)
            monster_window_x = FERRY_BOAT_WORLD_WIDTH - (self.monster_window_index + 1) * 300
            if self.lightning_time > 0 and world_x == monster_window_x:
                monster_rect = self.monster_image.get_rect(center=(position_x + 56, 286))
                screen.blit(self.monster_image, monster_rect)
            pygame.draw.rect(screen, (197, 227, 235), (position_x + 35, 255, 42, 62), 2, border_radius=4)

    def _draw_waves(self, screen, camera_x):
        pygame.draw.rect(screen, (16, 76, 118), (0, 470, WIDTH, HEIGHT - 470))
        first_wave_x = int(camera_x // 120) * 120 - 120
        for wave_index, world_x in enumerate(range(first_wave_x, int(camera_x + WIDTH + 120), 120)):
            position_x = world_x - camera_x - self.wave_offset
            if wave_index % 2 == 0:
                pygame.draw.arc(screen, (116, 194, 222), (position_x, 478, 92, 34), 3.35, 6.05, 4)
                pygame.draw.arc(screen, (69, 147, 190), (position_x + 44, 535, 96, 30), 3.2, 5.9, 3)
            else:
                pygame.draw.arc(screen, (82, 164, 202), (position_x, 496, 92, 30), 0.15, 2.95, 4)
                pygame.draw.arc(screen, (132, 205, 227), (position_x + 44, 548, 96, 28), 0.2, 2.9, 3)

    def _draw_rain(self, screen):
        for rain_x in range(-20, WIDTH + 30, 28):
            start_y = (rain_x * 7 + self.rain_offset) % 130 - 25
            for rain_y in range(int(start_y), HEIGHT, 130):
                pygame.draw.line(screen, (153, 197, 221), (rain_x, rain_y), (rain_x - 7, rain_y + 20), 2)

    def _draw_lightning(self, screen):
        if self.lightning_time <= 0:
            return
        flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        flash.fill((210, 229, 255, 72))
        screen.blit(flash, (0, 0))
        bolt_x = WIDTH - 250
        points = [(bolt_x, 85), (bolt_x - 18, 150), (bolt_x + 5, 150), (bolt_x - 30, 230), (bolt_x + 12, 178), (bolt_x - 8, 178)]
        pygame.draw.lines(screen, (246, 251, 255), False, points, 6)
        pygame.draw.lines(screen, (142, 201, 255), False, points, 2)

    def _draw_exit_sign(self, screen, camera_x):
        sign_x = FERRY_BOAT_WORLD_WIDTH - 190 - camera_x
        pygame.draw.rect(screen, (29, 124, 83), (sign_x, 150, 160, 54), border_radius=6)
        pygame.draw.rect(screen, (225, 244, 235), (sign_x, 150, 160, 54), 3, border_radius=6)
        label = self.sign_font.render("ΕΞΟΔΟΣ", True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=(sign_x + 80, 177)))


class PatrasCityBackground:
    def __init__(self):
        self.rain_offset = 0.0
        self.sunrise_progress = 0.0
        self.sunrise_started = False
        self.title_font = pygame.font.Font(None, 30)

    def start_sunrise(self):
        self.sunrise_started = True

    def update(self, delta_time):
        if self.sunrise_started:
            self.sunrise_progress = min(1.0, self.sunrise_progress + delta_time / 7)
        else:
            self.rain_offset = (self.rain_offset + 360 * delta_time) % 42

    def draw(self, screen, camera_x):
        progress = self.sunrise_progress
        sky_color = tuple(round(night + (sunrise - night) * progress) for night, sunrise in zip((8, 16, 35), (239, 174, 112)))
        screen.fill(sky_color)
        self._draw_city_silhouette(screen, camera_x, progress)
        self._draw_church(screen, camera_x)
        self._draw_bench(screen, camera_x)
        if not self.sunrise_started:
            self._draw_rain(screen)
        elif progress > 0.2:
            self._draw_sunrise(screen, progress)

    def _draw_city_silhouette(self, screen, camera_x, progress):
        ground_color = (46 + round(65 * progress), 53 + round(31 * progress), 67 + round(12 * progress))
        pygame.draw.rect(screen, ground_color, (0, 490, WIDTH, HEIGHT - 490))
        first_building_x = int(camera_x // 250) * 250 - 250
        for world_x in range(first_building_x, int(camera_x + WIDTH + 250), 250):
            position_x = world_x - camera_x
            building_height = 110 + (world_x // 250 % 3) * 35
            pygame.draw.rect(screen, (28, 35, 50), (position_x, 490 - building_height, 190, building_height))
            for window_y in range(490 - building_height + 18, 475, 30):
                pygame.draw.rect(screen, (220, 177, 99), (position_x + 25, window_y, 16, 10))
                pygame.draw.rect(screen, (220, 177, 99), (position_x + 88, window_y, 16, 10))

    def _draw_church(self, screen, camera_x):
        church_x = 45 - camera_x
        pygame.draw.rect(screen, (230, 228, 215), (church_x, 322, 155, 168))
        pygame.draw.polygon(screen, (195, 91, 78), [(church_x - 12, 322), (church_x + 77, 245), (church_x + 167, 322)])
        pygame.draw.rect(screen, (232, 231, 221), (church_x + 105, 275, 40, 215))
        pygame.draw.polygon(screen, (185, 82, 72), [(church_x + 99, 275), (church_x + 125, 225), (church_x + 151, 275)])
        pygame.draw.line(screen, (41, 48, 55), (church_x + 125, 215), (church_x + 125, 244), 4)
        pygame.draw.line(screen, (41, 48, 55), (church_x + 116, 228), (church_x + 134, 228), 4)
        pygame.draw.rect(screen, (88, 66, 54), (church_x + 56, 420, 42, 70), border_radius=20)
        pygame.draw.circle(screen, (127, 172, 200), (church_x + 37, 368), 14)
        pygame.draw.circle(screen, (127, 172, 200), (church_x + 116, 368), 14)

    def _draw_bench(self, screen, camera_x):
        bench_x = PATRAS_CITY_WORLD_WIDTH - 520 - camera_x
        pygame.draw.rect(screen, (101, 62, 38), (bench_x, 65, 154, 12), border_radius=3)
        pygame.draw.rect(screen, (119, 73, 42), (bench_x, 94, 154, 13), border_radius=3)
        pygame.draw.rect(screen, (61, 46, 38), (bench_x + 19, 105, 10, 38))
        pygame.draw.rect(screen, (61, 46, 38), (bench_x + 125, 105, 10, 38))
        label = self.title_font.render("Ξεκουράσου εδώ  [Shift]", True, (255, 240, 193))
        screen.blit(label, label.get_rect(center=(bench_x + 77, 38)))

    def _draw_rain(self, screen):
        for rain_x in range(-20, WIDTH + 30, 26):
            start_y = (rain_x * 9 + self.rain_offset) % 120 - 20
            for rain_y in range(int(start_y), HEIGHT, 120):
                pygame.draw.line(screen, (133, 177, 204), (rain_x, rain_y), (rain_x - 7, rain_y + 18), 2)

    def _draw_sunrise(self, screen, progress):
        sun_radius = round(20 + 34 * progress)
        pygame.draw.circle(screen, (255, 220, 131), (WIDTH - 160, 170), sun_radius)
        caption = self.title_font.render("Ανατολή πάνω από την Πάτρα", True, (255, 247, 215))
        screen.blit(caption, caption.get_rect(center=(WIDTH // 2, 78)))


class SchoolBackground:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 34)

    def update(self, delta_time):
        pass

    def draw(self, screen, camera_x):
        screen.fill((126, 196, 232))
        self._draw_clouds(screen)
        self._draw_hills(screen, camera_x)
        pygame.draw.rect(screen, (216, 197, 153), (0, 385, WIDTH, HEIGHT - 385))
        self._draw_courts(screen, camera_x)
        self._draw_olive_trees(screen, camera_x)
        self._draw_school_building(screen, camera_x)
        self._draw_fence(screen, camera_x)
        title = self.title_font.render("49ο Δημοτικό", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 54)))

    @staticmethod
    def _draw_clouds(screen):
        for cloud_x, cloud_y in ((110, 90), (430, 145), (790, 75), (1040, 135)):
            pygame.draw.ellipse(screen, (245, 250, 253), (cloud_x, cloud_y, 115, 32))
            pygame.draw.circle(screen, (245, 250, 253), (cloud_x + 38, cloud_y + 18), 22)
            pygame.draw.circle(screen, (245, 250, 253), (cloud_x + 72, cloud_y + 13), 26)

    def _draw_hills(self, screen, camera_x):
        first_hill_x = int(camera_x // 600) * 600 - 600
        for world_x in range(first_hill_x, int(camera_x + WIDTH + 600), 600):
            position_x = world_x - camera_x
            pygame.draw.polygon(screen, (112, 157, 134), [(position_x, 385), (position_x + 280, 210), (position_x + 620, 385)])

    def _draw_school_building(self, screen, camera_x):
        for world_x in range(900, SCHOOL_WORLD_WIDTH, 1050):
            position_x = world_x - camera_x
            pygame.draw.rect(screen, (235, 224, 194), (position_x, 195, 410, 190))
            pygame.draw.rect(screen, (197, 82, 67), (position_x - 14, 180, 438, 22))
            pygame.draw.rect(screen, (83, 125, 149), (position_x + 170, 300, 62, 85))
            for window_x in range(int(position_x + 35), int(position_x + 380), 72):
                pygame.draw.rect(screen, (104, 163, 193), (window_x, 238, 38, 36))
                pygame.draw.rect(screen, (240, 248, 247), (window_x, 238, 38, 36), 2)

    def _draw_courts(self, screen, camera_x):
        for world_x in range(280, SCHOOL_WORLD_WIDTH, 900):
            position_x = world_x - camera_x
            court_rect = pygame.Rect(position_x, 402, 520, 150)
            pygame.draw.rect(screen, (195, 113, 72), court_rect, border_radius=5)
            pygame.draw.rect(screen, (247, 239, 208), court_rect, 3, border_radius=5)
            pygame.draw.line(screen, (247, 239, 208), (position_x + 260, 402), (position_x + 260, 552), 3)
            pygame.draw.circle(screen, (247, 239, 208), (position_x + 260, 477), 44, 3)
            hoop_x = position_x + 465
            pygame.draw.line(screen, (94, 96, 98), (hoop_x, 402), (hoop_x, 300), 6)
            pygame.draw.rect(screen, (238, 243, 245), (hoop_x - 46, 300, 52, 38), 3)
            pygame.draw.circle(screen, (222, 81, 48), (hoop_x - 20, 345), 13, 3)

    def _draw_olive_trees(self, screen, camera_x):
        for world_x in range(100, SCHOOL_WORLD_WIDTH, 430):
            position_x = world_x - camera_x
            pygame.draw.rect(screen, (100, 77, 48), (position_x - 7, 300, 14, 100))
            for canopy_x, canopy_y, radius in ((-28, 320, 27), (0, 292, 34), (30, 322, 29)):
                pygame.draw.circle(screen, (78, 127, 72), (position_x + canopy_x, canopy_y), radius)
            for olive_x, olive_y in ((-15, 310), (12, 325), (24, 295), (-2, 340)):
                pygame.draw.circle(screen, (94, 103, 62), (position_x + olive_x, olive_y), 4)

    def _draw_fence(self, screen, camera_x):
        colors = ((222, 83, 66), (245, 193, 59), (54, 145, 193), (83, 165, 89), (168, 84, 164))
        first_pole_x = int(camera_x // 28) * 28 - 28
        for pole_index, world_x in enumerate(range(first_pole_x, int(camera_x + WIDTH + 28), 28)):
            position_x = world_x - camera_x
            pygame.draw.rect(screen, colors[pole_index % len(colors)], (position_x, 355, 7, 130), border_radius=3)
        pygame.draw.line(screen, (89, 99, 108), (0, 360), (WIDTH, 360), 4)
        pygame.draw.line(screen, (89, 99, 108), (0, 478), (WIDTH, 478), 4)


class ClassroomBackground:
    DESKS = ((150, 415), (360, 400), (570, 415), (760, 400))

    def __init__(self):
        self.title_font = pygame.font.Font(None, 38)

    def update(self, delta_time):
        pass

    def draw(self, screen, camera_x):
        screen.fill((239, 227, 192))
        pygame.draw.rect(screen, (189, 157, 112), (0, 460, WIDTH, HEIGHT - 460))
        self._draw_windows(screen, camera_x)
        self._draw_board(screen, camera_x)
        self._draw_desks(screen, camera_x)
        self._draw_classroom_details(screen, camera_x)
        title = self.title_font.render("Β1 τάξη", True, (73, 67, 55))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 42)))

    def _draw_windows(self, screen, camera_x):
        for world_x in range(60, CLASSROOM_WORLD_WIDTH, 230):
            position_x = world_x - camera_x
            pygame.draw.rect(screen, (111, 174, 205), (position_x, 105, 132, 135))
            pygame.draw.rect(screen, (250, 250, 240), (position_x, 105, 132, 135), 7)
            pygame.draw.line(screen, (250, 250, 240), (position_x + 66, 108), (position_x + 66, 237), 5)
            pygame.draw.line(screen, (250, 250, 240), (position_x + 4, 172), (position_x + 128, 172), 5)

    def _draw_board(self, screen, camera_x):
        board_x = 660 - camera_x
        pygame.draw.rect(screen, (78, 117, 82), (board_x, 100, 260, 155), border_radius=5)
        pygame.draw.rect(screen, (116, 76, 47), (board_x - 8, 92, 276, 171), 9, border_radius=6)
        pygame.draw.line(screen, (239, 239, 211), (board_x + 30, 145), (board_x + 190, 145), 3)
        pygame.draw.line(screen, (239, 239, 211), (board_x + 65, 185), (board_x + 220, 185), 3)

    def _draw_desks(self, screen, camera_x):
        for world_x, row_y in self.DESKS:
            position_x = world_x - camera_x
            pygame.draw.rect(screen, (171, 113, 65), (position_x, row_y, 115, 20), border_radius=4)
            pygame.draw.rect(screen, (91, 64, 44), (position_x + 12, row_y + 20, 8, 42))
            pygame.draw.rect(screen, (91, 64, 44), (position_x + 94, row_y + 20, 8, 42))
            pygame.draw.rect(screen, (97, 139, 175), (position_x + 34, row_y + 33, 48, 23), border_radius=4)

    def _draw_classroom_details(self, screen, camera_x):
        clock_x = 510 - camera_x
        pygame.draw.circle(screen, (248, 245, 227), (clock_x, 82), 25)
        pygame.draw.circle(screen, (73, 67, 55), (clock_x, 82), 25, 3)
        pygame.draw.line(screen, (73, 67, 55), (clock_x, 82), (clock_x, 67), 3)
        pygame.draw.line(screen, (73, 67, 55), (clock_x, 82), (clock_x + 11, 89), 3)
        for world_x in (40, 940):
            position_x = world_x - camera_x
            pygame.draw.rect(screen, (202, 84, 66), (position_x, 145, 20, 315))


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


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("T-Rex στη Γέφυρα Ρίου–Αντιρρίου")
        self.clock = pygame.time.Clock()
        self.background = BridgeBackground()
        self.player = Player()
        self.level_name = "Rio–Antirrio Bridge"
        self.world_width = BRIDGE_WORLD_WIDTH
        self.platforms = self._create_bridge_platforms()
        self.resources = self._create_resources()
        self.collected = {resource_type: 0 for resource_type in RESOURCE_TARGETS}
        self.health = MAX_HEALTH
        self.enemy_hit_cooldown = 0.0
        self.hud_font = pygame.font.Font(None, 32)
        self.hud_icons = self._load_hud_icons()
        self.camera_x = 0.0
        self.velociraptor = None
        self.sick_apatosaurus = None
        self.dropped_supplies = []
        self.thrown_weapons = []
        self.show_world_menu = True
        self.show_game_over = False
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
            Platform(520, ROAD_TOP - 80, 220),
            Platform(1120, ROAD_TOP - 125, 250),
            Platform(1740, ROAD_TOP - 95, 210),
            Platform(2340, ROAD_TOP - 150, 230),
            Platform(2780, ROAD_TOP - 105, 240),
        ]

    @staticmethod
    def _create_mountain_river_platforms():
        return [
            Platform(60, 455, 180, "log"),
            Platform(360, 405, 175, "log"),
            Platform(650, 355, 180, "log"),
            Platform(955, 405, 180, "log"),
            Platform(1260, 350, 180, "log"),
            Platform(1560, 400, 180, "log"),
            Platform(1860, 355, 180, "log"),
            Platform(2160, 405, 180, "log"),
            Platform(MOUNTAIN_RIVER_WORLD_WIDTH - 420, STONE_BRIDGE_DECK_Y, 420, "invisible"),
        ]

    @staticmethod
    def _create_ferry_boat_platforms():
        return [
            Platform(70, 430, 185, "car"),
            Platform(355, 375, 170, "car"),
            Platform(650, 420, 185, "car"),
            Platform(950, 360, 170, "car"),
            Platform(1240, 415, 185, "car"),
            Platform(1540, 365, 170, "car"),
            Platform(1830, 420, 185, "car"),
            Platform(2130, 365, 170, "car"),
            Platform(2420, 420, 185, "car"),
            Platform(2710, 365, 190, "car"),
        ]

    @staticmethod
    def _create_patras_city_platforms():
        platforms = [Platform(0, ROAD_TOP, 220, "invisible")]
        for step_index in range(19):
            platforms.append(Platform(220 + step_index * 125, 455 - step_index * 20, 145))
        platforms.append(Platform(PATRAS_CITY_WORLD_WIDTH - 800, 115, 450, "invisible"))
        return platforms

    @staticmethod
    def _create_school_platforms():
        return [
            Platform(530, 402, 150),
            Platform(1430, 402, 150),
        ]

    @staticmethod
    def _create_classroom_platforms():
        return [
            Platform(position_x, position_y, 115, "invisible")
            for position_x, position_y in ClassroomBackground.DESKS
        ]

    @staticmethod
    def _create_school_weapons():
        weapon_positions = random.sample(range(400, SCHOOL_WORLD_WIDTH - 300, 400), 3)
        return [Resource("weapon", position_x) for position_x in weapon_positions]

    def _create_awake_apatosaurus_platform(self):
        dinosaur = self.sick_apatosaurus
        return Platform(dinosaur.rect.left + 26, dinosaur.rect.top + 60, dinosaur.rect.width - 48, "invisible")

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
        panel = pygame.Surface((155, 157), pygame.SRCALPHA)
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

        heart_row_y = panel_y + 10 + len(RESOURCE_TARGETS) * 37
        heart_icon = self.hud_icons["heart"]
        heart_rect = heart_icon.get_rect(midleft=(panel_x + 14, heart_row_y + 13))
        self.screen.blit(heart_icon, heart_rect)
        health_surface = self.hud_font.render(f"{self.health}/{MAX_HEALTH}", True, (255, 255, 255))
        self.screen.blit(health_surface, (panel_x + 70, heart_row_y))

        if self.level_name == "Rio–Antirrio Bridge" and not self.resources:
            complete_surface = self.hud_font.render("Η πίστα ολοκληρώθηκε!", True, (255, 245, 158))
            self.screen.blit(complete_surface, complete_surface.get_rect(center=(WIDTH // 2, 82)))

        if self.level_name == "Nafpaktos" and self.velociraptor:
            status = "Νίκησες τον Βελοσιράπτορα" if self.velociraptor.dead else f"Βελοσιράπτορας: {2 - self.velociraptor.hits} χτυπήματα"
            status_surface = self.hud_font.render(status, True, (255, 245, 158))
            self.screen.blit(status_surface, (18, 18))
        elif self.level_name == "Mountain River":
            level_surface = self.hud_font.render("Ορεινό Ποτάμι", True, (255, 255, 255))
            self.screen.blit(level_surface, (18, 18))
        elif self.level_name == "Patras City":
            status = "Ανατολή πάνω από την Πάτρα" if self.background.sunrise_started else "Ανέβα τα σκαλιά της Αγίου Νικολάου"
            level_surface = self.hud_font.render(status, True, (255, 245, 193))
            self.screen.blit(level_surface, (18, 18))
        elif self.level_name == "49ο Δημοτικό":
            level_surface = self.hud_font.render("Αυλή του 49ου Δημοτικού", True, (255, 255, 255))
            self.screen.blit(level_surface, (18, 18))
        elif self.level_name == "Β1 τάξη" and self.velociraptor:
            status = "Νίκησες τον Βελοσιράπτορα" if self.velociraptor.dead else f"Βελοσιράπτορας: {2 - self.velociraptor.hits} χτυπήματα"
            level_surface = self.hud_font.render(status, True, (255, 245, 158))
            self.screen.blit(level_surface, (18, 18))

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
        if self.velociraptor is None:
            self.velociraptor = Velociraptor()
        self.thrown_weapons = []
        self.camera_x = 0.0

    def _return_to_bridge_level(self):
        self.level_name = "Rio–Antirrio Bridge"
        self.world_width = BRIDGE_WORLD_WIDTH
        self.background = BridgeBackground()
        self.platforms = self._create_bridge_platforms()
        self.player = Player()
        self.player.rect.centerx = BRIDGE_WORLD_WIDTH - 300
        self.thrown_weapons = []
        self.camera_x = BRIDGE_WORLD_WIDTH - WIDTH

    def _start_mountain_river_level(self):
        self.level_name = "Mountain River"
        self.world_width = MOUNTAIN_RIVER_WORLD_WIDTH
        self.background = MountainRiverBackground()
        self.platforms = self._create_mountain_river_platforms()
        self.resources = []
        self.player = Player()
        if self.sick_apatosaurus is None:
            self.sick_apatosaurus = SickApatosaurus()
        elif self.sick_apatosaurus.healed:
            self.platforms.append(self._create_awake_apatosaurus_platform())
        self._reset_mountain_river_player()
        self.dropped_supplies = []
        self.thrown_weapons = []
        self.camera_x = 0.0

    def _start_ferry_boat_level(self):
        self.level_name = "FerryBoat"
        self.world_width = FERRY_BOAT_WORLD_WIDTH
        self.background = FerryBoatBackground()
        self.platforms = self._create_ferry_boat_platforms()
        self.resources = []
        self.player = Player()
        self._reset_ferry_boat_player()
        self.dropped_supplies = []
        self.thrown_weapons = []
        self.camera_x = 0.0

    def _start_patras_city_level(self):
        self.level_name = "Patras City"
        self.world_width = PATRAS_CITY_WORLD_WIDTH
        self.background = PatrasCityBackground()
        self.platforms = self._create_patras_city_platforms()
        self.resources = []
        self.player = Player()
        self._reset_patras_city_player()
        self.dropped_supplies = []
        self.thrown_weapons = []
        self.camera_x = 0.0

    def _start_school_level(self):
        self.level_name = "49ο Δημοτικό"
        self.world_width = SCHOOL_WORLD_WIDTH
        self.background = SchoolBackground()
        self.platforms = self._create_school_platforms()
        self.resources = self._create_school_weapons()
        self.player = Player()
        self.dropped_supplies = []
        self.thrown_weapons = []
        self.camera_x = 0.0

    def _start_classroom_level(self):
        self.level_name = "Β1 τάξη"
        self.world_width = CLASSROOM_WORLD_WIDTH
        self.background = ClassroomBackground()
        self.platforms = self._create_classroom_platforms()
        self.resources = []
        self.player = Player()
        self.velociraptor = Velociraptor(CLASSROOM_WORLD_WIDTH - 230)
        self.thrown_weapons = []
        self.camera_x = 0.0

    def _feed_sick_apatosaurus(self):
        dinosaur = self.sick_apatosaurus
        is_close = dinosaur and self.player.rect.right >= dinosaur.rect.left - 120
        has_supplies = self.collected["meat"] >= 2 and self.collected["water"] >= 2
        if self.level_name != "Mountain River" or not is_close or dinosaur.healed or not has_supplies:
            return

        self.collected["meat"] -= 2
        self.collected["water"] -= 2
        supply_types = ("meat", "water", "meat", "water")
        supply_x = dinosaur.rect.left - 190
        self.dropped_supplies = [
            Resource(resource_type, supply_x + index * 48)
            for index, resource_type in enumerate(supply_types)
        ]
        dinosaur.healed = True
        self.platforms.append(self._create_awake_apatosaurus_platform())

    def _resolve_sick_apatosaurus_blocker(self):
        dinosaur = self.sick_apatosaurus
        if self.level_name != "Mountain River" or not dinosaur or dinosaur.healed:
            return
        if self.player.rect.right > dinosaur.rect.left and self.player.rect.centerx < dinosaur.rect.centerx:
            self.player.rect.right = dinosaur.rect.left

    def _resolve_rocky_barrier(self):
        if self.level_name != "Mountain River":
            return
        can_clear_barrier = self.player.rect.bottom <= STONE_BRIDGE_DECK_Y + 35
        is_crossing_from_left = self.player.rect.centerx < ROCKY_BARRIER_X + 75
        if self.player.rect.right > ROCKY_BARRIER_X and is_crossing_from_left and not can_clear_barrier:
            self.player.rect.right = ROCKY_BARRIER_X

    def _resolve_classroom_desks(self, previous_player_rect):
        if self.level_name != "Β1 τάξη" or self.player.ducking:
            return
        for desk in self.platforms:
            is_at_desk_height = self.player.rect.bottom > desk.rect.top + 10
            overlaps_desk = self.player.rect.colliderect(desk.rect)
            if not is_at_desk_height or not overlaps_desk:
                continue
            if previous_player_rect.right <= desk.rect.left:
                self.player.rect.right = desk.rect.left
            elif previous_player_rect.left >= desk.rect.right:
                self.player.rect.left = desk.rect.right

    def _reset_mountain_river_player(self):
        starting_log = self.platforms[0]
        self.player.rect.centerx = starting_log.rect.centerx
        self.player.rect.bottom = starting_log.rect.top
        self.player.velocity_y = 0
        self.player.on_ground = True

    def _handle_mountain_river_water(self):
        if self.level_name == "Mountain River" and self.player.rect.top > HEIGHT:
            self._reset_mountain_river_player()

    def _reset_ferry_boat_player(self):
        starting_car = self.platforms[0]
        self.player.rect.centerx = starting_car.rect.centerx
        self.player.rect.bottom = starting_car.rect.top
        self.player.velocity_y = 0
        self.player.on_ground = True

    def _handle_ferry_boat_water(self):
        if self.level_name == "FerryBoat" and self.player.rect.top > HEIGHT:
            self._reset_ferry_boat_player()

    def _reset_patras_city_player(self):
        starting_platform = self.platforms[0]
        self.player.rect.centerx = starting_platform.rect.centerx
        self.player.rect.bottom = starting_platform.rect.top
        self.player.velocity_y = 0
        self.player.on_ground = True

    def _handle_patras_city_fall(self):
        if self.level_name == "Patras City" and self.player.rect.top > HEIGHT:
            self._reset_patras_city_player()

    def _update_ferry_storm(self):
        is_near_exit = self.player.rect.right >= FERRY_BOAT_WORLD_WIDTH - 520
        if self.level_name == "FerryBoat" and is_near_exit:
            self.background.start_storm()

    def _rest_at_patras_bench(self):
        if self.level_name != "Patras City" or self.background.sunrise_started:
            return
        bench_x = PATRAS_CITY_WORLD_WIDTH - 520
        is_at_bench = self.player.rect.centerx >= bench_x - 50
        has_food_and_water = self.collected["meat"] > 0 and self.collected["water"] > 0
        if not is_at_bench or not has_food_and_water:
            return
        self.collected["meat"] = 0
        self.collected["water"] = 0
        self.player.resting = True
        self.background.start_sunrise()

    def _update_lochness_animation(self):
        if self.level_name != "Mountain River":
            return
        if not self.background.lochness_completed and self.player.rect.right >= MOUNTAIN_RIVER_WORLD_WIDTH - 420:
            self.background.lochness_visible = True

    def _throw_weapon(self):
        if self.level_name not in ("Nafpaktos", "Β1 τάξη") or self.collected["weapon"] <= 0:
            return
        self.collected["weapon"] -= 1
        self.thrown_weapons.append(
            ThrownWeapon(self.player.rect.centerx, self.player.rect.centery, self.player.facing_left)
        )

    def _update_combat(self, delta_time):
        self.enemy_hit_cooldown = max(0.0, self.enemy_hit_cooldown - delta_time)
        if self.level_name not in ("Nafpaktos", "Β1 τάξη") or not self.velociraptor:
            return
        self.velociraptor.update(delta_time, self.player, self.camera_x)
        self._handle_enemy_contact()
        for thrown_weapon in self.thrown_weapons[:]:
            thrown_weapon.update(delta_time)
            if thrown_weapon.rect.colliderect(self.velociraptor.rect) and not self.velociraptor.dead:
                self.velociraptor.take_hit()
                self.thrown_weapons.remove(thrown_weapon)
            elif thrown_weapon.rect.right < 0 or thrown_weapon.rect.left > self.world_width:
                self.thrown_weapons.remove(thrown_weapon)

    def _handle_enemy_contact(self):
        enemy = self.velociraptor
        if enemy.dead or self.enemy_hit_cooldown > 0 or not enemy.rect.colliderect(self.player.rect):
            return
        self.health = max(0, self.health - 1)
        if self.health == 0:
            self.show_game_over = True
        self.enemy_hit_cooldown = 0.8
        if enemy.rect.centerx <= self.player.rect.centerx:
            enemy.rect.right = max(0, self.player.rect.left - 180)
        else:
            enemy.rect.left = min(self.world_width - enemy.rect.width, self.player.rect.right + 180)

    def _restart_from_first_level(self):
        self.level_name = "Rio–Antirrio Bridge"
        self.world_width = BRIDGE_WORLD_WIDTH
        self.background = BridgeBackground()
        self.platforms = self._create_bridge_platforms()
        self.resources = self._create_resources()
        self.collected = {resource_type: 0 for resource_type in RESOURCE_TARGETS}
        self.health = MAX_HEALTH
        self.enemy_hit_cooldown = 0.0
        self.player = Player()
        self.velociraptor = None
        self.sick_apatosaurus = None
        self.dropped_supplies = []
        self.thrown_weapons = []
        self.camera_x = 0.0
        self.show_world_menu = False
        self.show_game_over = False

    def _draw_game_over(self):
        self.screen.fill((28, 20, 30))
        title_font = pygame.font.Font(None, 76)
        prompt_font = pygame.font.Font(None, 34)
        title = title_font.render("ΤΕΛΟΣ ΠΑΙΧΝΙΔΙΟΥ", True, (240, 92, 83))
        prompt = prompt_font.render("Πάτησε Space ή κάνε κλικ για νέα αρχή", True, (255, 244, 215))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 42)))
        self.screen.blit(prompt, prompt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 32)))

    def _check_level_transition(self):
        has_reached_nafpaktos_sign = self.player.rect.right >= BRIDGE_WORLD_WIDTH - 160
        has_reached_kravara_sign = self.player.rect.right >= NAFPAKTOS_WORLD_WIDTH - 160
        has_reached_antirrio_sign = self.player.rect.right >= MOUNTAIN_RIVER_WORLD_WIDTH - 150
        has_reached_ferry_exit = self.player.rect.right >= FERRY_BOAT_WORLD_WIDTH - 70
        has_reached_school_entrance = self.player.rect.right >= SCHOOL_WORLD_WIDTH - 70
        has_finished_patras_sunrise = self.level_name == "Patras City" and self.background.sunrise_started and self.background.sunrise_progress >= 1.0
        if self.level_name == "Rio–Antirrio Bridge" and not self.resources and has_reached_nafpaktos_sign:
            self._start_nafpaktos_level()
        elif self.level_name == "Nafpaktos" and self.player.rect.left <= 0:
            self._return_to_bridge_level()
        elif self.level_name == "Nafpaktos" and self.velociraptor and self.velociraptor.dead and has_reached_kravara_sign:
            self._start_mountain_river_level()
        elif self.level_name == "Mountain River" and has_reached_antirrio_sign:
            self._start_ferry_boat_level()
        elif self.level_name == "FerryBoat" and has_reached_ferry_exit:
            self._start_patras_city_level()
        elif has_finished_patras_sunrise:
            self._start_school_level()
        elif self.level_name == "49ο Δημοτικό" and has_reached_school_entrance:
            self._start_classroom_level()

    @staticmethod
    def _world_menu_buttons():
        return [
            (pygame.Rect(390, 185, 420, 48), "Γέφυρα Ρίου–Αντιρρίου"),
            (pygame.Rect(390, 237, 420, 48), "Ναύπακτος"),
            (pygame.Rect(390, 289, 420, 48), "Ορεινό Ποτάμι"),
            (pygame.Rect(390, 341, 420, 48), "Πλοίο"),
            (pygame.Rect(390, 393, 420, 48), "Πάτρα"),
            (pygame.Rect(390, 445, 420, 48), "49ο Δημοτικό"),
            (pygame.Rect(390, 497, 420, 48), "Β1 τάξη"),
        ]

    def _start_selected_world(self, index):
        if index == 0:
            self.level_name = "Rio–Antirrio Bridge"
            self.world_width = BRIDGE_WORLD_WIDTH
            self.background = BridgeBackground()
            self.platforms = self._create_bridge_platforms()
            self.player = Player()
            self.camera_x = 0.0
        elif index == 1:
            self._start_nafpaktos_level()
        elif index == 2:
            self._start_mountain_river_level()
        elif index == 3:
            self._start_ferry_boat_level()
        elif index == 4:
            self._start_patras_city_level()
        elif index == 5:
            self._start_school_level()
        elif index == 6:
            self._start_classroom_level()
        else:
            return
        if index in (1, 2, 3, 4, 5, 6):
            self.collected = RESOURCE_TARGETS.copy()
        self.show_world_menu = False

    def _handle_world_menu_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7):
            self._start_selected_world(event.key - pygame.K_1)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, (button_rect, _) in enumerate(self._world_menu_buttons()):
                if button_rect.collidepoint(event.pos):
                    self._start_selected_world(index)
                    break

    def _draw_world_menu(self):
        self.screen.fill((31, 70, 88))
        title_font = pygame.font.Font(None, 58)
        subtitle_font = pygame.font.Font(None, 30)
        title = title_font.render("Επιλογή Πίστας", True, (255, 245, 200))
        subtitle = subtitle_font.render("Διάλεξε πίστα για εκκίνηση", True, (225, 239, 244))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 125)))
        self.screen.blit(subtitle, subtitle.get_rect(center=(WIDTH // 2, 174)))
        for index, (button_rect, label) in enumerate(self._world_menu_buttons(), start=1):
            pygame.draw.rect(self.screen, (24, 104, 145), button_rect, border_radius=12)
            pygame.draw.rect(self.screen, (225, 240, 246), button_rect, 3, border_radius=12)
            button_text = subtitle_font.render(f"{index}. {label}", True, (255, 255, 255))
            self.screen.blit(button_text, button_text.get_rect(center=button_rect.center))

    def run(self):
        while self.running:
            delta_time = self.clock.tick(FPS) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif self.show_game_over and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                    self._restart_from_first_level()
                elif self.show_world_menu:
                    self._handle_world_menu_event(event)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL:
                    self._throw_weapon()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                    self._feed_sick_apatosaurus()
                    self._rest_at_patras_bench()

            if self.show_world_menu:
                self._draw_world_menu()
                pygame.display.flip()
                continue

            if self.show_game_over:
                self._draw_game_over()
                pygame.display.flip()
                continue

            keys = pygame.key.get_pressed()
            ground_y = None if self.level_name in ("Mountain River", "FerryBoat", "Patras City") else ROAD_TOP
            previous_player_rect = self.player.rect.copy()
            self.player.update(delta_time, keys, True, self.platforms, self.world_width, ground_y)
            self._handle_mountain_river_water()
            self._handle_ferry_boat_water()
            self._handle_patras_city_fall()
            self._update_ferry_storm()
            self._resolve_sick_apatosaurus_blocker()
            self._resolve_rocky_barrier()
            self._resolve_classroom_desks(previous_player_rect)
            self._update_lochness_animation()
            self._collect_resources()
            self._check_level_transition()
            self.update_camera()
            self.background.update(delta_time)
            self._update_combat(delta_time)

            self.background.draw(self.screen, self.camera_x)
            for platform in self.platforms:
                platform.draw(self.screen, self.camera_x)
            for resource in self.resources:
                resource.draw(self.screen, self.camera_x)
            for supply in self.dropped_supplies:
                supply.draw(self.screen, self.camera_x)
            for thrown_weapon in self.thrown_weapons:
                thrown_weapon.draw(self.screen, self.camera_x)
            if self.level_name in ("Nafpaktos", "Β1 τάξη") and self.velociraptor:
                self.velociraptor.draw(self.screen, self.camera_x, self.player.rect.centerx)
            if self.level_name == "Mountain River" and self.sick_apatosaurus:
                self.sick_apatosaurus.draw(self.screen, self.camera_x)
            self.player.draw(self.screen, self.camera_x)
            self._draw_hud()
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    Game().run()