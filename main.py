import pygame
import math
import random

pygame.init()

# ============================================================
# SETUP
# ============================================================

WIDTH = 950
HEIGHT = 650

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crazy Asteroids")

clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 26)
small_font = pygame.font.SysFont(None, 21)
controls_font = pygame.font.SysFont(None, 18)


# ============================================================
# COLORS
# ============================================================

BLACK = (5, 8, 18)
DARK_BLUE = (10, 18, 38)

WHITE = (245, 248, 255)

GRAY = (120, 130, 150)
LIGHT_GRAY = (180, 190, 210)

RED = (255, 80, 90)
YELLOW = (255, 220, 90)

BLUE = (90, 170, 255)
CYAN = (90, 235, 255)

GREEN = (100, 235, 150)
ORANGE = (255, 155, 70)


# ============================================================
# GAME CONSTANTS
# ============================================================

ROTATION_SPEED = 3

THRUST = 0.15
DRAG = 0.99
MAX_SPEED = 7

MISSILE_SPEED = 7

DETECTION_RANGE = 300
FOV_THRESHOLD = 0.7


# ============================================================
# BACKGROUND STARS
# ============================================================

stars = []

for i in range(90):
    stars.append(
        (
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.choice([1, 1, 1, 2])
        )
    )


# ============================================================
# SPACESHIP
# Lessons 3 and 4
# ============================================================

class Spaceship:

    def __init__(self):

        self.position = pygame.Vector2(
            WIDTH / 2,
            HEIGHT / 2
        )

        self.angle = 90

        self.velocity = pygame.Vector2(
            0,
            0
        )

        self.acceleration = pygame.Vector2(
            0,
            0
        )

        self.is_thrusting = False

        self.radius = 15


    def update(self, keys):

        # Rotate left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle += ROTATION_SPEED

        # Rotate right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle -= ROTATION_SPEED


        radians = math.radians(
            self.angle
        )


        forward = pygame.Vector2(
            math.cos(radians),
            -math.sin(radians)
        )


        self.acceleration = pygame.Vector2(
            0,
            0
        )

        self.is_thrusting = False


        # Thrust
        if keys[pygame.K_UP] or keys[pygame.K_w]:

            self.acceleration = (
                forward * THRUST
            )

            self.is_thrusting = True


        # Update velocity
        self.velocity += self.acceleration


        # Drag
        self.velocity *= DRAG


        # Maximum speed
        if self.velocity.length() > MAX_SPEED:

            self.velocity.scale_to_length(
                MAX_SPEED
            )


        # Update position
        self.position += self.velocity


        # Screen wrapping
        if self.position.x > WIDTH:
            self.position.x = 0

        if self.position.x < 0:
            self.position.x = WIDTH

        if self.position.y > HEIGHT:
            self.position.y = 0

        if self.position.y < 0:
            self.position.y = HEIGHT


    def get_forward(self):

        radians = math.radians(
            self.angle
        )

        forward = pygame.Vector2(
            math.cos(radians),
            -math.sin(radians)
        )

        return forward


    def draw(self):

        forward = self.get_forward()

        left = forward.rotate(140)
        right = forward.rotate(-140)

        p1 = self.position + forward * 24
        p2 = self.position + left * 17
        p3 = self.position + right * 17

        ship_points = [
            (
                int(p1.x),
                int(p1.y)
            ),
            (
                int(p2.x),
                int(p2.y)
            ),
            (
                int(p3.x),
                int(p3.y)
            )
        ]


        pygame.draw.polygon(
            screen,
            DARK_BLUE,
            ship_points
        )


        pygame.draw.polygon(
            screen,
            WHITE,
            ship_points,
            2
        )


        # Engine flame
        if self.is_thrusting:

            back = (
                self.position
                -
                forward * 18
            )

            flame_tip = (
                self.position
                -
                forward * 30
            )


            pygame.draw.line(
                screen,
                ORANGE,
                (
                    int(back.x),
                    int(back.y)
                ),
                (
                    int(flame_tip.x),
                    int(flame_tip.y)
                ),
                5
            )


            pygame.draw.circle(
                screen,
                YELLOW,
                (
                    int(back.x),
                    int(back.y)
                ),
                4
            )


        # Red forward direction line
        pygame.draw.line(
            screen,
            RED,
            (
                int(self.position.x),
                int(self.position.y)
            ),
            (
                int(
                    self.position.x
                    +
                    forward.x * 70
                ),
                int(
                    self.position.y
                    +
                    forward.y * 70
                )
            ),
            2
        )


        # Yellow velocity line
        pygame.draw.line(
            screen,
            YELLOW,
            (
                int(self.position.x),
                int(self.position.y)
            ),
            (
                int(
                    self.position.x
                    +
                    self.velocity.x * 10
                ),
                int(
                    self.position.y
                    +
                    self.velocity.y * 10
                )
            ),
            2
        )


# ============================================================
# ASTEROID
# Lesson 1
# ============================================================

class Asteroid:

    def __init__(
        self,
        x,
        y,
        radius,
        velocity
    ):

        self.position = pygame.Vector2(
            x,
            y
        )

        self.radius = radius

        self.velocity = pygame.Vector2(
            velocity
        )

        self.mass = radius * radius

        self.shape = []


        for i in range(10):

            angle = (
                i
                *
                360
                /
                10
            )

            distance = random.uniform(
                0.78,
                1.0
            )

            self.shape.append(
                (
                    angle,
                    distance
                )
            )


    def update(self):

        self.position += self.velocity


        if self.position.x > WIDTH:
            self.position.x = 0

        if self.position.x < 0:
            self.position.x = WIDTH

        if self.position.y > HEIGHT:
            self.position.y = 0

        if self.position.y < 0:
            self.position.y = HEIGHT


    def draw(self):

        points = []


        for angle, distance in self.shape:

            radians = math.radians(
                angle
            )

            point_x = (
                self.position.x
                +
                math.cos(radians)
                *
                self.radius
                *
                distance
            )

            point_y = (
                self.position.y
                +
                math.sin(radians)
                *
                self.radius
                *
                distance
            )

            points.append(
                (
                    int(point_x),
                    int(point_y)
                )
            )


        pygame.draw.polygon(
            screen,
            (25, 30, 45),
            points
        )


        pygame.draw.polygon(
            screen,
            LIGHT_GRAY,
            points,
            2
        )


        crater_position = (
            int(
                self.position.x
                -
                self.radius * 0.20
            ),
            int(
                self.position.y
                -
                self.radius * 0.10
            )
        )


        pygame.draw.circle(
            screen,
            GRAY,
            crater_position,
            max(
                3,
                int(
                    self.radius * 0.16
                )
            ),
            1
        )


# ============================================================
# MISSILE
# Lesson 2
# ============================================================

class Missile:

    def __init__(
        self,
        position,
        velocity,
        color=CYAN,
        outline_color=BLUE
    ):

        self.position = pygame.Vector2(
            position
        )

        self.velocity = pygame.Vector2(
            velocity
        )

        self.radius = 4

        self.color = color

        self.outline_color = outline_color


    def update(self):

        self.position += self.velocity


    def draw(self):

        pygame.draw.circle(
            screen,
            self.outline_color,
            (
                int(self.position.x),
                int(self.position.y)
            ),
            7,
            1
        )


        pygame.draw.circle(
            screen,
            self.color,
            (
                int(self.position.x),
                int(self.position.y)
            ),
            self.radius
        )


# ============================================================
# ENEMY
# Lesson 5
# ============================================================

class Enemy:

    def __init__(self):

        self.position = pygame.Vector2(
            WIDTH / 4,
            HEIGHT / 2
        )


        # ====================================================
        # NEW: RANDOM ENEMY MOVEMENT
        # ====================================================

        random_angle = random.uniform(
            0,
            360
        )

        random_speed = random.uniform(
            0.7,
            1.5
        )


        self.velocity = pygame.Vector2(
            math.cos(
                math.radians(random_angle)
            )
            *
            random_speed,

            -math.sin(
                math.radians(random_angle)
            )
            *
            random_speed
        )


        # ====================================================
        # NEW: RANDOM ROTATION
        # ====================================================

        self.angle = random.uniform(
            0,
            360
        )


        self.rotation_speed = random.uniform(
            -1.0,
            1.0
        )


        # Every once in a while the enemy changes direction
        self.wander_timer = random.randint(
            45,
            120
        )


        self.detected = False

        self.state = "PATROL"

        self.distance = 0

        self.dot = 0


        # ====================================================
        # NEW: SHOOTING TIMER
        # ====================================================

        self.shoot_cooldown = 0

        # 45 frames is about 0.75 seconds at 60 FPS
        self.shoot_delay = 45


    def update(
        self,
        player,
        enemy_missiles
    ):


        # ====================================================
        # NEW: RANDOM MOVEMENT
        # ====================================================

        self.wander_timer -= 1


        if self.wander_timer <= 0:

            # Turn movement slightly
            change_angle = random.uniform(
                -45,
                45
            )


            self.velocity = (
                self.velocity.rotate(
                    change_angle
                )
            )


            if self.velocity.length() == 0:

                self.velocity = pygame.Vector2(
                    1,
                    0
                )


            # Random movement speed
            self.velocity.scale_to_length(
                random.uniform(
                    0.7,
                    1.5
                )
            )


            # Random rotation direction/speed
            self.rotation_speed = random.uniform(
                -1.2,
                1.2
            )


            self.wander_timer = random.randint(
                45,
                120
            )


        # Move enemy
        self.position += self.velocity


        # Rotate enemy
        self.angle += self.rotation_speed


        # Enemy screen wrapping
        if self.position.x > WIDTH:
            self.position.x = 0

        if self.position.x < 0:
            self.position.x = WIDTH

        if self.position.y > HEIGHT:
            self.position.y = 0

        if self.position.y < 0:
            self.position.y = HEIGHT


        # ----------------------------------------------------
        # Enemy Forward Vector
        # ----------------------------------------------------

        radians = math.radians(
            self.angle
        )


        enemy_forward = pygame.Vector2(
            math.cos(radians),
            -math.sin(radians)
        )


        # ----------------------------------------------------
        # Direction Toward Player
        # ----------------------------------------------------

        to_player = (
            player.position
            -
            self.position
        )


        # ----------------------------------------------------
        # Distance
        # ----------------------------------------------------

        self.distance = (
            self.position.distance_to(
                player.position
            )
        )


        if to_player.length() > 0:

            to_player_normalized = (
                to_player.normalize()
            )

        else:

            to_player_normalized = pygame.Vector2(
                0,
                0
            )


        # ----------------------------------------------------
        # Dot Product
        # ----------------------------------------------------

        self.dot = (
            enemy_forward.dot(
                to_player_normalized
            )
        )


        # ----------------------------------------------------
        # AI Decision
        # ----------------------------------------------------

        if (
            self.distance < DETECTION_RANGE
            and
            self.dot > FOV_THRESHOLD
        ):

            self.detected = True

            self.state = "ATTACK"


            # ================================================
            # NEW: ACTUALLY SHOOT AT PLAYER
            # ================================================

            if self.shoot_cooldown > 0:

                self.shoot_cooldown -= 1


            if (
                self.shoot_cooldown <= 0
                and
                self.distance > 0
            ):

                # Shoot toward player's current location
                enemy_missile_velocity = (
                    to_player_normalized
                    *
                    MISSILE_SPEED
                )


                enemy_missiles.append(

                    Missile(
                        self.position,
                        enemy_missile_velocity,
                        RED,
                        ORANGE
                    )

                )


                # Reset firing timer
                self.shoot_cooldown = (
                    self.shoot_delay
                )


        else:

            self.detected = False

            self.state = "PATROL"


            if self.shoot_cooldown > 0:

                self.shoot_cooldown -= 1


    def draw(self):

        radians = math.radians(
            self.angle
        )


        enemy_forward = pygame.Vector2(
            math.cos(radians),
            -math.sin(radians)
        )


        if self.detected:

            color = RED

        else:

            color = WHITE


        # ----------------------------------------------------
        # Detection Range
        # ----------------------------------------------------

        pygame.draw.circle(
            screen,
            GRAY,
            (
                int(self.position.x),
                int(self.position.y)
            ),
            DETECTION_RANGE,
            1
        )


        # ----------------------------------------------------
        # Field of View
        # ----------------------------------------------------

        half_angle = math.degrees(
            math.acos(
                FOV_THRESHOLD
            )
        )


        left_fov = (
            enemy_forward.rotate(
                half_angle
            )
            *
            DETECTION_RANGE
        )


        right_fov = (
            enemy_forward.rotate(
                -half_angle
            )
            *
            DETECTION_RANGE
        )


        pygame.draw.line(
            screen,
            (80, 90, 120),
            self.position,
            self.position + left_fov,
            1
        )


        pygame.draw.line(
            screen,
            (80, 90, 120),
            self.position,
            self.position + right_fov,
            1
        )


        # ----------------------------------------------------
        # Draw Enemy Ship
        # ----------------------------------------------------

        left = enemy_forward.rotate(
            140
        )


        right = enemy_forward.rotate(
            -140
        )


        p1 = (
            self.position
            +
            enemy_forward * 22
        )


        p2 = (
            self.position
            +
            left * 16
        )


        p3 = (
            self.position
            +
            right * 16
        )


        enemy_points = [

            (
                int(p1.x),
                int(p1.y)
            ),

            (
                int(p2.x),
                int(p2.y)
            ),

            (
                int(p3.x),
                int(p3.y)
            )

        ]


        if self.detected:

            inside_color = (
                35,
                18,
                25
            )

        else:

            inside_color = DARK_BLUE


        pygame.draw.polygon(
            screen,
            inside_color,
            enemy_points
        )


        pygame.draw.polygon(
            screen,
            color,
            enemy_points,
            2
        )


        # Enemy forward vector
        pygame.draw.line(
            screen,
            RED,
            self.position,
            self.position
            +
            enemy_forward * 100,
            3
        )


# ============================================================
# CREATE SIX ASTEROIDS
# ============================================================

asteroids = []


for i in range(6):

    radius = random.randint(
        20,
        35
    )


    x = random.randint(
        50,
        WIDTH - 50
    )


    y = random.randint(
        80,
        HEIGHT - 50
    )


    angle = random.uniform(
        0,
        2 * math.pi
    )


    speed = (
        1
        +
        i * 0.3
    )


    velocity = pygame.Vector2(
        math.cos(angle) * speed,
        math.sin(angle) * speed
    )


    asteroids.append(

        Asteroid(
            x,
            y,
            radius,
            velocity
        )

    )


# ============================================================
# ASTEROID COLLISION
# ============================================================

def handle_asteroid_collision(
    a,
    b
):

    difference = (
        b.position
        -
        a.position
    )


    distance = (
        difference.length()
    )


    if distance == 0:

        return


    if (
        distance
        <
        a.radius + b.radius
    ):

        normal = (
            difference.normalize()
        )


        overlap = (
            a.radius
            +
            b.radius
            -
            distance
        )


        a.position -= (
            normal
            *
            (overlap / 2)
        )


        b.position += (
            normal
            *
            (overlap / 2)
        )


        relative_velocity = (
            a.velocity
            -
            b.velocity
        )


        velocity_along_normal = (
            relative_velocity.dot(
                normal
            )
        )


        if velocity_along_normal <= 0:

            return


        impulse = (

            2
            *
            velocity_along_normal

            /

            (
                a.mass
                +
                b.mass
            )
        )


        a.velocity -= (
            impulse
            *
            b.mass
            *
            normal
        )


        b.velocity += (
            impulse
            *
            a.mass
            *
            normal
        )


# ============================================================
# DRAW BACKGROUND
# ============================================================

def draw_background():

    screen.fill(
        BLACK
    )


    for star_x, star_y, star_size in stars:

        pygame.draw.circle(
            screen,
            (
                145,
                155,
                180
            ),
            (
                star_x,
                star_y
            ),
            star_size
        )


# ============================================================
# DISPLAY CONTROLS + INFORMATION
# ============================================================

def draw_information(
    ship,
    enemy
):

    forward = (
        ship.get_forward()
    )


    # --------------------------------------------------------
    # CONTROLS PANEL
    # --------------------------------------------------------

    controls = [

        "CONTROLS",

        "LEFT / A = Turn Left",

        "RIGHT / D = Turn Right",

        "UP / W = Thrust",

        "SPACE = Fire",

        "CLICK = Fire"

    ]


    panel_x = 12
    panel_y = 12

    panel_width = 165
    panel_height = 112


    pygame.draw.rect(
        screen,
        (
            12,
            18,
            32
        ),
        (
            panel_x,
            panel_y,
            panel_width,
            panel_height
        )
    )


    pygame.draw.rect(
        screen,
        (
            70,
            90,
            130
        ),
        (
            panel_x,
            panel_y,
            panel_width,
            panel_height
        ),
        1
    )


    y = panel_y + 8


    for i in range(
        len(controls)
    ):

        if i == 0:

            text = controls_font.render(
                controls[i],
                True,
                CYAN
            )

        else:

            text = controls_font.render(
                controls[i],
                True,
                WHITE
            )


        screen.blit(
            text,
            (
                panel_x + 7,
                y
            )
        )


        y += 16


    # --------------------------------------------------------
    # INFORMATION
    # --------------------------------------------------------

    angle_text = small_font.render(
        f"Angle: {ship.angle:.0f}",
        True,
        WHITE
    )


    forward_text = small_font.render(
        f"Forward: ({forward.x:.2f}, {forward.y:.2f})",
        True,
        WHITE
    )


    speed_text = small_font.render(
        f"Speed: {ship.velocity.length():.2f}",
        True,
        WHITE
    )


    velocity_text = small_font.render(
        f"Velocity: ({ship.velocity.x:.2f}, {ship.velocity.y:.2f})",
        True,
        WHITE
    )


    distance_text = small_font.render(
        f"Distance: {enemy.distance:.1f}",
        True,
        WHITE
    )


    dot_text = small_font.render(
        f"Dot Product: {enemy.dot:.2f}",
        True,
        WHITE
    )


    if enemy.detected:

        state_color = RED

    else:

        state_color = GREEN


    state_text = small_font.render(
        f"Enemy: {enemy.state}",
        True,
        state_color
    )


    # --------------------------------------------------------
    # MATH PANEL
    # --------------------------------------------------------

    math_panel_x = WIDTH - 245
    math_panel_y = 12

    math_panel_width = 230
    math_panel_height = 145


    pygame.draw.rect(
        screen,
        (
            12,
            18,
            32
        ),
        (
            math_panel_x,
            math_panel_y,
            math_panel_width,
            math_panel_height
        )
    )


    pygame.draw.rect(
        screen,
        (
            70,
            90,
            130
        ),
        (
            math_panel_x,
            math_panel_y,
            math_panel_width,
            math_panel_height
        ),
        1
    )


    screen.blit(
        state_text,
        (
            math_panel_x + 8,
            math_panel_y + 8
        )
    )


    screen.blit(
        angle_text,
        (
            math_panel_x + 8,
            math_panel_y + 28
        )
    )


    screen.blit(
        forward_text,
        (
            math_panel_x + 8,
            math_panel_y + 48
        )
    )


    screen.blit(
        speed_text,
        (
            math_panel_x + 8,
            math_panel_y + 68
        )
    )


    screen.blit(
        velocity_text,
        (
            math_panel_x + 8,
            math_panel_y + 88
        )
    )


    screen.blit(
        distance_text,
        (
            math_panel_x + 8,
            math_panel_y + 108
        )
    )


    screen.blit(
        dot_text,
        (
            math_panel_x + 8,
            math_panel_y + 128
        )
    )


    # --------------------------------------------------------
    # VECTOR COLOR KEY
    # --------------------------------------------------------

    red_key = small_font.render(
        "RED = Forward Direction",
        True,
        RED
    )


    yellow_key = small_font.render(
        "YELLOW = Velocity",
        True,
        YELLOW
    )


    screen.blit(
        red_key,
        (
            12,
            HEIGHT - 45
        )
    )


    screen.blit(
        yellow_key,
        (
            12,
            HEIGHT - 25
        )
    )


# ============================================================
# CREATE PLAYER, ENEMY, MISSILES
# ============================================================

ship = Spaceship()

enemy = Enemy()


# Player missiles
missiles = []


# ============================================================
# NEW: ENEMY MISSILES
# ============================================================

enemy_missiles = []


# ============================================================
# MAIN GAME LOOP
# ============================================================

running = True


while running:


    # --------------------------------------------------------
    # EVENTS
    # --------------------------------------------------------

    for event in pygame.event.get():


        if event.type == pygame.QUIT:

            running = False


        # ----------------------------------------------------
        # CLICK TO FIRE
        # ----------------------------------------------------

        if event.type == pygame.MOUSEBUTTONDOWN:


            direction = (
                ship.get_forward()
            )


            missile_velocity = (
                direction
                *
                MISSILE_SPEED
            )


            missiles.append(

                Missile(
                    ship.position,
                    missile_velocity
                )

            )


        # ----------------------------------------------------
        # SPACE TO FIRE
        # ----------------------------------------------------

        if event.type == pygame.KEYDOWN:


            if event.key == pygame.K_SPACE:


                direction = (
                    ship.get_forward()
                )


                missile_velocity = (
                    direction
                    *
                    MISSILE_SPEED
                )


                missiles.append(

                    Missile(
                        ship.position,
                        missile_velocity
                    )

                )


    # --------------------------------------------------------
    # KEYBOARD INPUT
    # --------------------------------------------------------

    keys = pygame.key.get_pressed()


    # --------------------------------------------------------
    # UPDATE PLAYER
    # --------------------------------------------------------

    ship.update(
        keys
    )


    # --------------------------------------------------------
    # NEW: UPDATE ENEMY
    # Enemy can now create enemy missiles.
    # --------------------------------------------------------

    enemy.update(
        ship,
        enemy_missiles
    )


    # --------------------------------------------------------
    # UPDATE ASTEROIDS
    # --------------------------------------------------------

    for asteroid in asteroids:

        asteroid.update()


    # --------------------------------------------------------
    # UPDATE PLAYER MISSILES
    # --------------------------------------------------------

    for missile in missiles:

        missile.update()


    # --------------------------------------------------------
    # NEW: UPDATE ENEMY MISSILES
    # --------------------------------------------------------

    for enemy_missile in enemy_missiles:

        enemy_missile.update()


    # --------------------------------------------------------
    # ASTEROID COLLISIONS
    # --------------------------------------------------------

    for i in range(
        len(asteroids)
    ):


        for j in range(
            i + 1,
            len(asteroids)
        ):


            handle_asteroid_collision(
                asteroids[i],
                asteroids[j]
            )


    # --------------------------------------------------------
    # PLAYER MISSILE / ASTEROID COLLISION
    # --------------------------------------------------------

    for missile in missiles[:]:


        for asteroid in asteroids[:]:


            distance = (
                missile.position.distance_to(
                    asteroid.position
                )
            )


            if (
                distance
                <
                missile.radius
                +
                asteroid.radius
            ):


                if missile in missiles:

                    missiles.remove(
                        missile
                    )


                if asteroid in asteroids:

                    asteroids.remove(
                        asteroid
                    )


                break


    # --------------------------------------------------------
    # REMOVE PLAYER MISSILES OUTSIDE SCREEN
    # --------------------------------------------------------

    for missile in missiles[:]:


        if (
            missile.position.x < 0
            or
            missile.position.x > WIDTH
            or
            missile.position.y < 0
            or
            missile.position.y > HEIGHT
        ):


            missiles.remove(
                missile
            )


    # --------------------------------------------------------
    # NEW: REMOVE ENEMY MISSILES OUTSIDE SCREEN
    # --------------------------------------------------------

    for enemy_missile in enemy_missiles[:]:


        if (
            enemy_missile.position.x < 0
            or
            enemy_missile.position.x > WIDTH
            or
            enemy_missile.position.y < 0
            or
            enemy_missile.position.y > HEIGHT
        ):


            enemy_missiles.remove(
                enemy_missile
            )


    # --------------------------------------------------------
    # NEW: ENEMY MISSILE HITS PLAYER
    # --------------------------------------------------------

    for enemy_missile in enemy_missiles[:]:


        distance_to_player = (
            enemy_missile.position.distance_to(
                ship.position
            )
        )


        if (
            distance_to_player
            <
            enemy_missile.radius
            +
            ship.radius
        ):


            # Right now the missile disappears when it hits.
            enemy_missiles.remove(
                enemy_missile
            )


    # --------------------------------------------------------
    # DRAW EVERYTHING
    # --------------------------------------------------------

    draw_background()


    for asteroid in asteroids:

        asteroid.draw()


    # Player missiles
    for missile in missiles:

        missile.draw()


    # Enemy missiles
    for enemy_missile in enemy_missiles:

        enemy_missile.draw()


    ship.draw()


    enemy.draw()


    draw_information(
        ship,
        enemy
    )


    pygame.display.flip()


    clock.tick(
        60
    )


pygame.quit()
