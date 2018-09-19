import random, time, sys, math, textwrap
from file_helpers import *


class Player():
    def __init__(self, name, gold=0, maxhp=20, ap=5, dp=1, items=[]):
        self.name = name
        self.gold = gold
        self.maxhp = maxhp
        self.hp = self.maxhp
        self.ap = ap
        self.dp = dp
        self.inventory = items
        self.equipped = []
        self.item_fre = dict()

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

    def use_potion(self, potion_type):
        global heal_effectors
        if (self.hp + heal_effectors[potion_type]['heal']) > self.maxhp:
            self.hp = self.maxhp
        else:
            self.hp += heal_effectors[potion_type]['heal']
        print(heal_effectors[potion_type]['desc'])

    def gui(self):
        borderfy_text('Name: ' + self.name + ' || HP: ' + str(self.hp) +
                      ' || Gold: ' + str(self.gold))

    def inventory_updater(self):
        displayed = list()
        self.item_fre = dict()
        for ite in self.inventory:
            if ite in self.item_fre:
                self.item_fre[ite] += 1
            else:
                self.item_fre[ite] = 1
        print('Inventory:')
        for i in self.inventory:
            if i in self.equipped and i not in displayed:
                print('* (' + str(self.item_fre[i]) + ') ' + i + '(E)')
                displayed.append(i)
            elif i not in displayed:
                print('* (' + str(self.item_fre[i]) + ') ' + i)
                displayed.append(i)

    def inventory_handler(self):
        global heal_effectors, armorer, blacksmith
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
                    if opts[1] not in self.inventory:
                        print(opts[1] + ' is not in your inventory.')
                    elif opts[1] not in self.equipped and opts[1] != '':
                        if opts[1] in armorer:
                            self.equipped.append(opts[1])
                            self.dp += armorer[opts[1]]['mod']
                            print('You have now equipped a ' + opts[1])
                        elif opts[1] in blacksmith:
                            self.equipped.append(opts[1])
                            self.ap += blacksmith[opts[1]]['mod']
                            print('You are now wearing a ' + opts[1])
                        else:
                            print(opts[1] + ' is not equipable.')
                    else:
                        print('You have already equipped this item.')
                except IndexError:
                    print(
                        'Please enter what item you would like to equip after you type "equip".'
                    )
            elif opts[0] == 'unequip':
                try:
                    if opts[1] not in self.equipped:
                        print(opts[1] + ' is not equipped.')
                    elif opts[1] != '' and opts[1] in self.equipped:
                        if opts[1] in armorer:
                            self.equipped.remove(opts[1])
                            self.dp -= armorer[opts[1]]['mod']
                            print('You are no longer wearing a ' + opts[1])
                        elif opts[1] in blacksmith:
                            self.equipped.remove(opts[1])
                            self.ap -= blacksmith[opts[1]]['mod']
                            print('You are no longer using a ' + opts[1])
                        else:
                            print(opts[1] + ' is not equipable.')
                    else:
                        print('GAH')
                except IndexError:
                    print(
                        'Please enter what item you would like to unequip after you type "unequip".'
                    )
            elif opts[0] == 'drop':
                try:
                    if opts[1] not in self.inventory:
                        print('You do not have this item.')
                    elif opts[1] in self.equipped and self.item_fre[opts[1]] == 1:
                        print('You must first unequip ' + opts[1])
                    else:
                        self.inventory.remove(opts[1])
                        print(opts[1] +
                              ' has now been removed from your inventory.')
                except IndexError:
                    print(
                        'Please enter what item you would like to drop after you type "drop".'
                    )
            elif opts[0] == 'use':
                try:
                    if opts[1] not in self.inventory:
                        print('You do not have this item.')
                    else:
                        if opts[1] in heal_effectors:
                            self.use_potion(opts[1])
                            self.inventory.remove(opts[1])
                            self.item_fre[opts[1]] -= 1
                except IndexError:
                    print(
                        'Please enter what item you would like to use after you type "use".'
                    )
            elif option == 'back':
                state = False
            else:
                print('Invalid Input.')


class Enemy():
    def __init__(self, name, cr):
        self.name = name
        self.cr = cr
        self.maxhp = random.randint(0, 7) + self.cr * 3
        self.hp = self.maxhp
        self.ap = random.randint(2, 5) + self.cr * 2
        self.loot = {
            1: [
                '', '', '', 'rusty_dagger', 'rusty_dagger', 'rusty_dagger',
                'healing_potion', 'healing_potion', 'healing_potion',
                'healing_potion', 'healing_potion', 'healing_potion',
                'leather_pants', 'leather_pants', 'leather_pants',
                'leather_pants', 'leather_pants', 'leather_pants',
                'leather_pants', 'leather_pants', 'purple_liquid'
            ],
            2: [
                '', '', '', 'rusty_dagger', 'healing_potion', 'healing_potion',
                'healing_potion', 'healing_potion', 'healing_potion',
                'healing_potion', 'sword', 'leather_helmet',
                'leather_breastplate', 'leather_boots', 'leather_pants',
                'artifact', 'purple_liquid'
            ],
            3: [
                '', 'rusty_dagger', 'rusty_dagger', 'rusty_dagger',
                'healing_potion', 'healing_potion', 'healing_potion',
                'healing_potion', 'healing_potion', 'healing_potion', 'sword',
                'battle-axe', 'leather_helmet', 'leather_breastplate',
                'leather_boots', 'leather_pants', 'artifact', 'purple_liquid'
            ]
        }

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
        randchoice = random.randint(0, len(self.loot[self.cr]) - 1)
        return self.loot[self.cr][randchoice]

    def drop_gold(self):
        return random.randint(0, self.cr)

    def gui(self):
        borderfy_text('Name: ' + self.name + ' || HP: ' + str(self.hp))


class Npc():
    def __init__(self, name='npc', gold=10):
        self.name = name
        self.gold = gold
        self.met = False
        self.trust = False
        self.item_fre = dict()

    def interact(self):
        if not self.met:
            self.introduction()
        self.trust_test()
        self.set_prices()
        self.shop()

    def introduction(self):
        self.met = True
        print(self.name + ': Well howdy, young traveller!')
        print(self.name +
              ": I seem to have lost my way but I ain't lost my wears.")

    def gui(self):
        global pl
        borderfy_text('Name: ' + pl.name + ' || HP: ' + str(pl.hp) +
                      ' || Gold: ' + str(pl.gold))


class Merchant(Npc):
    def __init__(self,
                 name='Merchant',
                 gold=10,
                 items=list(),
                 items_buy=list(),
                 items_sell=list()):
        super().__init__(name, gold)
        self.merchant = {
            'healing_potion': {
                'buy': 4,
                'sell': 2
            },
            'artifact': {
                'buy': 7,
                'sell': 5
            },
            'purple_liquid': {
                'buy': 25,
                'sell': 23
            }
        }

    def new(self, name, gold):
        self.name = name
        self.gold = gold
        self.met = False
        self.trust = False

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
                    temp_text = textwrap.wrap(
                        self.name +
                        ": Pleased to make your acquaintance! Thank you for telling me your name, it's nice to be nice!",
                        70)
                    print(self.name + ': Well hello there ' + pl.name)
                    for line in temp_text:
                        print(textwrap.dedent(line))
                    loop = False
                elif choi == 'no':
                    print(self.name + ': Well fine be like that!')
                    loop = False
                else:
                    print('Invalid Input.')

    def set_prices(self):
        if not self.trust:
            for i in self.merchant:
                self.merchant[i]['buy'] += 2
                self.merchant[i]['sell'] -= 2

    def shop(self):
        global pl
        loop = True
        while loop:
            self.gui()
            print('--------------------------------')
            pl.inventory_updater()
            self.item_fre = pl.item_fre
            print('--------------------------------')
            print('Items:')
            for i in self.merchant:
                print('* ' + i + ' | ' + str(self.merchant[i]['buy']) + ' | ' +
                      str(self.merchant[i]['sell']))
            print('')
            print('Actions:')
            print('* buy ____')
            print('* sell ____')
            print('* check inventory')
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
                print('Item | Sale Price | From You Price')
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass
            elif choice == 'check inventory':
                pl.inventory_handler()
            elif choi == 'leave':
                print(self.name + ': Farewell and good luck!')
                loop = False
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass
            elif chac != 'Failed' and choic[0] == 'buy' and choic[1] in self.merchant:
                if pl.gold >= self.merchant[choic[1]]['buy']:
                    print(self.name + ': You are now the proud owner of ' +
                          choic[1])
                    pl.gold -= self.merchant[choic[1]]['buy']
                    self.gold += self.merchant[choic[1]]['buy']
                    pl.inventory.append(choic[1])
                    try:
                        input("Press Enter to continue...")
                    except SyntaxError:
                        pass
                else:
                    print(
                        self.name +
                        ': I apologize kind sir but you do not have the required funds.'
                    )

            elif chac != 'Failed' and choic[0] == 'sell' and choic[1] in self.merchant:
                if self.gold >= self.merchant[choic[1]]['sell']:
                    if choic[1] in pl.inventory:
                        if choic[1] not in pl.equipped or self.item_fre[choic[1]] > 1:
                            print(self.name + ': Thanks for the ' + choic[1])
                            pl.gold += self.merchant[choic[1]]['sell']
                            self.gold -= self.merchant[choic[1]]['sell']
                            pl.inventory.remove(choic[1])
                            try:
                                input("Press Enter to continue...")
                            except SyntaxError:
                                pass
                        else:
                            print('Remove the item first.')
                    else:
                        print(
                            self.name +
                            ': Are you trying to rob me child?! I know you do not have that!'
                        )
                else:
                    print(
                        self.name +
                        ': I apologize kind sir but I do not have the required funds.'
                    )
            elif chac != 'Failed' and (choic[0] == 'buy' or choic[0] == 'sell'
                                       ) and choic[1] not in self.merchant:
                print(self.name +
                      ": Sorry partner, we don't deal with that here.")
            else:
                print('Invalid Input.')
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass


class Armorer(Npc):
    def __init__(self,
                 name='Armorer',
                 gold=10,
                 items=list(),
                 items_buy=list(),
                 items_sell=list()):
        super().__init__(name, gold)
        self.armorer = armorer = {
            'leather_boots': {
                'mod': 1,
                'buy': 1,
                'sell': 1
            },
            'leather_pants': {
                'mod': 1,
                'buy': 2,
                'sell': 1
            },
            'leather_breastplate': {
                'mod': 2,
                'buy': 3,
                'sell': 1
            },
            'leather_helmet': {
                'mod': 1,
                'buy': 2,
                'sell': 1
            },
            'elven_boots': {
                'mod': 3,
                'buy': 5,
                'sell': 2
            },
            'elven_pants': {
                'mod': 3,
                'buy': 6,
                'sell': 3
            },
            'elven_breastplate': {
                'mod': 4,
                'buy': 7,
                'sell': 4
            },
            'elven_helmet': {
                'mod': 3,
                'buy': 5,
                'sell': 3
            },
            'mithril_boots': {
                'mod': 6,
                'buy': 10,
                'sell': 8
            },
            'mithril_pants': {
                'mod': 6,
                'buy': 11,
                'sell': 9
            },
            'mithril_breastplate': {
                'mod': 7,
                'buy': 12,
                'sell': 10
            },
            'mithril_helmet': {
                'mod': 6,
                'buy': 10,
                'sell': 8
            }
        }

    def new(self, name, gold):
        self.name = name
        self.gold = gold
        self.met = False
        self.trust = False

    def introduction(self):
        self.met = True
        print(self.name + ': What do you want?!')
        print(self.name + ": You here to buy something?!")

    def trust_test(self):
        if not self.trust:
            loop = True
            while loop:
                print(self.name + ": Are you gonna tell me your name?!")
                print('* yes')
                print('* no')
                choi = input('> ')
                if choi == 'yes':
                    self.trust = True
                    print(self.name + ': Hi, ' + pl.name)
                    loop = False
                elif choi == 'no':
                    print(self.name + ': You cheeky sod!')
                    loop = False
                else:
                    print('Invalid Input.')

    def set_prices(self):
        if not self.trust:
            for i in self.armorer:
                self.armorer[i]['buy'] += 2
                self.armorer[i]['sell'] -= 2

    def shop(self):
        global pl
        loop = True
        while loop:
            self.gui()
            print('--------------------------------')
            pl.inventory_updater()
            self.item_fre = pl.item_fre
            print('--------------------------------')
            print('Items:')
            for i in self.armorer:
                print('* ' + i + ' | ' + str(self.armorer[i]['buy']) + ' | ' +
                      str(self.armorer[i]['sell']))
            print('')
            print('Actions:')
            print('* buy ____')
            print('* sell ____')
            print('* check inventory')
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
                print('Item | Sale Price | From You Price')
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass
            elif choice == 'check inventory':
                pl.inventory_handler()
            elif choi == 'leave':
                print(self.name + ': Peace and quiet at last.')
                loop = False
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass
            elif chac != 'Failed' and choic[0] == 'buy' and choic[1] in self.armorer:
                if pl.gold >= self.armorer[choic[1]]['buy']:
                    print(self.name + ': Here is your ' + choic[1])
                    pl.gold -= self.armorer[choic[1]]['buy']
                    self.gold += self.armorer[choic[1]]['buy']
                    pl.inventory.append(choic[1])
                    try:
                        input("Press Enter to continue...")
                    except SyntaxError:
                        pass
                else:
                    print(
                        self.name +
                        ': Gonna pay me in buttons? Come back when you have the gold.'
                    )

            elif chac != 'Failed' and choic[0] == 'sell' and choic[1] in self.armorer:
                if self.gold >= self.armorer[choic[1]]['sell']:
                    if choic[1] in pl.inventory:
                        if choic[1] not in pl.equipped or self.item_fre[choic[1]] > 1:
                            print(self.name + ': Thanks for the ' + choic[1])
                            pl.gold += self.armorer[choic[1]]['sell']
                            self.gold -= self.armorer[choic[1]]['sell']
                            pl.inventory.remove(choic[1])
                            try:
                                input("Press Enter to continue...")
                            except SyntaxError:
                                pass
                        else:
                            print(self.name + ": Take it off first!")
                    else:
                        print(
                            self.name +
                            ': Are you trying to rob me?! I know you do not have that!'
                        )
                else:
                    print(self.name + ": Ain't got the cash for that")
            elif chac != 'Failed' and (choic[0] == 'buy' or choic[0] == 'sell'
                                       ) and choic[1] not in self.armorer:
                print(self.name + ": We don't deal with that here.")
            else:
                print('Invalid Input.')
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass


class Blacksmith(Npc):
    def __init__(self,
                 name='Blacksmith',
                 gold=10,
                 items=list(),
                 items_buy=list(),
                 items_sell=list()):
        super().__init__(name, gold)
        self.blacksmith = blacksmith = {
            'rusty_dagger': {
                'mod': 1,
                'buy': 2,
                'sell': 1
            },
            'dagger': {
                'mod': 2,
                'buy': 5,
                'sell': 3
            },
            'sword': {
                'mod': 3,
                'buy': 7,
                'sell': 5
            },
            'battle-axe': {
                'mod': 4,
                'buy': 10,
                'sell': 8
            },
            'mace': {
                'mod': 5,
                'buy': 8,
                'sell': 6
            },
            'bow': {
                'mod': 6,
                'buy': 12,
                'sell': 10
            },
            'spear': {
                'mod': 7,
                'buy': 14,
                'sell': 12
            },
            'crossbow': {
                'mod': 8,
                'buy': 18,
                'sell': 16
            }
        }

    def new(self, name, gold):
        self.name = name
        self.gold = gold
        self.met = False
        self.trust = False

    def introduction(self):
        self.met = True
        print(self.name + ': Welcome to my establishment.')
        print(self.name + ': Feel free to browse my stock.')

    def set_prices(self):
        if not self.trust:
            for i in self.blacksmith:
                self.blacksmith[i]['buy'] += 2
                self.blacksmith[i]['sell'] -= 2

    def trust_test(self):
        if not self.trust:
            loop = True
            while loop:
                print(self.name + ': To whom am I speaking?')
                print('* tell_name')
                print('* fake_name')
                choi = input('> ')
                if choi == 'tell_name':
                    self.trust = True
                    print(self.name + ': Well met, ' + pl.name)
                    loop = False
                elif choi == 'fake_name':
                    print(self.name + ': So be it.')
                    loop = False
                else:
                    print('Invalid Input.')

    def shop(self):
        global pl
        loop = True
        while loop:
            self.gui()
            print('--------------------------------')
            pl.inventory_updater()
            self.item_fre = pl.item_fre
            print('--------------------------------')
            print('Items:')
            for i in self.blacksmith:
                print('* ' + i + ' | ' + str(self.blacksmith[i]['buy']) +
                      ' | ' + str(self.blacksmith[i]['sell']))
            print('')
            print('Actions:')
            print('* buy ____')
            print('* sell ____')
            print('* check inventory')
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
                print('Item | Sale Price | From You Price')
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass
            elif choice == 'check inventory':
                pl.inventory_handler()
            elif choi == 'leave':
                print(self.name + ': See you soon.')
                loop = False
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass
            elif chac != 'Failed' and choic[0] == 'buy' and choic[1] in self.blacksmith:
                if pl.gold >= self.blacksmith[choic[1]]['buy']:
                    print(self.name + ': Here is your ' + choic[1])
                    pl.gold -= self.blacksmith[choic[1]]['buy']
                    self.gold += self.blacksmith[choic[1]]['buy']
                    pl.inventory.append(choic[1])
                    try:
                        input("Press Enter to continue...")
                    except SyntaxError:
                        pass
                else:
                    print(self.name +
                          ': Come back with some gold and then we can talk.')

            elif chac != 'Failed' and choic[0] == 'sell' and choic[1] in self.blacksmith:
                print('made it to sell')
                if self.gold >= self.blacksmith[choic[1]]['sell']:
                    print('gold checked')
                    if choic[1] in pl.inventory:
                        print('is in inventory')
                        if (choic[1] not in pl.equipped) or (
                                self.item_fre[choic[1]] > 1):
                            print(self.name + ': Thanks for the ' + choic[1])
                            pl.gold += self.blacksmith[choic[1]]['sell']
                            self.gold -= self.blacksmith[choic[1]]['sell']
                            pl.inventory.remove(choic[1])
                            try:
                                input("Press Enter to continue...")
                            except SyntaxError:
                                pass
                        else:
                            print('Remove the item first.')
                    else:
                        print(
                            self.name +
                            ": Don't take me for a fool child, I know you do not posses that."
                        )
                else:
                    print(self.name +
                          ": I don't seem to have the funds for that.")
            elif chac != 'Failed' and (choic[0] == 'buy' or choic[0] == 'sell'
                                       ) and choic[1] not in self.blacksmith:
                print(self.name + ": That is not one of our specialties.")
            else:
                print('Invalid Input.')
                try:
                    input("Press Enter to continue...")
                except SyntaxError:
                    pass


class Dungeon():
    def __init__(self, dungeon='dungeon1', start_pos="1"):
        self.cur_dungeon = dungeon
        self.dungeon = game_data['dungeons'][dungeon]
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
        borderfy_text(
            'Name: ' + pl.name + ' || HP: ' + str(pl.hp) + ' || Gold: ' +
            str(pl.gold) + ' || Location: ' + str(self.current()))

    def game_loop(self):
        global market_data, game_data
        while self.check_game_state():
            self.dungeon_description()
            self.room_handler()
            self.move_room()
            scene_splitter()
        self.win_handler()
        try:
            ma = Market(self.dungeon['100']['market'])
            ma.main_market()
            scene_splitter()
            game_data['market_data'][self.dungeon['100']['market']] = dict()
            game_data['market_data'][self.dungeon['100']['market']] = ma.market
        except KeyError:
            pass
        game_data['dungeons_comp'].append(self.cur_dungeon)
        save_progress()

    def current(self):
        return self.dungeon[self.current_pos]['name']

    def dungeon_description(self):
        try:
            if self.current_pos == 1 and self.current_pos not in self.visited and self.dungeon[self.
                                                                                               current_pos]['desc'] != '':
                print('/' * 70)
                print('~' * 70)
                print('/' * 70)
                dungeon_intro = textwrap.wrap(
                    self.dungeon[self.current_pos]['desc'], 70)
                for i in dungeon_intro:
                    print(i)
                print('/' * 70)
                print('~' * 70)
                print('/' * 70)
                wfunc()
        except KeyError:
            pass

    def get_moves(self):
        print('You can go:')
        for i in self.dungeon[self.current_pos]:
            if i == 'name' or i == 'desc' or i == 'description' or i == 'loot' or i == 'enemy' or i == 'enemy_cr' or i == 'npc' or i == 'gold' or i == 'market':
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
            pl.inventory_handler()
        elif move == 'talk to npc' and self.dungeon[self.
                                                    current_pos]['npc'] != '':
            scene_splitter()
            self.npc_handler(self.dungeon[self.current_pos]['npc'])
        else:
            print('Invalid direction')

    def describe_room(self):
        if (self.current_pos not in self.visited):
            try:
                print('Description: ' +
                      self.dungeon[self.current_pos]['description'])
            except KeyError:
                pass
        else:
            pass

    def death_handler(self, how):
        print('\n' * 1000)
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
        print('Name: ' + pl.name + ' || HP: ' + str(pl.hp) + '/' +
              str(pl.maxhp) + ' || + Gold: ' + str(pl.gold))
        print('Room where you died: ' + self.dungeon[self.current_pos]['name'])
        pl.inventory_updater()

        wfunc()
        sys.exit(1)

    def win_handler(self):
        print('\n' * 100)
        print(
            " ____  ____                  ____    ____               __          _____  _    "
        )
        print(
            "|_  _||_  _|                |_   \  /   _|             |  ]        |_   _|/ |_  "
        )
        print(
            "  \ \  / / .--.   __   _      |   \/   |   ,--.    .--.| | .---.     | | `| |-' "
        )
        print(
            "   \ \/ // .'`\ \[  | | |     | |\  /| |  `'_\ : / /'`\' |/ /__\\    | |  | |   "
        )
        print(
            "   _|  |_| \__. | | \_/ |,   _| |_\/_| |_ // | |,| \__/  || \__.,   _| |_ | |,  "
        )
        print(
            "  |______|'.__.'  '.__.'_/  |_____||_____|\'-;__/ '.__.;__]'.__.'  |_____|\__/  "
        )
        print(
            "                                                                                "
        )
        print("Upon making it out...")
        print('Name: ' + pl.name + ' || HP: ' + str(pl.hp) + '/' +
              str(pl.maxhp) + ' || Gold: ' + str(pl.gold))
        pl.inventory_updater()
        wfunc()
        print('\n' * 100)

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
                self.en.take_dmg(pl.get_atk())
                if not self.en.is_dead():
                    dam = self.en.get_atk() - math.floor(pl.dp / 2)
                    if dam > 0:
                        pl.take_dmg(dam)
                    else:
                        pass
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
                npc_merchant.new('Merchant', 10)
            npc_merchant.interact()

        elif npc == 'armorer':
            if self.current_pos not in self.visited:
                npc_armorer.new('Armorer', 10)
            npc_armorer.interact()
        elif npc == 'blacksmith':
            if self.current_pos not in self.visited:
                npc_blacksmith.new('Blacksmith', 10)
            npc_blacksmith.interact()
        else:
            pass
        self.visited.append(self.current_pos)

    def room_handler(self):
        if self.dungeon[self.current_pos]['name'] == 'spike_pit':
            self.death_handler('spike_pit')
        if self.dungeon[self.
                        current_pos]['gold'] != 0 and self.current_pos not in self.visited:
            pl.gold += int(self.dungeon[self.current_pos]['gold'])
        self.gui()

        #If enemy present, fight
        if self.dungeon[self.
                        current_pos]['enemy'] != '' and self.current_pos not in self.visited:
            self.en = Enemy(self.dungeon[self.current_pos]['enemy'],
                            self.dungeon[self.current_pos]['enemy_cr'])
            print('You come across a ' + self.en.name + '!')
            print('Prepare to fight!')
            time.sleep(2)
            self.battler()
            print('You defeated the pathetic ' + self.en.name + '!')
            fight_loot = self.en.drop_loot()
            fight_gold = self.en.drop_gold()
            if fight_loot == '':
                print("The lousy " + self.en.name +
                      " didn't have any items on it!")
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
        if self.dungeon[self.
                        current_pos]['loot'] != '' and self.current_pos not in self.visited:
            pl.inventory.append(self.dungeon[self.current_pos]['loot'])
            #self.gui()
            print('You find ' + self.dungeon[self.current_pos]['loot'])
            print('--------------------------------------------')
        else:
            pass

        #If gold present, take
        if self.dungeon[self.
                        current_pos]['gold'] != 0 and self.current_pos not in self.visited:
            #pl.gold += int(self.dungeon[self.current_pos]['gold'])
            print('You find ' + str(self.dungeon[self.current_pos]['gold']) +
                  ' gold')
            print('--------------------------------------------')
        else:
            pass

        self.describe_room()
        if self.dungeon[self.current_pos]['npc'] == '':
            self.visited.append(self.current_pos)


class Market():
    def __init__(self, location):
        global game_data
        self.location = location
        self.running = True
        self.market = dict()
        if game_data['savename'] not in game_data['saves']:
            self.market[self.location] = game_data['markets'][self.location]
        elif game_data['savename'] in game_data['saves'] and self.location in game_data['saves'][game_data['savename']]["market_data"]:
            self.market[self.location] = game_data['saves'][game_data['savename']]["market_data"][
                self.location]
        else:
            self.market[self.location] = game_data['markets'][self.location]

    def market_description(self):
        print('/' * 70)
        print('~' * 70)
        print('/' * 70)
        market_de = textwrap.wrap(self.market[self.location]['desc'], 70)
        for i in market_de:
            print(i)
        print('/' * 70)
        print('~' * 70)
        print('/' * 70)
        try:
            input("Press Enter to continue...")
        except SyntaxError:
            pass
        print('\n' * 100)

    def gui(self):
        borderfy_text('Name: ' + pl.name + ' || HP: ' + str(pl.hp) +
                      ' || Gold: ' + str(pl.gold) + ' || Location: ' +
                      self.market[self.location]['name'])

    def main_market(self):
        if self.market[self.location]['visited'] == False:
            self.market_description()
        while self.running == True:
            self.gui()
            print('What would you like to do?')
            print('* visit merchant')
            print('* visit armorer')
            print('* visit blacksmith')
            print('* check inventory')
            print('* leave')
            choice = input('> ')
            if choice == 'visit merchant':
                if self.market[self.location]['merchant']['met'] == False:
                    self.market[self.location]['merchant']['met'] = True
                    npc_merchant.new(
                        'Merchant',
                        self.market[self.location]['merchant']['gold'])
                npc_merchant.met = self.market[self.location]['merchant'][
                    'met']
                npc_merchant.trust = self.market[self.location]['merchant'][
                    'trust']
                npc_merchant.interact()
                self.market[self.location]['merchant'][
                    'met'] = npc_merchant.met
                self.market[self.location]['merchant'][
                    'trust'] = npc_merchant.trust
                self.market[self.location]['merchant'][
                    'gold'] = npc_merchant.gold
            elif choice == 'visit armorer':
                if self.market[self.location]['armorer']['met'] == False:
                    self.market[self.location]['armorer']['met'] = True
                    npc_armorer.new(
                        'Armorer',
                        self.market[self.location]['armorer']['gold'])
                npc_armorer.met = self.market[self.location]['armorer']['met']
                npc_armorer.trust = self.market[self.location]['armorer'][
                    'trust']
                npc_armorer.interact()
                self.market[self.location]['armorer']['met'] = npc_armorer.met
                self.market[self.location]['armorer'][
                    'trust'] = npc_armorer.trust
                self.market[self.location]['armorer'][
                    'gold'] = npc_armorer.gold
            elif choice == 'visit blacksmith':
                if self.market[self.location]['blacksmith']['met'] == False:
                    self.market[self.location]['blacksmith']['met'] = True
                    npc_blacksmith.new(
                        'Blacksmith',
                        self.market[self.location]['blacksmith']['gold'])
                npc_blacksmith.met = self.market[self.location]['blacksmith'][
                    'met']
                npc_blacksmith.trust = self.market[self.location][
                    'blacksmith']['trust']
                npc_blacksmith.interact()
                self.market[self.location]['blacksmith'][
                    'met'] = npc_blacksmith.met
                self.market[self.location]['blacksmith'][
                    'trust'] = npc_blacksmith.trust
                self.market[self.location]['blacksmith'][
                    'gold'] = npc_blacksmith.gold
            elif choice == 'check inventory':
                pl.inventory_handler()
            elif choice == 'leave':
                self.running = False
            else:
                print('Invalid Input.')
        self.update_ma_state()

    def update_ma_state(self):
        global npc_merchant, npc_armorer, npc_blacksmith
        self.market[self.location]['visited'] = True
        self.market[self.location]['merchant']['met'] = npc_merchant.met
        self.market[self.location]['merchant']['trust'] = npc_merchant.trust
        self.market[self.location]['merchant']['gold'] = npc_merchant.gold
        self.market[self.location]['armorer']['met'] = npc_armorer.met
        self.market[self.location]['armorer']['trust'] = npc_armorer.trust
        self.market[self.location]['armorer']['gold'] = npc_armorer.gold
        self.market[self.location]['blacksmith']['met'] = npc_blacksmith.met
        self.market[self.location]['blacksmith'][
            'trust'] = npc_blacksmith.trust
        self.market[self.location]['blacksmith']['gold'] = npc_blacksmith.gold


## UPDATED ##
def scene_splitter():
    print('/' * 70)
    print('/' * 70)
    print('/' * 70)


## UPDATED ##
def wfunc():
    try:
        input('Press Enter to continue...')
    except SyntaxError:
        pass


## UPDATED ##
def save_game():
    global game_data
    if not os.path.isfile('Resources/saves.json'):
        write_file('Resources/saves.json', '')

    game_data['saves'][game_data['savename']] = {}
    game_data['saves'][game_data['savename']]['completed'] = game_data['dungeons_comp']
    game_data['saves'][game_data['savename']]['inventory'] = pl.inventory
    game_data['saves'][game_data['savename']]['equipped'] = pl.equipped
    game_data['saves'][game_data['savename']]['name'] = pl.name
    game_data['saves'][game_data['savename']]['gold'] = pl.gold
    game_data['saves'][game_data['savename']]['maxhp'] = pl.maxhp
    game_data['saves'][game_data['savename']]['hp'] = pl.hp
    game_data['saves'][game_data['savename']]['ap'] = pl.ap
    game_data['saves'][game_data['savename']]['dp'] = pl.dp
    game_data['saves'][game_data['savename']]['market_data'] = game_data['market_data']

    write_dict_data('Resources/saves.json', game_data['saves'])


## UPDATED ##
def save_progress():
    global game_data
    get_save_data()
    menu_state = True
    while menu_state:
        print('Would you like to save your progress?')
        print('* yes')
        print('* no')
        choice = input('> ')

        if choice == 'yes':
            print('Existing savefiles:')
            for i in game_data['saves']:
                print('* ' + i)
            print('What would you like your savename to be?')
            game_data['savename'] = input('> ')
            if game_data['savename'] not in game_data['saves']:
                save_game()
                menu_state = False
            else:
                temp_menu = True
                while temp_menu:
                    print('Would you like to overwrite previous savefiles?')
                    print('* yes')
                    print('* no')
                    choice = input('> ')
                    if choice == 'yes':
                        save_game()
                        temp_menu = False
                        menu_state = False
                    elif choice == 'no':
                        temp_menu = False
                    else:
                        print('Invalid input.')
        elif choice == 'no':
            menu_state = False
        else:
            print('Invalid Input.')
            scene_splitter()


## UPDATED ##
def load_game():
    global game_data

    game_data['dungeons_comp'] = game_data['saves'][game_data['savename']]['completed']
    pl.inventory = game_data['saves'][game_data['savename']]['inventory']
    pl.equipped = game_data['saves'][game_data['savename']]['equipped']
    pl.name = game_data['saves'][game_data['savename']]['name']
    pl.gold = game_data['saves'][game_data['savename']]['gold']
    pl.maxhp = game_data['saves'][game_data['savename']]['maxhp']
    pl.hp = game_data['saves'][game_data['savename']]['hp']
    pl.ap = game_data['saves'][game_data['savename']]['ap']
    pl.dp = game_data['saves'][game_data['savename']]['dp']
    game_data['market_data'] = game_data['saves'][game_data['savename']]['market_data']

    print('Successfully loaded player profile: ' + game_data['savename'] + '.')
    wfunc()


## UPDATED ##
def get_save_data():
    global game_data
    try:
        game_data['saves'] = load_dict('Resources/saves.json')
    except FileNotFoundError:
        pass


##### Game Initialization #####
pl = Player('Player')
game_data = {
    'running': True,
    'dungeons': load_dict('Resources/dungeons.json'),
    'dungeons_comp': [],
    'markets': load_dict('Resources/markets.json'),
    'market_data': {},
    'savename': '',
    'saves': {}
}


market = dict()
npc_merchant = Merchant()
npc_armorer = Armorer()
npc_blacksmith = Blacksmith()
merchant = {
    'healing_potion': {
        'buy': 4,
        'sell': 2
    },
    'artifact': {
        'buy': 7,
        'sell': 5
    },
    'purple_liquid': {
        'buy': 25,
        'sell': 23
    }
}
armorer = {
    'leather_boots': {
        'mod': 1,
        'buy': 1,
        'sell': 1
    },
    'leather_pants': {
        'mod': 1,
        'buy': 2,
        'sell': 1
    },
    'leather_breastplate': {
        'mod': 2,
        'buy': 3,
        'sell': 1
    },
    'leather_helmet': {
        'mod': 1,
        'buy': 2,
        'sell': 1
    },
    'elven_boots': {
        'mod': 3,
        'buy': 5,
        'sell': 2
    },
    'elven_pants': {
        'mod': 3,
        'buy': 6,
        'sell': 3
    },
    'elven_breastplate': {
        'mod': 4,
        'buy': 7,
        'sell': 4
    },
    'elven_helmet': {
        'mod': 3,
        'buy': 5,
        'sell': 3
    },
    'mithril_boots': {
        'mod': 6,
        'buy': 10,
        'sell': 8
    },
    'mithril_pants': {
        'mod': 6,
        'buy': 11,
        'sell': 9
    },
    'mithril_breastplate': {
        'mod': 7,
        'buy': 12,
        'sell': 10
    },
    'mithril_helmet': {
        'mod': 6,
        'buy': 10,
        'sell': 8
    }
}
blacksmith = {
    'rusty_dagger': {
        'mod': 1,
        'buy': 2,
        'sell': 1
    },
    'dagger': {
        'mod': 2,
        'buy': 5,
        'sell': 3
    },
    'sword': {
        'mod': 3,
        'buy': 7,
        'sell': 5
    },
    'battle-axe': {
        'mod': 4,
        'buy': 10,
        'sell': 8
    },
    'mace': {
        'mod': 5,
        'buy': 8,
        'sell': 6
    },
    'bow': {
        'mod': 6,
        'buy': 12,
        'sell': 10
    },
    'spear': {
        'mod': 7,
        'buy': 14,
        'sell': 12
    },
    'crossbow': {
        'mod': 8,
        'buy': 18,
        'sell': 16
    }
}
heal_effectors = {
    'healing_potion': {
        'heal': 5,
        'desc': 'You used a healing_potion.'
    },
    'purple_liquid': {
        'heal': 10000,
        'desc': 'You used a vial of purple_liquid.'
    },
    'nutella': {
        'heal': 8,
        'desc': 'You consumed a jar of nutella.'
    }
}

## UPDATED ##
# Game loop
while game_data['running']:
    get_save_data()
    print('\n' * 100)
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
    if len(game_data['saves']) > 0:
        print('* load')
    print('* help')
    print('* quit')
    choice = input('> ')

    if choice == 'load' and len(game_data['saves']) > 0:
        menu_state = True
        while menu_state:
            print('Existing savefiles:')
            for i in game_data['saves']:
                print('* ' + i)
            print('What is your savename?')
            game_data['savename'] = input('> ')
            if game_data['savename'] in game_data['saves']:
                load_game()
                menu_state = False
            else:
                print('Invalid savename.')
    elif choice == 'help':
        print('Coming soon.')
        wfunc()
    elif choice == 'quit':
        game_data['running'] = False
    elif choice == 'play':
        menu_state = True
        while menu_state:
            able_dungeons = list()
            for i in game_data['dungeons']:
                if i not in game_data['dungeons_comp']:
                    able_dungeons.append(i)
            if len(able_dungeons) > 0:
                print('\n' * 100)
                if len(game_data['dungeons_comp']) < 1 and pl.name == 'Player':
                    print('What would you like your name to be?')
                    choi = input('> ')
                    pl.name = choi
                else:
                    print('Welcome back ' + pl.name)
                    time.sleep(2)
                print('\n' * 100)
                print('Dungeons you can play: ')
                for i in able_dungeons:
                    print('* ' + i)
                print('Which dungeon would you like to play?')
                choice = input('> ')
                if choice in able_dungeons:
                    menu_state = False
                    print('\n' * 100)
                    du = Dungeon(choice)
                    du.game_loop()
                else:
                    print('Please enter a dungeon name you wish to play.')
                    wfunc()
            else:
                print(
                    'Sorry partner, you have completed all available dungeons.'
                )
                print('Look out for more soon, or create your own!')
                wfunc()
                menu_state = False
    else:
        print('Invalid Input.')
        wfunc()
