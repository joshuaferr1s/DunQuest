import random

class Character():

	def __init__(self, name = 'Player', hp = 100, ap = 20):
		self.name = name
		self.hp = hp
		self.ap = ap
		self.items = ['Sword', 'Health Potion']

	def take_dmg(self, dmg):
		self.hp = self.hp - dmg

	def is_dead(self):
		if self.hp < 1:
			return True
		else:
			return False

	def get_atk(self):
		atk = random.randint(0, self.ap)
		return atk

	def has_item(self, item):
		if item in self.items:
			return True
		else:
			return False

	def sneak(self):
		rnd = random.randint(0,1)
		if rnd == 0:
			return True
		else:
			return False

	def rnd_attack(self):
		atk = random.choice(['attack', 'defend'])
		return atk

class Combat_Manager():

	def check_attack(self, pc, npc):
		while not pc.is_dead() and not npc.is_dead():
			atk = self.check_answer('Attack or defend? ', ['attack', 'defend'])
			print('%s: %ss' %(pc.name, atk))
			npc_atk = npc.rnd_attack()
			print('%s: %ss' %(npc.name, npc_atk))
			if atk == 'attack':
				if npc_atk == 'attack':
					pc.take_dmg(npc.get_atk())
					npc.take_dmg(pc.get_atk())
				else:
					pc.take_dmg(npc.get_atk()/2)
					npc.take_dmg(pc.get_atk()/3)
			else:
				if npc_atk == 'attack':
					pc.take_dmg(npc.get_atk()/3)
					npc.take_dmg(pc.get_atk())
				else:
					print('You both block causing no damage.')
			print('Player has ' + str(pc.hp) + ' hitpoints.')
			print('NPC has ' + str(npc.hp) + ' hitpoints.')

	def check_answer(self, question, answers):
		answer = ''
		while answer not in answers:
			answer = input(question).lower()
		return answer

class Story():

	def __init__(self):
		self.cm = Combat_Manager()
		print('Welcome to Uther Underwood!')
		self.new_game()

	def check_answer(self, question, answers):
		answer = ''
		while answer not in answers:
			answer = input(question).lower()
		return answer

	def new_game(self):
		self.create_char()
		self.outside()

	def create_char(self):
		name = input('What is your name brave traveler? ')
		# CLASS SELECTION
		self.pc = Character(name)

	def dead(self):
		print('You have died.')
		answer = self.check_answer('Do you want to start again?', ['yes', 'no'])
		if answer == 'yes':
			self.new_game()
		else:
			print('GAME OVER!')

	def outside(self):
		print('After a long journey you have finally arrived to the dungeon where...')
		print('Uther Underwood is belived to be hiding. He is sure to have plenty...')
		print('of protection of traps layed out to defend himself but if anyone is up...')
		print('to the challenge it is you %s of Aregarath, son of Ireth.' %(self.pc.name))
		print('May the gods look kindly upon you.')

		answer = self.check_answer('The Entrance to the dungeon is ahead of you. Do you enter? ', ['yes', 'no'])
		
		if answer == 'yes':
			self.dungeon_entrance()
		else:
			print('A booming voice proclaims that you have failed!')
			print('Suddenly the ceiling above you drops and crushed you flat.')
			self.dead()

	def dungeon_entrance(self):
		skel = Character('Skeleton', 60, 8)

		print('You enter the dungeon. Before you is a skeleton who hasn\'t notices you yet.')
		options = ['flee', 'attack', 'sneak into the next room']
		print('You can:')
		for item in options:
			print(' > ' + item)
		answer = self.check_answer('What will you do? ', options)
		if answer == 'flee':
			print('You are a coward ' + self.pc.name + '!')
			print('Suddenly the ceiling above you drops and crushed you flat.')
			self.dead()
		elif answer == 'attack':
			print('You catch the skeleton by surprise!')
			self.cm.check_attack(self.pc, skel)
			if self.pc.is_dead():
				print('The skeleton delivered a crushing blow killing you!')
				self.dead()
			else:
				print('You move onto the next room.')
				self.dungeon_room_1()
		elif answer == 'sneak into the next room':
			print('You attempt to sneak to the next room.')
			if self.pc.sneak():
				print('You successfully sneak into the next room.')
				self.dungeon_room_1()
			else:
				print('You are caught trying to sneak into the next room by the skeleton!')
				print('He attacks you!')
		else:
			print('The skeleton catches you and attacks!')
			self.cm.check_attack(self.pc, skel)



	def dungeon_room_1(self):
		pass










new_game = Story()