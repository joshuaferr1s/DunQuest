import random, time, sys, math, textwrap
from file_helpers import *

class Player():

	def __init__(self, name, gold = 0, maxhp = 20, ap = 5, dp = 1, items = []):
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

	def use_potion(self, potion_type):
		if potion_type == 'healing_potion':
			if (self.hp + 5) > self.maxhp:
				self.hp = self.maxhp
			else:
				self.hp += 5
			self.inventory.remove('healing_potion')
			print('You used a healing_potion')
		elif potion_type == 'purple_liquid':
			self.hp = self.maxhp
			self.inventory.remove('purple_liquid')
			print('You used a vial of purple_liquid')

class Enemy():

	def __init__(self, name, cr):
		self.name = name
		self.cr = cr
		self.maxhp = random.randint(0, 10) + self.cr*3
		self.hp = self.maxhp
		self.ap = random.randint(2, 5) + self.cr*2

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
		loot = ['', 'rusty_dagger', 'gauntlets', 'healing_potion', 'sword', 'battle-axe', 'breastplate', 'boots', 'leg_plates', 'artifact', 'purple_liquid']
		randchoice = random.randint(0,len(loot) - 1)
		return loot[randchoice]

	def drop_gold(self):
		return random.randint(0, math.floor(self.maxhp/3)) + self.cr

	def gui(self):
		borderfy_text('Name: ' + self.name + ' || HP: ' + str(self.hp))

class Npc():

	def __init__(self, name = 'npc', items = list(), items_buy = list(), items_sell = list()):
		self.name = name
		self.gold = 10
		self.met = False
		self.trust = False
		self.items = items
		self.items_buy = items_buy
		self.items_sell = items_sell

	def new(self, name, items, items_buy, items_sell):
		self.name = name
		self.items = items
		self.items_buy = items_buy
		self.items_sell = items_sell

	def interact(self):
		if not self.met:
			self.introduction()
		self.trust_test()
		self.set_prices()
		self.shop()

	def introduction(self):
		self.met = True
		print(self.name + ': Well howdy, young traveller!')
		print(self.name + ":I seem to have lost my way but I ain't lost my wears.")

	def trust_test(self):
		if not self.trust:
			loop = True
			while loop:
				print(self.name + ': May I ask who I am speaking with?')
				print('* yes')
				print('* no')
				choi = input('> ')
				if choi == 'yes':
					self.trust = True
					print(self.name + ': Well hello there ' + pl.name)
					print(self.name + ': Pleased to make your acquaintance!')
					loop = False
				elif choi == 'no':
					print(self.name + ': Well fine be like that!')
					loop = False
				else:
					print('Invalid Input.')

	def set_prices(self):
		if not self.trust:
			for i in self.items:
				self.items_buy[i] += 2
				self.items_sell[i] -= 2

	def gui(self):
		borderfy_text('Name: ' + pl.name + ' || HP: ' + str(pl.hp) + ' || Gold: ' + str(pl.gold))

	def shop(self):
		loop = True
		while loop:
			self.gui()
			print('--------------------------------')
			print('Inventory:')
			for i in pl.inventory:
				if i in pl.equipped:
					print('* (E) ' + i)
				else:
					print('* ' + i)
			print('--------------------------------')
			print('Items:')
			for i in self.items:
				print('* ' + i + ' | ' + str(self.items_buy[i]) + ' | ' + str(self.items_sell[i]))
			print('')
			print('Actions:')
			print('* buy ____')
			print('* sell ____')
			print('* help')
			print('* leave')
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
			elif choi == 'leave':
				print(self.name + ': Farewell and good luck!')
				loop = False
				try:
					input("Press Enter to continue...")
				except SyntaxError:
					pass
			elif chac != 'Failed' and choic[0] == 'buy' and choic[1] in self.items:
				if pl.gold >= self.items_buy[choic[1]]:
					print(self.name + ': You are now the proud owner of ' + choic[1])
					pl.gold -= self.items_buy[choic[1]]
					self.gold += self.items_buy[choic[1]]
					pl.inventory.append(choic[1])
					try:
						input("Press Enter to continue...")
					except SyntaxError:
						pass
				else:
					print(self.name + ': I apologize kind sir but you do not have the required funds.')

			elif chac != 'Failed' and choic[0] == 'sell' and choic[1] in self.items:
				if self.gold >= self.items_sell[choic[1]]:
					if choic[1] in pl.inventory:
						if choic[1] not in pl.equipped:
							print(self.name + ': Thanks for the ' + choic[1])
							pl.gold += self.items_sell[choic[1]]
							self.gold -= self.items_sell[choic[1]]
							pl.inventory.remove(choic[1])
							try:
								input("Press Enter to continue...")
							except SyntaxError:
								pass
						else:
							print(self.name + ": You'll have to unequip that item first.")
					else:
						print(self.name + ': Are you trying to rob me child?! I know you do not have that!')
				else:
					print(self.name + ': I apologize kind sir but I do not have the required funds.')
			elif chac != 'Failed' and (choic[0] == 'buy' or choic[0] == 'sell') and choic[1] not in self.items:
				print(self.name + ": Sorry partner, we don't deal with that here.")
			else:
				print('Invalid Input.')
				try:
					input("Press Enter to continue...")
				except SyntaxError:
					pass

class Dungeon():

	def __init__(self, dungeon = 'dungeon1', start_pos = 1):
		self.cur_dungeon = dungeon.split('dungeon')[1]
		self.dungeon = load_dungeon('dungeons/' + dungeon + '.txt')
		self.current_pos = start_pos
		self.visited = list()
		self.item_fre = dict()
		self.rooms = dict()
		for i in self.dungeon:
			self.rooms[i] = self.dungeon[i]['name']

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
		running = True
		while self.check_game_state():
			self.dungeon_description()
			self.room_handler()
			self.move_room()
			scene_splitter()
		self.win_handler()
		update_pot_files(self.cur_dungeon)
		save_progress()

	def current(self):
		return self.dungeon[self.current_pos]['name']

	def dungeon_description(self):
		try:
			print('/'*70)
			print('~'*70)
			print('/'*70)
			if self.current_pos == 1 and self.current_pos not in self.visited and self.dungeon[self.current_pos]['desc'] != '':
				dungeon_intro = textwrap.wrap(self.dungeon[self.current_pos]['desc'], 70)
				for i in dungeon_intro:
					print(i)
			print('/'*70)
			print('~'*70)
			print('/'*70)
			try:
				input("Press Enter to continue...")
			except SyntaxError:
				pass
		except KeyError:
			pass

	def get_moves(self):
		print('You can go:')
		for i in self.dungeon[self.current_pos]:
			if i == 'name' or i == 'desc' or i == 'description' or i == 'loot' or i == 'enemy' or i == 'enemy_cr' or i == 'npc' or i == 'gold':
				pass
			else:
				print(' * ' + i)
		print('You can:')
		print('* check inventory')
		if self.dungeon[self.current_pos]['npc'] != '':
			print('* talk to npc')
		print('* quit')

	def move_room(self):
		self.get_moves()
		move = input('> ')
		if move == 'quit':
			sys.exit(1)
		elif move in self.dungeon[self.current_pos]:
			self.current_pos = self.dungeon[self.current_pos][move]
		elif move == 'check inventory':
			self.inventory_handler()
		elif move == 'talk to npc' and self.dungeon[self.current_pos]['npc'] != '':
			scene_splitter()
			self.npc_handler(self.dungeon[self.current_pos]['npc'])
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

	def death_handler(self, how):
		print('\n'*1000)
		print(" ____  ____                  ______     _               __  ")
		print("|_  _||_  _|                |_   _ `.  (_)             |  ] ")
		print("  \ \  / / .--.   __   _      | | `. \ __  .---.   .--.| |  ")
		print("   \ \/ // .'`\ \[  | | |     | |  | |[  |/ /__\\/ /'`\' |  ")
		print("   _|  |_| \__. | | \_/ |,   _| |_.' / | || \__.,| \__/  |  ")
		print("  |______|'.__.'  '.__.'_/  |______.' [___]'.__.' '.__.;__] ")
		print("                                                            ")
		print('')
		if how == 'spike_pit':
			print('You fell into a spike pit. Unlucky.')
		print('Upon death you...')
		print('Name: ' + pl.name + ' || HP: ' + str(pl.hp) + '/' + str(pl.maxhp) + ' || + Gold: ' + str(pl.gold))
		print('Room where you died: ' + self.dungeon[self.current_pos]['name'])
		print('Inventory:')
		self.inventory_updater()

		try:
			input("Press Enter to continue...")
		except SyntaxError:
			pass
		sys.exit(1)

	def win_handler(self):
		print('\n'*100)
		print(" ____  ____                  ____    ____               __          _____  _    ")
		print("|_  _||_  _|                |_   \  /   _|             |  ]        |_   _|/ |_  ")
		print("  \ \  / / .--.   __   _      |   \/   |   ,--.    .--.| | .---.     | | `| |-' ")
		print("   \ \/ // .'`\ \[  | | |     | |\  /| |  `'_\ : / /'`\' |/ /__\\    | |  | |   ")
		print("   _|  |_| \__. | | \_/ |,   _| |_\/_| |_ // | |,| \__/  || \__.,   _| |_ | |,  ")
		print("  |______|'.__.'  '.__.'_/  |_____||_____|\'-;__/ '.__.;__]'.__.'  |_____|\__/  ")
		print("                                                                                ")
		print("Upon making it out...")
		print('Name: ' + pl.name + ' || HP: ' + str(pl.hp) + '/' + str(pl.maxhp) + ' || Gold: ' + str(pl.gold))
		print('Inventory:')
		self.inventory_updater()
		try:
			input("Press Enter to continue...")
		except SyntaxError:
			pass

	def no_similar_weapon_equipped(self, item):
		loot = ['dagger', 'sword', 'battle-axe']
		loot.remove(item)
		for element in loot:
			if element in pl.equipped:
				return False
		return True

	def battler(self):
		while True:
				scene_splitter()
				self.gui()
				self.en.gui()
				print('What would you like to do?')
				print('* attack')
				print('* defend')
				if 'healing_potion' in pl.inventory:
					print('* use healing_potion')
				action = input('> ')
				if action == 'attack':
					self.en.take_dmg(pl.get_atk() - math.floor(self.en.ap/2))
					if self.en.hp > 0:
						pl.take_dmg(self.en.get_atk() - math.floor(pl.ap/2))
					else:
						pass
				elif action == 'defend':
					enem_atk = self.en.get_atk() - pl.dp
					if enem_atk < 0:
						pl.take_dmg(0)
					else:
						pl.take_dmg(enem_atk)
				elif action == 'use healing_potion' and 'healing_potion' in pl.inventory:
					pl.use_potion('healing_potion')
				else:
					pass
				if self.en.is_dead():
					break
				if pl.is_dead():
					self.death_handler()

	def npc_handler(self, npc):
		global npc_merchant, npc_armorer, npc_blacksmith
		if npc == 'merchant':
			if self.current_pos not in self.visited:
				npc_merchant.new('Merchant', ['healing_potion', 'artifact', 'purple_liquid'], {'healing_potion' : 2, 'artifact' : 5, 'purple_liquid' : 23}, {'healing_potion' : 4, 'artifact' : 7, 'purple_liquid' : 25})
			npc_merchant.interact()

		elif npc == 'armorer':
			if self.current_pos not in self.visited:
				npc_armorer.new('Armorer', ['breastplate', 'gauntlets', 'leg_plates', 'helmet', 'boot'], {'breastplate' : 3, 'gauntlets' : 1, 'leg_plates' : 2, 'helmet' : 2, 'boot' : 1}, {'breastplate' : 1, 'gauntlets' : 1, 'leg_plates' : 1, 'helmet' : 1, 'boot' : 1})
			npc_armorer.interact()
		elif npc == 'blacksmith':
			if self.current_pos not in self.visited:
				npc_blacksmith.new('Blacksmith', ['battle-axe', 'dagger', 'sword', 'mace', 'bow', 'arrows'], {'battle-axe' : 10, 'dagger' : 5, 'sword' : 7, 'mace' : 8, 'bow' : 12, 'arrows' : 2, 'crossbow' : 18, 'spear' : 14}, {'battle-axe' : 8, 'dagger': 3, 'sword' : 5, 'mace' : 6, 'bow' : 10, 'arrows' : 1, 'crossbow' : 16, 'spear' : 12})
			npc_blacksmith.interact()
		else:
			pass
		self.visited.append(self.current_pos)

	def room_handler(self):
		if self.dungeon[self.current_pos]['name'] == 'spike_pit':
			self.death_handler('spike_pit')
		if self.dungeon[self.current_pos]['gold'] != 0 and self.current_pos not in self.visited:
			pl.gold += int(self.dungeon[self.current_pos]['gold'])
		self.gui()

		#If enemy present, fight
		if self.dungeon[self.current_pos]['enemy'] != '' and self.current_pos not in self.visited:
			self.en = Enemy(self.dungeon[self.current_pos]['enemy'], self.dungeon[self.current_pos]['enemy_cr'])
			print('You come across a ' + self.en.name + '!')
			print('Prepare to fight!')
			time.sleep(2)
			self.battler()
			print('You defeated the pathetic ' + self.en.name + '!')
			fight_loot = self.en.drop_loot()
			fight_gold = self.en.drop_gold()
			if fight_loot == '':
				print("The lousy " + self.en.name + " didn't have any items on it!")
			else:
				print('You find ' + fight_loot + ' on the corpse!')
				pl.inventory.append(fight_loot)
			if fight_gold > 0:
				print('You found ' + str(fight_gold) + ' gold on the corpse')
				pl.gold += fight_gold
			scene_splitter()
			self.gui()
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
			#pl.gold += int(self.dungeon[self.current_pos]['gold'])
			print('You find ' + str(self.dungeon[self.current_pos]['gold']) + ' gold')
			print('--------------------------------------------')
		else:
			pass

		self.describe_room()
		if self.dungeon[self.current_pos]['npc'] == '':
			self.visited.append(self.current_pos)

	def inventory_updater(self):
		displayed = list()
		for ite in pl.inventory:
			if ite in self.item_fre:
				self.item_fre[ite] += 1
			else:
				self.item_fre[ite] = 1
		print('Inventory:')
		for i in pl.inventory:
			if i in pl.equipped and i not in displayed:
				print('* (' + str(self.item_fre[i]) + ') ' + i + '(E)')
				displayed.append(i)
			elif i not in displayed:
				print('* (' + str(self.item_fre[i]) + ') ' + i)
				displayed.append(i)

	def inventory_handler(self):
		global weapons_mods, armor_mods, heal_effectors
		state = True
		while state:
			scene_splitter()
			self.gui()
			self.inventory_updater()
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
				try:
					if opts[1] not in pl.inventory:
						print(opts[1] + ' is not in your inventory.')
					elif opts[1] not in pl.equipped and opts[1] != '':
						if opts[1] in armor_mods:
							pl.equipped.append(opts[1])
							pl.dp += armor_mods[opts[1]]
							print('You have now equipped a ' + opts[1])
						elif opts[1] in weapons_mods:
							pl.equipped.append(opts[1])
							pl.ap += weapons_mods[opts[1]]
							print('You are now wearing a ' + opts[1])
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
					elif opts[1] != '' and opts[1] in pl.equipped:
						if opts[1] in armor_mods:
							pl.equipped.remove(opts[1])
							pl.dp -= armor_mods[opts[1]]
							print('You have unequipped a ' + opts[1])
						elif opts[1] in weapons_mods:
							pl.equipped.remove(opts[1])
							pl.ap -= weapons_mods[opts[1]]
							print('You are no longer wearing a ' + opts[1])
						else:
							print(opts[1] + ' is not equipable.')
					else:
						print('GAH')
				except IndexError:
					print('Please enter what item you would like to unequip after you type "unequip".')
			elif opts[0] == 'drop':
				try:
					if opts[1] not in pl.inventory:
						print('You do not have this item.')
					elif opts[1] in pl.equipped and self.item_fre[opts[1]] == 1:
						print('You must first unequip ' + opts[1])
					else:
						pl.inventory.remove(opts[1])
						print(opts[1] + ' has now been removed from your inventory.')
				except IndexError:
					print('Please enter what item you would like to drop after you type "drop".')
			elif opts[0] == 'use':
				try:
					if opts[1] not in pl.inventory:
						print('You do not have this item.')
					else:
						if opts[1] in heal_effectors:
							pl.use_potion(opts[1])
				except IndexError:
					print('Please enter what item you would like to use after you type "use".')
			elif option == 'back':
				state = False
			else:
				print('Invalid Input.')

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

def update_pot_files(current_dun):
	global dungeons_comp
	global equipped
	global inventory
	global player
	if str(current_dun) not in dungeons_comp:
		dungeons_comp.append('dungeon' + str(current_dun))
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

def save_progress():
	update_save_files()
	menu_state = True
	while menu_state:
		print('Would you like to save your progress?')
		print('* yes')
		print('* no')
		choice = input('> ')
		if choice == 'yes':
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
				choice = input('> ')
				if choice == 'yes':
					delete_file_contents('saves/' + savename + 'dungeons.txt')
					delete_file_contents('saves/' + savename + 'equipped.txt')
					delete_file_contents('saves/' + savename + 'inventory.txt')
					delete_file_contents('saves/' + savename + 'player.txt')
					save_game(savename)
					menu_state = False
				elif choice == 'no':
					pass
				else:
					print('Invalid input.')
			else:
				print('Invalid savename.')
		elif choice == 'no':
			menu_state = False
		else:
			print('Invalid Input.')
			scene_splitter()

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

def scene_splitter():
	print('/'*70)
	print('/'*70)
	print('/'*70)

def update_save_files():
	global save_files_raw
	global save_files
	global list_dungeons
	try:
		list_dungeons = get_dungeon_files()
	except FileNotFoundError:
		pass
	try:
		save_files_raw = get_save_files()
	except FileNotFoundError:
		pass
	save_files = sort_save_files(save_files_raw)

		
##### Game Initialization #####
running = True
pl = Player('Player')
dungeons_comp = list()
equipped = list()
inventory = list()
player = list()
save_files_raw = list()
save_files = list()
list_dungeons = list()
npc_merchant = Npc()
npc_armorer = Npc()
npc_blacksmith = Npc()
armor_mods = {'rusty_boots' : 1, 'rusty_pants': 1, 'rusty_breastplate' : 2, 'rusty_helmet' : 1, 'elven_boots' : 2, 'elven_pants': 2, 'elven_breastplate' : 3, 'elven_helmet' : 2, 'dwarven_boots' : 3, 'dwarven_pants': 3, 'dwarven_breastplate' : 4, 'dwarven_helmet' : 3, 'mithril_boots' : 10, 'mithril_pants': 10, 'mithril_breastplate' : 15, 'mithril_helmet' : 10}
weapons_mods = {'rusty_dagger' : 1, 'dagger' : 2, 'sword' : 3, 'battle-axe' : 4, 'mace' : 5, 'bow' : 6}
heal_effectors = ['healing_potion', 'purple_liquid', 'nutella']
update_save_files()

# Main loop
while running:
	print('\n'*100)
	print(" ______                       ___                            _    ")
	print("|_   _ `.                   .'   `.                         / |_  ")
	print("  | | `. \ __   _   _ .--. /  .-.  \  __   _   .---.  .--. `| |-' ")
	print("  | |  | |[  | | | [ `.-. || |   | | [  | | | / /__\\( (`\] | |   ")
	print(" _| |_.' / | \_/ |, | | | |\  `-'  \_ | \_/ |,| \__., `'.'. | |,  ")
	print("|______.'  '.__.'_/[___||__]`.___.\__|'.__.'_/ '.__.'[\__) )\__/  ")
	print("                                                                  ")
	print('    Welcome to DunQuest! A game of infinite possibilities!')
	print('')
	print('* play')
	if len(save_files) > 0:
		print('* load')
	print('* help')
	print('* quit')
	choice = input('> ')
	if choice == 'load' and len(save_files) > 0:
		menu_state = True
		while menu_state:
			print('Existing savefiles:')
			for i in save_files:
				print('* ' + i)
			print('What is your savename?')
			savename = input('> ')
			if valid_file_name(savename) and savename in save_files:
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
	elif choice == 'play':
		menu_state = True
		while menu_state:
			able_dungeons = list()
			for i in list_dungeons:
				if i not in dungeons_comp:
					able_dungeons.append(i)
			if len(able_dungeons) > 0:
				scene_splitter()
				print('Dungeons you can play: ')
				for i in able_dungeons:
					print('* ' + i)
				print('Which dungeon would you like to play?')
				choice = input('> ')
				if choice in list_dungeons and choice in able_dungeons:
					menu_state = False
					print('\n'*100)
					if len(dungeons_comp) < 1:
						print('What would you like your name to be?')
						choi = input('> ')
						pl.name = choi
					else:
						print('Welcome back ' + pl.name)
						time.sleep(2)
					print('\n'*100)
					du = Dungeon(choice)
					du.game_loop()
				else:
					print('Please enter a dungeon name you wish to play.')
					try:
						input("Press Enter to continue...")
					except SyntaxError:
						pass
			else:
				print('Sorry partner, you have completed all available dungeons.')
				print('Look out for more soon, or create your own!')
				try:
					input("Press Enter to continue...")
				except SyntaxError:
					pass
				sys.exit(1)
	else:
		print('Invalid Input.')
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
