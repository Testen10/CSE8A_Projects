import random as r

TYELLOW = '\033[33m'
ENDC = '\033[m'

class Character:
    def __init__(self, name, text_color):
        self.name = name
        self.text_color = text_color
        
    def set_initstate(self,job):
        self.job_list = ["Swordman", "Archer", "Warrior"]
        self.state_list = ["ATK", "DEF", "HP"]
        self.job = self.job_list[job-1]

        if self.job == "Swordman":
            self.ATK = r.randint(4,6)
            self.DEF = r.randint(4,6)
            self.HP = r.randint(15,20)

        elif self.job == "Archer":
            self.ATK = r.randint(7,10)
            self.DEF = r.randint(3,6)
            self.HP = r.randint(12,16)

        else:
            self.ATK = r.randint(2,5)
            self.DEF = r.randint(7,10)
            self.HP = r.randint(17,25)

        self.remain_HP = self.HP
        self.remain_portion = 1

    def state_up(self, state, val):
        if state == "ATK": self.ATK += val
        elif state == "DEF": self.DEF += val
        elif state == "HP":
            self.HP += val
            self.remain_HP += val
    
    def get_portion(self):
        self.remain_portion += 1

    def use_portion(self):
        self.change_HP(99999999)
        self.remain_portion -= 1

    def attack(self, attack_type, enemy):
        if attack_type < 2:
            damage = 0
            print(TYELLOW+"Miss! Damage: {}".format(damage), ENDC)
        elif attack_type < 8:
            damage = int(round(max((self.ATK - (enemy.DEF) + r.randint(1,3))*0.7,1),0))
            print(TYELLOW+"Normal Attack! Damage: {}".format(damage), ENDC)
        else:
            damage = int(round(max((self.ATK - (enemy.DEF) + r.randint(1,3))*1.5,2),0))
            print(TYELLOW+"Critical Attack! Damage: {}".format(damage), ENDC)

        enemy.change_HP(-damage)

    def change_HP(self, val):
        if val>0: self.remain_HP =min(self.remain_HP+val,self.HP)
        else: self.remain_HP = max(self.remain_HP+val, 0)
    
    def check_defeat(self):
        if self.remain_HP <= 0: return True
        else: return False

    def print_charInfo(self):

        print("-"*10)
        print(self.text_color+"{}({})".format(self.name, self.job), ENDC)
        print("   ATK: {}".format(self.ATK))
        print("   DEF: {}".format(self.DEF))
        print("   HP: {}/{}".format(self.remain_HP, self.HP))
        print("   portion remaining: {}".format(self.remain_portion), ENDC)
        print("-"*10)

    def print_charInfo_simple(self):
        print("-"*10)
        print(self.text_color+"{}".format(self.name, self.job), end = ENDC+" // ", )
        print("HP: {}/{}".format(self.remain_HP, self.HP))
        print("-"*10)