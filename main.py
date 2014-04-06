import pygame
from pygame.locals import *
import sys
import math
import time
import random
from random import randint
right = 'right'
left = 'left'


'''
useful links:

http://www.stockfreeimages.com/p1/numbers.html

http://stackoverflow.com/questions/2189800/length-of-an-integer-in-python

http://www.generateit.net/gradient/index.php

http://www.fontspace.com/psyops/crash-numbering

http://www.colorzilla.com/gradient-editor/

http://shinylittlething.com/2009/07/22/pygame-and-animated-sprites-take-2/

http://thepythongamebook.com/en:pygame:step016

https://www.pygame.org/docs/ref/surface.html

https://www.pygame.org/docs/ref/rect.html#pygame.Rect.union

http://dr0id.homepage.bluewin.ch/pygame_tutorial01.html#optimizations

http://www.pygame.org/docs/tut/newbieguide.html

inventwithpython

'''

def num_update(screen, rect_list_to_passed_to_update, number, position, width_of_obj):
    '''
    updates the score counter in the top left-hand corner
    by updating the list of rectangles to pass into pygame.display.update()
    note: updates numbers horizontally i.e [ 2 ] [ 0 ] 
                                           as opposed to  [ 2 ] 
                                                          [ 0 ]

    position must be a list of coords x and y
    where x and y dictate where in the screen you want to put the number
    '''
    r = rect_list_to_passed_to_update
    w = width_of_obj
    p = position
    n = number

    if n == None:
        #display 3 zeros
        s = number_to_picNumber(0)
        for i in range(3):
            r.append(screen.blit(s, (p[0] + w*i, p[1])))
    
    else:
        for i in range(len(str(n))):
            s = number_to_picNumber(int(str(n)[i]))
            r.append(screen.blit(s, (p[0] + w*i, p[1])))
            
    return r

def game_reset():
    cpu_fishes.empty()
    main_fish.empty()

    f = Fish(screen, 'main_fish')
    main_fish.add(f)

    fc = cpu_Fish_Controller(number_of_fishes_to_deploy, cpu_Fish)
    main_bg_off = True

#    screen = pygame.display.set_mode([windowSize[0], windowSize[1] + 50], 0 , 32)
    screen.blit(main_bg, (0,0))
    print('blitted main_bg')
    pygame.display.update()
    #            pygame.time.delay(1000)
    main_bg_off = False

    
    return f

def number_to_picNumber(number):
    '''
    returns the surface image that corresponds to number
    '''
    a = pygame.image.load('fishdish/number' + '_' + str(number) + '.png').convert_alpha()
    a = pygame.transform.smoothscale(a, (30,24))
    return a 

def add_a_new_cpu(screen, available_sprites):
    Stype = random.choice(available_sprites)
    position = get_a_corner(screen)
    new = cpu_Fish(screen, Stype, right, random.uniform(0.1,1.0), position[0], position[1])
    #print(new.get_f_x(), new.get_f_y())
    return new

def get_a_corner(screen):
    edges = ['left','right','top','bottom']
    edge = random.choice(edges)
    print(edge)
    rv = None
    if edge == 'left':
        rv = [0, randint(0,300)]
    elif edge == 'right':
        rv = [400,randint(0,300)]
        #rv = [200,200]
    elif edge == 'top':
        rv = [randint(0,400),0]
    elif edge == 'bottom':
        rv = [randint(0,400), 300]
    return rv

def deg_to_rad(deg):
    rad = (deg/180) * math.pi
    return rad


def squeeze(num, max_num, min_num):
    '''
    squeezes a number between the max_num and the min_num
    useful for bounds checking
    
    >>> squeeze(50, 10, 4)
    10
    >>> squeeze(-20, 10, 4)
    4
    '''
    if num < min_num:
        num = min_num
    if num > max_num:
        num = max_num
    return num


class cpu_Fish_Controller():

    '''
    this will control the deployment of an instance of the cpu fish class

    '''
    
    def __init__(self, number_of_fishes, CpuFishClass):
        self.num = number_of_fishes
        self.actual_num = len(cpu_fishes.sprites())
        #randomly select four... or maybe five fishes to start with
        self.available_sprites = ['yellow_fish' , 'blue_fish', 'small_yellow_fish', 'green_fish', 'grey_fish', 'purple_fish', 'red_fish']
        self.available_sprites_scores = {'yellow_fish':200 , 'blue_fish':150, 'small_yellow_fish':30, 'green_fish':50, 'grey_fish':80, 'purple_fish':100, 'red_fish':10}

        self.y_spots = [windowSize[1]*1//5, windowSize[1]*2//5, windowSize[1]*3//5, windowSize[1]*4//5]


        self.exreme_case_sprites = ['shark'] # ---> note we need to standardize shark
        self.cpu = [] 
        self.Cclass = CpuFishClass

        self.d = [right,left]
        for num in range(self.num):
            #for each instance we randomly generate 
            #all important characteristics of the cpu fish

            i = randint(0, len(self.available_sprites)-1) # select random sprite from available sprites
            sp_name = self.available_sprites[i] #
            sp_direction = self.d[randint(0,1)] #randomly choose direction
            sp_speed = random.random()*10 + 5 # generally between 5 and 15
            sp_score = self.available_sprites_scores[sp_name]


            #create instance of class
#            cpu[num] = cpu_Fish(screen, sp_name, sp_direction, sp_speed)

            '''
            screen is:
            -----------------------------




            -----------------------------
            '''
            self.cpu.append(self.Cclass(screen, sp_name, sp_direction, sp_score, sp_speed, None, self.y_spots[randint(0,len(self.y_spots)-1)]))
            
            #add to cpu fish group
            cpu_fishes.add(self.cpu[num])
            
    def keep_updated(self):
        self.actual_num = len(cpu_fishes.sprites()) #update count

        if self.actual_num < self.num:
            print('adding one')
                #for each instance we randomly generate 
                #all important characteristics of the cpu fish

            i = randint(0, len(self.available_sprites)-1) # select random sprite from available sprites
            sp_name = self.available_sprites[i] #
            sp_direction = self.d[randint(0,1)] #randomly choose direction
            sp_speed = random.random()*10 + 5 # generally between 5 and 15
            sp_score = self.available_sprites_scores[sp_name]
            
                # noting that cpu fishes travelling across the same y coords
                # and going opposite directions, we know we do not need to 
                # monitor the y coords of each instance of this class
                # -- added two layers of randomization to the cpu fish class
                # don't exactly know if that makes it better or not
                
                #create instance of class
                #cpu[num] = cpu_Fish(screen, sp_name, sp_direction, sp_speed)
            self.cpu.append(self.Cclass(screen, sp_name, sp_direction, sp_score, sp_speed, None, self.y_spots[randint(0,len(self.y_spots)-1)]))

                #add to cpu fish group
            cpu_fishes.add(self.cpu[len(self.cpu)-1])
            
    
class cpu_Fish(pygame.sprite.Sprite):
    '''

    this class is somewhat complete in the sense that an instance of this class
    handles moving when given direction, drawing and overlapping with other 
    fishes of the same class and dirtyrect calculation is also functional

    #important: changed all instances of fish_main_rect to rect

    '''
    
    def __init__(self, screen, fish_name, directionTo, fish_score, fish_speed = randint(0,10), x = None, y = 0, fish_width = 0, fish_height = 0):
        #special note to the random generation of the y position
        #as well as the random generation of the fish_speed
        #as it is right now, it should generate a cpu fish at some y position between 100,300

        #initialze important variables
        #screen so we can blit in our class
        #onto the main screen
        self.screen = screen


        
        #we use the same fish naming standards as before
        self.f_n = fish_name
        
        #rate of movement of fish
        self.f_s = fish_speed


        self.fish_direction = directionTo
        
        #starting x and y for fish
        if self.fish_direction == right:
            self.f_x = 0
        elif self.fish_direction == left:
            self.f_x = windowSize[0]

        self.f_y = y + 50


        '''
        self.vector = randint(0,360) #Pick a random direction (in degrees)
        if self.vector >= 90 and self.vector <= 270:
            self.fish_direction = right #everything is backwards (keep in mind)
        else:
            self.fish_direction = left

        '''

        #starting width and height of fish
        self.f_h = fish_height
        self.f_w = fish_width

        
        pygame.sprite.Sprite.__init__(self)


        # load up all frames 
        # start by loading in the five left frames
        # then to get right, we simply flip them 
        a = pygame.image.load('fishdish/' + str(self.f_n) + '_left_1.png').convert_alpha()
        b = pygame.image.load('fishdish/' + str(self.f_n) + '_left_2.png').convert_alpha()                  
        c = pygame.image.load('fishdish/' + str(self.f_n) + '_left_3.png').convert_alpha()
        d = pygame.image.load('fishdish/' + str(self.f_n) + '_left_4.png').convert_alpha()
        e = pygame.image.load('fishdish/' + str(self.f_n) + '_left_5.png').convert_alpha()
        self.lfish_frame = [a,b,c,d,e]

        self.rfish_frame = [pygame.transform.flip(a, True, False),
                            pygame.transform.flip(b, True, False),
                            pygame.transform.flip(c, True, False),
                            pygame.transform.flip(d, True, False),
                            pygame.transform.flip(e, True, False)]

        #set width and height according to img width and height
        self.f_h = a.get_height()
        self.f_w = a.get_width()
        self.radius = self.f_h*0.35 # for the collide_circle method

#        print(self.f_h)
#        print(self.f_w)


        self.fish_frame_num = 0 #initialize fish frame count to zero


        #0-4 - first five frames for right facing fish
        #5-9 - second five frames for left facing fish
        self.fish_main_surf = []

        for frame in self.rfish_frame:
            self.fish_main_surf.append(frame)
        for frame in self.lfish_frame:
            self.fish_main_surf.append(frame)

        self.rect = self.fish_main_surf[0].get_rect()

    def get_f_y(self):
        return self.f_y
    def get_f_x(self):
        return self.f_x

    def update(self):
        #cpu fish direction is either from left to right
        #or right to left
        # 1: from left to right
        # 2: from right to left


        if self.fish_direction == right:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 5:
                self.fish_frame_num = 0 #first right facing frame

        elif self.fish_direction == left:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 9:
                self.fish_frame_num = 5 #first right facing frame



        #clear up old image
        bg2 = pygame.image.load(main_bg_file)
#        print(bg2.get_width())
#        print(bg2.get_height())
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 


        if self.rect.bottomright[0] >= windowSize[0]:
            # for the case when the fish is gone
            # commenting this out will casuse error with dirty rect calculation
            dirtyrect1 = bg2.subsurface((self.rect[0], self.rect[1], windowSize[0] - self.rect[0], self.rect[3]))
            rl.append(self.screen.blit(dirtyrect1, (self.f_x, self.f_y)))


        elif self.rect.left <= 0:
            # for the case when the fish is gone
            # commenting this out will casuse error with dirty rect calculation
            dirtyrect1 = bg2.subsurface((0, self.f_y, self.rect[2], self.rect[3]))
            rl.append(self.screen.blit(dirtyrect1, (0, self.f_y)))

        else:
            #most common case for when the fish is somewhere in the middle
            dirtyrect1 = bg2.subsurface(self.rect) #grabs a piece surface from bg, the same length as fish rect
           #and adds it to the update list rl
            rl.append(self.screen.blit(dirtyrect1, (self.f_x, self.f_y)))
           


        #blit 
        #remember to shift position of fish after calculating the dirtyrect
        d = self.fish_direction

        if d == right:
            self.f_x += self.f_s
        elif d == left:
            self.f_x -= self.f_s


#        print(d)
#        print("the above is the way the fish is going ")
        '''
        Note: we do not need to further complicate the cpu_Fish class
        in the original game, the fishes just come from either the -x direction and goes to the left
        or it comes from the +x direction and goes to the right
        
        what we can vary are the following parameters(not definitive):
        - y coordinate (once chosen, stays constant)
        - speed
        - fish type (I guess...)
        '''
#        self.f_x -= self.f_s * math.cos( (deg_to_rad(self.vector)))
#        self.f_y -= self.f_s * math.sin( (deg_to_rad(self.vector)))

        self.rect.topleft = (self.f_x, self.f_y)

        self.blito()
            

    def blito(self):
        #displays the main_rect fish frame and handles the updating of the frame count
        #at the topleft coordinates of the fish_rect of the instance of the fish

        #frame handling 
        if self.fish_direction == right:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 5:
                self.fish_frame_num = 0 #first right facing frame

        elif self.fish_direction == left:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 9:
                self.fish_frame_num = 5 #first right facing frame

        bg2 = pygame.image.load(main_bg_file)
        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 
        #dirty rect calc to get dimensions of the background the sprite messed up
        # calculate clean rect


        if (self.f_x > windowSize[0] + 50):
            #fish is gawwn dude ...to the right
            if cpu_fishes.has(self):
                #kill the sprite!!!
                cpu_fishes.remove(self)

        if (self.f_x < - 50): 
            #fish is gawwn dude ...to the left
            if cpu_fishes.has(self):
                #kill the sprite!!!
                cpu_fishes.remove(self)

        # this should handle overlapping for cpu fishes amonst each other
        #...
#        for fishes in cpu_fishes.sprites():
#            if (self.fish_main_rect.colliderect(fishes.fish_main_rect)):
        for fishes in pygame.sprite.spritecollide(self, cpu_fishes, False, pygame.sprite.collide_circle):
#                rl.remove(fishes.rect) # remove that #no need to remove !!!
#                rl.remove(self.rect) # no need to remove

            a = self.screen.blit(fishes.fish_main_surf[fishes.fish_frame_num], fishes.rect.topleft)
            b = self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.rect.topleft)
            rl.append(a)
            rl.append(b)



        self.rect = self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.rect.topleft) #update pos of fish
        rl.append(self.rect) # this appends the rectangle that's got the fish on it

#        print("done updating cpu fish")
#        print(self.f_n)


class Fish(pygame.sprite.Sprite):
    
    def __init__(self,screen,  fish_name, fish_speed = 10, x = 200, y = 200, fish_width = 0, fish_height = 0):


        #initialze important variables
        #screen so we can blit in our class
        #onto the main screen
        self.screen = screen
        self.score = 0
        self.fishes_eaten = 0
        self.growscore = 0
        self.alive = True
        self.scoreintervals = [150, 400, 750, 1200, 1750, 2400, 3150, 4000, 4950, 6000, 7150, 8400, 9750, 11200]
        self.scoreintervals.reverse()
        self.currentImage = 1 #controller variable to replace our fish image when a certain size is reached
        
        #we use the same fish naming standards as before
        self.f_n = fish_name
        
        #rate of movement of fish
        self.f_s = fish_speed
        
        #starting x and y for fish
        self.f_x = x
        self.f_y = y + 50

        #starting width and height of fish
        self.f_h = fish_height
        self.f_w = fish_width

        
        pygame.sprite.Sprite.__init__(self)


        # load up all frames 
        # start by loading in the five left frames
        # then to get right, we simply flip them 
        a = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_1.png').convert_alpha()
        b = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_2.png').convert_alpha()                  
        c = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_3.png').convert_alpha()
        d = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_4.png').convert_alpha()
        e = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_5.png').convert_alpha()
        self.lfish_frame = [a,b,c,d,e]

        self.rfish_frame = [pygame.transform.flip(a, True, False),
                            pygame.transform.flip(b, True, False),
                            pygame.transform.flip(c, True, False),
                            pygame.transform.flip(d, True, False),
                            pygame.transform.flip(e, True, False)]

        #set width and height according to img width and height
        self.f_h = a.get_height()
        self.f_w = a.get_width()
        self.radius = self.f_h*0.35 # for the collide_circle method
#        print(self.f_h)
#        print(self.f_w)


        self.fish_frame_num = 0 #initialize fish frame count to zero
        self.fish_direction = right #initialize the direction of the fish to be facing right
        #0-4 - first five frames for right facing fish
        #5-9 - second five frames for left facing fish
        self.fish_main_surf = []

        for frame in self.rfish_frame:
            self.fish_main_surf.append(frame)
        for frame in self.lfish_frame:
            self.fish_main_surf.append(frame)

        self.rect = self.fish_main_surf[0].get_rect()


    def update(self, direction_of_movement = 0):
        # direction == 0 no movement
        # direction == 1 right
        # direction == 2 left
        # direction == 3 up
        # direction == 4 down

        #clear up old image
        bg2 = pygame.image.load(main_bg_file)
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 

        #blit 
        dirtyrect1 = bg2.subsurface(self.rect)
        rl.append(self.screen.blit(dirtyrect1, (self.f_x, self.f_y)))



        d = direction_of_movement
        if d == 1:
            self.f_x += self.f_s
        elif d == 2:
            self.f_x -= self.f_s
        elif d == 3:
            self.f_y -= self.f_s
        elif d == 4:
            self.f_y += self.f_s


        # the bottom would bound the fish to the bounds of the window
#        self.f_x = squeeze(self.f_x, windowSize[0] - self.f_w, self.f_w)

        self.rect.topleft = (self.f_x, self.f_y)

        var = self.rect

        # the bottom four cases handle the fish's 
        # going off the edge and coming out from the opposite sides

        if (var[0] + var[2]) > windowSize[0]:
            self.f_x = (var[0] + var[2]) % windowSize[0]
            #self.f_y = (var[1] + var[3]) % windowSize[1]

            print('it left from the x side')

        '''
        if (var[1] + var[3]) > windowSize[1]:
            #self.f_x = (var[0] + var[2]) % windowSize[0]
            self.f_y = (var[1] + var[3]) % windowSize[1]
            self.rect.topleft = (self.f_x, self.f_y)

            print('it came from above!!!')

        '''
        if (var[0]) < 0:
            self.f_x =  windowSize[0] - var[2]
            #self.f_y = (var[1] + var[3]) % windowSize[1]
            self.rect.topleft = (self.f_x, self.f_y)

            print('it left from the x side')
        '''
        if (var[1]) < 0:
            #self.f_x = (var[0] + var[2]) % windowSize[0]
            self.f_y =  windowSize[1] - var[3]
            self.rect.topleft = (self.f_x, self.f_y)

            print('it came from above!!!')
        '''

        self.f_y = squeeze(self.f_y, windowSize[1], self.f_h)
        self.rect.topleft = (self.f_x, self.f_y)

    
        self.blito()
            

    def blito(self):
        #displays the main_rect fish frame and handles the updating of the frame count
        #at the topleft coordinates of the fish_rect of the instance of the fish

#        bg2 = pygame.image.load(main_bg_file)
#        bg2.fill((255,0,0)) #fills dirty with red to color to show how large rect is 

        #blit 
#        dirtyrect1 = bg2.subsurface(self.rect)
#        self.screen.blit(dirtyrect1, (self.f_x, self_f_y))
        #dirty rect calc to get dimensions of the background the sprite messed up
        # calculate clean rect

#        dirtyrect = bg2.subsurface((abs(self.f_x - self.f_w//2), abs(self.f_y - self.f_h//2), abs(self.f_w*2), abs(self.f_h*2)))  # old


        '''
        print('windowSize' + str(windowSize))

        print('fish x coords' + str(self.f_x))
        print('fish y coords' + str(self.f_y))
        print('fish rect coords' + str(self.rect))
        print('fish rect coords left' + str(self.rect.right))
        print('fish rect coords right' + str(self.rect.left))
        print('bg2.get rect'+str(bg2.get_rect()))

        '''
        #frame handling 
        if self.fish_direction == right:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 5:
                self.fish_frame_num = 0 #first right facing frame

        elif self.fish_direction == left:
            self.fish_frame_num += 1
            if self.fish_frame_num >= 9:
                self.fish_frame_num = 5 #first right facing frame


#        dirtyrect = bg2.subsurface(self.rect)

        # we need to do some editions to the fish rect when calculating the dirty rect around 
        # this is to ensure that no traces of the fish get eft on
        # and then we blit it on before the sprite
#        self.screen.blit(dirtyrect, (self.rect.topleft[0], self.rect.topleft[1]))
        # blit clean rect on top of "dirty" screen

#        for fishes in cpu_fishes.sprites():
#            if (self.rect.colliderect(fishes.rect)):
#                rl.remove(fishes.rect) # remove that #no need to remove !!!
#                rl.remove(self.rect) # no need to remove

        for fishes in pygame.sprite.spritecollide(self, cpu_fishes, False, pygame.sprite.collide_circle):

            cpuA = fishes.rect.width * fishes.rect.height
            mainA = self.rect.width * self.rect.height
                
            if cpuA > mainA:
                self.alive = False
            else:
                self.score += cpuA // 5
                self.fishes_eaten += 1
                if len(self.scoreintervals) > 0:
                    if self.score >= self.scoreintervals[-1]:
                        self.grow()
                        self.scoreintervals.pop()
                    
                cpu_fishes.remove(fishes) #TODO: Need to redraw the background after deleting the fish
                    #cpu_fishes.add(add_a_new_cpu(screen, available_sprites))
                    #self.screen.blit(
                x = fishes.f_x
                y = fishes.f_y
                fishes.screen.blit(main_bg,(x,y),pygame.Rect(x,y,fishes.f_w,fishes.f_h)) #Cover up the old fish with a slice of our background

                #a = self.screen.blit(fishes.fish_main_surf[fishes.fish_frame_num], fishes.rect.topleft)
                #b = self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.rect.topleft)

                #rl.append(a)
                #rl.append(b)
#                print("done magic " + str(self.f_n))

        self.rect = self.screen.blit(self.fish_main_surf[self.fish_frame_num], self.rect.topleft) #update pos of fish
        rl.append(self.rect)# this appends the rectangle that's got the fish on it


    def keys_pressed(self, k):
        #this is to handle all movements
        #when the user is holding a certain key down
        if k[K_RIGHT]:
            f.update(1)
        if k[K_LEFT]:
            f.update(2)
        if k[K_UP]:
            f.update(3)
        if k[K_DOWN]:
            f.update(4)

    def grow(self):
        self.growscore = self.score
        print('need to grow-------------------------------------------')

        #self.lfish_frame = [a,b,c,d,e]
        '''
        lframepos = 0
        self.rfish_frame = []
        for frame in list(self.lfish_frame):
            frame = pygame.transform.smoothscale(frame,(self.f_w,self.f_h))
            self.lfish_frame[lframepos] = frame
            self.rfish_frame.append(pygame.transform.flip(frame, True, False))
            lframepos = lframepos + 1


        self.fish_main_surf = []

        for frame in self.rfish_frame:
            self.fish_main_surf.append(frame)
        for frame in self.lfish_frame:
            self.fish_main_surf.append(frame)
            '''
        self.currentImage += 1
        
        a = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_1.png').convert_alpha()
        b = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_2.png').convert_alpha()                  
        c = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_3.png').convert_alpha()
        d = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_4.png').convert_alpha()
        e = pygame.image.load('fishdish/' + str(self.currentImage)+ str(self.f_n) + '_left_5.png').convert_alpha()
        self.lfish_frame = [a,b,c,d,e]

        self.rfish_frame = [pygame.transform.flip(a, True, False),
                            pygame.transform.flip(b, True, False),
                            pygame.transform.flip(c, True, False),
                            pygame.transform.flip(d, True, False),
                            pygame.transform.flip(e, True, False)]

        #set width and height according to img width and height
        self.f_h = a.get_height()
        self.f_w = a.get_width()
        print(self.currentImage)
        #print(self.f_h)
        #print(self.f_w)
        self.fish_main_surf = []

        for frame in self.rfish_frame:
            self.fish_main_surf.append(frame)
        for frame in self.lfish_frame:
            self.fish_main_surf.append(frame)
        


rl = []

bg_file = 'fishdish/fishtitle.png' # for starting screen background
background = pygame.image.load(bg_file)

bg_file_mouse_over_start = 'fishdish/title_highlight_button.png'
mouse_over_start = pygame.image.load(bg_file_mouse_over_start)


windowSize = [background.get_width(), background.get_height()]

#load up main surface with the height and width of the starting background image
screen = pygame.display.set_mode([windowSize[0], windowSize[1]], 0 , 32)

main_bg_file = 'fishdish/game_bg.png' # for game screen background
main_bg = pygame.image.load(main_bg_file).convert()
game_windowSize = [main_bg.get_width(), main_bg.get_height()]


game_over_image = 'fishdish/gameover.png'
g_o = pygame.image.load(game_over_image).convert()

game_over_image_clicked = 'fishdish/gameover_clicked.png'
g_o2 = pygame.image.load(game_over_image_clicked).convert()

pygame.init()

pygame.display.set_caption("FISH GAME")

#cpu fishes group
cpu_fishes = pygame.sprite.Group()
main_fish = pygame.sprite.Group()
#cpu_fishes = pygame.sprite.RenderUpdates()
#main_fish = pygame.sprite.RenderUpdates()


#initialize f as an instance of the main fish class
f = Fish(screen, 'main_fish')
#f = Fish(screen, 'yellow_fish')

number_of_fishes_to_deploy = 5
fc = cpu_Fish_Controller(number_of_fishes_to_deploy, cpu_Fish)

main_fish.add(f)

start_screen = True
start_screen_no_mouse = True #Controller variable to reload menu screen(erase new button) when mouse is not over it
game = False
            
clock = pygame.time.Clock()


while True:
    if start_screen:
        #display the starting screen background
        if start_screen_no_mouse:
            screen.blit(background,(0,0))
            start_screen_no_mouse = False
        pygame.display.update()
        # Top left : (187,257)
        # Bottom right: (305,293)
        for event in pygame.event.get(): # get events
            Mouse_pos = pygame.mouse.get_pos()
            if 187 <= Mouse_pos[0] <= 257 and 257 <= Mouse_pos[1] <= 305: #If our mouse is on the button display the new button
                screen.blit(mouse_over_start,(186,258))
                if event.type == MOUSEBUTTONDOWN: #check if they are mouse click
                    if event.button == 1: #check if it is a left button click
                        start_screen = False
                        game = True
                        main_bg_off = True
            else: 
                start_screen_no_mouse = True

           

    if game:

        if main_bg_off:
            screen = pygame.display.set_mode([windowSize[0], windowSize[1] + 50], 0 , 32)
            screen.blit(main_bg, (0,0))
            print('blitted main_bg')
            pygame.display.update()
#            pygame.time.delay(1000)
            main_bg_off = False
        f.keys_pressed(pygame.key.get_pressed())
    for event in pygame.event.get():
        
        #main game loop 
        #interesting stuff happens here

        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == K_SPACE):
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == K_RIGHT:
            f.fish_direction = right
            f.update(1)
        if event.type == pygame.KEYDOWN and event.key == K_LEFT:
            f.fish_direction = left
            f.update(2)

        if event.type == pygame.KEYDOWN and event.key == K_UP:
            f.update(3)
        if event.type == pygame.KEYDOWN and event.key == K_DOWN:
            f.update(4)


        if (event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN) and start_screen):
            #pressed enter
            #switch to game mode
            game = True
            start_screen = False
            
            
    clock.tick(15)

    if game:
        #so we only update when we are past the starting screen 
        #otherwise we update for no reason
        fc.keep_updated()
        cpu_fishes.update()
        main_fish.update()
        rl = num_update(screen, rl, f.score, [70, 0], 30) 
        rl = num_update(screen, rl, f.fishes_eaten, [70, 25], 30) 

        if f.alive == False:
            r = (game_windowSize[0]//2 - g_o.get_width()//2, game_windowSize[1]//2 - g_o.get_height()//2)
            screen.blit(g_o, r)
            pygame.display.update()
            while f.alive == False:
                for event in pygame.event.get(): # get events
                    if event.type == MOUSEBUTTONDOWN: #check if they are mouse click
                        if event.button == 1: #check if it is a left button click
                            m = pygame.mouse.get_pos() #get mouse pos everytime there is a click 
                            if (r[0] <= m[0] <= (r[0]+200)) and (r[1] <= m[1] <= (r[1]+120)): #compare x and y separetly **important**
#                                print("we got inside box mouse pos")
                                screen.blit(g_o2, r)
                                pygame.display.update()
                                pygame.time.delay(2000)
                                f = game_reset()
                                print(f.alive)
                                rl = []

        pygame.display.update(rl)    
        rl = []
