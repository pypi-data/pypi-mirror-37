import pygame
from panzerspiel import vector
from panzerspiel.box import (box, box_template)
from panzerspiel.line import (line, rect_to_lines)
from panzerspiel.event_definitions import TANK_HIT_EVENT


def line_line_collision(l1, l2):
    """
    This function returns the collisionpoint of l1 and l2 as a vector.
    If there is no collision None is returned
    """
    r_nom = l2.v.y * (l2.o.x - l1.o.x) + l2.v.x * (l1.o.y - l2.o.y)
    s_nom = l1.v.y * (l2.o.x - l1.o.x) + l1.v.x * (l1.o.y - l2.o.y)
    denom = l1.v.x * l2.v.y - l1.v.y * l2.v.x
    # If denom is 0 r and s are infinity and there is no collision
    if denom == 0:
        return None
    # r will be used to calculate the collision point
    r = r_nom / denom
    # s will be used to check if the collision happend inside the boundaries
    # of the lines
    s = s_nom / denom
    # Only if r and s are element of [0, 1] the collision happend
    # inside the borders of the line
    if r >= 0 and s >= 0 and r <= 1 and s <= 1:
        return vector.add(l1.o, vector.mul(l1.v, r))
    return None


def rect_rect_collision(rect1, rect2):
    """
    This function returns all collision points between to rectangles.
    If there is no collision an empty list is returned
    """
    rect1_lines = rect_to_lines(rect1)
    rect2_lines = rect_to_lines(rect2)
    collision_points = []
    for l1 in rect1_lines:
        for l2 in rect2_lines:
            collision_point = line_line_collision(l1, l2)
            if collision_point is not None:
                collision_points.append(collision_point)
    return collision_points


def ray_rect_collision(line1, rect):
    """
    This function returnes the first collision point of line1 with rect
    as a vector. If there is no collision None is returned
    """
    rect_lines = rect_to_lines(rect)
    collision_points = []
    for rect_line in rect_lines:
        collision_point = line_line_collision(line1, rect_line)
        if collision_point is not None:
            collision_points.append(collision_point)
    # If there are no collision points return None
    if len(collision_points) == 0:
        return None
    # To return only the "first" collision point all collision points
    # have to be sorted with the distance from the ray origin as the key
    collision_points.sort(key=lambda x: vector.abs(vector.sub(x, line1.o)))
    # Now the first element in the list can be returned
    # as this ist the collision point nearest to the ray origin
    return collision_points[0]


def handle_tank_arena_collision(tank, arena):
    """
    This function handles the collision of a tank with the arena.
    The used algorithm is very simple, the tanks velocity is substracted
    from the position. And the tanks velocity is set to zero.
    This way the tank is set to its previous position.
    The same code is used in handle_tank_tank_collision.
    If you want to add collision damage you could do it here.
    """
    for obj in arena:
        if tank.rect.colliderect(obj.rect):
            tank.position = vector.sub(tank.position, tank.velocity)
            tank.speed = 0


def handle_tank_tank_collision(tank, tanks):
    """
    This function handles the collision of a tank with the arena.
    The used algorithm is very simple, the tanks velocity is substracted
    from the position. And the tanks velocity is set to zero.
    This way the tank is set to its previous position.
    The same code is used in handle_tank_arena_collision.
    If you want to add collision damage you could do it here.
    """
    for t in tanks:
        if tank.rect.colliderect(t) and tank is not t:
            tank.position = vector.sub(tank.position, tank.velocity)
            tank.speed = 0


def handle_tank_shot(tank, environment):
    """
    This function handles the tank_shot event.
    To archieve this a ray is casted along the viewing direction of the tank.
    Every object hit by this ray is stored in a list and ordered by the
    distance to the tank. This way the first element of the list is the
    hit element. Its "decrease_health" function is invoked and
    a TANK_HIT_EVENT, with the collision point as an argument, is thrown.
    As the "decrease_health" function is invoked every object in the
    environment list has to have a "decrease_health" function.
    """
    collision_points_and_hit_objects = []
    ray = line(tank.position.as_int_tupel(),
            vector.polar(tank.angle, 2048).as_int_tupel())
    for obj in environment:
        if obj is tank:
            continue
        collision_point = ray_rect_collision(ray, obj.rect)
        if collision_point:
            collision_points_and_hit_objects.append((collision_point, obj))
    # Now the hit_objects list has to be sorted with the distance to tank
    # as key. This way the first element in the list is the first element
    # which is hit by the ray and should loos health
    if len(collision_points_and_hit_objects) == 0:
        return
    collision_points_and_hit_objects.sort(key=lambda x:
            vector.abs(vector.sub(x[0], tank.position)))
    collision_points_and_hit_objects[0][1].decrease_health(tank.dps)
    # Now a tank_hit_event is thrown which is catched by the animator
    # to draw an explosion
    event = pygame.event.Event(TANK_HIT_EVENT,
            collision_point=collision_points_and_hit_objects[0][0])
    pygame.event.post(event)


if __name__ == "__main__":
    """
    This testprogramme allows the user to move one box with the
    mouse while one other box remains static.
    On leftclick the collision of both boxes is checked and all
    collision points are displayed as red dots
    On rightclick the collision is checked of the static box with
    an invisible ray from (0, 0) to the position of the mouse.
    Again the collision point is displayed as a red dot
    """
    pygame.init()
    screen = pygame.display.set_mode((512, 512))
    running = True

    box_template = box_template(pygame.image.load("res/box1.png"), 100)
    # This box will be moved with the mouse
    box1 = box(pygame.Rect(0, 0, 25, 25), box_template)
    # This box will be static
    box2 = box(pygame.Rect(200, 200, 25, 25), box_template)
    collision_points = []

    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False

        # Get user input
        mouse_keys = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        pressed_keys = pygame.key.get_pressed()
        # Update box1
        box1.position(mouse_pos)

        if mouse_keys[0]:
            collision_points = rect_rect_collision(box1.rect, box2.rect)
        if mouse_keys[2]:
            ray = line((0, 0), mouse_pos)
            collision_points = ray_rect_collision(ray, box2.rect)
            if collision_points is None:
                collision_points = []
            else:
                collision_points = [collision_points]

        # Clear the screen
        screen.fill((0, 0, 0))
        # Render the game
        box2.draw(screen)
        box1.draw(screen)
        for cp in collision_points:
            pygame.draw.circle(screen, (255, 0, 0), cp.as_int_tupel(), 5, 5)

        # Flip the scene
        pygame.display.flip()
