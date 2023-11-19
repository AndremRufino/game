import pygame
from core.config.settings import BASE_DIR, WEAPON_DATA, MAGIC_DATA, HITBOX_OFFSET
from core.helpers.support import import_folder
from core.controllers.entity import Entity


class Player(Entity):
    def __init__(
        self, pos, groups, obstacle_sprites, create_attack, destroy_attack, create_magic
    ) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(
            f"{BASE_DIR}/assets/graphics/test/player.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET["player"])

        self.import_player_assets()
        self.status = "down"

        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None
        self.obstacle_sprites = obstacle_sprites

        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None
        self.switch_duration_cooldown = 200

        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(MAGIC_DATA.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 5}
        self.max_stats = {
            "health": 300,
            "energy": 140,
            "attack": 20,
            "magic": 10,
            "speed": 10,
        }
        self.upgrade_cost = {
            "health": 100,
            "energy": 100,
            "attack": 100,
            "magic": 100,
            "speed": 100,
        }
        self.health = self.stats["health"] * 0.5
        self.energy = self.stats["energy"] * 0.8
        self.exp = 5000
        self.speed = self.stats["speed"]

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

        self.weapon_attack_sound = pygame.mixer.Sound(
            f"{BASE_DIR}/assets/audio/sword.wav"
        )
        self.weapon_attack_sound.set_volume(0.4)

    def import_player_assets(self) -> None:
        character_path = f"{BASE_DIR}/assets/graphics/player/"
        self.animations = {
            "up": list(),
            "down": list(),
            "left": list(),
            "right": list(),
            "right_idle": list(),
            "left_idle": list(),
            "up_idle": list(),
            "down_idle": list(),
            "right_attack": list(),
            "left_attack": list(),
            "up_attack": list(),
            "down_attack": list(),
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def input(self) -> None:
        if not self.attacking:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                self.create_attack()
                self.weapon_attack_sound.play()

            if keys[pygame.K_LCTRL]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                style = list(MAGIC_DATA.keys())[self.magic_index]
                strength = (
                    list(MAGIC_DATA.values())[self.magic_index]["strength"]
                    + self.stats["magic"]
                )
                cost = list(MAGIC_DATA.values())[self.magic_index]["cost"]
                self.create_magic(style, strength, cost)

            if keys[pygame.K_q] and self.can_switch_weapon:
                self.can_switch_weapon = False
                self.weapon_switch_time = pygame.time.get_ticks()

                if self.weapon_index < len(list(WEAPON_DATA.keys())) - 1:
                    self.weapon_index += 1
                else:
                    self.weapon_index = 0

                self.weapon = list(WEAPON_DATA.keys())[self.weapon_index]

            if keys[pygame.K_e] and self.can_switch_magic:
                self.can_switch_magic = False
                self.magic_switch_time = pygame.time.get_ticks()

                if self.magic_index < len(list(MAGIC_DATA.keys())) - 1:
                    self.magic_index += 1
                else:
                    self.magic_index = 0

                self.magic = list(MAGIC_DATA.keys())[self.magic_index]

    def get_status(self) -> None:
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def cooldowns(self) -> None:
        current_time = pygame.time.get_ticks()
        if self.attacking:
            if (
                current_time - self.attack_time
                >= self.attack_cooldown + WEAPON_DATA[self.weapon]["cooldown"]
            ):
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self) -> None:
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self) -> None:
        base_damage = self.stats["attack"]
        weapon_damage = WEAPON_DATA[self.weapon]["damage"]
        return base_damage + weapon_damage

    def get_full_magic_damage(self) -> None:
        base_damage = self.stats["magic"]
        spell_damage = MAGIC_DATA[self.magic]["strength"]
        return base_damage + spell_damage

    def get_value_by_index(self, index) -> list:
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index) -> list:
        return list(self.upgrade_cost.values())[index]

    def energy_recovery(self) -> None:
        if self.energy < self.stats["energy"]:
            self.energy += 0.01 * self.stats["magic"]
        else:
            self.energy = self.stats["energy"]

    def update(self) -> None:
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.stats["speed"])
        self.energy_recovery()
