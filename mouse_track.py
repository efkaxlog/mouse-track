import pyHook
import pythoncom
import pygame
import time

def win_cords(pos):
    x, y = pos
    new_x = int(width * x / 1920)
    new_y = int(height * y / 1080)
    return (new_x, new_y)

def normalised_cords(pos):
    x, y, = pos
    new_x = x / 1920
    new_y = y / 1080
    new_x = "{0:.3f}".format(new_x)
    new_y = "{0:.3f}".format(new_y)
    return (new_x, new_y)

    
def on_click(event, button):
    global paused
    if not paused:
        if button == "left":
            colour = BLUE
        else:
            colour = RED
        global clicks
        x, y = win_cords(event.Position)    
        pygame.draw.circle(screen, RED, [x, y], 2, 1)
        clicks.append(normalised_cords(event.Position))-
    return True

def on_left_click(event):
    on_click(event, "left")
    return True

def on_right_click(event):
    on_click(event, "right")
    return True

def on_scroll_click(even):
    global paused
    paused = not paused
    return True

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
width, height = 960, 540
background_colour = WHITE
screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.flip()
pygame.display.set_caption("Mouse track")
running = True
paused = False # For pausing/resuming recording of mouse clicks
clicks = []

hm = pyHook.HookManager()
hm.SubscribeMouseMiddleDown(on_scroll_click)
hm.SubscribeMouseLeftDown(on_left_click)
hm.SubscribeMouseRightDown(on_right_click)
hm.HookMouse()

start = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()

pygame.quit()

hm.UnhookMouse()
print("Unhooked")

total_time = int(time.time() - start)
print(total_time)

if input("save?\n") == "y":
    filename = input("filename: ") + ".txt"
    file = open(filename, "w+")
    file.write(str(total_time) + "\n")
    for cords in clicks:
        file.write(str(cords[0]) + " " + str(cords[1]) + "\n")

    file.close()
    
