import pygame
from  pygame_widgets.textbox import TextBox
import math
from pygame.locals import *

BLACK = (0,0,0)
RED = (255,0,0)
BROWN = (92,64,51)
WHITE = (255,255,255)
GREEN = (0,255,0)
UNOWNED_COLOR = WHITE
HOST_COLOR = (242,207,169)
GUEST_COLOR = (102,72,71) 
PLAYER_NONE = 0
PLAYER_HOST = 1
PLAYER_GUEST = 2
DIALOGBOX = 3
PIECE_CENOTAPH = 1
PIECE_JADE=2
PIECE_JASMINE=3
PIECE_LOTUS=4
PIECE_SKY_BISON=5
PIECE_KOI_FISH=6
PIECE_BADGER_MOLE=7
PIECE_DRAGON=8

ROW_LENGTHS = [4,5,6,7,8,8,8,8,8,8,8,8,8,7,6,5,4]
gamestate = {
    "game_over": False,
    "turn_number": 1,
    "current_player": PLAYER_GUEST,
    "dialogbox_player": PLAYER_NONE,
    "board": [],
    "unused_host_pieces": [],
    "unused_guest_pieces": [],
    "host_lotus_active":False,
    "guest_lotus_active":False
}

class Piece(pygame.sprite.Sprite):
    def __init__(self, image, column, row, type=PIECE_CENOTAPH, owner=PLAYER_NONE):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(image)
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.column = column
        self.row = row
        self.type=type
        self.owner=owner
    def can_influence_position(self, column, row):
        if self.type == PIECE_JASMINE:
            #Jasmine influences up to range 3 unless in correct meadow
            meadow_range_bonus = 0
            if self.column > 0 and self.row < 0 and self.column + abs(self.row) <= 6:
                meadow_range_bonus = 1
            if self.column < 0 and self.row > 0 and abs(self.column) + self.row <= 6:
                meadow_range_bonus = 1
            return (abs(self.column - column)+abs(self.row - row) <= (3+meadow_range_bonus))
        elif self.type == PIECE_JADE:
            #Jade influences range 4-5 unless in correct meadow
            meadow_range_bonus = 0
            if self.column > 0 and self.row > 0 and self.column + self.row <= 6:
                meadow_range_bonus = 1
            if self.column < 0 and self.row < 0 and abs(self.column) + abs(self.row) <= 6:
                meadow_range_bonus = 1
            distance = abs(self.column - column) + abs(self.row - row)
            return (distance >= (4-meadow_range_bonus) ) and ( distance <= 5)
        elif self.type == PIECE_LOTUS:
            #Lotus influences to range 2
            return (abs(self.column - column) + abs(self.row - row) <= 2)
        else:
            return False
    def draw(self, screen):
        if self.owner == PLAYER_HOST:
            color = HOST_COLOR
        elif self.owner == PLAYER_GUEST:
            color = GUEST_COLOR
        else:
            color = UNOWNED_COLOR
        if self.type == PIECE_CENOTAPH:
            pygame.draw.circle(screen, color, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2)
            owner = influence_at_position(self.column, self.row)
            if owner > 0:
                pygame.draw.circle(screen, HOST_COLOR, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2, self.rect.width//10)
            elif owner < 0:
                pygame.draw.circle(screen, GUEST_COLOR, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2, self.rect.width//10)
            else:
                pygame.draw.circle(screen, UNOWNED_COLOR, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2, self.rect.width//10)
        else:
            pygame.draw.circle(screen, color, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2)
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
def influence_at_position(column, row):
    influence = 0
    for other_piece in gamestate['board']:
        if other_piece.can_influence_position(column, row):
            if (other_piece.owner == PLAYER_HOST) and not (other_piece.type == PIECE_LOTUS):
                influence += 1
            elif (other_piece.owner == PLAYER_GUEST) and not (other_piece.type == PIECE_LOTUS):
                influence -= 1
            elif (other_piece.owner == PLAYER_HOST) and (other_piece.type == PIECE_LOTUS):
                influence -= 1
            elif (other_piece.owner == PLAYER_GUEST) and (other_piece.type == PIECE_LOTUS):
                influence += 1
    return influence

def calculate_score():
    host_score = 0
    guest_score = 0
    unclaimed_score = 0
    for piece in gamestate['board']:
        if piece.type == PIECE_CENOTAPH:
            influence=influence_at_position(piece.column, piece.row)    
            if influence > 0:
                host_score += 1
            elif influence < 0:
                guest_score += 1
            else:
                unclaimed_score += 1
    return host_score, guest_score, unclaimed_score

def setup_board():
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,0,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,1,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,2,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,3,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,4,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,5,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,6,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,7,PIECE_JASMINE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jasmine.png",-14,8,PIECE_JASMINE, PLAYER_HOST))

    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,0,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,1,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,2,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,3,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,4,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,5,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,6,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,7,PIECE_JADE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-jade.png",-13,8,PIECE_JADE, PLAYER_HOST))

    gamestate['unused_host_pieces'].append(Piece("white-cenotaph.png",-12,0,PIECE_CENOTAPH, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-cenotaph.png",-12,1,PIECE_CENOTAPH, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-cenotaph.png",-12,2,PIECE_CENOTAPH, PLAYER_HOST))

    gamestate['unused_host_pieces'].append(Piece("white-lotus.png",-12,3,PIECE_LOTUS, PLAYER_HOST))

    gamestate['unused_host_pieces'].append(Piece("white-bison.png",-12,5,PIECE_SKY_BISON, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-badgermole.png",-12,6,PIECE_BADGER_MOLE, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-dragon.png",-12,7,PIECE_DRAGON, PLAYER_HOST))
    gamestate['unused_host_pieces'].append(Piece("white-koi.png",-12,8,PIECE_KOI_FISH, PLAYER_HOST))

    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,0,PIECE_JASMINE, PLAYER_GUEST)) 
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,1,PIECE_JASMINE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,2,PIECE_JASMINE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,3,PIECE_JASMINE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,4,PIECE_JASMINE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,5,PIECE_JASMINE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,6,PIECE_JASMINE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,7,PIECE_JASMINE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jasmine.png",14,8,PIECE_JASMINE, PLAYER_GUEST))

    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,0,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,1,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,2,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,3,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,4,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,5,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,6,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,7,PIECE_JADE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-jade.png",13,8,PIECE_JADE, PLAYER_GUEST))

    gamestate['unused_guest_pieces'].append(Piece("white-cenotaph.png",12,0,PIECE_CENOTAPH, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-cenotaph.png",12,1,PIECE_CENOTAPH, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-cenotaph.png",12,2,PIECE_CENOTAPH, PLAYER_GUEST))

    gamestate['unused_guest_pieces'].append(Piece("white-lotus.png",12,3,PIECE_LOTUS, PLAYER_GUEST))

    gamestate['unused_guest_pieces'].append(Piece("white-bison.png",12,5,PIECE_SKY_BISON, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-badgermole.png",12,6,PIECE_BADGER_MOLE, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-dragon.png",12,7,PIECE_DRAGON, PLAYER_GUEST))
    gamestate['unused_guest_pieces'].append(Piece("white-koi.png",12,8,PIECE_KOI_FISH, PLAYER_GUEST))

    starting_piece = Piece("white-cenotaph.png",0,0, PIECE_CENOTAPH, PLAYER_NONE)
    gamestate['board'].append(starting_piece)

def calculate_dimensions(screen):
    width,height = screen.get_width(),screen.get_height()
    center_x,center_y = width//2,height//2
    line_increment = min(width//30,height//20)
    return center_x,center_y,line_increment

def draw_board(screen, dragged_object=None):
    screen.fill(BLACK)
    center_x,center_y,line_increment = calculate_dimensions(screen)
    edge_width = line_increment

    pygame.draw.circle(screen, BROWN, (center_x, center_y), 19*line_increment//2)
    pygame.draw.polygon(screen, RED, [(center_x, center_y), (center_x, center_y-7*line_increment), (center_x+7*line_increment, center_y)])
    pygame.draw.polygon(screen, RED, [(center_x, center_y), (center_x, center_y+7*line_increment), (center_x-7*line_increment, center_y)])    
    pygame.draw.polygon(screen, WHITE, [(center_x, center_y), (center_x, center_y+7*line_increment), (center_x+7*line_increment, center_y)])
    pygame.draw.polygon(screen, WHITE, [(center_x, center_y), (center_x, center_y-7*line_increment), (center_x-7*line_increment, center_y)])    
    pygame.draw.polygon(screen, RED, [(center_x+7*line_increment, center_y), 
                                      (center_x+10*line_increment, center_y-3*line_increment), 
                                      (center_x+10*line_increment, center_y+3*line_increment)])
     
    pygame.draw.polygon(screen, RED, [(center_x-7*line_increment, center_y), 
                                      (center_x-10*line_increment, center_y-3*line_increment), 
                                      (center_x-10*line_increment, center_y+3*line_increment)])
     
    pygame.draw.polygon(screen, RED, [(center_x, center_y+7*line_increment), 
                                      (center_x-3*line_increment, center_y+10*line_increment), 
                                      (center_x+3*line_increment, center_y+10*line_increment)])
     
    pygame.draw.polygon(screen, RED, [(center_x, center_y-7*line_increment), 
                                      (center_x-3*line_increment, center_y-10*line_increment), 
                                      (center_x+3*line_increment, center_y-10*line_increment)])
    
    pygame.draw.circle(screen, BLACK, (center_x, center_y), 19*line_increment//2+edge_width, edge_width) #Covers up the bits where the triangles clip.

    for i in range(-8, 9):
        pygame.draw.line(screen, BLACK, (center_x + i*line_increment, center_y-ROW_LENGTHS[i+8]*line_increment), (center_x +  i*line_increment, center_y+ROW_LENGTHS[i+8]*line_increment), 3)
        pygame.draw.line(screen, BLACK, (center_x - ROW_LENGTHS[i+8]*line_increment,center_y+ i*line_increment), (center_x +  ROW_LENGTHS[i+8]*line_increment, center_y+i*line_increment), 3)

    if gamestate["current_player"] == PLAYER_HOST:
        pygame.draw.rect(screen,GREEN, (center_x-14*line_increment-line_increment//2,center_y-line_increment//2,line_increment*3, line_increment*9), 3)
    elif gamestate["current_player"] == PLAYER_GUEST:
        pygame.draw.rect(screen, GREEN, (center_x+11*line_increment+line_increment//2,center_y-line_increment//2,line_increment*3, line_increment*9), 3)    
    elif gamestate["current_player"] == DIALOGBOX:
        player = "Host" if gamestate["dialogbox_player"] == PLAYER_HOST else "Guest"
        dialogbox_text = "{0} must select\nwhich region the\ndragon will affect".format(player)
        dialogbox_textbox = TextBox(screen, center_x +10*line_increment-line_increment//2, line_increment//2, line_increment*5, line_increment*8,fontSize=line_increment//2,
                borderColour=(0, 255, 0), textColour=WHITE, colour=BLACK,
                radius=5, borderThickness=2, color=GREEN)
        dialogbox_textbox.setText(dialogbox_text)
        dialogbox_textbox.draw()
        for button_data in [(1,"NE Meadow"), (2,"SE Meadow"), (3,"SW Meadow"), (4,"NW Meadow"), (5,"NE Mountain"), (6,"SE Mountain"), (7,"SW Mountain"), (8,"NW Mountain")]:
            button_offset = button_data[0]
            button_text = button_data[1]
            dialogbox_button = TextBox(screen, center_x +10*line_increment-line_increment//4, (1+button_offset)*line_increment, line_increment*4, line_increment//2,fontSize=line_increment//3,
                    borderColour=(0, 255, 0), textColour=WHITE, colour=BLACK,
                    radius=5, borderThickness=2, color=GREEN)
            dialogbox_button.setText(button_text)
            dialogbox_button.draw()
      
    textbox = TextBox(screen, line_increment//2,line_increment//2, line_increment*5, line_increment*8,fontSize=line_increment//2,
                  borderColour=(255, 0, 0), textColour=WHITE, colour=BLACK,
                  radius=5, borderThickness=2)
    textbox.setText(status_box_text())
    textbox.draw()
    
    for piece in gamestate["board"]:
        piece.rect.x = center_x + piece.column * line_increment - line_increment//2
        piece.rect.y = center_y + piece.row * line_increment -line_increment//2
        piece.rect.width = line_increment
        piece.rect.height = line_increment
        piece.image = pygame.transform.scale(piece.original_image, (line_increment, line_increment))
        piece.draw(screen)
    print("Drawing unused pieces")
    for piece in gamestate["unused_host_pieces"]:
        print(piece)
        if piece != dragged_object:
            piece.rect.x = center_x + piece.column * line_increment - line_increment//2
            piece.rect.y = center_y + piece.row * line_increment -line_increment//2
            piece.rect.width = line_increment
            piece.rect.height = line_increment
            piece.image = pygame.transform.scale(piece.original_image, (line_increment, line_increment))
            piece.draw(screen)            
    for piece in gamestate["unused_guest_pieces"]:
        print(piece)
        if piece != dragged_object:
            piece.rect.x = center_x + piece.column * line_increment - line_increment//2
            piece.rect.y = center_y + piece.row * line_increment -line_increment//2
            piece.rect.width = line_increment
            piece.rect.height = line_increment
            piece.image = pygame.transform.scale(piece.original_image, (line_increment, line_increment))
            piece.draw(screen)
    if dragged_object:
        print("Drawing dragged object")
        dragged_object.draw(screen)
    pygame.display.update()
def status_box_text():

    host_score, guest_score, unclaimed_score = calculate_score()
    if gamestate["game_over"]:
        if host_score > guest_score:
            winner = "Host wins!"
        elif guest_score > host_score:
            winner = "Guest wins!"
        else:
            winner = "It's a tie!"
        return "Game Over!\n{}\nFinal Score:\nHost: {}\nGuest: {}\nUnclaimed: {}".format(winner, host_score, guest_score, unclaimed_score)
    else:
        player_string = "Guest" if gamestate["current_player"] == PLAYER_GUEST else "Host"
        north_temple_influence = influence_at_position(0,-8)
        if north_temple_influence > 0:
            north_temple = "Host"
        elif north_temple_influence < 0:
            north_temple = "Guest"
        else:
            north_temple = "Unclaimed"
        east_temple_influence = influence_at_position(8,0)
        if east_temple_influence > 0:
            east_temple = "Host"
        elif east_temple_influence < 0:
            east_temple = "Guest"
        else:
            east_temple = "Unclaimed"
        south_temple_influence = influence_at_position(0,8)
        if south_temple_influence > 0:
            south_temple = "Host"
        elif south_temple_influence < 0:
            south_temple = "Guest"
        else:
            south_temple = "Unclaimed"
        west_temple_influence = influence_at_position(-8,0)
        if west_temple_influence > 0:
            west_temple = "Host"
        elif west_temple_influence < 0:
            west_temple = "Guest"
        else:
            west_temple = "Unclaimed"
        host_lotus_string = ""
        if gamestate["host_lotus_active"]:
            host_lotus_string = "\n Host Lotus Active, next guest cenotaph played must be near it"
        guest_lotus_string = ""
        if gamestate["guest_lotus_active"]:
            guest_lotus_string = "\n Guest Lotus Active, next host cenotaph played must be near it"
        return "{}'s turn {}\nTemples:\n  North: {}\n  East: {}\n  South: {}\n  West: {}\nScore:\n  Host: {}\n  Guest: {}\n  Unclaimed: {} {} {}".format(player_string, gamestate["turn_number"], north_temple, east_temple, south_temple, west_temple, host_score, guest_score, unclaimed_score, host_lotus_string,guest_lotus_string)

def can_play_piece_at(piece, column, row):
    print("Checking if can play piece at {},{}".format(column, row))
    for other_piece in gamestate["board"]:
        print("Comparing to piece at {},{}".format(other_piece.column, other_piece.row))
        if other_piece.column == column and other_piece.row == row:
            print("Cannot play piece here, occupied")
            return False
    if (row ==8 and column ==0) or (row == -8 and column ==0) or (row ==0 and column ==8) or (row ==0 and column ==-8):
        if piece.type  <= PIECE_LOTUS:
            print("Cannot play piece here, temple restriction")
            return False
    if piece.type == PIECE_CENOTAPH:
        if gamestate["current_player"] == PLAYER_HOST and gamestate["guest_lotus_active"]:
            lotus_found = False
            for other_piece in gamestate["board"]:
                if other_piece.type == PIECE_LOTUS and other_piece.owner == PLAYER_GUEST:
                    distance = abs(other_piece.column - column) + abs(other_piece.row - row)
                    if distance <=2:
                        lotus_found = True
            return lotus_found
        elif gamestate["current_player"] == PLAYER_GUEST and gamestate["host_lotus_active"]:
            lotus_found = False
            for other_piece in gamestate["board"]:
                if other_piece.type == PIECE_LOTUS and other_piece.owner == PLAYER_HOST:
                    distance = abs(other_piece.column - column) + abs(other_piece.row - row)
                    if distance <=2:
                        lotus_found = True
            return lotus_found
    if piece.type == PIECE_DRAGON or piece.type == PIECE_KOI_FISH or piece.type == PIECE_BADGER_MOLE or piece.type == PIECE_SKY_BISON:
        temple_available = location_is_available_temple(column, row, gamestate["current_player"])
        if temple_available == False:
            print("Cannot play piece here, temple availability restriction")
            return False
    print("Can play piece here")
    return True

def grid_position_of_drag(position, screen, piece):
    print ("Finding grid position of drag at {}".format(position))   
    center_x,center_y,line_increment = calculate_dimensions(screen)
    for i in range(-8, 9):
        for j in range(-ROW_LENGTHS[i+8], ROW_LENGTHS[i+8]+1):
            print("Checking if {} is at {}".format((i,j), position))
            testrect = pygame.Rect(center_x + i*line_increment - line_increment//3, center_y + j*line_increment - line_increment//3, 2*line_increment//3, 2*line_increment//3)
            if testrect.collidepoint(position):
                print("Found a valid spot to place the piece")
                if can_play_piece_at(piece, i, j):
                    return True, i, j
                else:
                    return False, 0, 0
    return False, 0, 0

def location_occupied(column, row):
    for other_piece in gamestate["board"]:
        if other_piece.column == column and other_piece.row == row:
            return True
    return False
def location_is_available_temple(column, row, player):
    if not ((row ==8 and column ==0) or (row == -8 and column ==0) or (row ==0 and column ==8) or (row ==0 and column ==-8)):
        return False
    if location_occupied(column, row):
        return False
    if player == PLAYER_HOST and influence_at_position(column, row) > 0:
        return True
    if player == PLAYER_GUEST and influence_at_position(column, row) < 0:
        return True
    return False
    
def available_temple(player):
    for location in [(0,-8),(8,0),(0,8),(-8,0)]:
        if location_is_available_temple(location[0], location[1], player):
            return True
    return False

def check_for_draggable_piece(position, gamestate, pieces):
    remaining_cenotaphs = 0
    for possible_piece in pieces:
        if possible_piece.type == PIECE_CENOTAPH:
            remaining_cenotaphs += 1
    for possible_piece in pieces:
        if remaining_cenotaphs+gamestate["turn_number"] >12 and possible_piece.type != PIECE_CENOTAPH:
            print("Skipping non-cenotaph piece since host must play cenotaphs now")
            continue
        if possible_piece.type == PIECE_DRAGON or possible_piece.type == PIECE_KOI_FISH or possible_piece.type == PIECE_BADGER_MOLE or possible_piece.type == PIECE_SKY_BISON:
            if available_temple(gamestate["current_player"]) == False:
                continue
        print("Checking if {} is at {}".format("object", position))
        if possible_piece.rect.collidepoint(position):
            print("Found a valid piece to drag")
            print(possible_piece.rect)
            print(position)
            return possible_piece
    return None
def play_object(piece, column, row, gamestate):
    piece.column = column
    piece.row = row
    gamestate["board"].append(piece)
    if gamestate["current_player"] == PLAYER_HOST:
        gamestate["unused_host_pieces"].remove(piece)
        gamestate["turn_number"] = gamestate["turn_number"] + 1

        if piece.type == PIECE_DRAGON:
            gamestate["current_player"] = DIALOGBOX
            gamestate["dialogbox_player"] = PLAYER_HOST
        elif gamestate["turn_number"] > 12:
            gamestate["current_player"] = PLAYER_NONE
            gamestate["game_over"] = True
        else:
            gamestate["current_player"] = PLAYER_GUEST
    elif gamestate["current_player"] == PLAYER_GUEST:
        gamestate["unused_guest_pieces"].remove(piece)
        
        if piece.type == PIECE_DRAGON:
            gamestate["current_player"] = DIALOGBOX
            gamestate["dialogbox_player"] = PLAYER_GUEST
        else:
            gamestate["current_player"] = PLAYER_HOST
    if piece.type in [PIECE_BADGER_MOLE, PIECE_DRAGON, PIECE_KOI_FISH, PIECE_SKY_BISON]:
        if piece.owner == PLAYER_HOST:
            for other_piece in gamestate["unused_guest_pieces"]:
                if other_piece.type == piece.type:
                    gamestate["unused_guest_pieces"].remove(other_piece)
                    break
        elif piece.owner == PLAYER_GUEST:
            for other_piece in gamestate["unused_host_pieces"]:
                if other_piece.type == piece.type:
                    gamestate["unused_host_pieces"].remove(other_piece)
                    break

    if piece.type == PIECE_LOTUS:
        if piece.owner == PLAYER_HOST:
            gamestate["host_lotus_active"] = True
        elif piece.owner == PLAYER_GUEST:
            gamestate["guest_lotus_active"] = True
    if piece.type == PIECE_CENOTAPH:
        if piece.owner == PLAYER_HOST:
            gamestate["guest_lotus_active"] = False
        elif piece.owner == PLAYER_GUEST:
            gamestate["host_lotus_active"] = False
def paisho():
    pygame.init()
    screen = pygame.display.set_mode((1600, 1200), pygame.RESIZABLE)
    pygame.display.set_caption('Pai Sho')
    setup_board()
    draw_board(screen)
    dragged_object = None
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
                draw_board(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Mouse-down is start of a drag, but only if it is your turn and is on a valid piece-starting-spot
                print("Mouse down")
                if dragged_object != None:
                    pass
                elif gamestate["current_player"] == PLAYER_HOST:
                    dragged_object = check_for_draggable_piece(event.pos, gamestate, gamestate["unused_host_pieces"])
                elif gamestate["current_player"] == PLAYER_GUEST:                    
                    dragged_object = check_for_draggable_piece(event.pos, gamestate, gamestate["unused_guest_pieces"])
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragged_object != None:
                    #Mouse-up is end of a drag, but only if it is your turn and is on a valid piece-ending-spot and it is a valid move for that piece and you were dragging a piece
                    valid, grid_x, grid_y = grid_position_of_drag(event.pos, screen, dragged_object)
                    if valid:
                        print("Found a valid spot to place the piece")
                        play_object(dragged_object, grid_x, grid_y, gamestate)
  
                    dragged_object = None
                    draw_board(screen, None)

            elif event.type == pygame.MOUSEMOTION:
                if dragged_object != None:
                    print("Mouse motion, moving to {}".format(event.pos))
                    dragged_object.rect.x = event.pos[0]-dragged_object.rect.width//2
                    dragged_object.rect.y = event.pos[1]-dragged_object.rect.height//2
                    draw_board(screen, dragged_object)
                    #Move the dragged object to the current mouse position
                pass
            else:
                print(event)
    pygame.quit()

paisho()