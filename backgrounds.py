import random

import pygame

from config import *


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


