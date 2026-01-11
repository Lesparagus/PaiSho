import pygame
from  pygame_widgets.textbox import TextBox
import math
from pygame.locals import *

from enums import PlayerType, PieceType
from piece import Piece
from utilities import influence_at_position, piece_at_position_can_influence_position

BLACK = (0,0,0)
RED = (255,0,0)
BROWN = (92,64,51)
WHITE = (255,255,255)
GREEN = (0,255,0)
MAGENTA = (255, 0, 255)
UNOWNED_COLOR = WHITE
HOST_COLOR = (242,207,169)
GUEST_COLOR = (102,72,71) 




#Dialogbox types when the dialogbox is on turn
DIALOGBOX_DRAGON = 1
DIALOGBOX_KOI = 2

ROW_LENGTHS = [4,5,6,7,8,8,8,8,8,8,8,8,8,7,6,5,4]

gamestate = {
    "game_over": False,
    "turn_number": 1,
    "current_player": PlayerType.GUEST,
    "dialogbox_player": PlayerType.NONE,
    "dialogbox_type": None,
    "board": [],
    "unused_host_pieces": [],
    "unused_guest_pieces": [],
    "host_lotus_active":False,
    "guest_lotus_active":False
}

def calculate_score():
    host_score = 0
    guest_score = 0
    unclaimed_score = 0
    for piece in gamestate['board']:
        if piece.type == PieceType.CENOTAPH:
            influence=influence_at_position(piece.column, piece.row, gamestate["board"])    
            if influence > 0:
                host_score += 1
            elif influence < 0:
                guest_score += 1
            else:
                unclaimed_score += 1
    return host_score, guest_score, unclaimed_score

def setup_board():
    gamestate['unused_host_pieces'].append(Piece(-14,0,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,1,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,2,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,3,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,4,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,5,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,6,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,7,PieceType.JASMINE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-14,8,PieceType.JASMINE, PlayerType.HOST))

    gamestate['unused_host_pieces'].append(Piece(-13,0,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,1,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,2,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,3,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,4,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,5,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,6,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,7,PieceType.JADE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-13,8,PieceType.JADE, PlayerType.HOST))

    gamestate['unused_host_pieces'].append(Piece(-12,0,PieceType.CENOTAPH, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-12,1,PieceType.CENOTAPH, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-12,2,PieceType.CENOTAPH, PlayerType.HOST))

    gamestate['unused_host_pieces'].append(Piece(-12,3,PieceType.LOTUS, PlayerType.HOST))

    gamestate['unused_host_pieces'].append(Piece(-12,5,PieceType.SKY_BISON, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-12,6,PieceType.BADGER_MOLE, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-12,7,PieceType.DRAGON, PlayerType.HOST))
    gamestate['unused_host_pieces'].append(Piece(-12,8,PieceType.KOI_FISH, PlayerType.HOST))

    gamestate['unused_guest_pieces'].append(Piece(14,0,PieceType.JASMINE, PlayerType.GUEST)) 
    gamestate['unused_guest_pieces'].append(Piece(14,1,PieceType.JASMINE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(14,2,PieceType.JASMINE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(14,3,PieceType.JASMINE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(14,4,PieceType.JASMINE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(14,5,PieceType.JASMINE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(14,6,PieceType.JASMINE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(14,7,PieceType.JASMINE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(14,8,PieceType.JASMINE, PlayerType.GUEST))

    gamestate['unused_guest_pieces'].append(Piece(13,0,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,1,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,2,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,3,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,4,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,5,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,6,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,7,PieceType.JADE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(13,8,PieceType.JADE, PlayerType.GUEST))

    gamestate['unused_guest_pieces'].append(Piece(12,0,PieceType.CENOTAPH, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(12,1,PieceType.CENOTAPH, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(12,2,PieceType.CENOTAPH, PlayerType.GUEST))

    gamestate['unused_guest_pieces'].append(Piece(12,3,PieceType.LOTUS, PlayerType.GUEST))

    gamestate['unused_guest_pieces'].append(Piece(12,5,PieceType.SKY_BISON, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(12,6,PieceType.BADGER_MOLE, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(12,7,PieceType.DRAGON, PlayerType.GUEST))
    gamestate['unused_guest_pieces'].append(Piece(12,8,PieceType.KOI_FISH, PlayerType.GUEST))

    starting_piece = Piece(0,0, PieceType.CENOTAPH, PlayerType.NONE)
    gamestate['board'].append(starting_piece)

def calculate_dimensions(screen):
    width,height = screen.get_width(),screen.get_height()
    center_x,center_y = width//2,height//2
    line_increment = min(width//30,height//20)
    return center_x,center_y,line_increment

def draw_board(screen, dragged_object=None, dragged_object_position=None):
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

    if gamestate["current_player"] == PlayerType.HOST:
        pygame.draw.rect(screen,GREEN, (center_x-14*line_increment-line_increment//2,center_y-line_increment//2,line_increment*3, line_increment*9), 3)
    elif gamestate["current_player"] == PlayerType.GUEST:
        pygame.draw.rect(screen, GREEN, (center_x+11*line_increment+line_increment//2,center_y-line_increment//2,line_increment*3, line_increment*9), 3)    
    elif gamestate["current_player"] == PlayerType.DIALOGBOX:
        player = "Host" if gamestate["dialogbox_player"] == PlayerType.HOST else "Guest"
        piece_used = "dragon" if gamestate["dialogbox_type"] == DIALOGBOX_DRAGON else "koi"
        dialogbox_text = "{0} must select\nwhich region the\n{1} will affect".format(player,piece_used)
        dialogbox_textbox = TextBox(screen, center_x +10*line_increment-line_increment//2, line_increment//2, line_increment*5, line_increment*9,fontSize=line_increment//2,
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
        piece.draw(screen, gamestate["board"])
    #print("Drawing unused pieces")
    for piece in gamestate["unused_host_pieces"]:
        #print(piece)
        if piece != dragged_object:
            piece.rect.x = center_x + piece.column * line_increment - line_increment//2
            piece.rect.y = center_y + piece.row * line_increment -line_increment//2
            piece.rect.width = line_increment
            piece.rect.height = line_increment
            piece.image = pygame.transform.scale(piece.original_image, (line_increment, line_increment))
            piece.draw(screen, gamestate["board"])            
    for piece in gamestate["unused_guest_pieces"]:
        #print(piece)
        if piece != dragged_object:
            piece.rect.x = center_x + piece.column * line_increment - line_increment//2
            piece.rect.y = center_y + piece.row * line_increment -line_increment//2
            piece.rect.width = line_increment
            piece.rect.height = line_increment
            piece.image = pygame.transform.scale(piece.original_image, (line_increment, line_increment))
            piece.draw(screen, gamestate["board"])
    if dragged_object:
        print("Drawing dragged object with dragged oject ")
        valid, column, row = grid_position_of_drag(dragged_object_position, screen, dragged_object)
        print("drawing hallowed locations for dragged object {} {} {} ".format(valid, column, row))
        if valid:
            draw_hallowed_locations(screen, dragged_object, column, row)
            
        draw_blocked_locations(screen, dragged_object)
        dragged_object.draw(screen, gamestate["board"])
    pygame.display.update()

def draw_hallow_location_mark(screen, column, row):
    center_x,center_y,line_increment = calculate_dimensions(screen)    
    pygame.draw.circle(screen, GREEN, (center_x+column*line_increment, center_y+row*line_increment), line_increment//7)

def draw_blocked_location_mark(screen, column, row):
    center_x,center_y,line_increment = calculate_dimensions(screen)    
    pygame.draw.circle(screen, MAGENTA, (center_x+column*line_increment, center_y+row*line_increment), line_increment//10)
def draw_hallowed_locations(screen, dragged_object, column, row):
    if not(dragged_object.type == PieceType.JADE or dragged_object.type==PieceType.JASMINE or dragged_object.type== PieceType.LOTUS):
        print ("Abort, not a flower!")
        return
    for c in range(-8,9):
        for r in range(-ROW_LENGTHS[c +8], ROW_LENGTHS[c+8]+1):
            print("Checking influence at {} {}".format(c,r))
            if piece_at_position_can_influence_position(dragged_object.type,column,row,c,r):
                print("Piece can influence {} {}".format(c,r))
                draw_hallow_location_mark(screen, c, r)

def draw_blocked_locations(screen,dragged_object):
    for row in range(-8,9):
        for column in range(-ROW_LENGTHS[row+8], ROW_LENGTHS[row+8]+1):
            if not can_play_piece_at(dragged_object,column,row):
                draw_blocked_location_mark(screen, column, row)
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
        player_string = "Guest" if gamestate["current_player"] == PlayerType.GUEST else "Host"
        north_temple_influence = influence_at_position(0,-8, gamestate["board"])
        if north_temple_influence > 0:
            north_temple = "Host"
        elif north_temple_influence < 0:
            north_temple = "Guest"
        else:
            north_temple = "Unclaimed"
        east_temple_influence = influence_at_position(8,0, gamestate["board"])
        if east_temple_influence > 0:
            east_temple = "Host"
        elif east_temple_influence < 0:
            east_temple = "Guest"
        else:
            east_temple = "Unclaimed"
        south_temple_influence = influence_at_position(0,8, gamestate["board"])
        if south_temple_influence > 0:
            south_temple = "Host"
        elif south_temple_influence < 0:
            south_temple = "Guest"
        else:
            south_temple = "Unclaimed"
        west_temple_influence = influence_at_position(-8,0, gamestate["board"])
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
    #Check whether there's a tile at this spot already
    for other_piece in gamestate["board"]:
        #print("Comparing to piece at {},{}".format(other_piece.column, other_piece.row))
        if other_piece.column == column and other_piece.row == row:
            print("Cannot play piece here, occupied")
            return False
    #Check whether this is a temple here
    if (row ==8 and column ==0) or (row == -8 and column ==0) or (row ==0 and column ==8) or (row ==0 and column ==-8):
        if not piece.is_element():
            #print("Cannot play piece here, temple restriction")
            return False
    #If opponent has a badgermole within range, you can't place a flower down here
    if piece.type == PieceType.JADE or piece.type == PieceType.JASMINE or piece.type == PieceType.LOTUS:
        #print ("Trying to place a flower")
        for possible_mole in gamestate["board"]:
            #print("Checking for moles")
            if possible_mole.type == PieceType.BADGER_MOLE:
                #print("found mole")
                if possible_mole.owner != piece.owner:
                    #print("Mole has different owner")
                    distance = abs(row-possible_mole.row)+abs(column-possible_mole.column)                    
                    #print("Distance is {}".format(distance))
                    if  distance <= 5:
                        return False
    if piece.type == PieceType.CENOTAPH:
        for possible_cenotaph in gamestate["board"]:
            #print("Checking for other cenotaphs")            
            if possible_cenotaph.type == PieceType.CENOTAPH:
                distance = abs(row-possible_cenotaph.row)+abs(column-possible_cenotaph.column)                    
                #print("Distance is {}".format(distance))
                if  distance <= 5:
                    return False
        if gamestate["current_player"] == PlayerType.HOST and gamestate["guest_lotus_active"]:
            lotus_found = False
            for other_piece in gamestate["board"]:
                if other_piece.type == PieceType.LOTUS and other_piece.owner == PlayerType.GUEST:
                    distance = abs(other_piece.column - column) + abs(other_piece.row - row)
                    if distance <=2:
                        lotus_found = True
            return lotus_found
        elif gamestate["current_player"] == PlayerType.GUEST and gamestate["host_lotus_active"]:
            lotus_found = False
            for other_piece in gamestate["board"]:
                if other_piece.type == PieceType.LOTUS and other_piece.owner == PlayerType.HOST:
                    distance = abs(other_piece.column - column) + abs(other_piece.row - row)
                    if distance <=2:
                        lotus_found = True
            return lotus_found
    if piece.is_element():
        temple_available = location_is_available_temple(column, row, gamestate["current_player"])
        if temple_available == False:
            #print("Cannot play piece here, temple availability restriction")
            return False
    #print("Can play piece here")
    return True

def grid_position_of_drag(position, screen, piece):
    print ("Finding grid position of drag at {}".format(position))   
    center_x,center_y,line_increment = calculate_dimensions(screen)
    for column in range(-8, 9):
        for row in range(-ROW_LENGTHS[column+8], ROW_LENGTHS[column+8]+1):
            #print("Checking if {} is at {}".format((column,row), position))
            testrect = pygame.Rect(center_x + column*line_increment - line_increment//3, center_y + row*line_increment - line_increment//3, 2*line_increment//3, 2*line_increment//3)
            if testrect.collidepoint(position):
                #print("Found a valid spot to place the piece")
                if can_play_piece_at(piece, column, row):
                    return True, column, row
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
    if player == PlayerType.HOST and influence_at_position(column, row, gamestate["board"]) > 0:
        return True
    if player == PlayerType.GUEST and influence_at_position(column, row, gamestate["board"]) < 0:
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
        if possible_piece.type == PieceType.CENOTAPH:
            remaining_cenotaphs += 1
    for possible_piece in pieces:
        if remaining_cenotaphs+gamestate["turn_number"] >12 and possible_piece.type != PieceType.CENOTAPH:
            #print("Skipping non-cenotaph piece since host must play cenotaphs now")
            continue
        if possible_piece.type == PieceType.DRAGON or possible_piece.type == PieceType.KOI_FISH or possible_piece.type == PieceType.BADGER_MOLE or possible_piece.type == PieceType.SKY_BISON:
            if available_temple(gamestate["current_player"]) == False:
                continue
        #print("Checking if {} is at {}".format("object", position))
        if possible_piece.rect.collidepoint(position):
            #print("Found a valid piece to drag")
            #print(possible_piece.rect)
            #print(position)
            return possible_piece
    return None
def play_object(piece, column, row, gamestate):
    piece.column = column
    piece.row = row
    gamestate["board"].append(piece)
    if gamestate["current_player"] == PlayerType.HOST:
        gamestate["unused_host_pieces"].remove(piece)
        gamestate["turn_number"] = gamestate["turn_number"] + 1

        if piece.type == PieceType.DRAGON:
            gamestate["current_player"] = PlayerType.DIALOGBOX
            gamestate["dialogbox_type"] = DIALOGBOX_DRAGON
            gamestate["dialogbox_player"] = PlayerType.HOST
        elif piece.type == PieceType.KOI_FISH:
            gamestate["current_player"] = PlayerType.DIALOGBOX
            gamestate["dialogbox_type"] = DIALOGBOX_KOI
            gamestate["dialogbox_player"] = PlayerType.HOST
        elif gamestate["turn_number"] > 12:
            gamestate["current_player"] = PlayerType.NONE
            gamestate["game_over"] = True
        else:
            gamestate["current_player"] = PlayerType.GUEST
    elif gamestate["current_player"] == PlayerType.GUEST:
        gamestate["unused_guest_pieces"].remove(piece)
        
        if piece.type == PieceType.DRAGON:
            gamestate["current_player"] = PlayerType.DIALOGBOX            
            gamestate["dialogbox_type"] = DIALOGBOX_DRAGON
            gamestate["dialogbox_player"] = PlayerType.GUEST
        elif piece.type == PieceType.KOI_FISH:
            gamestate["current_player"] = PlayerType.DIALOGBOX
            gamestate["dialogbox_type"] = DIALOGBOX_KOI
            gamestate["dialogbox_player"] = PlayerType.GUEST
        else:
            gamestate["current_player"] = PlayerType.HOST
    if piece.type in [PieceType.BADGER_MOLE, PieceType.DRAGON, PieceType.KOI_FISH, PieceType.SKY_BISON]:
        if piece.owner == PlayerType.HOST:
            for other_piece in gamestate["unused_guest_pieces"]:
                if other_piece.type == piece.type:
                    gamestate["unused_guest_pieces"].remove(other_piece)
                    break
        elif piece.owner == PlayerType.GUEST:
            for other_piece in gamestate["unused_host_pieces"]:
                if other_piece.type == piece.type:
                    gamestate["unused_host_pieces"].remove(other_piece)
                    break

    if piece.type == PieceType.LOTUS:
        if piece.owner == PlayerType.HOST:
            gamestate["host_lotus_active"] = True
        elif piece.owner == PlayerType.GUEST:
            gamestate["guest_lotus_active"] = True
    if piece.type == PieceType.CENOTAPH:
        if piece.owner == PlayerType.HOST:
            gamestate["guest_lotus_active"] = False
        elif piece.owner == PlayerType.GUEST:
            gamestate["host_lotus_active"] = False
def process_koi_dialogbox_button_press(location, screen):
    
    center_x,center_y,line_increment = calculate_dimensions(screen)
    button = 0
    for button_offset in range(1,9):

        testrect = pygame.Rect( center_x +10*line_increment-line_increment//4, (1+button_offset)*line_increment, line_increment*4, line_increment//2)
        #print("Colliding button with rect {} to position {}".format(testrect, location))
        if testrect.collidepoint(location):
            button=button_offset
            break
    #print("Button pressed is {}".format(button))
    pieces_to_change = []
    if button==0:
        return
    elif button==1:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row < 0 and piece.column >0 and abs(piece.row)+piece.column<=6:
                    pieces_to_change.append(piece)
    elif button==2:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row > 0 and piece.column >0 and piece.row+piece.column<=6:
                    pieces_to_change.append(piece)
    elif button==3:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row > 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)<=6:
                    pieces_to_change.append(piece)
    elif button==4:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row < 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)<=6:
                    pieces_to_change.append(piece)
    elif button==5:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row < 0 and piece.column >0 and abs(piece.row)+piece.column>=8) and not (piece.row==-1 and piece.column==8) and not (piece.row==-8 and piece.column==1):
                    pieces_to_change.append(piece)
    elif button==6:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row > 0 and piece.column >0 and piece.row+piece.column>=8) and not (piece.row==1 and piece.column==8) and not (piece.row==8 and piece.column==1):
                    pieces_to_change.append(piece)
    elif button==7:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row > 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)>=8) and not (piece.row==1 and piece.column==-8) and not (piece.row==8 and piece.column==-1):
                    pieces_to_change.append(piece)
    elif button==8:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row < 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)>=8) and not (piece.row==-1 and piece.column==-8) and not (piece.row==-8 and piece.column==-1):
                    pieces_to_change.append(piece)
    #print("Pieces to remove is: {}".format(pieces_to_change))
    for piece in pieces_to_change:
        if piece.type== PieceType.JADE:
            piece.set_type(PieceType.JASMINE)
        else:
            piece.set_type(PieceType.JADE)

    if gamestate["dialogbox_player"]==PlayerType.GUEST:
        #print("Setting current player to host")
        gamestate["current_player"]=PlayerType.HOST
    else:        
        if gamestate["turn_number"] > 12:
            gamestate["current_player"] = PlayerType.NONE
            gamestate["game_over"] = True
        else:            
            #print("Setting current player to guest")
            gamestate["current_player"]=PlayerType.GUEST

def process_dragon_dialogbox_button_press(location, screen):
    
    center_x,center_y,line_increment = calculate_dimensions(screen)
    button = 0
    for button_offset in range(1,9):

        testrect = pygame.Rect( center_x +10*line_increment-line_increment//4, (1+button_offset)*line_increment, line_increment*4, line_increment//2)
        #print("Colliding button with rect {} to position {}".format(testrect, location))
        if testrect.collidepoint(location):
            button=button_offset
            break
    #print("Button pressed is {}".format(button))
    pieces_to_remove = []
    if button==0:
        return
    elif button==1:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row < 0 and piece.column >0 and abs(piece.row)+piece.column<=6:
                    pieces_to_remove.append(piece)
    elif button==2:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row > 0 and piece.column >0 and piece.row+piece.column<=6:
                    pieces_to_remove.append(piece)
    elif button==3:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row > 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)<=6:
                    pieces_to_remove.append(piece)
    elif button==4:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if piece.row < 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)<=6:
                    pieces_to_remove.append(piece)
    elif button==5:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row < 0 and piece.column >0 and abs(piece.row)+piece.column>=8) and not (piece.row==-1 and piece.column==8) and not (piece.row==-8 and piece.column==1):
                    pieces_to_remove.append(piece)
    elif button==6:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row > 0 and piece.column >0 and piece.row+piece.column>=8) and not (piece.row==1 and piece.column==8) and not (piece.row==8 and piece.column==1):
                    pieces_to_remove.append(piece)
    elif button==7:    
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row > 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)>=8) and not (piece.row==1 and piece.column==-8) and not (piece.row==8 and piece.column==-1):
                    pieces_to_remove.append(piece)
    elif button==8:
        for piece in gamestate["board"]:
            if piece.type == PieceType.JADE or piece.type== PieceType.JASMINE:
                if (piece.row < 0 and piece.column < 0 and abs(piece.row)+abs(piece.column)>=8) and not (piece.row==-1 and piece.column==-8) and not (piece.row==-8 and piece.column==-1):
                    pieces_to_remove.append(piece)
    for piece in pieces_to_remove:
        gamestate["board"].remove(piece)

    if gamestate["dialogbox_player"]==PlayerType.GUEST:
        gamestate["current_player"]=PlayerType.HOST
    else:        
        if gamestate["turn_number"] > 12:
            gamestate["current_player"] = PlayerType.NONE
            gamestate["game_over"] = True
        else:            
            gamestate["current_player"]=PlayerType.GUEST
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
                if dragged_object != None:
                    pass
                elif gamestate["current_player"] == PlayerType.HOST:
                    dragged_object = check_for_draggable_piece(event.pos, gamestate, gamestate["unused_host_pieces"])
                elif gamestate["current_player"] == PlayerType.GUEST:                    
                    dragged_object = check_for_draggable_piece(event.pos, gamestate, gamestate["unused_guest_pieces"])
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                if gamestate["current_player"] == PlayerType.DIALOGBOX and gamestate["dialogbox_type"] == DIALOGBOX_DRAGON:
                    process_dragon_dialogbox_button_press(event.pos, screen)                    
                    draw_board(screen, None)
                elif gamestate["current_player"] == PlayerType.DIALOGBOX and gamestate["dialogbox_type"] == DIALOGBOX_KOI:
                    process_koi_dialogbox_button_press(event.pos, screen)                    
                    draw_board(screen, None)
                elif dragged_object != None:
                    #Mouse-up is end of a drag, but only if it is your turn and is on a valid piece-ending-spot and it is a valid move for that piece and you were dragging a piece
                    valid, grid_x, grid_y = grid_position_of_drag(event.pos, screen, dragged_object)
                    if valid:
                        play_object(dragged_object, grid_x, grid_y, gamestate)
  
                    dragged_object = None
                    draw_board(screen, None)

            elif event.type == pygame.MOUSEMOTION:
                if dragged_object != None:
                    dragged_object.rect.x = event.pos[0]-dragged_object.rect.width//2
                    dragged_object.rect.y = event.pos[1]-dragged_object.rect.height//2
                    draw_board(screen, dragged_object, event.pos)
                    #Move the dragged object to the current mouse position
                pass
            else:
                print(event)
    pygame.quit()

paisho()