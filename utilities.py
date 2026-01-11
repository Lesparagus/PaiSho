from enums import PieceType, PlayerType
def piece_at_position_can_influence_position(piece_type, piece_column, piece_row, column, row):
    distance = abs(piece_column-column)+abs(piece_row-row)
    if piece_type == PieceType.JASMINE:
        #Jasmine influences up to range 3 unless in correct meadow
        meadow_range_bonus = 0
        if  piece_column > 0 and piece_row < 0 and piece_column + abs(piece_row) <= 6:
            meadow_range_bonus = 1
        if  piece_column < 0 and piece_row > 0 and abs(piece_column) + piece_row <= 6:
            meadow_range_bonus = 1
        return distance <= (3+meadow_range_bonus)
    elif piece_type == PieceType.JADE:
        #Jade influences range exactly 5 unless in correct meadow
        meadow_range_bonus = 0
        if piece_column > 0 and piece_row > 0 and  piece_column + piece_row <= 6:
            meadow_range_bonus = 1
        if  piece_column < 0 and piece_row < 0 and abs( piece_column) + abs(piece_row) <= 6:
            meadow_range_bonus = 1
        return (distance >= (5-meadow_range_bonus) ) and ( distance <= 5)
    elif piece_type == PieceType.LOTUS:
        #Lotus influences to range 2
        return distance <= 2
    else:
        return False
    
def influence_at_position(column, row, board):
    influence = 0
    for other_piece in board:
        if other_piece.can_influence_position(column, row):
            if (other_piece.owner == PlayerType.HOST) and not (other_piece.type == PieceType.LOTUS):
                influence += 1
            elif (other_piece.owner == PlayerType.GUEST) and not (other_piece.type == PieceType.LOTUS):
                influence -= 1
            elif (other_piece.owner == PlayerType.HOST) and (other_piece.type == PieceType.LOTUS):
                influence -= 1
            elif (other_piece.owner == PlayerType.GUEST) and (other_piece.type == PieceType.LOTUS):
                influence += 1
    return influence
