from pygame.sprite import Sprite
import pygame

from enums import PieceType, PlayerType, Color
from utilities import influence_at_position, piece_at_position_can_influence_position

class Piece(Sprite):

    def set_type(self,type: PieceType):
        self.type=type
        image=None
        if type==PieceType.CENOTAPH:
            image="white-cenotaph.png"            
        elif type==PieceType.JADE:
            image="white-jade.png"
        elif type==PieceType.JASMINE:
            image="white-jasmine.png"
        elif type==PieceType.LOTUS:
            image="white-lotus.png"
        elif type==PieceType.SKY_BISON:
            image="white-bison.png"
        elif type==PieceType.KOI_FISH:
            image="white-koi.png"     
        elif type==PieceType.BADGER_MOLE:
            image="white-badgermole.png"
        elif type==PieceType.DRAGON:
            image="white-dragon.png"

        self.original_image = pygame.image.load(image)
        self.image = self.original_image

    def __init__(self, column: int, row: int, type: PieceType = PieceType.CENOTAPH, owner:PlayerType =PlayerType.NONE):
        Sprite.__init__(self)        
        self.set_type(type)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.column = column
        self.row = row
        self.owner=owner

    def is_flower(self):
        return self.type == PieceType.LOTUS or self.type==PieceType.JADE or self.type==PieceType.JASMINE
    
    def is_element(self):
        return self.type==PieceType.BADGER_MOLE or self.type==PieceType.DRAGON or self.type==PieceType.KOI_FISH or self.type==PieceType.SKY_BISON
    
    def can_influence_position(self, column: int, row: int):
        return piece_at_position_can_influence_position(self.type, self.column, self.row, column, row)

    def draw(self, screen, board):
        if self.owner == PlayerType.HOST:
            color = Color.HOST_COLOR
        elif self.owner == PlayerType.GUEST:
            color = Color.GUEST_COLOR
        else:
            color = Color.UNOWNED_COLOR
        if self.type == PieceType.CENOTAPH:
            pygame.draw.circle(screen, color.value, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2)
            owner = influence_at_position(self.column, self.row, board)
            if owner > 0:
                pygame.draw.circle(screen, Color.HOST_COLOR.value, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2, self.rect.width//10)
            elif owner < 0:
                pygame.draw.circle(screen, Color.GUEST_COLOR.value, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2, self.rect.width//10)
            else:
                pygame.draw.circle(screen, Color.UNOWNED_COLOR.value, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2, self.rect.width//10)
        else:
            pygame.draw.circle(screen, color.value, (self.rect.x + self.rect.width//2, self.rect.y + self.rect.height//2), self.rect.width//2)
        screen.blit(self.image, (self.rect.x, self.rect.y))
