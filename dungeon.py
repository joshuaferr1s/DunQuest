import random, time, sys

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
		else:
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

	def take_dmg(self, dmg):
		self.hp = self.hp - dmg

	def is_dead(self):
		if self.hp < 1:
			return True
		else:
			return False

	def has_item(self, item):
		if item in self.inventory:
			return True
		else:
			return False

	def get_atk(self):
		return random.randint(0, self.ap)

	def sneak(self):
		rnd = random.randint(0,1)
		if rnd == 0:
			return True
		else:
			return False

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
		else:
			return False

	def get_atk(self):
		return random.randint(0, self.ap)

	def drop_loot(self):
		loot = ['', 'dagger', 'gauntlets', 'healing potion', 'smooth stone']
		randchoice = random.randint(0,len(loot))
		return loot[randchoice]

class Dungeon():

	def __init__(self, name, start_pos = 1):
		self.dungeon = {1: {"name" : "entrance", "description" : "An unkept cube of a room that looks like a once lush entrance.", "loot" : "", "enemy" : "", "north" : 2}, 2: {"name" : "barracks", "loot" : "", "enemy" : "", "east" : 3, "south": 1}, 3: {"name" : "grand hall", "loot" : "", "enemy" : "", "south" : 4, "west" : 2}, 4: {"name" : "treasure room", "loot" : "", "enemy" : "", "north" : 3, "south" : 100}, 100: {"name" : 'exit'}}
		self.current_pos = start_pos
		self.visited = list()
		self.pl = Player(name)
		self.running = True

	def check_game_state(self):
		if self.pl.is_dead():
			self.running = False
			print('You died! Better luck next time.')
		elif self.dungeon[self.current_pos]['name'] == 'exit':
			self.running = False
			print('You made it!')
		else:
			pass

	def borderfy_text(self, text):
		border = ''
		output_text = '# '
		counter = 0
		var = 4 + len(text)

		while counter < var:
			border += '#'
			counter += 1

		output_text += text
		output_text = output_text + ' #'

		print(border)
		print(output_text)
		print(border)

	def gui(self):
		self.borderfy_text('Name: ' + self.pl.name + ' || HP: ' + str(self.pl.hp) + ' || Location: ' + str(self.current()))
		inv_items = 'Inventory: '
		for i in self.pl.inventory:
			inv_items = inv_items + i + ', '
		self.borderfy_text(inv_items)

	def game_loop(self):
		while self.running:
			self.gui()
			self.room_handler()
			self.describe_room()
			self.move_room()
			print('\n'*50)
			self.check_game_state()

	def current(self):
		return self.dungeon[self.current_pos]['name']

	def get_moves(self):
		print('You can go:')
		for i in self.dungeon[self.current_pos]:
			if i == 'name' or i == 'description' or i == 'loot' or i == 'enemy':
				pass
			else:
				print(' * ' + i)

	def move_room(self):
		self.get_moves()
		move = input('-> ')
		if move == 'quit':
			sys.exit(1)
		if move in self.dungeon[self.current_pos]:
			self.visited.append(self.current_pos)
			self.current_pos = self.dungeon[self.current_pos][move]
		else:
			print('Invalid direction')

	def describe_room(self):
		if(self.current_pos not in self.visited):
			try:
				print('Description: ' + self.dungeon[self.current_pos]['description'])
			except KeyError:
				pass
		else:
			pass

	def death_handler(self):
		print('You dead')
		sys.exit(1)

	def room_handler(self):
		if self.dungeon[self.current_pos]['enemy'] != '':
			en = Enemy(self.dungeon[self.current_pos]['enemy'])
			print('You come across a ' + en.name + '!')
			print('Prepare to fight!')
			time.sleep(2)
			while True:
				print('\n'*50)
				self.gui()
				print('Would you like to attack or defend?')
				action = input('> ')
				if action == 'attack':
					en.take_dmg(self.pl.get_atk())
					if en.hp > 0:
						self.pl.take_dmg(en.get_atk())
					else:
						pass
				elif action == 'defend':
					self.pl.take_dmg(en.get_atk() - self.pl.dp)
				else:
					pass
				if en.is_dead():
					break
				if self.pl.is_dead():
					self.death_handler()
			fight_loot = en.drop_loot()
			if fight_loot == '':
				print("The lousy " + en.name + " didn't have anything on it")
			else:
				print('You find a ' + fight_loot + ' on the corpse.')
				self.pl.inventory.append(fight_loot)
				for i in self.pl.inventory:
					print('* ' + i)
		else:
			pass

		if self.dungeon[self.current_pos]['loot'] != '' and self.current_pos not in self.visited:
			#Describe loot and acquire it
			print('You find ' + self.dungeon[self.current_pos]['loot'])
			self.pl.inventory.append(self.dungeon[self.current_pos]['loot'])
		else:
			pass
		
##### Game Initialization #####
print('\n'*1000)
print(" ______                       ___                            _    ")
print("|_   _ `.                   .'   `.                         / |_  ")
print("  | | `. \ __   _   _ .--. /  .-.  \  __   _   .---.  .--. `| |-' ")
print("  | |  | |[  | | | [ `.-. || |   | | [  | | | / /__\\( (`\] | |   ")
print(" _| |_.' / | \_/ |, | | | |\  `-'  \_ | \_/ |,| \__., `'.'. | |,  ")
print("|______.'  '.__.'_/[___||__]`.___.\__|'.__.'_/ '.__.'[\__) )\__/  ")
print("                                                                  ")
print('    Welcome to DunQuest! A game of infinite possibilities!')
time.sleep(3)
print('\n'*1000)

print('What is your name?')
name = input('> ')
print('\n'*1000)

du = Dungeon(name)
du.game_loop()
