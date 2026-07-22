import random

import pygame

from backgrounds import (
    BridgeBackground,
    ClassroomBackground,
    FerryBoatBackground,
    MountainRiverBackground,
    NafpaktosBackground,
    PatrasCityBackground,
    SchoolBackground,
)
from config import (
    BRIDGE_WORLD_WIDTH,
    CLASSROOM_WORLD_WIDTH,
    FERRY_BOAT_WORLD_WIDTH,
    FPS,
    GROUND_Y,
    MAX_HEALTH,
    MOUNTAIN_RIVER_WORLD_WIDTH,
    NAFPAKTOS_WORLD_WIDTH,
    PATRAS_CITY_WORLD_WIDTH,
    RESOURCE_IMAGE_PATHS,
    RESOURCE_TARGETS,
    RESOURCE_WIDTHS,
    ROAD_TOP,
    ROCKY_BARRIER_X,
    SCHOOL_WORLD_WIDTH,
    STONE_BRIDGE_DECK_Y,
    WIDTH,
    HEIGHT,
)
from entities import Player, Platform, Resource, SickApatosaurus, ThrownWeapon, Velociraptor


class Game:
    def __init__(self):
        pygame.init()
        self.fullscreen = False
        self.screen = None
        self._apply_display_mode()
        pygame.display.set_caption("Πατρόσαυρος: Η Περιπέτεια")
        self.clock = pygame.time.Clock()
        self.background = BridgeBackground()
        self.player = Player()
        self.level_name = "Γέφυρα Ρίου-Αντιρίου"
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
        self.paused = False

    
    def draw_pause_menu(self):
        pause_font = pygame.font.Font(None, 72)
        pause_text = pause_font.render("ΠΑΥΣΗ", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        self.screen.blit(pause_text, pause_rect)

        resume_font = pygame.font.Font(None, 36)
        resume_text = resume_font.render("Πατήστε ESC για συνέχιση ή Q για έξοδο", True, (255, 255, 255))
        resume_rect = resume_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        self.screen.blit(resume_text, resume_rect)

        pygame.display.flip()

    def _apply_display_mode(self):
        display_flags = pygame.FULLSCREEN if self.fullscreen else 0
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), display_flags)

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        self._apply_display_mode()

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

        if self.level_name == "Γέφυρα Ρίου-Αντιρίου" and not self.resources:
            complete_surface = self.hud_font.render("Η πίστα ολοκληρώθηκε!", True, (255, 245, 158))
            self.screen.blit(complete_surface, complete_surface.get_rect(center=(WIDTH // 2, 82)))

        if self.level_name == "Ναύπακτος" and self.velociraptor:
            status = "Νίκησες τον Βελοσιράπτορα" if self.velociraptor.dead else f"Βελοσιράπτορας: {2 - self.velociraptor.hits} χτυπήματα"
            status_surface = self.hud_font.render(status, True, (255, 245, 158))
            self.screen.blit(status_surface, (18, 18))
        elif self.level_name == "Ορεινό Ποτάμι":
            level_surface = self.hud_font.render("Ορεινό Ποτάμι", True, (255, 255, 255))
            self.screen.blit(level_surface, (18, 18))
        elif self.level_name == "Πάτρα":
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
        self.level_name = "Ναύπακτος"
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
        self.level_name = "Γέφυρα Ρίου-Αντιρίου"
        self.world_width = BRIDGE_WORLD_WIDTH
        self.background = BridgeBackground()
        self.platforms = self._create_bridge_platforms()
        self.player = Player()
        self.player.rect.centerx = BRIDGE_WORLD_WIDTH - 300
        self.thrown_weapons = []
        self.camera_x = BRIDGE_WORLD_WIDTH - WIDTH

    def _start_mountain_river_level(self):
        self.level_name = "Ορεινό Ποτάμι"
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
        self.level_name = "Πάτρα"
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
        if self.level_name != "Ορεινό Ποτάμι" or not is_close or dinosaur.healed or not has_supplies:
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
        if self.level_name != "Ορεινό Ποτάμι" or not dinosaur or dinosaur.healed:
            return
        if self.player.rect.right > dinosaur.rect.left and self.player.rect.centerx < dinosaur.rect.centerx:
            self.player.rect.right = dinosaur.rect.left

    def _resolve_rocky_barrier(self):
        if self.level_name != "Ορεινό Ποτάμι":
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
        if self.level_name == "Ορεινό Ποτάμι" and self.player.rect.top > HEIGHT:
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
        if self.level_name == "Πάτρα" and self.player.rect.top > HEIGHT:
            self._reset_patras_city_player()

    def _update_ferry_storm(self):
        is_near_exit = self.player.rect.right >= FERRY_BOAT_WORLD_WIDTH - 1200
        if self.level_name == "FerryBoat" and is_near_exit:
            self.background.start_storm()

    def _rest_at_patras_bench(self):
        if self.level_name != "Πάτρα" or self.background.sunrise_started:
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
        if self.level_name != "Ορεινό Ποτάμι":
            return
        if not self.background.lochness_completed and self.player.rect.right >= MOUNTAIN_RIVER_WORLD_WIDTH - 420:
            self.background.lochness_visible = True

    def _throw_weapon(self):
        if self.level_name not in ("Ναύπακτος", "Β1 τάξη") or self.collected["weapon"] <= 0:
            return
        self.collected["weapon"] -= 1
        self.thrown_weapons.append(
            ThrownWeapon(self.player.rect.centerx, self.player.rect.centery, self.player.facing_left)
        )

    def _update_combat(self, delta_time):
        self.enemy_hit_cooldown = max(0.0, self.enemy_hit_cooldown - delta_time)
        if self.level_name not in ("Ναύπακτος", "Β1 τάξη") or not self.velociraptor:
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
        self.level_name = "Γέφυρα Ρίου-Αντιρίου"
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
        has_finished_classroom = self.level_name == "Β1 τάξη" and self.velociraptor and self.velociraptor.dead
        has_finished_patras_sunrise = self.level_name == "Πάτρα" and self.background.sunrise_started and self.background.sunrise_progress >= 1.0
        if self.level_name == "Γέφυρα Ρίου-Αντιρίου" and not self.resources and has_reached_nafpaktos_sign:
            self._start_nafpaktos_level()
        elif self.level_name == "Ναύπακτος" and self.player.rect.left <= 0:
            self._return_to_bridge_level()
        elif self.level_name == "Ναύπακτος" and self.velociraptor and self.velociraptor.dead and has_reached_kravara_sign:
            self._start_mountain_river_level()
        elif self.level_name == "Ορεινό Ποτάμι" and has_reached_antirrio_sign:
            self._start_ferry_boat_level()
        elif self.level_name == "FerryBoat" and has_reached_ferry_exit:
            self._start_patras_city_level()
        elif has_finished_patras_sunrise:
            self._start_school_level()
        elif self.level_name == "49ο Δημοτικό" and has_reached_school_entrance:
            self._start_classroom_level()
        elif has_finished_classroom:
            self.show_world_menu = True
              

    @staticmethod
    def _world_menu_buttons():
        return [
            (pygame.Rect(390, 185, 420, 48), "Γέφυρα Ρίου-Αντιρίου"),
            (pygame.Rect(390, 237, 420, 48), "Ναύπακτος"),
            (pygame.Rect(390, 289, 420, 48), "Ορεινό Ποτάμι"),
            (pygame.Rect(390, 341, 420, 48), "Πλοίο"),
            (pygame.Rect(390, 393, 420, 48), "Πάτρα"),
            (pygame.Rect(390, 445, 420, 48), "49ο Δημοτικό"),
            (pygame.Rect(390, 497, 420, 48), "Β1 τάξη"),
        ]

    @staticmethod
    def _fullscreen_checkbox_rect():
        return pygame.Rect(390, 556, 26, 26)

    def _start_selected_world(self, index):
        if index == 0:
            self.level_name = "Γέφυρα Ρίου-Αντιρίου"
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
            if self._fullscreen_checkbox_rect().collidepoint(event.pos):
                self._toggle_fullscreen()
                return
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

        checkbox_rect = self._fullscreen_checkbox_rect()
        pygame.draw.rect(self.screen, (225, 240, 246), checkbox_rect, 3, border_radius=4)
        if self.fullscreen:
            pygame.draw.line(self.screen, (118, 223, 158), checkbox_rect.topleft, checkbox_rect.bottomright, 4)
            pygame.draw.line(self.screen, (118, 223, 158), checkbox_rect.bottomleft, checkbox_rect.topright, 4)
        fullscreen_label = subtitle_font.render("Πλήρης οθόνη", True, (225, 239, 244))
        self.screen.blit(fullscreen_label, fullscreen_label.get_rect(midleft=(checkbox_rect.right + 12, checkbox_rect.centery)))

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
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
            if self.paused:
                        self.draw_pause_menu()
                        keys = pygame.key.get_pressed()
                        if keys[pygame.K_q]:
                            self.running = False
                        

            if self.show_world_menu:
                self._draw_world_menu()
                pygame.display.flip()
                continue

            if self.show_game_over:
                self._draw_game_over()
                pygame.display.flip()
                continue

            keys = pygame.key.get_pressed()
            ground_y = None if self.level_name in ("Ορεινό Ποτάμι", "FerryBoat", "Πάτρα") else ROAD_TOP
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
            if self.level_name in ("Ναύπακτος", "Β1 τάξη") and self.velociraptor:
                self.velociraptor.draw(self.screen, self.camera_x, self.player.rect.centerx)
            if self.level_name == "Ορεινό Ποτάμι" and self.sick_apatosaurus:
                self.sick_apatosaurus.draw(self.screen, self.camera_x)
            self.player.draw(self.screen, self.camera_x)
            self._draw_hud()
            pygame.display.flip()

        pygame.quit()

