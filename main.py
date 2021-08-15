import pygame
import sys
from random import choice

pygame.init()
SCREENWIDTH, SCREENHEIGHT = 500, 500
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
pygame.display.set_caption("Mouse Escape")
white_color = (255, 255, 255)
black_color = (0, 0, 0)
blue_color = (50, 80, 100)
green_color = (50, 150, 80)
red_color = (180, 40, 50)
grey_color = (150, 150, 150)

number_of_tiles = 7
side_spaces = 2
tiles_width = int(SCREENWIDTH / (number_of_tiles + side_spaces))
tiles_height = tiles_width
seperation_line_width = 1

initial_x = tiles_width
initial_y = initial_x

island_rectangles = []
water_rectangles = []
bridge_rectangle = []
# Create reference index to seperate board rectangles and water rectangles
water_references = []
for y in range(number_of_tiles):
    water_references.append((0, y))
    water_references.append((number_of_tiles - 1, y))
for y in range(1, number_of_tiles - 1):
    water_references.append((y, 0))
    water_references.append((y, number_of_tiles - 1))

# For the frame on  which the game board is
frame_height = int(number_of_tiles * (tiles_width + seperation_line_width) + 2 * seperation_line_width)
frame_width = frame_height
frame = pygame.Surface((frame_height, frame_width))
frame.fill(white_color)
frame_rect = frame.get_rect()
frame_rect.x = tiles_width - 2
frame_rect.y = tiles_width - 2

move_up = False
move_down = False
move_left = False
move_right = False
mouse_died = False

number_of_moves = 0


def handle_events():
    global move_up, move_down, move_right, move_left

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                move_up = True
            if event.key == pygame.K_DOWN:
                move_down = True
            if event.key == pygame.K_LEFT:
                move_left = True
            if event.key == pygame.K_RIGHT:
                move_right = True


def make_rectangles():
    global initial_x, initial_y, tiles_width, tiles_height
    # Use global here because we will need to modify these variables which were already defined
    for x in range(number_of_tiles):
        for y in range(number_of_tiles):
            a_rectangle = pygame.Rect(initial_x, initial_y, tiles_width, tiles_height)
            if (x, y) in water_references:
                if (x, y) == (int(number_of_tiles / 2), number_of_tiles - 1):
                    bridge_rectangle.append(a_rectangle)
                else:
                    water_rectangles.append(a_rectangle)
            else:
                island_rectangles.append(a_rectangle)
            # Move to the next column
            initial_x += tiles_width + seperation_line_width
        # Now reinitialize x position to move down (reinitialize columns)
        initial_x = tiles_width
        # And move to the next row starting at first column
        initial_y += tiles_width + seperation_line_width


def draw_board():
    # Draw the frame , these are the arguments(surface, color, rectangle, width)
    pygame.draw.rect(screen, white_color, frame_rect, 2)

    # Draw all the rectangles on top of that surface
    for rect in island_rectangles:
        pygame.draw.rect(screen, white_color, rect)

    for rect in water_rectangles:
        pygame.draw.rect(screen, blue_color, rect)

    # Display the bridge too
    pygame.draw.rect(screen, green_color, bridge_rectangle[0])


# Call the make_board function to create the board before the game starts
make_rectangles()

allowed_x = [rect.x for rect in island_rectangles]
allowed_y = [rect.y for rect in island_rectangles]

forbidden = [(rect.x, rect.y) for rect in water_rectangles]


def create_mouse_and_cat():
    global mouse_rectangle, cat_rectangle
    cat_x = choice(allowed_x)
    cat_y = choice(allowed_y)

    mouse_x = [x for x in allowed_x if not x == cat_x]
    mouse_y = [y for y in allowed_y if not y == cat_y]
    cat_rectangle = pygame.Rect(cat_x, cat_y, tiles_width, tiles_height)
    mouse_rectangle = pygame.Rect(choice(mouse_x), choice(mouse_y), tiles_width, tiles_height)


create_mouse_and_cat()


def update_mouse():
    global mouse_rectangle, move_up, move_down, move_left, move_right, mouse_died, number_of_moves

    if move_up:
        mouse_rectangle.y -= tiles_width + seperation_line_width
        number_of_moves += 1
        move_up = False
    if move_down:
        mouse_rectangle.y += tiles_width + seperation_line_width
        number_of_moves += 1
        move_down = False
    if move_left:
        mouse_rectangle.x -= tiles_width + seperation_line_width
        number_of_moves += 1
        move_left = False
    if move_right:
        mouse_rectangle.x += tiles_width + seperation_line_width
        number_of_moves += 1
        move_right = False

    if (mouse_rectangle.x, mouse_rectangle.y) in forbidden:
        mouse_died = True

    if mouse_rectangle.x == cat_rectangle.x and mouse_rectangle.y == cat_rectangle.y:
        mouse_died = True

    if number_of_moves == 20:
        mouse_died = True

    if mouse_rectangle.x == bridge_rectangle[0].x and mouse_rectangle.y == bridge_rectangle[0].y:
        win2 = pygame.display.set_mode((500, 500))
        background = pygame.image.load("Congratulations.jpg")
        screen.blit(background, (0, 0))


def draw_mouse_and_cat():
    pygame.draw.rect(screen, grey_color, mouse_rectangle)
    pygame.draw.rect(screen, red_color, cat_rectangle)


while True:
    screen.fill(black_color)
    handle_events()
    draw_board()

    if not mouse_died:
        update_mouse()
    else:
        create_mouse_and_cat()
        number_of_moves = 0
        mouse_died = False
    draw_mouse_and_cat()

    pygame.display.update()


