import random, time, sys
from file_helpers
import *

'''
class Character():
	def __init__(self, name, maxhp = 100, ap = 20, dp = 2):
		self.name = name
		self.maxhp = maxhp
		self.hp = self.maxhp
		self.ap = ap
		self.dp = dp

	def take_dmg(self, dmg):
		self.hp = self.hp - dmg

	def is_dead(self):
		if self.hp < 1:
			return True
		else :
			return False

	def get_atk(self):
		return random.randint(0, self.ap)
'''

class Player():

	def __init__(self, name, maxhp = 100, ap = 20, dp = 2, items = []):
		self.name = name
		self.maxhp = maxhp
		self.hp = self.maxhp
		self.ap = ap
		self.dp = dp
		self.inventory = items
		self.equipped = []

	def take_dmg(self, dmg):
		self.hp = self.hp - dmg

	def is_dead(self):
		if self.hp < 1:
			return True
		else :
			return False

	def has_item(self, item):
		if item in self.inventory:
			return True
		else :
			return False

	def get_atk(self):
		return random.randint(0, self.ap)

	def sneak(self):
		rnd = random.randint(0, 1)
		if rnd == 0:
			return True
		else :
			return False

	def use_potion(self):
		if (self.hp + 20) > self.maxhp:
			self.hp = self.maxhp
		else :
			self.hp += 20
		self.inventory.remove('healing_potion')
		print('You used a healing_potion')

class Enemy():

	def __init__(self, name, maxhp = 100, ap = 20):
		self.name = name
		self.maxhp = random.randint(0, maxhp)
		self.hp = self.maxhp
		self.ap = random.randint(0, ap)

	def take_dmg(self, dmg):
		self.hp = self.hp - dmg

	def is_dead(self):
		if self.hp < 1:
			return True
		else :
			return False

	def get_atk(self):
		return random.randint(0, self.ap)

	def drop_loot(self):
		loot = ['', 'dagger', 'gauntlets', 'healing_potion', 'sword', 'battle-axe', 'breastplate', 'boots', 'leg_plates', 'artifact']
		randchoice = random.randint(0, len(loot) - 1)
		return loot[randchoice]

	def gui(self):
		borderfy_text('Name: ' + self.name + ' || HP: ' + str(self.hp))

class Dungeon():

	def __init__(self, name, start_pos = 1):
		self.dungeon = load_dungeon('dungeon.txt')
		# self.dungeon = {1: {"name": "entrance", "description": "An unkept cube of a room that looks like a once lush entrance.", "loot": "", "enemy": "", "north": 2},2: {"name": "barracks","loot": "","enemy": "hobgoblin","east": 3,"south": 1},3: {"name": "grand hall","loot": "healing_potion","enemy": "","south": 4,"west": 2},4: {"name": "treasure room","loot": "10,000 Gold","enemy": "","north": 3,"south": 100},100: {"name": 'exit'}}
		self.current_pos = start_pos
		self.visited = list()
		self.pl = Player(name)
		self.running = True

	def check_game_state(self):
		if self.pl.is_dead():
			self.death_handler()
		elif self.dungeon[self.current_pos]['name'] == 'exit':
			self.running = False
		else :
			pass

def gui(self):
	borderfy_text('Name: ' + self.pl.name + ' || HP: ' + str(self.pl.hp) + ' || Location: ' + str(self.current()))

def game_loop(self):
	while self.running:
		self.room_handler()
		self.move_room()
		self.scene_splitter()
		self.check_game_state()
		self.win_handler()

def current(self):
	return self.dungeon[self.current_pos]['name']

def get_moves(self):
	print('You can go:')
	for i in self.dungeon[self.current_pos]:
		if i == 'name' or i == 'description' or i == 'loot' or i == 'enemy':
			pass
		else :
			print(' * ' + i)
			print('You can:')
			print('* inventory')
	if 'healing_potion' in self.pl.inventory:
		print('* use healing_potion')

def move_room(self):
	self.get_moves()
	move = input('> ')
	if move == 'quit':
		sys.exit(1)
	elif move in self.dungeon[self.current_pos]:
		self.current_pos = self.dungeon[self.current_pos][move]
	elif move == 'inventory':
		self.inventory_handler()
	elif move == 'use healing_potion' and 'healing_potion' in self.pl.inventory:
		if (self.pl.hp + 20) > self.pl.maxhp:
			self.pl.hp = self.pl.maxhp
		else :
			self.pl.hp += 20
	else :
		print('Invalid direction')

def describe_room(self):
	if self.current_pos not in self.visited:
		try:
			print('Description: ' + self.dungeon[self.current_pos]['description'])
		except KeyError:
			pass
	else:
		pass

def death_handler(self):
	print('\n' * 1000)
	print(" ____  ____                  ______     _               __  ")
	print("|_  _||_  _|                |_   _ `.  (_)             |  ] ")
	print("  \ \  / / .--.   __   _      | | `. \ __  .---.   .--.| |  ")
	print("   \ \/ // .'`\ \[  | | |     | |  | |[  |/ /__\\/ /'`\' |  ")
	print("   _|  |_| \__. | | \_/ |,   _| |_.' / | || \__.,| \__/  |  ")
	print("  |______|'.__.'  '.__.'_/  |______.' [___]'.__.' '.__.;__] ")
	print("                                                            ")
	print('')
	print('Upon death you...')
	sys.exit(1)

def win_handler(self):
	print('\n' * 1000)
	print(" ____  ____                  ____    ____               __          _____  _    ")
	print("|_  _||_  _|                |_   \  /   _|             |  ]        |_   _|/ |_  ")
	print("  \ \  / / .--.   __   _      |   \/   |   ,--.    .--.| | .---.     | | `| |-' ")
	print("   \ \/ // .'`\ \[  | | |     | |\  /| |  `'_\ : / /'`\' |/ /__\\    | |  | |   ")
	print("   _|  |_| \__. | | \_/ |,   _| |_\/_| |_ // | |,| \__/  || \__.,   _| |_ | |,  ")
	print("  |______|'.__.'  '.__.'_/  |_____||_____|\'-;__/ '.__.;__]'.__.'  |_____|\__/  ")
	print("                                                                                ")
	print("Upon making it out...")

def scene_splitter(self):
	print('/' * 70)
	print('/' * 70)
	print('/' * 70)

def no_similar_weapon_equipped(item):
	loot = ['dagger', 'sword', 'battle-axe']
	loot.remove(item)
	for element in loot:
		if element in self.pl.equipped:
		return False
	return True

def battler(self):
	while True:
	self.scene_splitter()
	self.gui()
	self.en.gui()
	print('WWhat would you like to do?')
	print('* attack')
	print('* defend')
	if 'healing_potion' in self.pl.inventory:
		print('* use healing_potion')
	action = input('> ')
	if action == 'attack':
		self.en.take_dmg(self.pl.get_atk())
	if self.en.hp > 0:
		self.pl.take_dmg(self.en.get_atk())
	else:
		pass
	elif action == 'defend':
		enem_atk = self.en.get_atk() - self.pl.dp
	if enem_atk < 0:
		self.pl.take_dmg(0)
	else:
		self.pl.take_dmg(enem_atk)
	elif action == 'use healing_potion' and 'healing_potion' in self.pl.inventory:
		self.pl.use_potion()
	else:
		pass
	if self.en.is_dead():
		break
	if self.pl.is_dead():
		self.death_handler()

def room_handler(self):
	self.gui()

# If enemy present, fight
if self.dungeon[self.current_pos]['enemy'] != ''
and self.current_pos not in self.visited:
	self.en = Enemy(self.dungeon[self.current_pos]['enemy'])
print('You come across a ' + self.en.name + '!')
print('Prepare to fight!')
time.sleep(2)
self.battler()
print('You defeated the pathetic ' + self.en.name + '!')
fight_loot = self.en.drop_loot()
if fight_loot == '':
	print("The lousy " + self.en.name + " didn't have anything on it")
else :
	print('You find ' + fight_loot + ' on the corpse.')
self.pl.inventory.append(fight_loot)
self.scene_splitter()
self.gui()
else :
	pass

# If loot present, loot
if self.dungeon[self.current_pos]['loot'] != ''
and self.current_pos not in self.visited:
	self.pl.inventory.append(self.dungeon[self.current_pos]['loot'])# self.gui()
print('You find ' + self.dungeon[self.current_pos]['loot'])
print('--------------------------------------------')
else :
	pass

self.describe_room()
self.visited.append(self.current_pos)

def inventory_handler(self):
	state = True
while state:
	self.scene_splitter()
print('Inventory:')
for i in self.pl.inventory:
	print('* ' + i)
print('----------------')

print('Options: ')
print('* equip _____')
print('* unequip _____')
print('* drop _____')
print('* use _____')
print('* sort_gold')
print('* back')
option = input('> ')
opts = option.split(' ')
if opts[0] == 'equip': #loot: dagger, gauntlets, healing_potion, sword, battle - axe# breastplate, boots, leg_plates, artifact
try:
if opts[1] not in self.pl.inventory:
	print(opts[1] + ' is not in your inventory.')
elif opts[1] not in self.pl.equipped and opts[1] != '':
	if opts[1] == 'gauntlets':
	self.pl.equipped.append('gauntlets')
self.pl.dp += 2
print('You have now equipped ' + opts[1])
elif opts[1] == 'dagger':
	if self.no_similar_weapon_equipped(opts[1]):
	self.pl.equipped.append('dagger')
self.pl.ap += 2
print('You have now equipped ' + opts[1])
else :
	print('You already have a weapon equipped.')
elif opts[1] == 'sword':
	if self.no_similar_weapon_equipped(opts[1]):
	self.pl.equipped.append(opts[1])
self.pl.ap += 4
print('You have now equipped ' + opts[1])
else :
	print('You already have a weapon equipped.')
elif opts[1] == 'battle-axe':
	if self.no_similar_weapon_equipped(opts[1]):
	self.pl.equipped.append('battle-axe')
self.pl.ap += 2
print('You have now equipped ' + opts[1])
else :
	print('You already have a weapon equipped.')
elif opts[1] == 'breastplate':
	self.pl.equipped.append(opts[1])
self.pl.dp += 4
print('You have now equipped ' + opts[1])
elif opts[1] == 'boots':
	self.pl.equipped.append(opts[1])
self.pl.dp += 2
print('You have now equipped ' + opts[1])
elif opts[1] == 'leg_plates':
	self.pl.equipped.append(opts[1])
self.pl.dp += 2
print('You have now equipped ' + opts[1])
else :
	print(opts[1] + ' is not equipable.')
else :
	print('You have already equipped this item.')
except IndexError:
	print('Please enter what item you would like to equip after you type "equip".')
elif opts[0] == 'unequip':
	try:
	if opts[1] not in self.pl.equipped:
	print(opts[1] + ' is not equipped.')
elif opts[1] != '':
	if opts[1] == 'gauntlets':
	self.pl.equipped.remove('gauntlets')
self.pl.dp -= 2
print('You have now unequipped ' + opts[1])
elif opts[1] == 'dagger':
	self.pl.equipped.remove('dagger')
self.pl.ap -= 2
print('You have now unequipped ' + opts[1])
elif opts[1] == 'sword':

	elif opts[1] == 'battle-axe':

	elif opts[1] == 'breastplate':

	elif opts[1] == 'boots':

	elif opts[1] == 'leg_plates':

	else :
		print('GAH')
except IndexError:
	print('Please enter what item you would like to unequip after you type "unequip".')
elif opts[0] == 'drop':
	try:
	temp_fre = 0
for inve in self.pl.inventory:
	if inve == opts[1]:
	temp_fre += 1
if opts[1] not in self.pl.inventory:
	print('You do not have this item.')
elif opts[1] in self.pl.equipped and temp_fre = 1:
	print('You must first unequip ' + opts[1])
else :
	self.pl.inventory.remove(opts[1])
print(opts[1] + ' has now been removed from your inventory.')
except IndexError:
	print('Please enter what item you would like to drop after you type "drop".')
elif opts[0] == 'use': #Handle using items
try:
if opts[1] not in self.pl.inventory:
	print('You do not have this item.')
else :
	if opts[1] == 'healing_potion':
	self.pl.use_potion()
except IndexError:
	print('Please enter what item you would like to use after you type "use".')
elif option == 'sort_gold':
	temp_li = list()
temp_tot = 0
for ite in self.pl.inventory:
	if ite.split('_')[1] == 'gold':
	temp_li.append(ite)
self.pl.inventory.remove(ite)
else :
	pass
for ite in temp_li:
	temp_tot += int(ite.split('_')[0])
self.pl.inventory.append(str(temp_tot) + '_gold')
elif option == 'back':
	state = False
else :
	pass

##### Game Initialization#####
print('\n' * 1000)
print(" ______                       ___                            _    ")
print("|_   _ `.                   .'   `.                         / |_  ")
print("  | | `. \ __   _   _ .--. /  .-.  \  __   _   .---.  .--. `| |-' ")
print("  | |  | |[  | | | [ `.-. || |   | | [  | | | / /__\\( (`\] | |   ")
print(" _| |_.' / | \_/ |, | | | |\  `-'  \_ | \_/ |,| \__., `'.'. | |,  ")
print("|______.'  '.__.'_/[___||__]`.___.\__|'.__.'_/ '.__.'[\__) )\__/  ")
print("                                                                  ")
print('    Welcome to DunQuest! A game of infinite possibilities!')
time.sleep(3)
print('\n' * 1000)

print('What is your name?')
name = input('> ')
print('\n' * 1000)

du = Dungeon(name)
du.game_loop()


'''
try:
	input("Press Enter to continue")
except SyntaxError:
	pass 
'''