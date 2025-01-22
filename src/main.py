from tablero import Tablero
from square import Square
from pieza import Pieza
from peon import Peon
from guerrero import Guerrero

# Entry point of the program

tableroprincipal = Tablero(2)
peon = Peon('Blanco')

tableroprincipal.place_piece(peon,0,0)

print(tableroprincipal)

peon.move(0,1)

print(tableroprincipal)