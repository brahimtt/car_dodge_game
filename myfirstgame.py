# Importing the library
import time
import random
import sys
import pygame
from pygame.locals import *

# Initializing the pygame
pygame.init()

# window
width=800
height=600
screen_size=(width,height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("CAR RACING")

# Loading all images
GRAY = (128,128,128)
YELLOW=(255,255,0)
WHITE=(255,255,255)
RED=(255,0,0)
c1_img = pygame.image.load("images/car.png")
clock = pygame.time.Clock()
left = pygame.image.load("images/left.png")
right = pygame.image.load("images/right.png")




# Function for getting all images
def background():
    screen.blit(left, (0, 0))
    screen.blit(right, (700, 0))
    pygame.draw.line(screen, (255, 255, 0),(400,0),(400,50))
    pygame.draw.line(screen, (255, 255, 0),(400,100),(400,150))
    pygame.draw.line(screen, (255, 255, 0),(400,200),(400,250))
    pygame.draw.line(screen, (255, 255, 0),(400,300),(400,350))
    pygame.draw.line(screen, (255, 255, 0),(400,400),(400,450))
    pygame.draw.line(screen, (255, 255, 0),(400,500),(400,550))
    pygame.draw.line(screen, (255, 255, 0),(400,600),(400,630))
    


# player's starting coordinates
x = 360
y = 470

marker_width = 10
marker_height = 50
#lane cordinates
left_lane = 250
center_lane = 470
right_lane = 670
lanes = [150,left_lane,360, center_lane,550, right_lane]
# road and edge markers
left_edge_marker = (115, 0, marker_width, height)
right_edge_marker = (690, 0, marker_width, height)
# for animating movement of the lane markers
lane_marker_move_y = 0
# game settings
gameover = False
speed = 2
score = 0
class Vehicle(pygame.sprite.Sprite):
    
    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        # scale the image down so it's not wider than the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width* image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))
        
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        
class PlayerVehicle(Vehicle):
    
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)


player_group = pygame.sprite.Group()
vehicle_group = pygame.sprite.Group()
player = PlayerVehicle(x,y)
player_group.add(player)

# load the vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('images/' + image_filename)
    vehicle_images.append(image)
# load the crash image
crash = pygame.image.load('images/crash.png')
crash_rect = crash.get_rect()

running = True
while running:
    clock.tick(120)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            
            if event.key == K_LEFT and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.center[0] < right_lane:
                player.rect.x += 100
            # check if there's a side swipe collision after changing lanes
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    
                    gameover = True
                    # place the player's car next to other vehicle
                    # and determine where to position the crash image
                    if event.key == K_LEFT:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                        print(vehicle.rect.center)
                    elif event.key == K_RIGHT:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center= [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                        print(vehicle.rect.center)
                    


    screen.fill(GRAY)
    background()
    pygame.draw.rect(screen, YELLOW, left_edge_marker)
    pygame.draw.rect(screen, YELLOW, right_edge_marker)
    # draw the lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, WHITE, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, WHITE, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
    # draw the player's car
    player_group.draw(screen)
    if len(vehicle_group) < 2:
        
        # ensure there's enough gap between vehicles
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1:
                add_vehicle = False
                
        if add_vehicle:
            
            # select a random lane
            lane = random.choice(lanes)
            
            # select a random vehicle image
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / -2)
            vehicle_group.add(vehicle)
    # make the vehicles move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        
        # remove vehicle once it goes off screen
        if vehicle.rect.top >= height:
            vehicle.kill()
            
            # add to score
            score += 1
            
            # speed up the game after passing 5 vehicles
            if score > 0 and score % 5 == 0:
                speed += 0.3
    
    # draw the vehicles
    vehicle_group.draw(screen)
    
    # display the score
    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, WHITE)
    text_rect = text.get_rect()
    text_rect.center = (50, 400)
    screen.blit(text, text_rect)
    # check if there's a head on collision
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
    # display game over
    if gameover:
        screen.blit(crash, crash_rect)
            
        pygame.draw.rect(screen, RED, (0, 50, width, 100))
            
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game over. Play again? (Enter Y or N)', True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)
    
        
    

    pygame.display.update()
    # wait for user's input to play again or exit
    while gameover:
        
        clock.tick(120)
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                gameover = False
                running = False
                
            # get the user's input (y or n)
            if event.type == KEYDOWN:
                if event.key == K_y:
                    # reset the game
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    # exit the loops
                    gameover = False
                    running = False

    
pygame.quit()
