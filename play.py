# -*- coding: utf-8 -*-
# assigning values to X and Y variable 
import pygame
from PIL import Image
import math as math

class game():
    def set_image(X, Y, filename, speed, displ):
        programIcon = pygame.image.load('AGH.png')
        pygame.display.set_icon(programIcon)
        pygame.display.set_caption('tryb manualny') 
        display_surface = pygame.display.set_mode((X, Y), 0,0,0,0)
        image = pygame.image.load(filename)  
        rob_pos = [X - displ, displ]
        game.game(display_surface, image,filename, speed, rob_pos, displ)

    def get_walls(filename):
            im = Image.open(filename, 'r')
            width, height = im.size
            walls = []
            pix_val = list(im.getdata())
            i = 0
            for y in range(height): 
                for x in range(width):
                    if pix_val[i] == (0,0,0):
                        walls.append((x,y,1,1))
                    i+= 1 
            return walls
    
    def get_centre_and_resize(displ):
        im = Image.open('a.png', 'r')
        new_size = (int(displ/2), int(displ/2))
        im1 = im.resize(new_size) 
        im1.save('a.png', "PNG")
        width, height = im1.size

        
        return width, height
    
    def game(display_surface, image, filename, speed, rob_pos, displ):
        done = False
        x, y = rob_pos[0], rob_pos[1]
        clock = pygame.time.Clock()
        walls = game.get_walls(filename)
        width, height = game.get_centre_and_resize(displ)
        img = pygame.image.load('a.png').convert()
        rect_robot = img.get_rect()
        rect_robot.center = (width/2, height/2)
        
        while not done:
            display_surface.fill((255,255,255))
            display_surface.blit(image, (0, 0)) 
            display_surface.blit(img, (x, y)) 
            pressed = pygame.key.get_pressed()
            move_up = True
            move_down = True
            move_left = True
            move_right = True
            if pressed[pygame.K_w] or pressed[pygame.K_UP]:
                for m in walls:
                    player = pygame.Rect(x, y - speed, displ/2, displ/2)
                    if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                        move_up = False
                        break
                if move_up:
                    y -= speed

            if pressed[pygame.K_s] or pressed[pygame.K_DOWN]:
                player = pygame.Rect(x, y + speed, displ/2, displ/2)
                for m in walls:
                    if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                        move_down = False
                        break
                if move_down:
                    y += speed
                    

            if pressed[pygame.K_a] or pressed[pygame.K_LEFT]:
                player = pygame.Rect(x - speed, y, displ/2, displ/2)
                for m in walls:
                    if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                        move_left = False
                        break
                if move_left:
                    x -= speed


            if pressed[pygame.K_d] or pressed[pygame.K_RIGHT]:
                player = pygame.Rect(x + speed, y, displ/2, displ/2)
                for m in walls:
                    if player.colliderect(pygame.Rect(m[0],m[1],m[2],m[3])):
                        move_right = False
                        break
                if move_right:
                    x += speed                 
                
            rect_robot.move_ip(x,y)
            pygame.draw.rect(display_surface, (100, 100, 100), pygame.Rect(x,y,speed/2,speed/2))
            clock.tick(60)
            pygame.display.flip()
            for event in pygame.event.get() : 
                if event.type == pygame.QUIT : 
                    pygame.quit() 
                    done = True 
                    break
#game.set_image(500,500, "LABIRYNT.png", 8,30)
