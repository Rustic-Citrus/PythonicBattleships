import pandas as pd
from tabulate import tabulate
import string
import random
import warnings
import pyglet
from pydub import AudioSegment
from pydub.playback import play
import pathlib

letters = string.ascii_uppercase

directions = ["west", "east", "north", "south"]

board_blank = {
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

board_player = {
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

board_ai = {
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

ships_player = {
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

ships_ai = {
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

symbols = [ships_player["aircraft_carrier"]["symbol"], ships_player["battleship"]["symbol"], ships_player["cruiser"]["symbol"], ships_player["destroyer"]["symbol"], ships_player["submarine"]["symbol"]]

game_initialized = False

game_in_progress = True

turn_counter = 1

# Tracking coordinates that were already hit

coord_hit_ai = []

coord_hit_player = []

# Keeping scores

player_score = 0

ai_score = 0

# Condition of ai fleet

aircraft_carrier_sunk_ai = False

battleship_sunk_ai = False

cruiser_sunk_ai = False

destroyers_sunk_ai = False

submarines_sunk_ai = False

# Condition of player fleet

aircraft_carrier_sunk_player = False

battleship_sunk_player = False

cruiser_sunk_player = False

destroyers_sunk_player = False

submarines_sunk_player = False

def play_explosion():

	pathname = str(pathlib.Path(__file__).parent.resolve())
	filename = "\\\\explosion.mp3"

	song = AudioSegment.from_file(pathname + filename)

	play(song)

def play_splash():

	pathname = str(pathlib.Path(__file__).parent.resolve())
	filename = "\\\\big_water_splash.wav"

	song = AudioSegment.from_file(pathname + filename)

	play(song)

def play_victory_song():

	pathname = str(pathlib.Path(__file__).parent.resolve())
	filename = "\\\\victory_fanfare.wav"

	song = AudioSegment.from_file(pathname + filename)

	play(song)

def play_defeat_song():

	pathname = str(pathlib.Path(__file__).parent.resolve())
	filename = "\\\\epic_heroic_orchestral_dramatic.mp3"

	song = AudioSegment.from_file(pathname + filename)

	play(song)

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
		df = pd.DataFrame(board_blank)
		print(tabulate(df, headers = "keys", tablefmt = "psql"))

def fire(coord, attacker="human"):

	x = coord[0]
	y = int(coord[1:])

	if attacker.lower() == "human":
	
		board_defender = board_ai

		# if coord in coord_hit_player:

		# 	print("MISFIRE!")
		# 	return "misfire"

	elif attacker.lower() == "ai":

		board_defender = board_player

		# if coord in coord_hit_ai:

		# 	print("MISFIRE!")
		# 	return "misfire"

	if board_defender[x][y] in symbols:

		print("DIRECT HIT!")
		play_explosion()

		if attacker.lower() == "human":
	
			try:

				board_defender[x][y] = "!"
				board_blank[x][y] = "!"
				coord_hit_player.append(coord)

			except:

				print("SHOT UNSUCCESSFUL")
				print(f"{coord} is not a valid coordinate")

		elif attacker.lower() == "ai":

			try:

				board_defender[x][y] = "!"
				coord_hit_ai.append(coord)

			except:

				print("SHOT UNSUCCESSFUL")
				print(f"{coord} is not a valid coordinate")

	elif board_defender[x][y] == "-":

		print("MISS!")
		play_splash()

		if attacker == "human":

			try:

				board_blank[x][y] = "X"
				board_defender[x][y] = "X"
				coord_hit_player.append(coord)

			except:

				print("SHOT UNSUCCESSFUL")
				print(f"{coord} is not a valid coordinate")

		elif attacker == "ai":

			try:

				board_defender[x][y] = "X"
				coord_hit_ai.append(coord)

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

		warnings.warn("Ship already deployed")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1:])

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

		warnings.warn("Ship already deployed")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1:])

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

		warnings.warn("Ship already deployed")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1:])

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

		warnings.warn("Ship already deployed")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1:])

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

		warnings.warn("Ship already deployed")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1:])

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
					ships_dict["destroyer"]["destroyer_two"]["on_board"] = True

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

		warnings.warn("Ship already deployed")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1:])

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

		warnings.warn("Ship already deployed")
		return

	else:

		if type(coord) == str:

			try:

				x = coord[0].upper()
				y = int(coord[1:])

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

	while ships_ai["battleship"]["on_board"] == False:

		set_battleship(coord, direction, "ai")

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

	while ships_ai["cruiser"]["on_board"] == False:

		set_cruiser(coord, direction, "ai")

		direction = directions[random.randint(0, 3)]
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)

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

def get_ship_sunk_gif(victorious_player):

	filename = ""

	if victorious_player == "human":

		filename = "battleship_firing.gif"

	elif victorious_player == "ai":

		filename = "battleship_sinking.gif"
	
	animation = pyglet.resource.animation(filename)
	sprite = pyglet.sprite.Sprite(animation)

	win = pyglet.window.Window(width=sprite.width, height=sprite.height)

	green = 0, 1, 0, 1
	pyglet.gl.glClearColor(*green)

	@win.event
	
	def on_draw():
		
		win.clear()
		
		sprite.draw()

	pyglet.app.run()

def is_ship_present(player, ship):

	is_present = True

	if player == "human":

		board = board_player

	elif player == "ai":

		board = board_ai
	
	count = 0
	
	for m in board.values():
    	
		if ships_player[ship]["symbol"] not in m.values():
			
			count += 1
	
	if count == 10:
		
		is_present = False

	return is_present

while game_initialized == False:

	get_board()
	set_player_positions()
	print("It's a quiet day. Almost too quiet.")
	print("Admiral, there's a ship on the horizon!")
	set_ai_positions()
	print("It's an enemy fleet!")
	print("Flip a coin to see whether you go first.")
	choice = input("Heads or tails? ")
	player_start = coin_toss(choice)
	game_initialized = True

while game_in_progress == True:

	print(f"~~~~~~~~~~ TURN #{turn_counter} ~~~~~~~~~~")
	
	# Player goes first

	if player_start == True:

		get_board("ai")
		coord = input("What coordinates should we fire upon, Admiral? ")
		fire(coord)
		if fire(coord) == "misfire":

			print("It looks like we already fired on those coordinates, Sir.")
			coord = input("What coordinates should we fire upon, Admiral? ")
			fire(coord)

		print("The enemy fleet is returning fire!")
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		fire(coord, "ai")
		if fire(coord, "ai") == "misfire":

			row = letters[random.randint(0, 9)]
			column = random.randint(1, 10)
			coord = row + str(column)
			fire(coord, "ai")

		get_board()

	# Computer goes first

	elif player_start == False:

		print("The enemy fleet is firing on us, Admiral!")
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		fire(coord, "ai")
		if fire(coord, "ai") == "misfire":

			row = letters[random.randint(0, 9)]
			column = random.randint(1, 10)
			coord = row + str(column)
			fire(coord, "ai")

		get_board()

		get_board("ai")
		coord = input("What coordinates should we return fire upon? ")
		fire(coord)
		if fire(coord) == "misfire":

			print("It looks like we already fired on those coordinates, Sir.")
			coord = input("What coordinates should we fire upon, Admiral? ")
			fire(coord)
	
	# Have any of the computer's ships been sunk?

	if (is_ship_present("ai", "aircraft_carrier") == False) and (aircraft_carrier_sunk_ai == False):

		print("We've sunk the enemy's aircraft carrier, Admiral!")
		aircraft_carrier_sunk_ai = True
		player_score += 1

		get_ship_sunk_gif("human")

	elif (is_ship_present("ai", "destroyer") == False) and (destroyers_sunk_ai == False):

		print("We've sunk both the enemy's destroyers, Admiral!")
		destroyers_sunk_ai = True
		player_score += 1

		get_ship_sunk_gif("human")

	elif (is_ship_present("ai", "battleship") == False) and (battleship_sunk_ai == False):

		print("We've sunk the enemy's battleship, Admiral!")
		battleship_sunk_ai = True
		player_score += 1

		get_ship_sunk_gif("human")

	elif (is_ship_present("ai", "cruiser") == False) and (cruiser_sunk_ai == False):

		print("We've sunk the enemy's cruiser, Admiral!")
		cruiser_sunk_ai = True
		player_score += 1

		get_ship_sunk_gif("human")


	elif (is_ship_present("ai", "submarine") == False) and (destroyers_sunk_ai == False):

		print("A direct hit on the last enemy submarine! They've lost both their submarines, Admiral!")
		submarines_sunk_ai = True
		player_score += 1

		get_ship_sunk_gif("human")

	# Have any of the player's ships been sunk?

	if (is_ship_present("human", "aircraft_carrier") == False) and (aircraft_carrier_sunk_player == False):

		print("Our aircraft carrier's sinking, Admiral!")
		aircraft_carrier_sunk_player = True
		ai_score += 1
		
		get_ship_sunk_gif("ai")
	
	elif (is_ship_present("human", "battleship") == False) and (battleship_sunk_player == False):

		print("Our battleship is sinking, Admiral!")
		battleship_sunk_player = True
		ai_score += 1
		
		get_ship_sunk_gif("ai")
	
	elif (is_ship_present("human", "cruiser") == False) and (cruiser_sunk_player == False):

		print("Our cruiser's sinking, Admiral!")
		cruiser_sunk_player = True
		ai_score += 1

		get_ship_sunk_gif("ai")

	elif (is_ship_present("human", "destroyer") == False) and (destroyers_sunk_player == False):

		print("We've lost both our destroyers, Admiral!")
		destroyers_sunk_player = True
		player_score += 1

		get_ship_sunk_gif("ai")

	elif (is_ship_present("human", "submarine") == False) and (submarines_sunk_player == False):

		print("That's our last submarine, Admiral! They've both been sunk")
		submarines_sunk_player = True
		ai_score += 1

		get_ship_sunk_gif("ai")
		
	# Has either player won the game?

	if player_score == 5:

		print("VICTORY, Admiral! We've sunk the last of the enemy fleet!")

		play_victory_song()
		
		animation = pyglet.resource.animation("ve_day.gif")
		sprite = pyglet.sprite.Sprite(animation)

		win = pyglet.window.Window(width=sprite.width, height=sprite.height)

		green = 0, 1, 0, 1
		pyglet.gl.glClearColor(*green)

		@win.event
		
		def on_draw():
    		
			win.clear()
    		
			sprite.draw()

		pyglet.app.run()
		
		game_in_progress = False

	elif ai_score == 5:

		print("DEFEAT, Admiral! It has been an honor to serve with you.")

		play_defeat_song()

		animation = pyglet.resource.animation("pearl_harbor.gif")
		sprite = pyglet.sprite.Sprite(animation)

		win = pyglet.window.Window(width=sprite.width, height=sprite.height)

		green = 0, 1, 0, 1
		pyglet.gl.glClearColor(*green)

		@win.event
		
		def on_draw():
    		
			win.clear()
    		
			sprite.draw()

		pyglet.app.run()

		game_in_progress = False

	turn_counter += 1
