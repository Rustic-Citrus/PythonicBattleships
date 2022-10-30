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
directions = {
	"north": {
		"axis": "y",
		"count": -1
	},
	"south": {
		"axis": "y",
		"count": 1
	},
	"east": {
		"axis": "x",
		"count": 1
	},
	"west": {
		"axis": "x",
		"count": -1
	}
}

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

def get_enemy_ship_sunk_gif():
	animation = pyglet.resource.animation("battleship_firing.gif")
	sprite = pyglet.sprite.Sprite(animation)
	win = pyglet.window.Window(width=sprite.width, height=sprite.height)
	@win.event
	def on_draw():
		win.clear()
		sprite.draw()
	green = 0, 1, 0, 1
	pyglet.gl.glClearColor(*green)
	pyglet.app.run()

def get_ship_lost_gif():
	animation = pyglet.resource.animation("battleship_sinking.gif")
	sprite = pyglet.sprite.Sprite(animation)
	win = pyglet.window.Window(width=sprite.width, height=sprite.height)
	@win.event
	def on_draw():
		win.clear()
		sprite.draw()
	green = 0, 1, 0, 1
	pyglet.gl.glClearColor(*green)
	pyglet.app.run()


class Player:
	def __init__(self, type):
		self.type = type

		if self.type == "human":
			self.name = str(input("Please type your name: "))

		elif self.type == "ai":
			self.name = "Computer"

		self.board = {
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
		self.enemy_board = {
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
		self.ships = {
			"Aircraft Carrier": {
				"on_board": False,
				"symbol": "A",
				"coordinates": [],
				"hits": 0,
				"size": 5,
				"limits": {
					"east": ["G", "H", "I", "J"],
					"west": ["A", "B", "C", "D"],
					"south": range(7, 11),
					"north": range(1, 5)
				}
			},
			"Battleship": {
				"on_board": False,
				"symbol": "B",
				"coordinates": [],
				"hits": 0,
				"size": 4,
				"limits": {
					"east": ["H", "I", "J"],
					"west": ["A", "B", "C"],
					"south": range(8, 11),
					"north": range(1, 4)				
				}
			},
			"Cruiser": {
				"on_board": False,
				"symbol": "C",
				"coordinates": [],
				"hits": 0,
				"size": 3,
				"limits": {
					"east": ["I", "J"],
					"west": ["A", "B"],
					"south": range(9, 11),
					"north": range(1, 3)				
				}
			},
			"Destroyer One": {
				"on_board": False,
				"symbol": "D1",
				"coordinates": [],
				"hits": 0,
				"size": 2,
				"limits": {
					"east": ["J"],
					"west": ["A"],
					"south": [10],
					"north": [1]
				}
			},
			"Destroyer Two": {
				"on_board": False,
				"symbol": "D2",
				"coordinates": [],
				"hits": 0,
				"size": 2,
				"limits": {
					"east": ["J"],
					"west": ["A"],
					"south": [10],
					"north": [1]
				}
			},
			"Submarine One": {
				"on_board": False,
				"symbol": "S1",
				"coordinates": [],
				"hits": 0,
				"size": 1,
				"limits": {
					"east": [],
					"west": [],
					"south": [],
					"north": []				
				}
			},
			"Submarine Two": {
				"on_board": False,
				"symbol": "S2",
				"coordinates": [],
				"hits": 0,
				"size": 1,
				"limits": {
					"east": [],
					"west": [],
					"south": [],
					"north": []				
				}
			}
		}
		self.occupied_coord = []
		self.coord_hit = []
		self.damaged_ship_coord = []
		self.score = 0
	
	def set_ship(self, ship, direction, coord):
		try:
			x = coord[0].upper()
			y = int(coord[1:])
			count = letters.find(x)

		except:
			warnings.warn("ERROR: Invalid coordinate")

		if coord in self.occupied_coord:
			warnings.warn("ERROR: Invalid direction")

		elif x in self.ships[ship]["limits"][direction.lower()] or y in self.ships[ship]["limits"][direction.lower()]:
			warnings.warn("ERROR: Coordinates place ship off-board")

		else:
			try:
				potential_coordinates = set()
				for n in range(self.ships[ship]["size"]):
					potential_coordinates.add(letters[count] + str(y))

					if directions[direction.lower()]["axis"] == "x":
						count += directions[direction.lower()]["count"]

					elif directions[direction.lower()]["axis"] == "y":
						y += directions[direction.lower()]["count"]

				if len(set(self.occupied_coord).intersection(potential_coordinates)) == 0:
					for n in potential_coordinates:
						x = n[0].upper()
						y = int(n[1:])
						count = letters.find(x)
						self.board[letters[count]][y] = self.ships[ship]["symbol"]
						self.occupied_coord.append(letters[count] + str(y))
						self.ships[ship]["coordinates"].append(letters[count] + str(y))
					self.ships[ship]["on_board"] = True

			except:
				warnings.warn("ERROR: Coordinates overlap another ship")
	
	def set_fleet(self, any=False):
		for ship in self.ships.keys():
			while self.ships[ship]["on_board"] == False:
				if self.type == "human" and any == False:
					game.get_board()
					coord = input(f"Type the coordinates of the stern of {ship}. ").upper()

					if ship not in ["Submarine One", "Submarine Two"]:
						direction = input(f"Type the direction your {ship} is facing (North, East, South, West). ").lower()

				elif self.type == "ai" or any == True:
					direction = list(directions.keys())[random.randint(0, 3)]
					row = letters[random.randint(0, 9)]
					column = random.randint(1, 10)
					coord = row + str(column)
				
				try:
					self.set_ship(ship, direction, coord)

				except KeyError:
					warnings.warn("ERROR: Invalid coordinates/direction.")

	def get_ship_presence(self, ship):
		is_present = True
		count = 0

		for m in self.board.values():
			if self.ships[ship]["symbol"] not in m.values():
				count += 1
		
		if count == 10:
			is_present = False

		return is_present


class Game:
	def __init__(self, turn=1):
		self.turn = turn
		player_one = Player("human")
		player_two = Player("ai")
		self.players = [player_one, player_two]
		self.in_progress = True

	def deploy(self):
		print("It's a quiet day. Almost too quiet.")
		print("Admiral, there's a ship on the horizon!")
		random_formation = input("Press Y for a random formation. ").lower()

		if random_formation == "y":
			self.players[0].set_fleet(any=True)

		else:
			self.players[0].set_fleet()

		print("It's an enemy fleet!")
		self.players[1].set_fleet()

	def fire(self, attacker, defender, coord):
		x = coord[0]
		y = int(coord[1:])

		try:
			if coord in attacker.coord_hit:
				print("MISFIRE")
				return False

			elif (defender.board[x][y] != "-") and (coord not in attacker.coord_hit):
				play_explosion()	
				defender.board[x][y] = "!"
				attacker.enemy_board[x][y] = "!"
				attacker.coord_hit.append(coord)
				defender.damaged_ship_coord.append(coord)
				print("DIRECT HIT!")
				for ship in defender.ships:
					for coordinate in defender.ships[ship]["coordinates"]:
						if coordinate == coord:
							defender.ships[ship]["hits"] += 1
				return True

			elif defender.board[x][y] == "-":
				play_splash()
				defender.board[x][y] = "X"
				attacker.enemy_board[x][y] = "X"
				attacker.coord_hit.append(coord)
				print("MISS!")
				return True

		except KeyError:
			print("ERROR: Invalid coordinates")

	def coin_toss(self):
		print("Flip a coin to see whether you go first.")
		choice = input("Heads or tails? ")
		result = random.choice(["heads", "tails"])

		if choice.lower() == result:
			print(f"{choice.upper()}! {self.players[0].name.upper()} goes first.")
			self.player_one_starts = True

		elif choice.lower() != result:
			print(f"{choice.upper()}! {self.players[1].name.upper()} goes first.")
			self.player_one_starts = False

	def get_board(self):
		print(f"~~~~~~~~~~ {self.players[0].name.upper()}'S FLEET ~~~~~~~~~~")
		df = pd.DataFrame(self.players[0].board)
		print(tabulate(df, headers = "keys", tablefmt = "psql"))

		print(f"~~~~~~~~~~ {self.players[1].name.upper()}'S FLEET ~~~~~~~~~~")
		df = pd.DataFrame(self.players[0].enemy_board)
		print(tabulate(df, headers = "keys", tablefmt = "psql"))

	def damage_report(self):
		for player in self.players:
			for ship in player.ships:
				if player.ships[ship]["on_board"] == True:
					if player.ships[ship]["hits"] >= player.ships[ship]["size"]:
						print(f"{player.name}'s {ship} is sinking!")
						if player == self.players[0]:
							get_ship_lost_gif()
						elif player == self.players[1]:
							get_enemy_ship_sunk_gif()
						player.ships[ship]["on_board"] = False
						player.score -= 1
					
	def is_victory(self):
		if self.players[1].score == -7:
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
			self.in_progress = False

		elif self.players[0].score == -7:
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
			self.in_progress = False

game = Game()

game.deploy()
game.coin_toss()
game.get_board()

while game.in_progress == True:
	print(f"~~~~~~~~~~ TURN #{game.turn} ~~~~~~~~~~")
	
	# Player goes first
	if game.player_one_starts == True:
		game.get_board()
		coord = input("What coordinates should we fire upon, Admiral? ")
		game.fire(attacker=game.players[0], defender=game.players[1], coord=coord)
		game.damage_report()
		print("The enemy fleet is returning fire!")
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		game.fire(attacker=game.players[1], defender=game.players[0], coord=coord)

	# Computer goes first
	elif game.player_one_starts == False:
		print("The enemy fleet is firing on us, Admiral!")
		row = letters[random.randint(0, 9)]
		column = random.randint(1, 10)
		coord = row + str(column)
		game.fire(attacker=game.players[1], defender=game.players[0], coord=coord)
		game.damage_report()
		game.get_board()
		coord = input("What coordinates should we fire upon, Admiral? ")
		game.fire(attacker=game.players[0], defender=game.players[1], coord=coord)
		
	game.damage_report()
	game.is_victory()
	game.turn += 1
	