from enum import Enum

class PieceType(Enum):
    CENOTAPH = 1
    JADE=2
    JASMINE=3
    LOTUS=4
    SKY_BISON=5
    KOI_FISH=6
    BADGER_MOLE=7
    DRAGON=8
    
#Whose turn is it
class PlayerType(Enum):
    NONE = 0
    HOST = 1
    GUEST = 2
    DIALOGBOX = 3

class Color(Enum):
    BLACK = (0,0,0)
    RED = (255,0,0)
    BROWN = (92,64,51)
    WHITE = (255,255,255)
    GREEN = (0,255,0)
    MAGENTA = (255, 0, 255)
    UNOWNED_COLOR = WHITE
    HOST_COLOR = (242,207,169)
    GUEST_COLOR = (102,72,71) 