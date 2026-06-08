"""Глобальные константы и настройки игры."""

# Виртуальное разрешение (вся отрисовка идёт сюда, потом масштабируется на экран)
VIRTUAL_W = 1280
VIRTUAL_H = 720
GROUND_Y = 620          # уровень пола (низ ног персонажа)

FPS = 60

# Цвета
WHITE = (240, 240, 240)
BLACK = (12, 12, 16)
RED = (200, 50, 50)
GREEN = (60, 200, 90)
BLUE = (70, 130, 220)
GOLD = (235, 195, 70)
PURPLE = (150, 80, 200)
DARKP = (30, 24, 40)
GREY = (90, 90, 100)

# ---- Сложности ----
DIFFICULTIES = {
    "EASY":   {"hp": 20, "label": "ЛЁГКАЯ"},
    "MEDIUM": {"hp": 12, "label": "СРЕДНЯЯ"},
    "HARD":   {"hp": 7,  "label": "ТЯЖЁЛАЯ"},
}

# Награда за босса: (мин, макс для 1-го босса, множитель границ на каждого
# следующего босса). Внутри диапазона — по скорости убийства и сохранённому HP.
# Цены в магазине одинаковые на всех сложностях (настроены под EASY), поэтому
# на MEDIUM/HARD денег меньше => сложнее. Округление границ — математическое.
REWARD_TUNING = {
    "EASY":   (3, 22, 1.5),
    "MEDIUM": (2, 17, 1.25),
    "HARD":   (1, 11, 1.1),
}

# Шанс босса увернуться от удара меча (по сложности). Сложнее => уворачивается чаще.
DODGE_CHANCE = {
    "EASY":   1 / 8,  # 1/8
    "MEDIUM": 1 / 7,  # 1/7
    "HARD":   1 / 4,  # 1/4
}

# Отброс босса при попадании меча игрока (пиксели) — сильный
HIT_KNOCKBACK = 120

# ---- Игрок (базовые значения) ----
PLAYER_SCALE = 2.6
PLAYER_SPEED = 4.6
PLAYER_JUMP = 15.5
GRAVITY = 0.7
PLAYER_BASE_DAMAGE = 1.0
DASH_SPEED = 16
DASH_TIME = 12          # кадров
DASH_COOLDOWN = 45
ATTACK_COOLDOWN = 60    # авто-атака раз в 1 секунду (белый слэш-индикатор)

# ---- Стены и лазание ----
WALL_MARGIN = 40        # где находятся «стены» (от краёв экрана)
WALL_SLIDE_SPEED = 1.8  # скорость сползания по стене (медленно)
WALL_JUMP_VY = 15.0     # вертикальный импульс отталкивания
WALL_JUMP_PUSH = 6.5    # горизонтальный толчок от стены
WALL_JUMP_DECAY = 0.82  # затухание толчка (чтобы можно было вернуться к стене)

# ---- Босс ----
BOSS_SCALE = 2.2
BOSS_FINAL_SCALE = 2.7   # демон: кадр 288x160, контент ~107px

# Глобальное ускорение боссов: движение и касты умений. НЕ влияет на личные
# механики (юла, телепорт, призыв, энергоформа, шарик, полёт, рост силы).
BOSS_SPEED_MULT = 1.8

# Параметры 7 боссов: hp, скорость, урон по игроку, кулдаун атаки, фон, тип
# Типы способностей:
#   charger  — врывается рывком (контактный урон телом)
#   jumper   — прыгает и бьёт по земле ударной волной
#   ranged   — стреляет снарядами на расстоянии
#   summoner — выпускает веер из 3 снарядов
#   berserk  — ускоряется и звереет при HP < 50%
#   demon    — финал: всё сразу (использует спрайт boss1.png)
# art — папка со спрайтами босса, НОМЕР ПАПКИ = НОМЕР ЛОКАЦИИ.
#   assets_boss1 — боец 1-й локации (готов), assets_boss7 — красный демон (готов).
#   assets_boss2..6 пока пусты => берут заглушку из assets_boss1.
#   Положишь в пустую папку свои листы (idle/run/attack/hurt, кадр 96x96 в
#   строку) — и босс этой локации сразу станет уникальным.
BOSSES = [
    {"name": "Страж Леса",       "hp": 12, "speed": 2.0, "cd": 70, "bg": "assets_bg/bg1.png", "type": "charger",  "art": "assets_boss1"},
    {"name": "Пламенный Сёгун",  "hp": 16, "speed": 2.7, "cd": 48, "bg": "assets_bg/bg2.png", "type": "ranged",   "art": "assets_boss6"},
    {"name": "Туманный Самурай", "hp": 20, "speed": 2.6, "cd": 60, "bg": "assets_bg/bg3.png", "type": "ranged",   "art": "assets_boss3"},
    {"name": "Бамбуковый Дух",   "hp": 26, "speed": 2.8, "cd": 55, "bg": "assets_bg/bg4.png", "type": "jumper",   "art": "assets_boss2"},
    {"name": "Хозяин Тории",     "hp": 32, "speed": 3.0, "cd": 52, "bg": "assets_bg/bg5.png", "type": "summoner", "art": "assets_boss5"},
    {"name": "Алый Странник",    "hp": 40, "speed": 3.2, "cd": 48, "bg": "assets_bg/bg6.png", "type": "berserk",  "art": "assets_boss4"},
    {"name": "ТЁМНЫЙ ДАЙМЁ",     "hp": 60, "speed": 3.4, "cd": 44, "bg": "assets_bg/bg7.png", "type": "demon",    "art": "assets_boss7"},
]

# ---- Щит игрока (доступен сразу, клавиша G) ----
# Блокирует ВСЕ удары в течение SHIELD_TIME, затем перезарядка.
SHIELD_TIME = 90       # 1.5 секунды активного щита
SHIELD_COOLDOWN = 90   # перезарядка после спадания (~1.5с)

# ---- Файрбол ----
FIREBALL_COOLDOWN = 90  # 1.5 секунды

# ---- Аура огня ----
AURA_BUDGET = 3.0       # сколько HP аура снимает за цикл
AURA_OFF_TIME = 300     # пауза после расхода бюджета (5 секунд)
AURA_DPS = 0.04         # урон ауры за кадр, пока враг в зоне

# ---- Пассивные регены ----
HP_REGEN_FRAMES = 180   # 1 HP за 3 секунды
MANA_REGEN_FRAMES = 180  # 1 мана за 3 секунды

# ---- Снаряды боссов ----
BOSS_PROJ_COLOR = {
    "ranged":   (120, 220, 160),
    "summoner": (200, 140, 240),
    "jumper":   (220, 200, 120),
    "demon":    (255, 120, 200),
}

# У каждого босса свой уникальный арт — подкраска не нужна.
BOSS_TINTS = [(255, 255, 255)] * 7

# ПОЛНОЕ описание каждого босса (после внимательного разбора ассетов).
#   scale     — масштаб тела
#   anims     — состояние: (файл, ширина кадра, высота кадра).
#               Листы нарезаются СЕТКОЙ построчно (cols*rows кадров).
#   abilities — список способностей, босс выбирает случайную готовую:
#     {"kind":"jump", "cd"}                       — прыжок + ударная волна
#     {"kind":"charge", "cd"}                     — рывок телом (контактный урон)
#     {"kind":"projectile","anim","fire_frame",   — каст: проигрывает анимацию
#       "proj":(файл,fw,fh,scale),"speed","radius","spin","cd"}  тела, на кадре
#                                                  fire_frame выпускает снаряд
#     {"kind":"beam","anim","fire_frame","reach","cd"} — луч (анимация уже рисует
#                                                  луч, хитбокс — вперёд на reach)
#     {"kind":"summon","anim","fire_frame",       — призыв миньонов
#       "minion":(файл,fw,fh,scale),"count","cd"}
#   anims-ключи: idle, run(ходьба), charge(рывок), attack, attack2(комбо),
#                flinch(вздрагивание при ударе), death(смерть), jump, cast_*,
#                float(парение в воздухе). Задействован КАЖДЫЙ ассет.
BOSS_SPEC = {
    "assets_boss1": {                       # Старик-мастер (96x96)
        "scale": 3.4,
        "anims": {
            "idle": ("idle.png", 96, 96), "run": ("run.png", 96, 96),
            "attack": ("attack.png", 96, 96),
            "flinch": ("hurt.png", 96, 96), "death": ("hurt.png", 96, 96)},
        "abilities": [
            {"kind": "charge", "cd": 140},
            {"kind": "jump", "cd": 160}],
    },
    "assets_boss2": {                       # Жнец (сетки 100x100)
        "scale": 2.2,
        "anims": {
            "idle": ("idle.png", 100, 100), "run": ("idle.png", 100, 100),
            "float": ("idle2.png", 100, 100),
            "attack": ("attacking.png", 100, 100),
            "death": ("death.png", 100, 100),
            "cast": ("summon.png", 100, 100),
            "spin": ("skill1.png", 100, 100)},
        # телепорт за спину: каждые 3с (cd=180) гарантированно бьёт косой
        "blink": {"cd": 180, "chance": 1.0, "offset": 95},
        # «юла»: каждые cd кадров с шансом chance включается на min..max кадров.
        # cd=300(5с), chance=0.8, длительность 180..540 кадров (3..9с).
        "spin_cfg": {"cd": 300, "chance": 0.8, "min_dur": 180, "max_dur": 540,
                     "spin_frames": [6, 7, 8]},
        "abilities": [
            # призыв чёрных слизней (чаще), они сносят HP контактом
            {"kind": "summon", "anim": "cast", "fire_frame": 4,
             "minion": ("summonIdle.png", 50, 50, 2.0),
             "appear": ("summonAppear.png", 50, 50, 2.0),
             "death_fx": ("summonDeath.png", 50, 50, 2.0),
             "count": 3, "cd": 200}],
    },
    "assets_boss3": {                       # Маг света
        "scale": 1.7,
        "anims": {
            "idle": ("Idle.png", 128, 128), "run": ("Walk.png", 128, 128),
            "charge": ("Run.png", 128, 128),
            "attack": ("Attack_1.png", 128, 128),
            "attack2": ("Attack_2.png", 128, 128),
            "flinch": ("Hurt.png", 128, 128), "death": ("Dead.png", 128, 128),
            "jump": ("Jump.png", 128, 128),
            "cast_ball": ("Light_ball.png", 128, 128),
            "cast_beam": ("Light_charge.png", 128, 128)},
        # Если 6с не наносит игроку урон — превращается в сгустки энергии
        # (спрайт Charge.png) и 9с преследует игрока по 2D, рядом = 1 HP/сек.
        "energy_form": {"trigger": 360, "duration": 540, "speed": 5.4,
                        "near": 95, "hit_cd": 60,
                        "frames": ("Charge.png", 64, 64, 2.0)},
        # МОЛНИЯ (луч) — кастуется каждые 5с с шансом 80%
        "scheduled": {"cd": 300, "chance": 0.8,
                      "ability": {"kind": "beam", "anim": "cast_beam",
                                  "fire_frame": 6, "reach": 540, "cd": 220}},
        "abilities": [
            {"kind": "projectile", "anim": "cast_ball", "fire_frame": 5,
             "proj": ("Charge.png", 64, 64, 1.6), "speed": 7, "radius": 22,
             "cd": 130},
            {"kind": "charge", "anim": "charge", "cd": 160},
            {"kind": "jump", "cd": 160}],
    },
    "assets_boss4": {                       # Тёмный маг
        "scale": 1.7,
        "anims": {
            "idle": ("Idle.png", 128, 128), "run": ("Walk.png", 128, 128),
            "charge": ("Run.png", 128, 128),
            "attack": ("Attack_1.png", 128, 128),
            "flinch": ("Hurt.png", 128, 128), "death": ("Dead.png", 128, 128),
            "jump": ("Jump.png", 128, 128),
            "cast_sphere": ("Magic_sphere.png", 128, 128),
            "cast_arrow": ("Magic_arrow.png", 128, 128),
            "cast_volley": ("Attack_2.png", 128, 128)},
        # чем дольше живёт — тем больше снарядов за каст и тем они быстрее
        # (буст за каждые period кадров жизни)
        "time_scaling": {"period": 420, "speed_mul": 0.18, "max_level": 6},
        # летающий портал: парит по карте и обстреливает; сбивается мечом (кд 5с)
        "flight": {"cd": 300, "proj": ("Charge_1.png", 128, 128, 0.7),
                   "interval": 65, "speed": 6, "radius": 20,
                   "color": (120, 170, 255)},
        # каждый снаряд при попадании отталкивает игрока (≈ как отдача игрока)
        "proj_shove": 22,
        "abilities": [
            {"kind": "projectile", "anim": "cast_sphere", "fire_frame": 10,
             "proj": ("Charge_1.png", 128, 128, 0.7), "speed": 5, "radius": 22,
             "cd": 150},
            {"kind": "projectile", "anim": "cast_arrow", "fire_frame": 4,
             "proj": ("Charge_2.png", 128, 128, 0.7), "speed": 9, "radius": 15,
             "spin": True, "cd": 110},
            {"kind": "volley", "anim": "cast_volley", "fire_frame": 7,
             "proj": ("Charge_2.png", 128, 128, 0.6), "count": 3, "spread": 0.32,
             "speed": 8, "radius": 13, "spin": True, "cd": 170},
            {"kind": "charge", "anim": "charge", "cd": 170},
            {"kind": "jump", "cd": 160}],
    },
    "assets_boss5": {                       # Теневой дух (247x87)
        "scale": 2.4,
        "anims": {
            "idle": ("idle.png", 247, 87), "run": ("walk.png", 247, 87),
            "attack": ("Attack 1.png", 247, 87),
            "attack2": ("Attack 2.png", 247, 87),
            "flinch": ("hit.png", 247, 87), "death": ("death.png", 247, 87),
            "cast_saw": ("Pre-Attack 3.png", 247, 87),
            "nova": ("end-Attack 3.png", 247, 87)},
        # фаза-шарик: при потере каждой 1/3 HP формируется в крутящийся шарик
        # (mid-Attack 3) и 7с очень быстро носится по арене: то отскакивает от
        # стен/пола/потолка, то «прилипает» и катится по периметру.
        "ball_phase": {"duration": 420, "speed": 68, "hit_cd": 40, "ceiling": 50,
                       "frames": ("mid-Attack 3.png", 247, 87, 1.0)},
        "abilities": [
            {"kind": "projectile", "anim": "cast_saw", "fire_frame": 2,
             "proj": ("mid-Attack 3.png", 247, 87, 1.0), "speed": 6,
             "radius": 26, "cd": 150},
            {"kind": "aoe", "anim": "nova", "fire_frame": 3, "radius": 175,
             "cd": 220},
            {"kind": "charge", "cd": 140},
            {"kind": "jump", "cd": 160}],
    },
    "assets_boss6": {                       # Огненный сёгун
        "scale": 1.7,
        "anims": {
            "idle": ("Idle.png", 128, 128), "run": ("Walk.png", 128, 128),
            "charge": ("Run.png", 128, 128),
            "attack": ("Attack_2.png", 128, 128),
            "attack2": ("Attack_1.png", 128, 128),
            "flinch": ("Hurt.png", 128, 128), "death": ("Dead.png", 128, 128),
            "jump": ("Jump.png", 128, 128),
            "cast_fire": ("Fireball.png", 128, 128),
            "cast_jet": ("Flame_jet.png", 128, 128)},
        # Активный босс: часто кидает фаербол, прыгает, рвётся и бьёт мечом;
        # луч (flame jet) — редко. (фаербол дублирован для веса при выборе)
        "abilities": [
            {"kind": "projectile", "anim": "cast_fire", "fire_frame": 5,
             "proj": ("Charge.png", 64, 64, 1.6), "speed": 7, "radius": 22,
             "spin": True, "cd": 50},
            {"kind": "projectile", "anim": "cast_fire", "fire_frame": 5,
             "proj": ("Charge.png", 64, 64, 1.6), "speed": 7, "radius": 22,
             "spin": True, "cd": 50},
            {"kind": "projectile", "anim": "cast_fire", "fire_frame": 5,
             "proj": ("Charge.png", 64, 64, 1.6), "speed": 7, "radius": 22,
             "spin": True, "cd": 50},
            {"kind": "charge", "anim": "charge", "cd": 75},
            {"kind": "jump", "cd": 65},
            {"kind": "jump", "cd": 65},
            {"kind": "beam", "anim": "cast_jet", "fire_frame": 5,
             "reach": 500, "cd": 200}],
    },
}

# ---- Умения ----
SKILLS = ["fireball", "dash", "double_jump", "fire_aura", "hp_regen", "mana_regen"]

# На EASY и MEDIUM умения выдаются в фиксированном порядке (босс 1..6).
# На HARD — порядок случайный.
SKILL_ORDER_FIXED = [
    "dash",         # босс 1
    "fireball",     # босс 2
    "hp_regen",     # босс 3 — пассивный реген HP
    "double_jump",  # босс 4
    "mana_regen",   # босс 5 — пассивный реген маны
    "fire_aura",    # босс 6
]
SKILL_NAMES = {
    "fireball":    "ФАЙРБОЛ (E)",
    "dash":        "РЫВОК (Shift)",
    "double_jump": "ДВОЙНОЙ ПРЫЖОК",
    "fire_aura":   "АУРА ОГНЯ",
    "hp_regen":    "РЕГЕН HP",
    "mana_regen":  "РЕГЕН МАНЫ",
}
SKILL_DESC = {
    "fireball":    "Бросай огонь во врага. Стоит 1 ману.",
    "dash":        "Быстрый рывок с неуязвимостью.",
    "double_jump": "Второй прыжок в воздухе.",
    "fire_aura":   "Огонь вокруг тебя жжёт врагов.",
    "hp_regen":    "Медленно восстанавливает HP.",
    "mana_regen":  "Медленно восстанавливает ману.",
}

# ---- Магазин ----
# id, название, описание, базовая цена, рост цены
# Цены подогнаны под доход на MEDIUM (за прохождение ~100-110 монет на покупки).
SHOP_ITEMS = [
    {"id": "speed",    "name": "Скорость +",    "desc": "+12% к скорости бега",   "cost": 5,  "grow": 3},
    {"id": "damage",   "name": "Урон +",        "desc": "+0.5 к урону меча",      "cost": 6,  "grow": 4},
    {"id": "maxhp",    "name": "Макс. HP +1",   "desc": "Увеличить макс. HP",     "cost": 7,  "grow": 5},
    {"id": "maxmana",  "name": "Макс. мана +1", "desc": "Увеличить макс. ману",   "cost": 6,  "grow": 4},
    {"id": "healhp",   "name": "Зелье HP",      "desc": "Восстановить всё HP",    "cost": 3,  "grow": 2},
    {"id": "healmana", "name": "Зелье маны",    "desc": "Восстановить всю ману",  "cost": 3,  "grow": 2},
]
