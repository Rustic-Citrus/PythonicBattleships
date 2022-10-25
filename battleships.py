from pyexpat.errors import XML_ERROR_UNKNOWN_ENCODING
import pandas as pd
from tabulate import tabulate
import string
import random
import warnings

letters = string.ascii_uppercase

directions = ["left", "right", "up", "down"]

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

def get_occupied_coordinates():

	occupied_coordinates = []

	for m, n in board.items():

		for i, j in n.items():

			if j in [ships["aircraft_carrier"]["symbol"], ships["battleship"]["symbol"], ships["cruiser"]["symbol"], ships["destroyer"]["symbol"], ships["submarine"]["symbol"]]:

				coordinate = m + str(i)
				occupied_coordinates.append(coordinate)

	return occupied_coordinates

def get_forbidden_coordinates():

	# Currently, this function calculates the forbidden coordinates for a aircraft carrier placed in the direction "up" or "down", but not "left" or "right"
	
	forbidden_coordinates = []

	for n in get_occupied_coordinates():
		
		x = int(letters.find(n[0]))
		y = int(n[1:])

		x_protected_area = []
		y_protected_area = []

		x_new = 0
		y_new = 0

		for n in range(5):
			x_new = x + n
			x_protected_area.append(x_new)
		
		for n in range(5):
			y_new = y + n
			y_protected_area.append(y_new)

		for n in range(len(x_protected_area)):
			forbidden_coordinates.append(letters[x_protected_area[n]] + str(y_protected_area[n]))

	return forbidden_coordinates

def get_board():
	
	print("=== BOARD ===")
	df = pd.DataFrame(board)
	print(tabulate(df, headers = "keys", tablefmt = "psql"))

def fire(coord):

	x = board[coord[0]]
	y = int(coord[1:])

	if board[x][y] == "1":

		print("DIRECT HIT!")

	elif board[x][y] == "0":

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

			if (x in ["G", "H", "I", "J"]) and (direction == "right"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x in ["A", "B", "C", "D"]) and (direction == "left"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 6) and (direction == "down"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 5) and (direction == "up"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "left":
					count = letters.find(x)
					for n in range(5):
						board[letters[count]][y] = ships["aircraft_carrier"]["symbol"]
						count -= 1
					ships["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "right":
					count = letters.find(x)
					for n in range(5):
						board[letters[count]][y] = ships["aircraft_carrier"]["symbol"]
						count += 1
					ships["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "up":
					count = y
					for n in range(5):
						board[x][count] = ships["aircraft_carrier"]["symbol"]
						count -= 1
					ships["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "down":
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

			if (x in ["H", "I", "J"]) and (direction == "right"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x in ["A", "B", "C"]) and (direction == "left"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 7) and (direction == "down"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 4) and (direction == "up"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "left":
					count = letters.find(x)
					for n in range(4):
						board[letters[count]][y] = ships["battleship"]["symbol"]
						count -= 1
					ships["battleship"]["on_board"] = True

				elif direction.lower() == "right":
					count = letters.find(x)
					for n in range(4):
						board[letters[count]][y] = ships["battleship"]["symbol"]
						count += 1
					ships["battleship"]["on_board"] = True

				elif direction.lower() == "up":
					count = y
					for n in range(4):
						board[x][count] = ships["battleship"]["symbol"]
						count -= 1
					ships["battleship"]["on_board"] = True

				elif direction.lower() == "down":
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

			if (x in ["I", "J"]) and (direction == "right"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x in ["A", "B"]) and (direction == "left"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 8) and (direction == "down"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 3) and (direction == "up"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "left":
					count = letters.find(x)
					for n in range(3):
						board[letters[count]][y] = ships["cruiser"]["symbol"]
						count -= 1
					ships["cruiser"]["on_board"] = True

				elif direction.lower() == "right":
					count = letters.find(x)
					for n in range(3):
						board[letters[count]][y] = ships["cruiser"]["symbol"]
						count += 1
					ships["cruiser"]["on_board"] = True

				elif direction.lower() == "up":
					count = y
					for n in range(3):
						board[x][count] = ships["cruiser"]["symbol"]
						count -= 1
					ships["cruiser"]["on_board"] = True

				elif direction.lower() == "down":
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

			if (x == "J") and (direction == "right"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x == "A") and (direction == "left"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 9) and (direction == "down"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 2) and (direction == "up"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "left":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "right":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count += 1
					ships["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "up":
					count = y
					for n in range(2):
						board[x][count] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "down":
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

			if (x == "J") and (direction == "right"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (x == "A") and (direction == "left"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y > 9) and (direction == "down"):

				warnings.warn("Invalid coordinates and direction")
				return

			elif (y < 2) and (direction == "up"):

				warnings.warn("Invalid coordinates and direction")
				return

			else:

				if direction.lower() == "left":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "right":
					count = letters.find(x)
					for n in range(2):
						board[letters[count]][y] = ships["destroyer"]["symbol"]
						count += 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "up":
					count = y
					for n in range(2):
						board[x][count] = ships["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "down":
					count = y
					for n in range(2):
						board[x][count] = ships["destroyer"]["symbol"]
						count += 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

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

set_ai_positions()

print(get_forbidden_coordinates())
