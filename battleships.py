from re import S
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

board_player = board

board_ai = board

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

ships_player = ships

ships_ai = ships

symbols = [ships["aircraft_carrier"]["symbol"], ships["battleship"]["symbol"], ships["cruiser"]["symbol"], ships["destroyer"]["symbol"], ships["submarine"]["symbol"]]

game_initialized = False

game_in_progress = True

def get_occupied_coordinates(player="player"):

	board_dict = board_player

	if player == "ai":

		board_dict = board_ai
	
	occupied_coordinates = []

	for m, n in board_dict.items():

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

def get_board(player="human"):

	if player.lower() == "human":

		print("~~~~~~~~~~ PLAYER'S FLEET ~~~~~~~~~~")
		df = pd.DataFrame(board_player)
		print(tabulate(df, headers = "keys", tablefmt = "psql"))

	elif player.lower() == "ai":

		print("~~~~~~~~~~ ENEMY FLEET ~~~~~~~~~~")
		df = pd.DataFrame(board_ai)
		print(tabulate(df, headers = "keys", tablefmt = "psql"))

def fire(coord, attacker="human"):

	if attacker.lower() == "human":
	
		board_defender = board_ai

	elif attacker.lower() == "ai":

		board_defender = board_player

	x = coord[0]
	y = int(coord[1:])

	if board_defender[x][y] in symbols:

		print("DIRECT HIT!")

	elif board_defender[x][y] == "-":

		print("MISS!")

	try:

		board_defender[x][y] = "X"

	except:

		print("SHOT UNSUCCESSFUL")
		print(f"{coord} is not a valid coordinate")

def set_aircraft_carrier(coord, direction, player="player"):

	if player.lower() == "ai":

		ships_dict = ships_ai
		board_dict = board_ai

	elif player.lower() == "player":
	
		ships_dict = ships_player
		board_dict = board_player
	
	if ships_dict["aircraft_carrier"]["on_board"] == True:

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
						board_dict[letters[count]][y] = ships_dict["aircraft_carrier"]["symbol"]
						count -= 1
					ships_dict["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(5):
						board_dict[letters[count]][y] = ships_dict["aircraft_carrier"]["symbol"]
						count += 1
					ships_dict["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(5):
						board_dict[x][count] = ships_dict["aircraft_carrier"]["symbol"]
						count -= 1
					ships_dict["aircraft_carrier"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(5):
						board_dict[x][count] = ships_dict["aircraft_carrier"]["symbol"]
						count += 1
					ships_dict["aircraft_carrier"]["on_board"] = True

def set_battleship(coord, direction, player="player"):

	if player.lower() == "ai":

		ships_dict = ships_ai
		board_dict = board_ai

	elif player.lower() == "player":
	
		ships_dict = ships_player
		board_dict = board_player
	
	if ships_dict["battleship"]["on_board"] == True:

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
						board_dict[letters[count]][y] = ships_dict["battleship"]["symbol"]
						count -= 1
					ships_dict["battleship"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(4):
						board_dict[letters[count]][y] = ships_dict["battleship"]["symbol"]
						count += 1
					ships_dict["battleship"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(4):
						board_dict[x][count] = ships_dict["battleship"]["symbol"]
						count -= 1
					ships_dict["battleship"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(4):
						board_dict[x][count] = ships_dict["battleship"]["symbol"]
						count += 1
					ships_dict["battleship"]["on_board"] = True

def set_cruiser(coord, direction, player="player"):

	if player.lower() == "ai":

		ships_dict = ships_ai
		board_dict = board_ai

	elif player.lower() == "player":
	
		ships_dict = ships_player
		board_dict = board_player

	if ships_dict["cruiser"]["on_board"] == True:

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
						board_dict[letters[count]][y] = ships_dict["cruiser"]["symbol"]
						count -= 1
					ships_dict["cruiser"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(3):
						board_dict[letters[count]][y] = ships_dict["cruiser"]["symbol"]
						count += 1
					ships_dict["cruiser"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(3):
						board_dict[x][count] = ships_dict["cruiser"]["symbol"]
						count -= 1
					ships_dict["cruiser"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(3):
						board_dict[x][count] = ships_dict["cruiser"]["symbol"]
						count += 1
					ships_dict["cruiser"]["on_board"] = True

def set_destroyer_one(coord, direction, player="player"):

	if player.lower() == "ai":

		ships_dict = ships_ai
		board_dict = board_ai

	elif player.lower() == "player":
	
		ships_dict = ships_player
		board_dict = board_player

	if ships_dict["destroyer"]["destroyer_one"]["on_board"] == True:

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
						board_dict[letters[count]][y] = ships_dict["destroyer"]["symbol"]
						count -= 1
					ships_dict["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(2):
						board_dict[letters[count]][y] = ships_dict["destroyer"]["symbol"]
						count += 1
					ships_dict["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(2):
						board_dict[x][count] = ships_dict["destroyer"]["symbol"]
						count -= 1
					ships_dict["destroyer"]["destroyer_one"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(2):
						board_dict[x][count] = ships_dict["destroyer"]["symbol"]
						count += 1
					ships_dict["destroyer"]["destroyer_one"]["on_board"] = True

def set_destroyer_two(coord, direction, player="player"):

	if player.lower() == "ai":

		ships_dict = ships_ai
		board_dict = board_ai

	elif player.lower() == "player":
	
		ships_dict = ships_player
		board_dict = board_player

	if ships_dict["destroyer"]["destroyer_two"]["on_board"] == True:

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
						board_dict[letters[count]][y] = ships_dict["destroyer"]["symbol"]
						count -= 1
					ships_dict["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "east":
					count = letters.find(x)
					for n in range(2):
						board_dict[letters[count]][y] = ships_dict["destroyer"]["symbol"]
						count += 1
					ships_dict["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "north":
					count = y
					for n in range(2):
						board_dict[x][count] = ships_dict["destroyer"]["symbol"]
						count -= 1
					ships["destroyer"]["destroyer_two"]["on_board"] = True

				elif direction.lower() == "south":
					count = y
					for n in range(2):
						board_dict[x][count] = ships_dict["destroyer"]["symbol"]
						count += 1
					ships_dict["destroyer"]["destroyer_two"]["on_board"] = True

def set_submarine_one(coord, player="player"):

	if player.lower() == "ai":

		ships_dict = ships_ai
		board_dict = board_ai

	elif player.lower() == "player":
	
		ships_dict = ships_player
		board_dict = board_player

	if ships_dict["submarine"]["submarine_one"]["on_board"] == True:

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
			board_dict[letters[count]][y] = ships_dict["submarine"]["symbol"]
			ships_dict["submarine"]["submarine_one"]["on_board"] = True

def set_submarine_two(coord, player="player"):

	if player.lower() == "ai":

		ships_dict = ships_ai
		board_dict = board_ai

	elif player.lower() == "player":
	
		ships_dict = ships_player
		board_dict = board_player

	if ships_dict["submarine"]["submarine_two"]["on_board"] == True:

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
			board_dict[letters[count]][y] = ships_dict["submarine"]["symbol"]
			ships_dict["submarine"]["submarine_two"]["on_board"] = True

def set_ai_positions():

	direction = directions[random.randint(0, 3)]
	row = letters[random.randint(0, 9)]
	column = random.randint(1, 10)
	coord = row + str(column)
	
	while ships_ai["aircraft_carrier"]["on_board"] == False:

		set_aircraft_carrier(coord, direction, "ai")

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		print("SUCCESS #1")

	while ships_ai["battleship"]["on_board"] == False:

		set_battleship(coord, direction, "ai")

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		print("SUCCESS #2")

	while ships_ai["cruiser"]["on_board"] == False:

		set_cruiser(coord, direction, "ai")

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		print("SUCCESS #3")

	while ships_ai["destroyer"]["destroyer_one"]["on_board"] == False:

		set_destroyer_one(coord, direction, "ai")

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships_ai["destroyer"]["destroyer_two"]["on_board"] == False:

		set_destroyer_two(coord, direction, "ai")

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships_ai["submarine"]["submarine_one"]["on_board"] == False:

		set_submarine_one(coord, "ai")

		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships_ai["submarine"]["submarine_two"]["on_board"] == False:

		set_submarine_two(coord, "ai")

		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

def set_player_positions():

	while ships_player["aircraft_carrier"]["on_board"] == False:

		coord_aircraft_carrier = input("Type the coordinates of the stern of your AIRCRAFT CARRIER. ").upper()
		direction_aircraft_carrier = input("Type the direction your AIRCRAFT CARRIER is facing (North, East, South, West). ").lower()

		try:

			set_aircraft_carrier(coord_aircraft_carrier, direction_aircraft_carrier)

		except KeyError:

			warnings.warn("Please input valid coordinates.")

	get_board()

	while ships_player["battleship"]["on_board"] == False:

		coord_battleship = input("Type the coordinates of the stern of your BATTLESHIP. ").upper()
		direction_battleship = input("Type the direction your BATTLESHIP is facing (North, East, South, West). ").lower()

		try:
			
			set_battleship(coord_battleship, direction_battleship)

		except KeyError:

			warnings.warn("Please input valid coordinates.")

	get_board()

	while ships_player["cruiser"]["on_board"] == False:

		coord_cruiser = input("Type the coordinates of the stern of your CRUISER. ").upper()
		direction_cruiser = input("Type the direction your CRUISER is facing (North, East, South, West). ").lower()

		try:

			set_cruiser(coord_cruiser, direction_cruiser)

		except KeyError:

			warnings.warn("Please input valid coordinates.")

	get_board()

	while ships_player["destroyer"]["destroyer_one"]["on_board"] == False:

		coord_destroyer_one = input("Type the coordinates of the stern of your FIRST DESTROYER. ").upper()
		direction_destroyer_one = input("Type the direction your FIRST DESTROYER is facing (North, East, South, West). ").lower()

		try:

			set_destroyer_one(coord_destroyer_one, direction_destroyer_one)

		except KeyError:

			warnings.warn("Please input valid coordinates.")

	get_board()

	while ships_player["destroyer"]["destroyer_two"]["on_board"] == False:

		coord_destroyer_two = input("Type the coordinates of the stern of your SECOND DESTROYER. ").upper()
		direction_destroyer_two = input("Type the direction your SECOND DESTROYER is facing (North, East, South, West). ").lower()

		try:
		
			set_destroyer_two(coord_destroyer_two, direction_destroyer_two)

		except KeyError:

			warnings.warn("Please input valid coordinates.")

	get_board()

	while ships_player["submarine"]["submarine_one"]["on_board"] == False:

		coord_submarine_one = input("Type the coordinates of your FIRST SUBMARINE. ").upper()

		try:
		
			set_submarine_one(coord_submarine_one)

		except KeyError:

			warnings.warn("Please input valid coordinates.")

	get_board()

	while ships_player["submarine"]["submarine_two"]["on_board"] == False:

		coord_submarine_two = input("Type the coordinates of your SECOND SUBMARINE. ").upper()

		try:

			set_submarine_two(coord_submarine_two)

		except KeyError:

			warnings.warn("Please input valid coordinates.")

	get_board()

def coin_toss(choice):

	result = random.randint(0, 1)
	player_starts = False

	if choice.lower() == "tails" and result == 0:

		print("TAILS! Player goes first.")
		player_starts = True

	elif choice.lower() == "tails" and result == 1:

		print("HEADS! Computer goes first.")

	elif choice.lower() == "heads" and result == 0:

		print("TAILS! Computer goes first.")

	elif choice.lower() == "heads" and result == 1:

		print("HEADS! Player goes first.")
		player_starts = True

	return player_starts

while game_initialized == False:

	get_board()
	set_player_positions()
	print("FLEET DEPLOYED. READY FOR COMBAT.")
	set_ai_positions()
	print("AN ENEMY FLEET APPEARS ON THE HORIZON.")
	choice = input("Heads or tails?")
	player_start = coin_toss(choice)
	game_initialized = True

while game_in_progress == True:

	if player_start == True:

		get_board("ai")
		coord = input("What coordinates should we fire upon, Admiral? ")
		fire(coord)

		print("The enemy fleet is returning fire!")
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		fire(coord, "ai")
		get_board()

	elif player_start == False:

		print("The enemy fleet is firing on us, Admiral!")
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		fire(coord, "ai")
		get_board()

		get_board("ai")
		coord = input("What coordinates should we return fire upon? ")
		fire(coord)



