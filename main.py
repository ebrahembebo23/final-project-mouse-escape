import pygame
import sys

pygame.init()
SCREENWIDTH, SCREENHEIGHT = 500, 500
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
pygame.display.set_caption("Mouse Escape")
white_color = (255, 255, 255)
black_color = (0, 0, 0)
blue_color = (50, 80, 100)
green_color = (50, 150, 80)

number_of_tiles = 7
side_spaces = 2
tiles_width = int(SCREENWIDTH / (number_of_tiles + side_spaces))
tiles_height = int(tiles_width)

initial_x = int(tiles_width)
initial_y = int(tiles_width)
small_separation_line = 1

board_rectangles = []
water_rectangles = []
bridge_rectangle = []
# Create reference index to separate board rectangles with water rectangles
water_references = [
    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
    (1, 0), (1, 6), (2, 0), (2, 6), (3, 0), (3, 6), (4, 0),
    (4, 6), (5, 0), (5, 6),
    (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6)
]

# For the frame one which the game board is
frame_height = int(SCREENWIDTH - 2 * tiles_width + 5)
frame_width = frame_height
frame = pygame.Surface((frame_height, frame_width))
frame.fill(white_color)
frame_rect = frame.get_rect()
frame_rect.x = tiles_width - 2
frame_rect.y = tiles_width - 2


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Complete yourself for the mouse movement and collisions


def make_board_rectangles():
    global initial_x, initial_y, tiles_width, tiles_height
    # Use global here because we will need to modify these variables which were already defined
    for x in range(7):
        for y in range(7):
            a_rectangle = pygame.Rect(initial_x, initial_y, tiles_width, tiles_height)
            if (x, y) in water_references:
                water_rectangles.append(a_rectangle)
            if (x, y) == (3, 6):
                bridge_rectangle.append(a_rectangle)
            else:
                board_rectangles.append(a_rectangle)
            # Move to the next column
            initial_x += tiles_width + small_separation_line
        # Now reinitialize x position to move down (reinitialize columns)
        initial_x = tiles_width
        # And move to the next row starting at first column
        initial_y += tiles_width + small_separation_line


def draw_board():
    # Draw the frame , these are the arguments(surface, color, rectangle, width)
    pygame.draw.rect(screen, white_color, frame_rect, 2)

    # Draw all the rectangles on top of that surface
    for rect in board_rectangles:
        pygame.draw.rect(screen, white_color, rect)

    for rect in water_rectangles:
        pygame.draw.rect(screen, blue_color, rect)

    # Display the bridge too
    pygame.draw.rect(screen, green_color, bridge_rectangle[0])


def create_mouse():
    # Leaving this empty for yourself
    pass


# Call the make_board function to create the board before the game starts
make_board_rectangles()

while True:
    screen.fill(black_color)
    handle_events()
    draw_board()
    pygame.display.update()
