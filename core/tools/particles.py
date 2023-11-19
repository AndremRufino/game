import pygame
from random import choice
from core.helpers.support import import_folder
from core.config.settings import BASE_DIR


class AnimationPlayer:
    def __init__(self) -> None:
        self.frames = {
            "flame": import_folder(
                f"{BASE_DIR}/assets/graphics/particles/flame/frames"
            ),
            "aura": import_folder(f"{BASE_DIR}/assets/graphics/particles/aura"),
            "heal": import_folder(f"{BASE_DIR}/assets/graphics/particles/heal/frames"),
            "claw": import_folder(f"{BASE_DIR}/assets/graphics/particles/claw"),
            "slash": import_folder(f"{BASE_DIR}/assets/graphics/particles/slash"),
            "sparkle": import_folder(f"{BASE_DIR}/assets/graphics/particles/sparkle"),
            "leaf_attack": import_folder(
                f"{BASE_DIR}/assets/graphics/particles/leaf_attack"
            ),
            "thunder": import_folder(f"{BASE_DIR}/assets/graphics/particles/thunder"),
            "squid": import_folder(
                f"{BASE_DIR}/assets/graphics/particles/smoke_orange"
            ),
            "raccoon": import_folder(f"{BASE_DIR}/assets/graphics/particles/raccoon"),
            "spirit": import_folder(f"{BASE_DIR}/assets/graphics/particles/nova"),
            "bamboo": import_folder(f"{BASE_DIR}/assets/graphics/particles/bamboo"),
            "leaf": (
                import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf1"),
                import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf2"),
                import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf3"),
                import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf4"),
                import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf5"),
                import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf6"),
                self.reflect_images(
                    import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf1")
                ),
                self.reflect_images(
                    import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf2")
                ),
                self.reflect_images(
                    import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf3")
                ),
                self.reflect_images(
                    import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf4")
                ),
                self.reflect_images(
                    import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf5")
                ),
                self.reflect_images(
                    import_folder(f"{BASE_DIR}/assets/graphics/particles/leaf6")
                ),
            ),
        }

    def reflect_images(self, frames) -> None:
        new_frames = list()

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame, True, False)
            new_frames.append(flipped_frame)
        return new_frames

    def create_grass_particles(self, pos, groups) -> None:
        animation_frames = choice(self.frames["leaf"])
        ParticleEffect(pos, animation_frames, groups)

    def create_particles(self, animation_type, pos, groups) -> None:
        animation_frames = self.frames[animation_type]
        ParticleEffect(pos, animation_frames, groups)


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups) -> None:
        super().__init__(groups)
        self.sprite_type = "magic"
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self) -> None:
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self) -> None:
        self.animate()
