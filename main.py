from helpers import *
import random

class Player:
	def __init__(self, name):
		self.name = name
		self.maxhealth = 100
		self.health = self.maxhealth
		self.attack = 2
		self.inventory = list()

	def attack(enemy):
		return random.randint(0, self.attack)

class Enemy:
	def __init__(self, name):
		self.name = name
		self.maxhealth = random.randint(50,100)
		self.health = self.maxhealth
		self.attack = random.randint(0,5)
		self.inventory = list()


def display_menu():
	print('------------------------------------------------')
	print('Welcome to the menu!')
	print('1) New Game')
	print('2) Load Game')
	print('3) Help')
	print('4) Exit')
	print('------------------------------------------------')
	option = input('-> ')
	if option == '1':
		start()
	elif option == '2':
		pass
	elif option == '3':
		pass
	elif option == '4':
		sys.exit()
	else:
		display_menu()

def start():
	print('What is your name?')
	option = input('-> ')
	global playerIG
	playerIG = Player(option)
	start1()

def start1():
	new_screen()
	print('Hello %s! How are you?' %(playerIG.name))

def prefight():
	global enemy
	enemynum = random.randint(1,2)
	if enemynum == 1:
		enemy = GoblinIG
	else:
		enemy = ZombieIG
	fight()

def fight():
	print('You are now battling a ' + enemy)

def new_screen():
	os.system('clear')
	print('------------------------------------------------')
	print('Player: %s  |  Health: %s/%s  | Inv: %s' %(playerIG.name, playerIG.health, playerIG.maxhealth, len(playerIG.inventory)))
	print('------------------------------------------------')


def __init__():
	create_project_dir('save_files')
	create_configs_file()
	global save_files
	save_files = get_save_files('save_files')

def debug_mode():
	__init__()
	print_list(save_files)
	display_menu()

debug_mode()