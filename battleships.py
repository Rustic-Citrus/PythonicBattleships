import pandas as pd
from tabulate import tabulate
import string
import random
import warnings

letters = string.ascii_uppercase

directions = ["west", "east", "north", "south"]

board = {
	"A": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"B": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"C": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"D": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"E": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"F": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"G": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"H": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"I": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"},
	"J": {1: "-", 2: "-", 3: "-", 4: "-", 5: "-", 6: "-", 7: "-", 8: "-", 9: "-", 10: "-"}
}
ships = {
	"aircraft_carrier": {
		"on_board": False,
		"symbol": "A",
		"hits": 0
	},
	"battleship": {
		"on_board": False,
		"symbol": "B",
		"hits": 0
	},
	"cruiser": {
		"on_board": False,
		"symbol": "C",
		"hits": 0
	},
	"destroyer": {
		"destroyer_one": {
			"on_board": False,
			"hits": 0
		},
		"destroyer_two": {
			"on_board": False,
			"hits": 0
		},
		"symbol": "D",
		"count": 0
	},
	"submarine": {
		"submarine_one": {
			"on_board": False,
			"hits": 0
			},
		"submarine_two": {
			"on_board": False,
			"hits": 0
			},
		"symbol": "S",
		"count": 0
	}
}

symbols = [ships["aircraft_carrier"]["symbol"], ships["battleship"]["symbol"], ships["cruiser"]["symbol"], ships["destroyer"]["symbol"], ships["submarine"]["symbol"]]

def set_player_positions():

	while ships["aircraft_carrier"]["on_board"] == False:

		coord_aircraft_carrier = input("Type the coordinates of the stern of your AIRCRAFT CARRIER. ").upper()
		direction_aircraft_carrier = input("Type the direction your AIRCRAFT CARRIER is facing (North, East, South, West). ").lower()
		set_aircraft_carrier(coord_aircraft_carrier, direction_aircraft_carrier)

	while ships["battleship"]["on_board"] == False:

		coord_battleship = input("Type the coordinates of the stern of your BATTLESHIP. ").upper()
		direction_battleship = input("Type the direction your BATTLESHIP is facing (North, East, South, West). ").lower()
		set_battleship(coord_battleship, direction_battleship)

	while ships["cruiser"]["on_board"] == False:

		coord_cruiser = input("Type the coordinates of the stern of your CRUISER. ").upper()
		direction_cruiser = input("Type the direction your CRUISER is facing (North, East, South, West). ").lower()
		set_cruiser(coord_cruiser, direction_cruiser)

	while ships["destroyer"]["destroyer_one"]["on_board"] == False:

		coord_destroyer_one = input("Type the coordinates of the stern of your FIRST DESTROYER. ").upper()
		direction_destroyer_one = input("Type the direction your FIRST DESTROYER is facing (North, East, South, West). ").lower()
		set_destroyer_one(coord_destroyer_one, direction_destroyer_one)

	while ships["destroyer"]["destroyer_two"]["on_board"] == False:

		coord_destroyer_two = input("Type the coordinates of the stern of your SECOND DESTROYER. ").upper()
		direction_destroyer_two = input("Type the direction your SECOND DESTROYER is facing (North, East, South, West). ").lower()
		set_destroyer_two(coord_destroyer_two, direction_destroyer_two)

	while ships["submarine"]["submarine_one"]["on_board"] == False:

		coord_submarine_one = input("Type the coordinates of your FIRST SUBMARINE. ").upper()
		set_submarine_one(coord_submarine_one)

	while ships["submarine"]["submarine_two"]["on_board"] == False:

		coord_submarine_two = input("Type the coordinates of your SECOND SUBMARINE. ").upper()
		set_submarine_two(coord_submarine_two)

def get_occupied_coordinates():

	occupied_coordinates = []

	for m, n in board.items():

		for i, j in n.items():

			if j in symbols:

				coordinate = m + str(i)
				occupied_coordinates.append(coordinate)

	occupied_coordinates = set(occupied_coordinates)

	return occupied_coordinates

def get_forbidden_coordinates_aircraft_carrier():

	# Currently, this function calculates the forbidden coordinates for a aircraft carrier placed in the direction "up" or "south", but not "west" or "east"
	
	forbidden_coordinates = []

	for n in get_occupied_coordinates():
		
		x = int(letters.find(n[0]))
		y = int(n[1:])

		x_protected_area = []
		y_protected_area = []

		x_new = 0
		y_new = 0

		for i in range(5):
			x_new = x + i
			x_protected_area.append(x_new)
		
		for i in range(5):
			y_new = y + i
			y_protected_area.append(y_new)
		
		for i in range(0, -5, -1):
			y_new = y - i
			y_protected_area.append(y_new)

		for i in range(len(x_protected_area)):
			forbidden_coordinates.append(letters[x_protected_area[i]] + str(y_protected_area[i]))
			forbidden_coordinates.append(letters[x] + str(y_protected_area[i]))
			
	forbidden_coordinates = set(forbidden_coordinates)

	return forbidden_coordinates

def get_board():
	
	print("=== BOARD ===")
	df = pd.DataFrame(board)
	print(tabulate(df, headers = "keys", tablefmt = "psql"))

def fire(coord):

	x = board[coord[0]]
	y = int(coord[1:])

	if board[x][y] in symbols:

		print("DIRECT HIT!")

	elif board[x][y] == "-":

		print("MISS!")

	try:

		board[x][y] = "X"

	except:

		print("SHOT UNSUCCESSFUL")
		print(f"{coord} is not a valid coordinate")

	get_board()

def set_aircraft_carrier(coord, direction):

	if ships["aircraft_carrier"]["on_board"] == True:

		warnings.warn("Invalid coordinate-direction combo")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1])

			except:

				warnings.warn("Invalid coordinate format")

		if coord in get_occupied_coordinates():

			warnings.warn("Coordinates already occupied")
			return

		if direction.lower() in directions:

			if (x in ["G", "H", "I", "J"]) and (direction == "east"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x in ["A", "B", "C", "D"]) and (direction == "west"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 6) and (direction == "south"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 5) and (direction == "north"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "west":
					count = letters.find(x)
					for n in range(5):
						board[letters[count]][y] = ships["aircraft_carrier"]["symbol"]
						count -= 1
					ships["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(5):
						board[letters[count]][y] = ships["aircraft_carrier"]["symbol"]
						count += 1
					ships["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(5):
						board[x][count] = ships["aircraft_carrier"]["symbol"]
						count -= 1
					ships["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(5):
						board[x][count] = ships["aircraft_carrier"]["symbol"]
						count += 1
					ships["aircraft_carrier"]["on_board"] = True

	get_board()

def set_battleship(coord, direction):

	if ships["battleship"]["on_board"] == True:

		warnings.warn("Invalid coordinate-direction combo")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1])

			except:

				warnings.warn("Invalid coordinate format")

		if coord in get_occupied_coordinates():

			warnings.warn("Coordinates already occupied")
			return

		if direction.lower() in directions:

			if (x in ["H", "I", "J"]) and (direction == "east"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x in ["A", "B", "C"]) and (direction == "west"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 7) and (direction == "south"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 4) and (direction == "north"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "west":
					count = letters.find(x)
					for n in range(4):
						board[letters[count]][y] = ships["battleship"]["symbol"]
						count -= 1
					ships["battleship"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(4):
						board[letters[count]][y] = ships["battleship"]["symbol"]
						count += 1
					ships["battleship"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(4):
						board[x][count] = ships["battleship"]["symbol"]
						count -= 1
					ships["battleship"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(4):
						board[x][count] = ships["battleship"]["symbol"]
						count += 1
					ships["battleship"]["on_board"] = True

	get_board()

def set_cruiser(coord, direction):

	if ships["cruiser"]["on_board"] == True:

		warnings.warn("Invalid coordinate-direction combo")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1])

			except:

				warnings.warn("Invalid coordinate format")

		if coord in get_occupied_coordinates():

			warnings.warn("Coordinates already occupied")
			return

		if direction.lower() in directions:

			if (x in ["I", "J"]) and (direction == "east"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x in ["A", "B"]) and (direction == "west"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 8) and (direction == "south"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 3) and (direction == "north"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "west":
					count = letters.find(x)
					for n in range(3):
						board[letters[count]][y] = ships["cruiser"]["symbol"]
						count -= 1
					ships["cruiser"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(3):
						board[letters[count]][y] = ships["cruiser"]["symbol"]
						count += 1
					ships["cruiser"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(3):
						board[x][count] = ships["cruiser"]["symbol"]
						count -= 1
					ships["cruiser"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(3):
						board[x][count] = ships["cruiser"]["symbol"]
						count += 1
					ships["cruiser"]["on_board"] = True

	get_board()

def set_destroyer_one(coord, direction):

	if ships["destroyer"]["destroyer_one"]["on_board"] == True:

		warnings.warn("Invalid coordinate-direction combo")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1])

			except:

				warnings.warn("Invalid coordinate format")

		if coord in get_occupied_coordinates():

			warnings.warn("Coordinates already occupied")
			return

		if direction.lower() in directions:

			if (x == "J") and (direction == "east"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x == "A") and (direction == "west"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 9) and (direction == "south"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 2) and (direction == "north"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "west":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count += 1
					ships["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(2):
						board[x][count] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(2):
						board[x][count] = ships["destroyer"]["symbol"]
						count += 1
					ships["destroyer"]["destroyer_one"]["on_board"] = True

	get_board()

def set_destroyer_two(coord, direction):

	if ships["destroyer"]["destroyer_two"]["on_board"] == True:

		warnings.warn("Invalid coordinate-direction combo")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1])

			except:

				warnings.warn("Invalid coordinate format")

		if coord in get_occupied_coordinates():

			warnings.warn("Coordinates already occupied")
			return

		if direction.lower() in directions:

			if (x == "J") and (direction == "east"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x == "A") and (direction == "west"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 9) and (direction == "south"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 2) and (direction == "north"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "west":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count += 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(2):
						board[x][count] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(2):
						board[x][count] = ships["destroyer"]["symbol"]
						count += 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

	get_board()

def set_submarine_one(coord):

	if ships["submarine"]["submarine_one"]["on_board"] == True:

		warnings.warn("Invalid coordinate-direction combo")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1])

			except:

				warnings.warn("Invalid coordinate format")

		if coord in get_occupied_coordinates():

			warnings.warn("Coordinates already occupied")
			return

		else:

			count = letters.find(x)
			board[letters[count]][y] = ships["submarine"]["symbol"]
			ships["submarine"]["submarine_one"]["on_board"] = True

	get_board()

def set_submarine_two(coord):

	if ships["submarine"]["submarine_two"]["on_board"] == True:

		warnings.warn("Invalid coordinate-direction combo")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1])

			except:

				warnings.warn("Invalid coordinate format")

		if coord in get_occupied_coordinates():

			warnings.warn("Coordinates already occupied")
			return

		else:

			count = letters.find(x)
			board[letters[count]][y] = ships["submarine"]["symbol"]
			ships["submarine"]["submarine_two"]["on_board"] = True

	get_board()

def set_ai_positions():

	direction = directions[random.randint(0, 3)]
	row = letters[random.randint(0, 9)]
	column = random.randint(1, 10)
	coord = row + str(column)
	
	while ships["aircraft_carrier"]["on_board"] == False:

		set_aircraft_carrier(coord, direction)

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships["battleship"]["on_board"] == False:

		set_battleship(coord, direction)

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships["cruiser"]["on_board"] == False:

		set_cruiser(coord, direction)

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships["destroyer"]["destroyer_one"]["on_board"] == False:

		set_destroyer_one(coord, direction)

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships["destroyer"]["destroyer_two"]["on_board"] == False:

		set_destroyer_two(coord, direction)

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships["submarine"]["submarine_one"]["on_board"] == False:

		set_submarine_one(coord)

		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships["submarine"]["submarine_two"]["on_board"] == False:

		set_submarine_two(coord)

		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

set_player_positions()
