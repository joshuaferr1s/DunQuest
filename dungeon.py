import random

class Character():

	def __init__(self, name, maxhp = 100, ap = 20, dp = 2):
		self.name = name
		self.maxhp = hp
		self.hp = self.maxhp
		self.ap = ap
		self.dp = dp

	def take_dmg(self, dmg):
		self.hp = self.hp - dmg

	def is_dead(self):
		if self.hp < 1:
			return True
		else:
			return False

	def get_atk(self):
		return random.randint(0, self.ap)


class Player(Character):

	def __init__(self, name, maxhp = 100, ap = 20, dp = 2, items = []):
		Character.__init__(self, name, maxhp, ap, dp)
		self.inventory = items

	def has_item(self, item):
		if item in self.inventory:
			return True
		else:
			return False

	def sneak(self):
		rnd = random.randint(0,1)
		if rnd == 0:
			return True
		else:
			return False

class Enemy(Character):

	def __init__(self, name, maxhp = 100, ap = 20, dp = 2):
		Character.__init__(self, name, maxhp, ap, dp)

class Dungeon():

	def __init__(self, start_pos = 1):
		self.dungeon = {1: {"name" : "entrance", "north" : 2}, 2: {"name" : "barracks", "east" : 3, "south": 1}, 3: {"name" : "grand hall", "south" : 4, "west" : 2}, 4: {"name" : "treasure room", "north" : 3, "west" : 1}}
		self.current_pos = start_pos

	def current(self):
		print('Current room: ' + self.dungeon[self.current_pos]['name'])

	def move_room(self):
		pass


###############
#   Testing   #
###############
du = Dungeon()
du.current()