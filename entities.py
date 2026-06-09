import random
import pygame
import config as C
import assets


class Fireball:
    def __init__(self, x, y, direction, damage):
        self.x = x
        self.y = y
        self.dir = direction
        self.speed = 11
        self.damage = damage
        self.radius = 16
        self.alive = True
        self.anim = 0

    def update(self):
        self.x += self.speed * self.dir
        self.anim += 0.3
        if self.x < -50 or self.x > C.VIRTUAL_W + 50:
            self.alive = False

    @property
    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, surf):
        import math
        r = self.radius + int(math.sin(self.anim) * 2)

        glow = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 120, 30, 80), (r * 2, r * 2), r * 2)
        pygame.draw.circle(glow, (255, 180, 60, 160), (r * 2, r * 2), r)
        pygame.draw.circle(glow, (255, 240, 180), (r * 2, r * 2), r // 2)
        surf.blit(glow, (self.x - r * 2, self.y - r * 2))


class Projectile:

    def __init__(self, x, y, vx, vy, damage, color, radius=14, gravity=0.0,
                 life=180, frames=None, spin=False, frame_speed=0.3, shove=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.shove = shove
        self.damage = damage
        self.color = color
        self.radius = radius
        self.gravity = gravity
        self.life = life
        self.alive = True
        self.t = 0
        self.frames = frames
        self.frames_l = ([pygame.transform.flip(f, True, False) for f in frames]
                         if frames else None)
        self.spin = spin
        self.frame_speed = frame_speed
        self.anim = 0.0

    def update(self):
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.t += 1
        self.life -= 1
        self.anim += self.frame_speed
        if self.gravity and self.y >= C.GROUND_Y:
            self.y = C.GROUND_Y
            self.alive = False
        if self.life <= 0 or self.x < -60 or self.x > C.VIRTUAL_W + 60:
            self.alive = False

    @property
    def rect(self):
        r = self.radius
        return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)

    def draw(self, surf):
        if self.frames:
            frames = self.frames if self.vx >= 0 else self.frames_l
            img = frames[int(self.anim) % len(frames)]
            if self.spin:
                import math
                ang = math.degrees(math.atan2(-self.vy, abs(self.vx) + 0.01))
                img = pygame.transform.rotate(img, ang)
            r = img.get_rect(center=(int(self.x), int(self.y)))
            surf.blit(img, r)
            return
        r = self.radius
        glow = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        c = self.color
        pygame.draw.circle(glow, c + (70,), (r * 2, r * 2), r * 2)
        pygame.draw.circle(glow, c + (170,), (r * 2, r * 2), r)
        pygame.draw.circle(glow, (255, 255, 255), (r * 2, r * 2), r // 2)
        surf.blit(glow, (self.x - r * 2, self.y - r * 2))


class VFX:

    def __init__(self, x, y, frames, speed=0.3):
        self.x = x
        self.y = y
        self.frames = frames
        self.frames_l = [pygame.transform.flip(f, True, False) for f in frames]
        self.foot_pad = assets.bottom_pad(frames[0]) if frames else 0
        self.anim = 0.0
        self.speed = speed
        self.alive = True

    def update(self):
        self.anim += self.speed
        if self.anim >= len(self.frames):
            self.alive = False

    def draw(self, surf):
        img = self.frames[min(int(self.anim), len(self.frames) - 1)]
        r = img.get_rect()
        r.midbottom = (int(self.x), int(self.y) + self.foot_pad)
        surf.blit(img, r)


class Minion:

    def __init__(self, x, frames, damage, death_frames=None):
        self.x = x
        self.y = C.GROUND_Y
        self.frames = frames
        self.frames_l = [pygame.transform.flip(f, True, False) for f in frames]
        self.foot_pad = assets.bottom_pad(frames[0])
        self.death_frames = death_frames
        self.damage = damage
        self.hp = 2
        self.speed = 3.1
        self.facing = -1
        self.anim = 0.0
        self.alive = True
        self.life = 420
        self.hit_cd = 0

    @property
    def h(self):
        return self.frames[0].get_height()

    @property
    def rect(self):
        w = 70
        return pygame.Rect(self.x - w // 2, self.y - self.h, w, self.h)

    def update(self, player):
        self.life -= 1
        if self.hit_cd > 0:
            self.hit_cd -= 1
        self.facing = 1 if player.x > self.x else -1
        self.x += self.speed * self.facing
        self.anim += 0.15
        if self.life <= 0 or self.hp <= 0:
            self.alive = False

    def draw(self, surf):
        frames = self.frames if self.facing == 1 else self.frames_l
        img = frames[int(self.anim) % len(frames)]
        r = img.get_rect()
        r.midbottom = (int(self.x), int(self.y) + self.foot_pad)
        surf.blit(img, r)


class Player:
    def __init__(self, max_hp):
        self.anims = assets.load_player_anims()
        self.anims_l = {k: assets.flip(v) for k, v in self.anims.items()}

        self.foot_pad = assets.bottom_pad(self.anims["idle"][0])

        self.max_hp = max_hp
        self.hp = max_hp
        self.max_mana = 1
        self.mana = 0
        self.coins = 0
        self.damage = C.PLAYER_BASE_DAMAGE
        self.speed = C.PLAYER_SPEED

        self.x = 250
        self.y = C.GROUND_Y
        self.vy = 0
        self.on_ground = True
        self.facing = 1
        self.crouch = False

        self.state = "idle"
        self.frame = 0.0
        self.anim_speed = 0.15

        self.attacking = False
        self.attack_timer = 0
        self.attack_cd = 0
        self.hit_done = False

        self.dashing = False
        self.dash_timer = 0
        self.dash_cd = 0

        self.invuln = 0
        self.jumps_used = 0

        self.attack_variant = "attack"

        self.wall_sliding = False
        self.wall_side = None
        self.wall_jump_vx = 0.0

        self.shield_up = False
        self.shield_timer = 0
        self.shield_cd = 0

        self.fire_cd = 0

        self.god_mode = False

        self.skills = set()

        self.regen_acc = 0.0
        self.mana_regen_acc = 0.0
        self.aura_tick = 0

        self.aura_dealt = 0.0
        self.aura_off = 0

    @property
    def h(self):
        return 130

    @property
    def w(self):
        return 70

    @property
    def rect(self):
        return pygame.Rect(self.x - self.w // 2, self.y - self.h,
                           self.w, self.h)

    def attack_hitbox(self):
        reach = 95
        if self.facing == 1:
            return pygame.Rect(self.x, self.y - self.h, reach, self.h)
        return pygame.Rect(self.x - reach, self.y - self.h, reach, self.h)

    def jump(self):

        if self.wall_sliding:
            away = 1 if self.wall_side == "left" else -1
            self.vy = -C.WALL_JUMP_VY
            self.wall_jump_vx = away * C.WALL_JUMP_PUSH
            self.facing = away
            self.wall_sliding = False
            self.wall_side = None
            self.jumps_used = 1
            return

        max_jumps = 2 if "double_jump" in self.skills else 1
        if self.on_ground:
            self.vy = -C.PLAYER_JUMP
            self.on_ground = False
            self.jumps_used = 1
        elif self.jumps_used < max_jumps:
            self.vy = -C.PLAYER_JUMP
            self.jumps_used += 1

    def start_attack(self):
        if self.attack_cd <= 0 and not self.dashing:
            self.attacking = True
            self.attack_timer = 0
            self.attack_cd = C.ATTACK_COOLDOWN
            self.hit_done = False
            self.frame = 0.0

            self.attack_variant = ("attack2"
                                   if self.attack_variant == "attack"
                                   else "attack")

    def start_dash(self):
        if "dash" in self.skills and self.dash_cd <= 0 and not self.dashing:
            self.dashing = True
            self.dash_timer = C.DASH_TIME
            self.dash_cd = C.DASH_COOLDOWN
            self.invuln = C.DASH_TIME + 4
            self.frame = 0.0

    def try_fireball(self):
        if ("fireball" in self.skills and self.mana >= 1
                and self.fire_cd <= 0 and not self.attacking):
            self.mana -= 1
            self.fire_cd = C.FIREBALL_COOLDOWN
            fx = self.x + self.facing * 50
            fy = self.y - self.h // 2
            return Fireball(fx, fy, self.facing, self.damage * 2)
        return None

    def start_shield(self):
        if self.shield_cd <= 0 and not self.shield_up and not self.dashing:
            self.shield_up = True
            self.shield_timer = C.SHIELD_TIME

    def shove(self, from_x, power=16, lift=7):

        away = 1 if self.x >= from_x else -1
        self.wall_jump_vx = away * power
        if self.on_ground:
            self.vy = -lift
            self.on_ground = False

    def take_damage(self, dmg, direct=True):

        if self.god_mode:
            return False

        if self.shield_up and direct:
            return False
        if self.invuln > 0:
            return False
        self.hp -= dmg
        self.invuln = 50
        if self.hp < 0:
            self.hp = 0
        return True

    def update(self, keys):
        moving = False

        if self.dashing:
            self.x += C.DASH_SPEED * self.facing
            self.dash_timer -= 1
            if self.dash_timer <= 0:
                self.dashing = False
        else:

            if not (self.attacking and self.on_ground):
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    self.x -= self.speed
                    self.facing = -1
                    moving = True
                if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    self.x += self.speed
                    self.facing = 1
                    moving = True
            self.crouch = ((keys[pygame.K_s] or keys[pygame.K_DOWN])
                           and self.on_ground)

        if self.wall_jump_vx != 0:
            self.x += self.wall_jump_vx
            self.wall_jump_vx *= C.WALL_JUMP_DECAY
            if abs(self.wall_jump_vx) < 0.4:
                self.wall_jump_vx = 0.0

        left = C.WALL_MARGIN
        right = C.VIRTUAL_W - C.WALL_MARGIN
        self.x = max(left, min(right, self.x))

        self.vy += C.GRAVITY
        self.y += self.vy

        if self.y - self.h < 4:
            self.y = self.h + 4
            if self.vy < 0:
                self.vy = 0

        self.wall_sliding = False
        if (not self.on_ground and not self.dashing and self.vy > 0):
            at_left = self.x <= left + 2 and (keys[pygame.K_a] or keys[pygame.K_LEFT])
            at_right = self.x >= right - 2 and (keys[pygame.K_d] or keys[pygame.K_RIGHT])
            if at_left or at_right:
                self.wall_sliding = True
                self.wall_side = "left" if at_left else "right"

                self.facing = 1 if at_left else -1
                self.jumps_used = 0
                if self.vy > C.WALL_SLIDE_SPEED:
                    self.vy = C.WALL_SLIDE_SPEED

        if self.y >= C.GROUND_Y:
            self.y = C.GROUND_Y
            self.vy = 0
            self.on_ground = True
            self.jumps_used = 0
            self.wall_sliding = False
        else:
            self.on_ground = False

        if self.attack_cd > 0:
            self.attack_cd -= 1
        if self.dash_cd > 0:
            self.dash_cd -= 1
        if self.invuln > 0:
            self.invuln -= 1
        if self.fire_cd > 0:
            self.fire_cd -= 1

        if self.shield_cd > 0:
            self.shield_cd -= 1
        if self.shield_up:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_up = False
                self.shield_cd = C.SHIELD_COOLDOWN

        if self.attacking:
            self.attack_timer += 1
            if self.attack_timer > 18:
                self.attacking = False

        if "hp_regen" in self.skills and self.hp < self.max_hp:
            self.regen_acc += 1
            if self.regen_acc >= C.HP_REGEN_FRAMES:
                self.regen_acc = 0
                self.hp = min(self.max_hp, self.hp + 1)
        if "mana_regen" in self.skills and self.mana < self.max_mana:
            self.mana_regen_acc += 1
            if self.mana_regen_acc >= C.MANA_REGEN_FRAMES:
                self.mana_regen_acc = 0
                self.mana = min(self.max_mana, self.mana + 1)

        if self.aura_off > 0:
            self.aura_off -= 1

        if self.dashing:
            self.state = "dash"
        elif self.attacking:
            self.state = self.attack_variant
        elif self.wall_sliding:
            self.state = "idle"
        elif not self.on_ground:
            self.state = "idle"
        elif moving:
            self.state = "run"
        else:
            self.state = "idle"

        is_attack = self.state in ("attack", "attack2")
        spd = 0.4 if is_attack else self.anim_speed
        self.frame += spd
        frames = self.anims[self.state]
        if self.frame >= len(frames):
            self.frame = 0.0

    def current_frame(self):
        anims = self.anims if self.facing == 1 else self.anims_l
        frames = anims[self.state]
        idx = int(self.frame) % len(frames)
        return frames[idx]

    def draw(self, surf):
        frame = self.current_frame()
        rect = frame.get_rect()
        rect.midbottom = (int(self.x), int(self.y) + self.foot_pad)

        if self.invuln > 0 and (self.invuln // 4) % 2 == 0:
            tmp = frame.copy()
            tmp.set_alpha(120)
            surf.blit(tmp, rect)
        else:
            surf.blit(frame, rect)

        if "fire_aura" in self.skills and self.aura_off <= 0:
            self.aura_tick += 1
            import math
            r = 75 + int(math.sin(self.aura_tick * 0.1) * 6)
            aura = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(aura, (255, 120, 30, 60), (r, r), r)
            pygame.draw.circle(aura, (255, 80, 20, 40), (r, r), r - 10)
            surf.blit(aura, (self.x - r, self.y - self.h // 2 - r))

        if self.attack_cd > 0:
            import math
            frac = self.attack_cd / C.ATTACK_COOLDOWN
            R = int(78 * frac)
            if R > 5:
                cx = int(self.x + self.facing * 58)
                cy = int(self.y - self.h // 2)
                pad = R + 10
                slash = pygame.Surface((pad * 2, pad * 2), pygame.SRCALPHA)
                a = int(220 * frac)
                rect = pygame.Rect(pad - R, pad - R, R * 2, R * 2)
                if self.facing == 1:
                    a0, a1 = -0.95, 0.95
                else:
                    a0, a1 = math.pi - 0.95, math.pi + 0.95
                width = max(3, int(R * 0.45))
                pygame.draw.arc(slash, (255, 255, 255, a), rect, a0, a1, width)
                pygame.draw.arc(slash, (200, 230, 255, a // 2), rect,
                                a0, a1, max(1, width // 2))
                surf.blit(slash, (cx - pad, cy - pad))

        if self.shield_up:
            import math
            cx = int(self.x)
            cy = int(self.y - self.h // 2)
            r = 62
            pulse = int(math.sin(pygame.time.get_ticks() * 0.02) * 4)
            bubble = pygame.Surface((r * 2 + 12, r * 2 + 12), pygame.SRCALPHA)
            pygame.draw.circle(bubble, (120, 200, 255, 70),
                               (r + 6, r + 6), r + pulse)
            pygame.draw.circle(bubble, (180, 230, 255, 200),
                               (r + 6, r + 6), r + pulse, 4)
            surf.blit(bubble, (cx - r - 6, cy - r - 6))

    def aura_hitbox(self):
        if "fire_aura" not in self.skills or self.aura_off > 0:
            return None
        r = 80
        return pygame.Rect(self.x - r, self.y - self.h // 2 - r, r * 2, r * 2)


class Boss:
    def __init__(self, index, data, scale, tint_color, is_final=False):
        import math
        self.index = index
        self.name = data["name"]
        self.max_hp = data["hp"]
        self.hp = data["hp"]
        self.move_speed = data["speed"] * C.BOSS_SPEED_MULT
        self.base_speed = self.move_speed
        self.attack_cd_max = data["cd"]
        self.is_final = is_final
        self.btype = data.get("type", "melee")

        if self.btype == "demon":
            anims = assets.load_boss1_anims(scale)
        else:

            anims = assets.load_boss_spec_anims(data.get("art", "assets_boss1"))
        self.anims = anims
        self.anims_l = {k: assets.flip(v) for k, v in anims.items()}
        self.foot_pad = assets.bottom_pad(anims["idle"][0])

        self.x = C.VIRTUAL_W - 300
        self.y = C.GROUND_Y
        self.vy = 0
        self.on_ground = True
        self.facing = -1

        self.state = "idle"
        self.frame = 0.0

        self.attack_cd = 60
        self.attacking = False
        self.attack_timer = 0
        self.hit_done = False

        self.hurt_timer = 0
        self.dead = False
        self.death_timer = 0

        self.ability_cd = 120
        self.charging = False
        self.charge_timer = 0
        self.contact_done = False
        self.pending_slam = False
        self.enraged = False
        self.new_projectiles = []
        self.new_minions = []
        self.dodge_cd = 0
        self.kb_vx = 0.0
        self.melee_variant = "attack"
        self.melee_active = False
        self.new_vfx = []

        self.spinning = False
        self.spin_timer = 0
        self.spin_anim = 0.0
        self.spin_dir = 1
        self.spin_frames = None
        self.spin_cfg = None
        self.spin_check_cd = 300
        self.blink_cfg = None
        self.blink_cd = 180
        self.hover_timer = 0
        self.hover_y = 0

        self.sched_cfg = None
        self.sched_ability = None
        self.sched_check_cd = 300

        self.hp_regen_frames = 0
        self.hp_regen_acc = 0

        self.fire_cfg = None
        self.fire_phase = 0
        self.fire_phase_timer = 0
        self.fire_timer = 0
        self.fire_side = "left"

        self.alive_frames = 0
        self.power_level = 0
        self.ts_cfg = None
        self.can_fly = False
        self.flight_cfg = None
        self.flying = False
        self.flight_cd = 0
        self.flight_t = 0
        self.energy_frames = None
        self.proj_shove = 0

        self.ball_cfg = None
        self.ball_frames = None
        self.ball_mode = False
        self.ball_timer = 0
        self.ball_vx = 0.0
        self.ball_vy = 0.0
        self.ball_anim = 0.0
        self.ball_hit_cd = 0
        self.ball_pending = False
        self.ball_thresholds = []
        self.ball_triggered = set()
        self.ball_aura_timer = 0
        self.dmg_cap = 0
        self.ball_state = "bounce"
        self.ball_state_timer = 0
        self.ball_want_roll = False
        self.roll_edge = "top"
        self.roll_cw = True

        self.energy_cfg = None
        self.energy_cluster = None
        self.energy_mode = False
        self.energy_timer = 0
        self.energy_hit_cd = 0
        self.energy_anim = 0.0
        self.no_dmg_timer = 0

        self.casting = None
        self.cast_anim = "attack"
        self.cast_t = 0.0
        self.cast_fired = False
        self.beam_active = False

        self.abilities = []
        if self.btype == "demon":

            self.abilities = [
                {"kind": "demon_spread", "anim": "cast", "fire_frame": 2,
                 "cd": 85},
                {"kind": "demon_shot", "anim": "cast", "fire_frame": 2,
                 "cd": 80},
                {"kind": "charge", "anim": "run", "cd": 120},
                {"kind": "jump", "cd": 140},
            ]
            self.hp_regen_frames = 20

            self.fire_cfg = {"warn": 90, "burn": 210, "idle": 300, "dmg": 2}
            self.fire_timer = 300
        else:
            folder = data.get("art", "assets_boss1")
            spec = C.BOSS_SPEC.get(folder) or C.BOSS_SPEC["assets_boss1"]
            self.blink_cfg = spec.get("blink")
            sc = spec.get("scheduled")
            if sc:
                self.sched_cfg = sc
                self.sched_ability = dict(sc["ability"])
                self.sched_check_cd = sc.get("cd", 300)
            if self.blink_cfg:
                self.blink_cd = self.blink_cfg.get("cd", 180)
            self.spin_cfg = spec.get("spin_cfg")
            if self.spin_cfg:
                self.spin_check_cd = self.spin_cfg.get("cd", 300)
            self.ts_cfg = spec.get("time_scaling")
            self.proj_shove = spec.get("proj_shove", 0)
            self.dmg_cap = spec.get("dmg_cap", 0)
            self.ball_cfg = spec.get("ball_phase")
            if self.ball_cfg:
                self.ball_thresholds = [self.max_hp * 2 / 3.0,
                                        self.max_hp / 3.0]
                try:
                    f, fw, fh, sc = self.ball_cfg["frames"]
                    self.ball_frames = assets.load_grid_anim(
                        folder, f, fw, fh, sc)
                except Exception as e:
                    print("ball frames load fail:", e)
            self.energy_cfg = spec.get("energy_form")
            if self.energy_cfg:
                try:
                    f, fw, fh, sc = self.energy_cfg["frames"]
                    self.energy_cluster = assets.load_grid_anim(
                        folder, f, fw, fh, sc)
                except Exception as e:
                    print("energy frames load fail:", e)
            fl = spec.get("flight")
            if fl:
                self.can_fly = True
                self.flight_cfg = fl
                self.flight_cd = 180
                try:
                    f, fw, fh, sc = fl["proj"]
                    self.energy_frames = assets.load_grid_anim(
                        folder, f, fw, fh, sc)
                except Exception as e:
                    print("flight proj load fail:", e)
            for raw in spec["abilities"]:
                ab = dict(raw)
                try:
                    if "proj" in ab:
                        f, fw, fh, sc = ab["proj"]
                        ab["proj_frames"] = assets.load_grid_anim(
                            folder, f, fw, fh, sc)
                    if "minion" in ab:
                        f, fw, fh, sc = ab["minion"]
                        ab["minion_frames"] = assets.load_grid_anim(
                            folder, f, fw, fh, sc)
                    if "appear" in ab:
                        f, fw, fh, sc = ab["appear"]
                        ab["appear_frames"] = assets.load_grid_anim(
                            folder, f, fw, fh, sc)
                    if "death_fx" in ab:
                        f, fw, fh, sc = ab["death_fx"]
                        ab["death_fx_frames"] = assets.load_grid_anim(
                            folder, f, fw, fh, sc)
                except Exception as e:
                    print("ability load fail:", folder, ab.get("kind"), e)
                self.abilities.append(ab)

    @property
    def h(self):
        return 150 if not self.is_final else 220

    @property
    def w(self):
        return 90 if not self.is_final else 130

    @property
    def rect(self):
        if self.ball_mode:
            r = 55
            return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)
        if self.energy_mode:
            r = 70
            return pygame.Rect(self.x - r, self.y - r, r * 2, r * 2)
        return pygame.Rect(self.x - self.w // 2, self.y - self.h,
                           self.w, self.h)

    def attack_hitbox(self):
        reach = 110 if not self.is_final else 150
        if self.facing == 1:
            return pygame.Rect(self.x, self.y - self.h, reach, self.h)
        return pygame.Rect(self.x - reach, self.y - self.h, reach, self.h)

    def take_damage(self, dmg):
        if self.dead or self.ball_mode or self.energy_mode:
            return
        if self.dmg_cap and dmg > self.dmg_cap:
            dmg = self.dmg_cap
        self.hp -= dmg
        self.hurt_timer = 14

        if self.ball_cfg and self.hp > 0:
            for thr in self.ball_thresholds:
                if thr not in self.ball_triggered and self.hp <= thr:
                    self.ball_triggered.add(thr)
                    self.ball_pending = True
        if self.hp <= 0:
            self.hp = 0
            self.dead = True
            self.death_timer = 60

    def knockback(self, from_x):

        if self.spinning:
            return
        away = 1 if self.x >= from_x else -1

        self.kb_vx = away * (C.HIT_KNOCKBACK / 4.0)

    def can_dodge(self):
        return (self.on_ground and self.dodge_cd <= 0
                and not self.dead and not self.charging)

    def do_dodge(self, player):
        away = -1 if player.x > self.x else 1
        self.vy = -12
        self.on_ground = False
        self.x = max(60, min(C.VIRTUAL_W - 60, self.x + away * 45))
        self.dodge_cd = 45

    def _proj_dmg(self):
        return 2 if self.is_final else 1

    def _shoot_at(self, player, speed, color, radius=14, frames=None,
                  spin=False, frame_speed=0.3):
        import math
        px = player.x
        py = player.y - player.h // 2
        sx = self.x + self.facing * 30
        sy = self.y - int(self.h * 0.6)
        dx = px - sx
        dy = py - sy
        d = max(1.0, math.hypot(dx, dy))
        vx = dx / d * speed
        vy = dy / d * speed
        self.new_projectiles.append(
            Projectile(sx, sy, vx, vy, self._proj_dmg(), color, radius,
                       frames=frames, spin=spin, frame_speed=frame_speed))

    def beam_hitbox(self):
        if not self.beam_active or not self.casting:
            return None
        reach = self.casting.get("reach", 480)
        top = int(self.y - self.h * 0.78)
        hh = int(self.h * 0.5)
        if self.facing == 1:
            return pygame.Rect(self.x, top, reach, hh)
        return pygame.Rect(self.x - reach, top, reach, hh)

    def end_flight(self):

        if self.flying:
            self.flying = False
            self.flight_cd = self.flight_cfg.get("cd", 300) if self.flight_cfg else 300
            self.vy = 1.0
            self.on_ground = False

    def _energy_shot(self, player, base_speed, color, radius, frames):

        import math
        count = 1 + self.power_level
        spd = base_speed * (1 + self.power_level *
                            (self.ts_cfg or {}).get("speed_mul", 0.0))
        sx = self.x
        sy = self.y - int(self.h * 0.5)
        base = math.atan2((player.y - player.h // 2) - sy, player.x - sx)
        spread = 0.16
        for k in range(count):
            a = base + spread * (k - (count - 1) / 2.0)
            vx = math.cos(a) * spd
            vy = math.sin(a) * spd
            self.new_projectiles.append(
                Projectile(sx, sy, vx, vy, self._proj_dmg(), color, radius,
                           frames=frames, spin=True, shove=self.proj_shove))

    def _update_flight(self, player):
        import math
        FS = 1.05
        self.flight_t += 1
        self.facing = 1 if player.x > self.x else -1

        y_hi, y_lo = 180, C.GROUND_Y - 20
        mid = (y_hi + y_lo) / 2.0
        amp = (y_lo - y_hi) / 2.0
        self.y = mid + amp * math.sin(self.flight_t * 0.035 * FS)
        self.vy = 0
        self.on_ground = False

        side = (C.VIRTUAL_W - 180) if player.x < C.VIRTUAL_W / 2 else 180
        self.x += (side - self.x) * 0.05 * FS
        self.x += math.sin(self.flight_t * 0.09) * 5.0 * FS
        self.x = max(70, min(C.VIRTUAL_W - 70, self.x))

        interval = max(18, int(self.flight_cfg.get("interval", 65) / FS)
                       - self.power_level * 6)
        if self.flight_t % interval == 0:
            self._energy_shot(player, self.flight_cfg.get("speed", 6),
                              self.flight_cfg.get("color", (120, 170, 255)),
                              self.flight_cfg.get("radius", 20),
                              self.energy_frames)
        self.state = "idle"
        self._advance_frame()

    def _update_fire(self, player):

        cfg = self.fire_cfg
        if self.fire_phase == 0:
            self.fire_timer -= 1
            if self.fire_timer <= 0:
                self.fire_phase = 1
                self.fire_phase_timer = cfg["warn"]

                self.fire_side = "left" if player.x < C.VIRTUAL_W / 2 else "right"
        elif self.fire_phase == 1:
            self.fire_phase_timer -= 1
            if self.fire_phase_timer <= 0:
                self.fire_phase = 2
                self.fire_phase_timer = cfg["burn"]
        elif self.fire_phase == 2:
            self.fire_phase_timer -= 1
            in_zone = ((self.fire_side == "left" and player.x < C.VIRTUAL_W / 2)
                       or (self.fire_side == "right"
                           and player.x >= C.VIRTUAL_W / 2))
            if in_zone:
                player.take_damage(cfg.get("dmg", 2), direct=True)
            if self.fire_phase_timer <= 0:
                self.fire_phase = 0
                self.fire_timer = cfg["idle"]

    def draw_fire(self, surf):

        if self.fire_phase == 0 or not self.fire_cfg:
            return
        import math
        x0 = 0 if self.fire_side == "left" else C.VIRTUAL_W // 2
        w = C.VIRTUAL_W // 2
        ov = pygame.Surface((w, C.GROUND_Y), pygame.SRCALPHA)
        t = pygame.time.get_ticks() * 0.01
        if self.fire_phase == 1:

            a = 40 + int(35 * (0.5 + 0.5 * math.sin(t * 1.2)))
            ov.fill((255, 80, 30, a // 3))

            for i in range(80):
                aa = int(a * (i / 80))
                pygame.draw.line(ov, (255, 120, 40, aa),
                                 (0, C.GROUND_Y - 80 + i), (w, C.GROUND_Y - 80 + i))
        else:

            ov.fill((255, 70, 20, 90))
            for i in range(0, w, 26):
                fh = 60 + int(40 * (0.5 + 0.5 * math.sin(t + i * 0.05)))
                col = (255, 160 + int(60 * math.sin(t + i)), 40, 150)
                pygame.draw.polygon(ov, col, [
                    (i, C.GROUND_Y), (i + 13, C.GROUND_Y - fh), (i + 26, C.GROUND_Y)])
        surf.blit(ov, (x0, 0))

    def _start_ball(self):
        cfg = self.ball_cfg
        sp = cfg.get("speed", 68)
        self.ball_mode = True
        self.ball_timer = cfg.get("duration", 420)
        self.ball_hit_cd = 0
        self.ball_anim = 0.0
        self.ball_state = "bounce"
        self.ball_state_timer = random.randint(45, 90)
        self.ball_aura_timer = 15
        self.ball_want_roll = False
        self.ball_vx = random.choice([-1, 1]) * sp * 0.72
        self.ball_vy = -sp * 0.72
        self.y = C.GROUND_Y - 130
        self.on_ground = False
        self.casting = None
        self.attacking = False
        self.charging = False

    def _ball_bounce(self, d, left, right, top, bottom):
        import math
        mag = max(0.01, math.hypot(self.ball_vx, self.ball_vy))
        self.x += self.ball_vx / mag * d
        self.y += self.ball_vy / mag * d
        hit = None
        if self.x <= left:
            self.x = left
            self.ball_vx = abs(self.ball_vx)
            hit = "left"
        elif self.x >= right:
            self.x = right
            self.ball_vx = -abs(self.ball_vx)
            hit = "right"
        if self.y <= top:
            self.y = top
            self.ball_vy = abs(self.ball_vy)
            hit = "top"
        elif self.y >= bottom:
            self.y = bottom
            self.ball_vy = -abs(self.ball_vy)
            hit = "bottom"

        if hit and self.ball_want_roll:
            self.ball_want_roll = False
            self.ball_state = "roll"
            self.ball_state_timer = random.randint(110, 200)
            self.roll_edge = hit
            self.roll_cw = random.choice([True, False])

    def _ball_roll(self, d, left, right, top, bottom):
        cw = self.roll_cw
        e = self.roll_edge
        if e == "top":
            self.y = top
            self.x += d if cw else -d
            if cw and self.x >= right:
                self.x = right
                self.roll_edge = "right"
            elif not cw and self.x <= left:
                self.x = left
                self.roll_edge = "left"
        elif e == "right":
            self.x = right
            self.y += d if cw else -d
            if cw and self.y >= bottom:
                self.y = bottom
                self.roll_edge = "bottom"
            elif not cw and self.y <= top:
                self.y = top
                self.roll_edge = "top"
        elif e == "bottom":
            self.y = bottom
            self.x += -d if cw else d
            if cw and self.x <= left:
                self.x = left
                self.roll_edge = "left"
            elif not cw and self.x >= right:
                self.x = right
                self.roll_edge = "right"
        else:
            self.x = left
            self.y += -d if cw else d
            if cw and self.y <= top:
                self.y = top
                self.roll_edge = "top"
            elif not cw and self.y >= bottom:
                self.y = bottom
                self.roll_edge = "bottom"

    def _update_ball(self, player):
        cfg = self.ball_cfg
        sp = cfg.get("speed", 68)
        left, right = 70, C.VIRTUAL_W - 70
        top, bottom = cfg.get("ceiling", 50), C.GROUND_Y
        self.ball_timer -= 1
        self.ball_anim += 0.9
        if self.ball_hit_cd > 0:
            self.ball_hit_cd -= 1

        self.ball_aura_timer -= 1
        if self.ball_aura_timer <= 0:
            self.ball_aura_timer = 60
            import math
            n = cfg.get("aura_count", 10)
            sp_a = cfg.get("aura_speed", 8.0)
            for k in range(n):
                a = (k / float(n)) * 2 * math.pi + self.ball_anim * 0.1
                self.new_projectiles.append(
                    Projectile(self.x, self.y, math.cos(a) * sp_a,
                               math.sin(a) * sp_a, 1, (45, 20, 60), 16,
                               life=110))

        self.ball_state_timer -= 1
        if self.ball_state == "bounce":

            if self.ball_state_timer <= 0:
                self.ball_want_roll = True
        else:
            if self.ball_state_timer <= 0:
                self.ball_state = "bounce"
                self.ball_state_timer = random.randint(60, 130)
                self.ball_vx = random.choice([-1, 1]) * sp * 0.72
                self.ball_vy = random.choice([-1, 1]) * sp * 0.72

        steps = max(1, int(sp / 11))
        d = sp / steps
        for _ in range(steps):
            if self.ball_state == "roll":
                self._ball_roll(d, left, right, top, bottom)
            else:
                self._ball_bounce(d, left, right, top, bottom)
            if self.ball_hit_cd <= 0 and self.rect.colliderect(player.rect):
                if player.take_damage(self._proj_dmg(), direct=True):
                    self.ball_hit_cd = cfg.get("hit_cd", 40)

        if self.ball_timer <= 0:
            self.ball_mode = False
            self.y = C.GROUND_Y
            self.vy = 0
            self.on_ground = True

    def _update_energy(self, player):

        import math
        cfg = self.energy_cfg
        self.energy_timer -= 1
        self.energy_anim += 0.45
        if self.energy_hit_cd > 0:
            self.energy_hit_cd -= 1
        tx = player.x
        ty = player.y - player.h * 0.5
        dx, dy = tx - self.x, ty - self.y
        d = max(1.0, math.hypot(dx, dy))
        sp = cfg.get("speed", 5.4)
        self.x += dx / d * sp
        self.y += dy / d * sp
        self.x = max(40, min(C.VIRTUAL_W - 40, self.x))
        self.y = max(60, min(C.GROUND_Y, self.y))
        self.facing = 1 if dx >= 0 else -1

        if d < cfg.get("near", 95) and self.energy_hit_cd <= 0:
            if player.take_damage(1, direct=True):
                self.energy_hit_cd = cfg.get("hit_cd", 60)
        if self.energy_timer <= 0:
            self.energy_mode = False
            self.no_dmg_timer = 0
            self.y = C.GROUND_Y
            self.vy = 0
            self.on_ground = True

    def _do_effect(self, ab, player):
        kind = ab["kind"]
        if kind == "projectile":
            col = (255, 210, 90)
            if self.ts_cfg:
                self._energy_shot(player, ab.get("speed", 7), col,
                                  ab.get("radius", 18), ab.get("proj_frames"))
            else:
                self._shoot_at(player, ab.get("speed", 7), col,
                               ab.get("radius", 18),
                               frames=ab.get("proj_frames"),
                               spin=ab.get("spin", False),
                               frame_speed=ab.get("proj_speed", 0.3))
        elif kind == "summon":
            frames = ab.get("minion_frames")
            death_fx = ab.get("death_fx_frames")
            appear = ab.get("appear_frames")
            if frames:
                cnt = ab.get("count", 2)
                for k in range(cnt):
                    off = -70 + (140 * k / max(1, cnt - 1)) if cnt > 1 else 0
                    mx = self.x + off
                    self.new_minions.append(
                        Minion(mx, frames, self._proj_dmg(), death_fx))
                    if appear:
                        self.new_vfx.append(VFX(mx, C.GROUND_Y, appear))
        elif kind == "aoe":

            import math
            bx, by = self.x, self.y - self.h * 0.4
            px, py = player.x, player.y - player.h * 0.5
            if math.hypot(px - bx, py - by) <= ab.get("radius", 150):
                player.take_damage(self._proj_dmg(), direct=True)
        elif kind == "volley":

            import math
            frames = ab.get("proj_frames")
            sx = self.x + self.facing * 30
            sy = self.y - int(self.h * 0.6)
            base = math.atan2((player.y - player.h // 2) - sy, player.x - sx)
            cnt = ab.get("count", 3)
            spread = ab.get("spread", 0.3)
            speed = ab.get("speed", 8)
            for k in range(cnt):
                a = base + spread * (k - (cnt - 1) / 2.0)
                vx = math.cos(a) * speed
                vy = math.sin(a) * speed
                self.new_projectiles.append(
                    Projectile(sx, sy, vx, vy, self._proj_dmg(),
                               (190, 200, 255), ab.get("radius", 14),
                               frames=frames, spin=ab.get("spin", True)))
        elif kind == "demon_spread":

            import math
            sx = self.x + self.facing * 30
            sy = self.y - int(self.h * 0.6)
            base = math.atan2((player.y - player.h // 2) - sy, player.x - sx)
            for off in (-0.5, -0.25, 0.0, 0.25, 0.5):
                vx = math.cos(base + off) * 7
                vy = math.sin(base + off) * 7
                self.new_projectiles.append(
                    Projectile(sx, sy, vx, vy, self._proj_dmg(),
                               (255, 120, 60), 18))
        elif kind == "demon_shot":
            self._shoot_at(player, 10, (255, 170, 70), 20)

    def _shockwave(self, color):
        for d in (-1, 1):
            self.new_projectiles.append(
                Projectile(self.x + d * 40, C.GROUND_Y - 16, d * 7, 0,
                           self._proj_dmg(), color, 18, life=90))

    def _start_charge(self, t=20, cd=130):
        self.charging = True
        self.charge_timer = t
        self.contact_done = False
        self.ability_cd = cd

    def _start_jump(self, cd=130):
        if self.on_ground:
            self.vy = -16
            self.on_ground = False
            self.pending_slam = True
        self.ability_cd = cd

    def _start_spin(self, player):
        cfg = self.spin_cfg or {}
        self.spinning = True
        self.attacking = False
        self.melee_active = False
        self.kb_vx = 0.0
        self.spin_timer = random.randint(cfg.get("min_dur", 180),
                                         cfg.get("max_dur", 540))
        self.spin_dir = 1 if player.x >= self.x else -1
        self.spin_anim = 0.0
        self.spin_frames = cfg.get("spin_frames")

    def _trigger_ability(self, player):

        if not self.abilities:
            self.ability_cd = 120
            return
        ab = random.choice(self.abilities)
        kind = ab["kind"]
        if kind == "charge":
            self._start_charge(20, ab.get("cd", 130))
        elif kind == "jump":
            self._start_jump(ab.get("cd", 150))
        else:

            self.casting = ab
            self.cast_anim = ab.get("anim", "attack")
            self.cast_t = 0.0
            self.cast_fired = False
            self.beam_active = False

    def update(self, player):
        if self.dead:
            self.death_timer -= 1
            self.flying = False
            self.energy_mode = False
            self.ball_mode = False
            if self.y < C.GROUND_Y:
                self.vy += C.GRAVITY
                self.y = min(C.GROUND_Y, self.y + self.vy)
            ds = "death" if "death" in self.anims else "idle"
            self.state = ds
            self.frame += 0.15
            if self.frame >= len(self.anims[ds]):
                self.frame = len(self.anims[ds]) - 1
            return

        if self.fire_cfg:
            self._update_fire(player)

        if self.ball_pending and not self.ball_mode:
            self.ball_pending = False
            self._start_ball()
        if self.ball_mode:
            self._update_ball(player)
            return

        if self.hp_regen_frames > 0 and 0 < self.hp < self.max_hp:
            self.hp_regen_acc += 1
            if self.hp_regen_acc >= self.hp_regen_frames:
                self.hp_regen_acc = 0
                self.hp = min(self.max_hp, self.hp + 1)

        self.alive_frames += 1
        if self.ts_cfg:
            self.power_level = min(
                self.ts_cfg.get("max_level", 6),
                self.alive_frames // self.ts_cfg.get("period", 420))

        if self.energy_cfg:
            self.no_dmg_timer += 1
            if self.energy_mode:
                self._update_energy(player)
                return
            if (self.no_dmg_timer >= self.energy_cfg.get("trigger", 360)
                    and self.on_ground and not self.casting
                    and not self.charging and not self.attacking
                    and not self.spinning):
                self.energy_mode = True
                self.energy_timer = self.energy_cfg.get("duration", 540)
                self.energy_hit_cd = 0
                return

        if self.flying:
            self._update_flight(player)
            return

        hovering = self.hover_timer > 0
        if hovering:
            self.hover_timer -= 1
            self.y = self.hover_y
            self.vy = 0
            self.on_ground = False
        else:

            was_air = not self.on_ground
            self.vy += C.GRAVITY
            self.y += self.vy
            if self.y >= C.GROUND_Y:
                self.y = C.GROUND_Y
                self.vy = 0
                if was_air and self.pending_slam:
                    self._shockwave(C.BOSS_PROJ_COLOR["jumper"])
                    self.pending_slam = False
                self.on_ground = True
            else:
                self.on_ground = False

        if abs(self.kb_vx) > 0.2:
            self.x = max(60, min(C.VIRTUAL_W - 60, self.x + self.kb_vx))
            self.kb_vx *= 0.78
            self._advance_frame()
            return

        self.facing = 1 if player.x > self.x else -1
        dist = abs(player.x - self.x)

        if self.attack_cd > 0:
            self.attack_cd -= 1
        if self.hurt_timer > 0:
            self.hurt_timer -= 1
        if self.ability_cd > 0:
            self.ability_cd -= 1
        if self.dodge_cd > 0:
            self.dodge_cd -= 1
        if self.flight_cd > 0:
            self.flight_cd -= 1

        if (self.btype == "berserk" and not self.enraged
                and self.hp <= self.max_hp * 0.5):
            self.enraged = True
            self.move_speed = self.base_speed * 1.6
            self.attack_cd_max = int(self.attack_cd_max * 0.7)

        if (self.blink_cfg and self.on_ground
                and not self.casting and not self.charging):
            self.blink_cd -= 1
            if self.blink_cd <= 0:
                self.blink_cd = self.blink_cfg.get("cd", 180)
                if random.random() < self.blink_cfg.get("chance", 1.0):
                    off = self.blink_cfg.get("offset", 95)
                    behind = player.x - player.facing * off
                    on_wall = getattr(player, "wall_sliding", False)
                    if on_wall:

                        tx = player.x + player.facing * off
                        self.hover_y = max(60, player.y)
                        self.y = self.hover_y
                        self.hover_timer = 50
                    elif behind < 80 or behind > C.VIRTUAL_W - 80:
                        tx = player.x + player.facing * off
                    else:
                        tx = behind
                    self.x = max(70, min(C.VIRTUAL_W - 70, tx))
                    self.facing = 1 if player.x > self.x else -1
                    if self.spinning:
                        self.spin_dir = self.facing
                    else:
                        self.attacking = True
                        self.attack_timer = 0
                        self.melee_variant = "attack"
                        self.melee_active = False
                        self.hit_done = False
                        return

        if (self.sched_cfg and not self.casting and not self.charging
                and not self.spinning and not self.attacking and self.on_ground):
            self.sched_check_cd -= 1
            if self.sched_check_cd <= 0:
                self.sched_check_cd = self.sched_cfg.get("cd", 300)
                if random.random() < self.sched_cfg.get("chance", 0.8):
                    self.casting = self.sched_ability
                    self.cast_anim = self.sched_ability.get("anim", "attack")
                    self.cast_t = 0.0
                    self.cast_fired = False
                    self.beam_active = False
                    return

        if (self.can_fly and self.flight_cd <= 0 and self.on_ground
                and not self.charging and not self.casting
                and not self.spinning and not self.attacking):
            self.flying = True
            self.flight_t = 0
            return

        if self.spin_cfg and not self.spinning:
            self.spin_check_cd -= 1
            if self.spin_check_cd <= 0:
                self.spin_check_cd = self.spin_cfg.get("cd", 300)
                if (self.on_ground and not self.casting and not self.charging
                        and random.random() < self.spin_cfg.get("chance", 0.8)):
                    self._start_spin(player)
                    return

        if self.charging:
            self.x += 13 * self.facing
            self.charge_timer -= 1
            self.state = "charge" if "charge" in self.anims else "run"
            if (not self.contact_done
                    and self.rect.colliderect(player.rect)):
                if player.take_damage(self._proj_dmg(), direct=True):
                    self.contact_done = True
            if self.charge_timer <= 0:
                self.charging = False
            self.x = max(60, min(C.VIRTUAL_W - 60, self.x))
            self._advance_frame()
            return

        if self.spinning:
            self.spin_timer -= 1
            frames = self.anims.get("spin", self.anims["attack"])
            self.state = "spin" if "spin" in self.anims else "attack"
            self.spin_anim += 0.4
            n = len(frames)

            seq = [i for i in (self.spin_frames or
                               list(range(max(0, n - 6), n))) if i < n]
            if not seq:
                seq = [n - 1]
            self.frame = seq[int(self.spin_anim) % len(seq)]
            self.x += self.spin_dir * 11
            if self.x <= 70:
                self.x = 70
                self.spin_dir = 1
            elif self.x >= C.VIRTUAL_W - 70:
                self.x = C.VIRTUAL_W - 70
                self.spin_dir = -1
            self.facing = self.spin_dir
            if self.rect.colliderect(player.rect):
                player.take_damage(2, direct=True)
                player.shove(self.x, power=20, lift=9)
            if self.spin_timer <= 0:
                self.spinning = False
            return

        if self.attacking:
            self.facing = 1 if player.x > self.x else -1
            frames = self.anims[self.melee_variant]
            T = 34
            self.state = self.melee_variant
            self.attack_timer += 1
            self.frame = self.attack_timer * (len(frames) / T)
            self.melee_active = (T * 0.30 <= self.attack_timer <= T * 0.72)
            if self.attack_timer >= T:
                self.attacking = False
                self.melee_active = False
            return

        if self.casting:
            ab = self.casting
            self.cast_anim = ab.get("anim", "attack")
            if self.cast_anim not in self.anims:
                self.cast_anim = "attack"
            frames = self.anims[self.cast_anim]
            self.state = self.cast_anim
            self.cast_t += ab.get("anim_speed", 0.3) * C.BOSS_SPEED_MULT
            idx = int(self.cast_t)
            if not self.cast_fired and idx >= ab.get("fire_frame", 2):
                self._do_effect(ab, player)
                self.cast_fired = True
            if ab["kind"] == "beam":
                self.beam_active = self.cast_fired and idx < len(frames) - 1
            self.frame = min(self.cast_t, len(frames) - 1)
            if idx >= len(frames):
                self.casting = None
                self.beam_active = False
                self.ability_cd = ab.get("cd", 140)
            return

        if (self.ability_cd <= 0 and not self.attacking and not self.casting
                and not self.spinning and self.on_ground
                and self.hurt_timer == 0):
            self._trigger_ability(player)

        if not self.on_ground:
            if "jump" in self.anims:
                self.state = "jump"
            elif "float" in self.anims:
                self.state = "float"
            else:
                self.state = "run"
        else:
            attack_range = 120 if not self.is_final else 160
            if dist > attack_range:
                self.x += self.move_speed * self.facing
                self.state = "run"
            else:
                self.state = "idle"
                if self.attack_cd <= 0:
                    self.attacking = True
                    self.attack_timer = 0
                    self.attack_cd = self.attack_cd_max
                    self.hit_done = False

                    if "attack2" in self.anims:
                        self.melee_variant = ("attack2"
                                              if self.melee_variant == "attack"
                                              else "attack")
                    else:
                        self.melee_variant = "attack"

        self.x = max(60, min(C.VIRTUAL_W - 60, self.x))
        self._advance_frame()

    def _advance_frame(self):
        self.frame += 0.2
        if self.frame >= len(self.anims[self.state]):
            self.frame = 0.0

    def current_frame(self):
        anims = self.anims if self.facing == 1 else self.anims_l
        frames = anims[self.state]
        idx = int(self.frame) % len(frames)
        return frames[idx]

    def draw(self, surf):

        if self.ball_mode and self.ball_frames:
            cx, cy = int(self.x), int(self.y)
            glow = pygame.Surface((150, 150), pygame.SRCALPHA)
            pygame.draw.circle(glow, (200, 220, 255, 70), (75, 75), 60)
            pygame.draw.circle(glow, (160, 200, 255, 90), (75, 75), 38)
            surf.blit(glow, (cx - 75, cy - 75))
            img = self.ball_frames[int(self.ball_anim) % len(self.ball_frames)]
            img = pygame.transform.rotate(img, (self.ball_anim * 47) % 360)
            surf.blit(img, img.get_rect(center=(cx, cy)))
            return

        if self.energy_mode and self.energy_cluster:
            import math
            fr = self.energy_cluster
            nf = len(fr)
            cx, cy = int(self.x), int(self.y)

            glow = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(glow, (180, 210, 120, 50), (100, 100), 90)
            surf.blit(glow, (cx - 100, cy - 100))
            for i, (ox, oy, ph) in enumerate(
                    [(0, 0, 0), (-30, -16, 2), (28, -12, 4),
                     (-14, 20, 6), (18, 18, 1)]):
                idx = int(self.energy_anim + i * 1.7) % nf
                img = fr[idx]
                wob = int(math.sin((self.energy_anim + ph) * 0.5) * 5)
                r = img.get_rect(center=(cx + ox, cy + oy + wob))
                surf.blit(img, r)
            return

        if self.flying and self.flight_cfg:
            import math
            col = self.flight_cfg.get("color", (120, 170, 255))
            cx = int(self.x)
            cy = int(self.y) - 2
            pw, ph = 210, 80
            portal = pygame.Surface((pw, ph), pygame.SRCALPHA)
            t = pygame.time.get_ticks() * 0.006
            for rw, rh, a in ((98, 36, 60), (76, 28, 110), (50, 18, 190)):
                rw2 = rw + int(math.sin(t) * 5)
                pygame.draw.ellipse(portal, col + (a,),
                                    (pw // 2 - rw2, ph // 2 - rh, rw2 * 2, rh * 2))
            pygame.draw.ellipse(portal, col + (220,),
                                (pw // 2 - 50, ph // 2 - 18, 100, 36), 3)
            surf.blit(portal, (cx - pw // 2, cy - ph // 2))

        use_flinch = (self.hurt_timer > 0 and not self.dead
                      and "flinch" in self.anims)
        if use_flinch:
            anims = self.anims if self.facing == 1 else self.anims_l
            ff = anims["flinch"]
            idx = min(int((1 - self.hurt_timer / 14.0) * len(ff)), len(ff) - 1)
            frame = ff[idx]
        else:
            frame = self.current_frame()
        rect = frame.get_rect()
        rect.midbottom = (int(self.x), int(self.y) + self.foot_pad)
        if (not use_flinch and self.hurt_timer > 0 and not self.dead
                and (self.hurt_timer // 2) % 2 == 0):
            tmp = frame.copy()
            tmp.fill((255, 255, 255, 90), special_flags=pygame.BLEND_RGBA_ADD)
            surf.blit(tmp, rect)
        else:
            surf.blit(frame, rect)
