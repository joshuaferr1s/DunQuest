import random, time, sys
from file_helpers import *

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

	def __init__(self, name, gold = 0, maxhp = 100, ap = 20, dp = 2, items = []):
		self.name = name
		self.gold = gold
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

	def use_potion(self):
		if (self.hp + 20) > self.maxhp:
			self.hp = self.maxhp
		else:
			self.hp += 20
		self.inventory.remove('healing_potion')
		print('You used a healing_potion')

class Enemy():

	def __init__(self, name, maxhp = 100, ap = 20):
		self.name = name
		self.maxhp = random.randint(0, maxhp)
		self.hp = self.maxhp
		self.ap = random.randint(2, ap)

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
		loot = ['', 'rusty_dagger', 'gauntlets', 'healing_potion', 'sword', 'battle-axe', 'breastplate', 'boots', 'leg_plates', 'artifact']
		randchoice = random.randint(0,len(loot) - 1)
		return loot[randchoice]

	def gui(self):
		borderfy_text('Name: ' + self.name + ' || HP: ' + str(self.hp))

class Merchant():

	def __init__(self):
		self.gold = 10
		self.met = False
		self.trust = False
		self.items = ['healing_potion', 'artifact', 'purple_liquid']
		self.items_buy = {'healing_potion' : 2, 'artifact' : 5, 'purple_liquid' : 13}
		self.items_sell = {'healing_potion' : 4, 'artifact' : 7, 'purple_liquid' : 15}

	def interact(self):
		if not self.met:
			self.introduction()
		self.trust_test()
		self.set_prices()
		self.shop()

	def introduction(self):
		self.met = True
		print('Well howdy, young traveller!')
		print("I seem to have lost my way but I ain't lost my wears.")

	def trust_test(self):
		if not self.trust:
			loop = True
			while loop:
				print('May I ask who I am speaking with?')
				print('* yes')
				print('* no')
				choi = input('> ')
				if choi == 'yes':
					self.trust = True
					print('Well hello there ' + pl.name)
					print('Pleased to make your acquaintance!')
					loop = False
				elif choi == 'no':
					print('Well fine be like that!')
					loop = False
				else:
					print('Invalid Input.')

	def set_prices(self):
		if not self.trust:
			for i in items:
				self.items_buy[i] += 2
				self.items_sell[i] -= 2

	def shop(self):
		loop = True
		while loop:
			print('--------------------------------')
			print('Items:')
			for i in self.items:
				print('* ' + i + ' | ' + str(self.items_buy[i]) + ' | ' + str(self.items_sell[i]))
			print('')
			print('Actions:')
			print('* help')
			print('* quit')
			choi = input('> ')
			choic = choi.split(' ')
			try:
				chac = choic[0] + ' ' + choic[1]
			except IndexError:
				chac = 'Failed'
			if choi == 'help':
				print('(Type "buy/sell ____")')
				print('(Guide: Item | Buy Price | Sell Price)')
				try:
					input("Press Enter to continue...")
				except SyntaxError:
					pass
			elif choi == 'quit':
				print('Farewell and good luck!')
				loop = False
				try:
					input("Press Enter to continue...")
				except SyntaxError:
					pass
			elif chac != 'Failed' and choic[0] == 'buy' and choic[1] in self.items:
				if pl.gold >= self.items_buy[choic[1]]:
					print('Merchant: You are now the proud owner of ' + choic[1])
					pl.gold -= self.items_buy[choic[1]]
					self.gold += self.items_buy[choic[1]]
					pl.inventory.append(choic[1])
					loop = False
					try:
						input("Press Enter to continue...")
					except SyntaxError:
						pass
				else:
					print('Merchant: I apologize kind sir but you do not have the required funds.')

			elif chac != 'Failed' and choic[0] == 'sell' and choic[1] in self.items:
				if self.gold >= items_sell[choic[1]]:
					if choic[1] in pl.inventory:
						print('Merchant: Thanks for the ' + choic[1])
						pl.gold += self.items_sell[choic[1]]
						self.gold -= self.items_sell[choic[1]]
						pl.inventory.remove(choic[1])
						loop = False
						try:
							input("Press Enter to continue...")
						except SyntaxError:
							pass
					else:
						print('Merchant: Are you trying to rob me child?! I know you do not have that!')
				else:
					print('Merchant: I apologize kind sir but I do not have the required funds.')
			else:
				print('Invalid Input.')
				try:
					input("Press Enter to continue...")
				except SyntaxError:
					pass





class Dungeon():

	def __init__(self, start_pos = 1, dungeon = 1):
		self.cur_dungeon = dungeon
		self.dungeon = load_dungeon('dungeon' + str(dungeon) + '.txt')
		self.current_pos = start_pos
		self.visited = list()

	def check_game_state(self):
		if pl.is_dead():
			self.death_handler()
		elif self.dungeon[self.current_pos]['name'] == 'exit':
			return False
		else:
			return True

	def gui(self):
		borderfy_text('Name: ' + pl.name + ' || HP: ' + str(pl.hp) + ' || Gold: ' + str(pl.gold) + ' || Location: ' + str(self.current()))

	def game_loop(self):
		global running
		global dungeons_comp
		global equipped
		global inventory
		global player
		running = True
		while self.check_game_state():
			self.room_handler()
			self.move_room()
			self.scene_splitter()
		self.win_handler()
		if str(self.cur_dungeon) not in dungeons_comp:
			dungeons_comp.append(self.cur_dungeon)
		for i in pl.equipped:
			equipped.append(i)
		for i in pl.inventory:
			inventory.append(i)
		player.append(pl.name)
		player.append(pl.gold)
		player.append(pl.maxhp)
		player.append(pl.hp)
		player.append(pl.ap)
		player.append(pl.dp)

		menu_state = True
		while menu_state:
			print('Would you like to save your progress?')
			print('* yes')
			print('* no')
			choi = input('> ')
			if choi == 'yes':
				print('Existing savefiles:')
				for i in save_files:
					print('* ' + i)
				print('What would you like your savename to be?')
				savename = input('> ')
				if valid_file_name(savename) and savename not in save_files:
					save_game(savename)
					menu_state = False
				elif valid_file_name(savename) and savename in save_files:
					print('Would you like to overwrite previous savefiles?')
					print('* yes')
					print('* no')
					choi = input('> ')
					if choi == 'yes':
						delete_file_contents('saves/' + savename + 'dungeons.txt')
						delete_file_contents('saves/' + savename + 'equipped.txt')
						delete_file_contents('saves/' + savename + 'inventory.txt')
						delete_file_contents('saves/' + savename + 'player.txt')
						save_game(savename)
						menu_state = False
					elif choi == 'no':
						pass
					else:
						print('Invalid input.')
				else:
					print('Invalid savename.')
			elif choi == 'no':
				menu_state = False
			else:
				print('Invalid Input.')
				print('/'*70)
				print('/'*70)
				print('/'*70)

	def current(self):
		return self.dungeon[self.current_pos]['name']

	def get_moves(self):
		print('You can go:')
		for i in self.dungeon[self.current_pos]:
			if i == 'name' or i == 'description' or i == 'loot' or i == 'enemy' or i == 'npc' or i == 'gold':
				pass
			else:
				print(' * ' + i)
		print('You can:')
		print('* inventory')
		if 'healing_potion' in pl.inventory:
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
		elif move == 'use healing_potion' and 'healing_potion' in pl.inventory:
			pl.use_potion()
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
		print('\n'*1000)
		print(" ____  ____                  ______     _               __  ")
		print("|_  _||_  _|                |_   _ `.  (_)             |  ] ")
		print("  \ \  / / .--.   __   _      | | `. \ __  .---.   .--.| |  ")
		print("   \ \/ // .'`\ \[  | | |     | |  | |[  |/ /__\\/ /'`\' |  ")
		print("   _|  |_| \__. | | \_/ |,   _| |_.' / | || \__.,| \__/  |  ")
		print("  |______|'.__.'  '.__.'_/  |______.' [___]'.__.' '.__.;__] ")
		print("                                                            ")
		print('')
		print('Upon death you...')
		try:
			input("Press Enter to continue...")
		except SyntaxError:
			pass
		sys.exit(1)

	def win_handler(self):
		print('\n'*1000)
		print(" ____  ____                  ____    ____               __          _____  _    ")
		print("|_  _||_  _|                |_   \  /   _|             |  ]        |_   _|/ |_  ")
		print("  \ \  / / .--.   __   _      |   \/   |   ,--.    .--.| | .---.     | | `| |-' ")
		print("   \ \/ // .'`\ \[  | | |     | |\  /| |  `'_\ : / /'`\' |/ /__\\    | |  | |   ")
		print("   _|  |_| \__. | | \_/ |,   _| |_\/_| |_ // | |,| \__/  || \__.,   _| |_ | |,  ")
		print("  |______|'.__.'  '.__.'_/  |_____||_____|\'-;__/ '.__.;__]'.__.'  |_____|\__/  ")
		print("                                                                                ")
		print("Upon making it out...")
		try:
			input("Press Enter to continue...")
		except SyntaxError:
			pass

	def scene_splitter(self):
		print('/'*70)
		print('/'*70)
		print('/'*70)

	def no_similar_weapon_equipped(self, item):
		loot = ['dagger', 'sword', 'battle-axe']
		loot.remove(item)
		for element in loot:
			if element in pl.equipped:
				return False
		return True

	def battler(self):
		while True:
				self.scene_splitter()
				self.gui()
				self.en.gui()
				print('What would you like to do?')
				print('* attack')
				print('* defend')
				if 'healing_potion' in pl.inventory:
					print('* use healing_potion')
				action = input('> ')
				if action == 'attack':
					self.en.take_dmg(pl.get_atk())
					if self.en.hp > 0:
						pl.take_dmg(self.en.get_atk())
					else:
						pass
				elif action == 'defend':
					enem_atk = self.en.get_atk() - pl.dp
					if enem_atk < 0:
						pl.take_dmg(0)
					else:
						pl.take_dmg(enem_atk)
				elif action == 'use healing_potion' and 'healing_potion' in pl.inventory:
					pl.use_potion()
				else:
					pass
				if self.en.is_dead():
					break
				if pl.is_dead():
					self.death_handler()

	def npc_handler(self, npc):
		npcs = dict()
		if npc == 'merchant':
			self.gui()
			if self.current_pos not in self.visited:
				npcs[self.current_pos] = Merchant()
			npcs[self.current_pos].interact()

		elif npc == 'armorer':
			pass
		elif npc == 'blacksmith':
			pass
		else:
			pass

	def room_handler(self):
		self.gui()

		#If enemy present, fight
		if self.dungeon[self.current_pos]['enemy'] != '' and self.current_pos not in self.visited:
			self.en = Enemy(self.dungeon[self.current_pos]['enemy'])
			print('You come across a ' + self.en.name + '!')
			print('Prepare to fight!')
			time.sleep(2)
			self.battler()
			print('You defeated the pathetic ' + self.en.name + '!')
			fight_loot = self.en.drop_loot()
			fight_gold = self.en.drop_gold()
			if fight_loot == '':
				print("The lousy " + self.en.name + " didn't have anything on it!")
			else:
				print('You find ' + fight_loot + ' on the corpse!')
				pl.inventory.append(fight_loot)
			if fight_gold > 0:
				print('You also found ' + str(fight_gold) + ' gold on the corpse')
			self.scene_splitter()
			self.gui()
		else:
			pass

		#If npc present, interact
		if self.dungeon[self.current_pos]['npc'] != '':
			self.npc_handler(self.dungeon[self.current_pos]['npc'])
		else:
			pass


		#If loot present, loot
		if self.dungeon[self.current_pos]['loot'] != '' and self.current_pos not in self.visited:
			pl.inventory.append(self.dungeon[self.current_pos]['loot'])
			#self.gui()
			print('You find ' + self.dungeon[self.current_pos]['loot'])
			print('--------------------------------------------')
		else:
			pass

		#If gold present, take
		if self.dungeon[self.current_pos]['gold'] != 0 and self.current_pos not in self.visited:
			pl.gold += self.dungeon[self.current_pos]['gold']
			print('You find ' + str(self.dungeon[self.current_pos]['gold']) + ' gold')
			print('--------------------------------------------')
		else:
			pass

		self.describe_room()
		self.visited.append(self.current_pos)

	def inventory_handler(self):
		state = True
		while state:
			self.scene_splitter()
			print('Inventory:')
			for i in pl.inventory:
				if i in pl.equipped:
					print('* (E) ' + i)
				else:
					print('(* ' + i)
			print('----------------')

			print('Options: ')
			print('* equip _____')
			print('* unequip _____')
			print('* drop _____')
			print('* use _____')
			print('* back')
			option = input('> ')
			opts = option.split(' ')
			if opts[0] == 'equip':
				#loot: dagger, gauntlets, healing_potion, sword, battle-axe
				#      breastplate, boots, leg_plates, artifact
				try:
					if opts[1] not in pl.inventory:
						print(opts[1] + ' is not in your inventory.')
					elif opts[1] not in pl.equipped and opts[1] != '':
						if opts[1] == 'gauntlets':
							pl.equipped.append('gauntlets')
							pl.dp += 2
							print('You have now equipped ' + opts[1])
						elif opts[1] == 'dagger':
							if self.no_similar_weapon_equipped(opts[1]):
								pl.equipped.append('dagger')
								pl.ap += 2
								print('You have now equipped ' + opts[1])
							else:
								print('You already have a weapon equipped.')
						elif opts[1] == 'sword':
							if self.no_similar_weapon_equipped(opts[1]):
								pl.equipped.append(opts[1])
								pl.ap += 4
								print('You have now equipped ' + opts[1])
							else:
								print('You already have a weapon equipped.')
						elif opts[1] == 'battle-axe':
							if self.no_similar_weapon_equipped(opts[1]):
								pl.equipped.append('battle-axe')
								pl.ap += 6
								print('You have now equipped ' + opts[1])
							else:
								print('You already have a weapon equipped.')
						elif opts[1] == 'breastplate':
							pl.equipped.append(opts[1])
							pl.dp += 4
							print('You have now equipped ' + opts[1])
						elif opts[1] == 'boots':
							pl.equipped.append(opts[1])
							pl.dp += 2
							print('You have now equipped ' + opts[1])
						elif opts[1] == 'leg_plates':
							pl.equipped.append(opts[1])
							pl.dp += 2
							print('You have now equipped ' + opts[1])
						else:
							print(opts[1] + ' is not equipable.')
					else:
						print('You have already equipped this item.')
				except IndexError:
					print('Please enter what item you would like to equip after you type "equip".')
			elif opts[0] == 'unequip':
				try:
					if opts[1] not in pl.equipped:
						print(opts[1] + ' is not equipped.')
					elif opts[1] != '':
						if opts[1] == 'gauntlets':
							pl.equipped.remove('gauntlets')
							pl.dp -= 2
							print('You have now unequipped ' + opts[1])
						elif opts[1] == 'dagger':
							pl.equipped.remove('dagger')
							pl.ap -= 2
							print('You have now unequipped ' + opts[1])
						elif opts[1] == 'sword':
							pl.equipped.remove(opts[1])
							pl.ap -= 4
							print('You have now unequipped ' + opts[1])
						elif opts[1] == 'battle-axe':
							pl.equipped.remove(opts[1])
							pl.ap -= 6
							print('You have now unequipped ' + opts[1])
						elif opts[1] == 'breastplate':
							pl.equipped.remove(opts[1])
							pl.ap -= 4
							print('You have now unequipped ' + opts[1])
						elif opts[1] == 'boots':
							pl.equipped.remove(opts[1])
							pl.ap -= 2
							print('You have now unequipped ' + opts[1])
						elif opts[1] == 'leg_plates':
							pl.equipped.remove(opts[1])
							pl.ap -= 2
							print('You have now unequipped ' + opts[1])
					else:
						print('GAH')
				except IndexError:
					print('Please enter what item you would like to unequip after you type "unequip".')
			elif opts[0] == 'drop':
				try:
					temp_fre = 0
					for inve in pl.inventory:
						if inve == opts[1]:
							temp_fre += 1
					if opts[1] not in pl.inventory:
						print('You do not have this item.')
					elif opts[1] in pl.equipped and temp_fre == 1:
						print('You must first unequip ' + opts[1])
					else:
						pl.inventory.remove(opts[1])
						print(opts[1] + ' has now been removed from your inventory.')
				except IndexError:
					print('Please enter what item you would like to drop after you type "drop".')
			elif opts[0] == 'use':
				#Handle using items
				try:
					if opts[1] not in pl.inventory:
						print('You do not have this item.')
					else:
						if opts[1] == 'healing_potion':
							pl.use_potion()
				except IndexError:
					print('Please enter what item you would like to use after you type "use".')
			elif option == 'back':
				state = False
			else:
				pass

def sort_save_files(sfr):
	sf = list()
	sfre = list()
	for i in sfr:
		if 'dungeons' in i:
			sfre.append(str(i).replace('dungeons', ''))
		if 'equipped' in i:
			sfre.append(str(i).replace('equipped', ''))
		if 'inventory' in i:
			sfre.append(str(i).replace('inventory', ''))
		if 'player' in i:
			sfre.append(str(i).replace('player', ''))
	for k in sfre:
		if k not in sf:
			sf.append(k)
	return sf
		
##### Game Initialization #####
running = True
pl = Player('Player')
dungeons_comp = list()
equipped = list()
inventory = list()
player = list()
save_files_raw = list()
try:
	save_files_raw = get_save_files()
except FileNotFoundError:
	pass
save_files = sort_save_files(save_files_raw)

def save_game(savename):
	global dungeons_comp
	global equipped
	global inventory
	global player
	#Save file
	create_save_dir()
	print('Save directory created.')
	if create_save_files(savename):
		print('Blank Save Files created')
		#Write to dungeons file
		for i in dungeons_comp:
			append_to_file('saves/' + savename + 'dungeons.txt', i)
		#Write to equipped file
		for i in equipped:
			append_to_file('saves/' + savename + 'equipped.txt', i)
		#Write to inventory file
		for i in inventory:
			append_to_file('saves/' + savename + 'inventory.txt', i)
		#Write to player file
		for i in player:
			append_to_file('saves/' + savename + 'player.txt', i)

def load_game(savename):
	global dungeons_comp
	dungeons_comp = file_to_set('saves/' + savename + 'dungeons.txt')
	_equipped = file_to_set('saves/' + savename + 'equipped.txt')
	_inventory = file_to_set('saves/' + savename + 'inventory.txt')
	_player = file_to_set('saves/' + savename + 'player.txt')
	for i in _equipped:
		if i != '' and i != ' ':
			pl.equipped.append(i)
	for i in _inventory:
		if i != '' and i != ' ':
			pl.inventory.append(i)
	pl.name = _player[0]
	pl.gold = int(_player[1])
	pl.maxhp = int(_player[2])
	pl.hp = int(_player[3])
	pl.ap = int(_player[4])
	pl.dp = int(_player[5])
	print('Successfully loaded player profile: ' + savename + '.')
	try:
		input("Press Enter to continue...")
	except SyntaxError:
		pass

# Main Menu
while running:
	print('\n'*1000)
	print(" ______                       ___                            _    ")
	print("|_   _ `.                   .'   `.                         / |_  ")
	print("  | | `. \ __   _   _ .--. /  .-.  \  __   _   .---.  .--. `| |-' ")
	print("  | |  | |[  | | | [ `.-. || |   | | [  | | | / /__\\( (`\] | |   ")
	print(" _| |_.' / | \_/ |, | | | |\  `-'  \_ | \_/ |,| \__., `'.'. | |,  ")
	print("|______.'  '.__.'_/[___||__]`.___.\__|'.__.'_/ '.__.'[\__) )\__/  ")
	print("                                                                  ")
	print('    Welcome to DunQuest! A game of infinite possibilities!')
	print('')
	print('* play dungeon ____')
	print('* load')
	print('* help')
	print('* quit')
	choice = input('> ')
	spl_choice = choice.split(' ')
	try:
		pldun = spl_choice[0] + ' ' + spl_choice[1]
	except IndexError:
		pldun = 'Failed'
	if choice == 'load':
		menu_state = True
		while menu_state:
			print('Existing savefiles:')
			for i in save_files:
				print('* ' + i)
			print('What is your savename?')
			savename = input('> ')
			if valid_file_name(savename):
				load_game(savename)
				menu_state = False
			else:
				print('Invalid savename.')
	elif choice == 'help':
		print('Coming soon.')
		try:
			input("Press Enter to continue...")
		except SyntaxError:
			pass
	elif choice == 'quit':
		running = False
	elif pldun == 'play dungeon':
		try:
			int_state = isinstance(int(spl_choice[2]), int)
		except IndexError:
			continue
		except ValueError:
			continue
		if int_state:
			print('\n'*1000)
			if len(dungeons_comp) < 1:
				print('What would you like your name to be?')
				choi = input('> ')
				pl.name = choi
			print('\n'*1000)
			du = Dungeon(1, int(spl_choice[2]))
			du.game_loop()
		else:
			print('Please enter a number after "play dungeon".')
			try:
				input("Press Enter to continue...")
			except SyntaxError:
				pass
	else:
		print('Invalid input.')
		try:
			input("Press Enter to continue...")
		except SyntaxError:
			pass

'''
try:
	input("Press Enter to continue...")
except SyntaxError:
	pass
'''
