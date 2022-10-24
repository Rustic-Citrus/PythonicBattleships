import pandas as pd
from tabulate import tabulate
import string

letters = string.ascii_uppercase

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
		"hits": 0
	},
	"battleship": {
		"on_board": False,
		"hits": 0
	},
	"cruiser": {
		"on_board": False,
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
		"count": 0
	}
}

def get_board():
	
	print("=== BOARD ===")
	df = pd.DataFrame(board)
	print(tabulate(df, headers = "keys", tablefmt = "psql"))

# get_board()

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

# fire("F3")

def set_aircraft_carrier(coord, direction):

	directions = ["left", "right", "up", "down"]

	if ships["aircraft_carrier"]["on_board"] == True:

		print("Cannot place! There is already an aircraft carrier on the board.")
		return

	else:

		ships["aircraft_carrier"]["on_board"] = True

	if type(coord) == str:

		try:

			x = coord[0].upper()
			y = int(coord[1])

		except:

			print("Make sure you type a coordinate, e.g. A1 or B2")

	if direction.lower() in directions:

			if direction.lower() == "left":
				count = letters.find(x)
				for n in range(5):
					board[letters[count]][y] = 1
					count -= 1

			elif direction.lower() == "right":
				count = letters.find(x)
				for n in range(5):
					board[letters[count]][y] = 1
					count += 1

			elif direction.lower() == "up":
				count = y
				for n in range(5):
					board[x][count] = 1
					count -= 1

			elif direction.lower() == "down":
				count = y
				for n in range(5):
					board[x][count] = 1
					count += 1

	get_board()

# set_aircraft_carrier("A1", "right")

def set_battleship(coord, direction):

	directions = ["left", "right", "up", "down"]

	if type(coord) == str:

		try:

			x = coord[0].upper()
			y = int(coord[1])

		except:

			print("Make sure you type a coordinate, e.g. A1 or B2")

	if direction.lower() in directions:

		if direction.lower() == "left":
			count = letters.find(x)
			for n in range(4):
				board[letters[count]][y] = 1
				count -= 1

		elif direction.lower() == "right":
			count = letters.find(x)
			for n in range(4):
				board[letters[count]][y] = 1
				count += 1

		elif direction.lower() == "up":
			count = y
			for n in range(4):
				board[x][count] = 1
				count -= 1

		elif direction.lower() == "down":
			count = y
			for n in range(4):
				board[x][count] = 1
				count += 1

	get_board()

# set_battleship("A5", "right")

def set_cruiser(coord, direction):

	directions = ["left", "right", "up", "down"]

	if type(coord) == str:

		try:

			x = coord[0].upper()
			y = int(coord[1])

		except:

			print("Make sure you type a coordinate, e.g. A1 or B2")

	if direction.lower() in directions:

			if direction.lower() == "left":
				count = letters.find(x)
				for n in range(3):
					board[letters[count]][y] = 1
					count -= 1

			elif direction.lower() == "right":
				count = letters.find(x)
				for n in range(3):
					board[letters[count]][y] = 1
					count += 1

			elif direction.lower() == "up":
				count = y
				for n in range(3):
					board[x][count] = 1
					count -= 1

			elif direction.lower() == "down":
				count = y
				for n in range(3):
					board[x][count] = 1
					count += 1

def set_destroyer(coord, direction):

	directions = ["left", "right", "up", "down"]

	if type(coord) == str:

		try:

			x = coord[0].upper()
			y = int(coord[1])

		except:

			print("Make sure you type a coordinate, e.g. A1 or B2")

	if direction.lower() in directions:

			if direction.lower() == "left":
				count = letters.find(x)
				for n in range(2):
					board[letters[count]][y] = 1
					count -= 1

			elif direction.lower() == "right":
				count = letters.find(x)
				for n in range(2):
					board[letters[count]][y] = 1
					count += 1

			elif direction.lower() == "up":
				count = y
				for n in range(2):
					board[x][count] = 1
					count -= 1

			elif direction.lower() == "down":
				count = y
				for n in range(2):
					board[x][count] = 1
					count += 1
