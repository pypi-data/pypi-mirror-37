from rada_package_moiseieiva.rada_metaclass import MetaDescriptors
from rada_package_moiseieiva.utils import Sorting


class Human(metaclass=MetaDescriptors):
    int_types = ('weight', 'height')

    def __init__(self, weight, height):
        self.weight = weight
        self.height = height



class Spiker(Human):
    str_types = ('last_name', 'first_name')
    int_types = ('age', 'weight', 'height')

    def __init__(self, weight, height, last_name, first_name, age):
        super(Spiker, self).__init__(weight, height)
        self.last_name = last_name
        self.first_name = first_name
        self.age = age

    def notify_all_habarnikiv(self, verkhovna_rada):
        for fraction in verkhovna_rada.fractions:
            for deputat in fraction.deputies:
                if deputat.bribe_taker:
                    deputat.update()

class Deputat(Human):
    str_types = ('last_name', 'first_name')
    int_types = ('age', 'bribe_amount')

    def __init__(self, weight, height, last_name, first_name, age):
        super(Deputat, self).__init__(weight, height)
        self.last_name = last_name
        self.first_name = first_name
        self.age = age

    def __eq__(self, other):
        return self.weight == other.weight and \
               self.height == other.height and \
               self.age == other.age

    def __hash__(self):
        return hash(self.weight) + hash(self.height) + hash(self.age)

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.weight}kg {self.height}cm {self.age}age'


class UkraineDeputat(Deputat):
    def __init__(self, weight, height, last_name, first_name, age, bribe_taker):
        super(UkraineDeputat, self).__init__(weight, height, last_name, first_name, age)
        self.bribe_taker = bool(int(bribe_taker))
        self.bribe_amount = 0

    def give_tribute(self):
        if self.bribe_taker is False:
            print('this deputy does not take bribes...')
            return False

        money = input('how much grivnjas would you like to give:')
        if int(money) > 10000:
            print('Police will arrest the deputy!')
            return False

        self.bribe_amount += int(money)
        return self.bribe_amount

    def update(self):
        self.bribe_amount = 0
        self.bribe_taker = False
        print(f"This deputat {self.last_name}, {self.first_name} is not bribe taker anymore")

    @classmethod
    def describe_deputy(cls):
        personal_data = input(
            'Please enter: weight, height, last_name, first_name, age, is_briber?[0 or 1]: '
        )

        pd = personal_data.split(', ')

        try:
            deputy = cls(pd[0], pd[1], pd[2], pd[3], pd[4], pd[5])
            return deputy
        except IndexError as err:
            print('data should be separated by comma and whitespace', 'Invalid Data')


class PolandDeputat(Deputat):
    def __init__(self, weight, height, last_name, first_name, age):
        super(PolandDeputat, self).__init__(weight, height, last_name, first_name, age)

    @classmethod
    def describe_deputy(cls):
        personal_data = input(
            'Please enter: weight, height, last_name, first_name, age: '
        )

        pd = personal_data.split(', ')

        try:
            deputy = cls(pd[0], pd[1], pd[2], pd[3], pd[4])
            return deputy
        except IndexError as err:
            print('data should be separated by comma and whitespace', 'Invalid Data')


class Fraction(metaclass=MetaDescriptors):
    str_types = ('name',)

    def __init__(self, name, deputat_class):
        self.name = name
        self.deputat_class = deputat_class
        self.deputies = set()

    def __str__(self):
        return f'{self.name} members: {len(self.deputies)}'

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def add_deputy(self):
        deputy = self.deputat_class.describe_deputy()

        if not deputy:
            print('please describe deputy correctly, Invalid Data')
            return False

        if deputy not in self.deputies:
            self.deputies.add(deputy)
            print(f'{deputy} has been added to the fraction; {self.name}')
            return deputy
        else:
            print(f'{deputy} is already a participant of the fraction {self.name}')

    def remove_deputy(self, deputy=None):
        if not deputy:
            personal_data = input(
                'Please enter: weight, height, last_name, first_name, age, is_briber?[True or False]: '
            )
            pd = personal_data.split(', ')

            # should work fine if Deputat class is hashed. expected equal() to return True.
            try:
                deputy = Deputat(pd[0], pd[1], pd[2], pd[3], pd[4], bool(pd[5]))
            except IndexError as err:
                print('data should be separated by comma and whitespace', 'Invalid Data')
                return False

        if deputy in self.deputies:
            self.deputies.remove(deputy)
            print(f'{deputy} has been excluded from the fraction: {self.name}')
        else:
            print(f'{deputy} is not a participant of the fraction: {self.name}')

    def find_all_deputies(self):
        deputies = list(self.deputies)
        deputies.sort(key=Sorting('first_name', 'last_name'))

        print('List of all deputies...')
        for deputy in deputies:
            print(deputy)

    def clean_out_deputies(self):
        print('All deputies has been cleaned out')
        self.deputies = set()

    def is_participant(self, vr, deputy):
        for fraction in vr.fractions:
            if deputy in fraction.deputies:
                print(f'{deputy} is a member of the {self.name} fraction')
                return True

        print(f'{deputy} is not a member of the {self.name} fraction')
        return False


class UkraineFraction(Fraction):

    def __init__(self, name, deputat_class):
        super(UkraineFraction, self).__init__(name, deputat_class)

    def find_all_bribe_takers(self):
        print('The following bribe_takers have been found...')
        deputies = [dep for dep in self.deputies if dep.bribe_taker]
        deputies.sort(key=Sorting('bribe_amount'))

        for deputy in deputies:
            print(deputy, 'grivnjas taken: {}'.format(deputy.bribe_amount))

    def find_highest_bribe_taker(self):
        print('The most greedy deputy is:')
        deputies = [dep for dep in self.deputies if dep.bribe_taker]
        deputies.sort(key=Sorting('bribe_amount'))

        print(deputies[-1], 'grivnjas taken: {}'.format(deputies[-1].bribe_amount))


class PolandFraction(Fraction):

    def __init__(self, name, deputat_class):
        super(PolandFraction, self).__init__(name, deputat_class)


class VerkhovnaRada:

    def __init__(self):
        self.fractions = set()

    def add_fraction(self, fraction):
        if fraction not in self.fractions and fraction.name:
            print(f'Fraction {fraction.name} has been added to VR')
            self.fractions.add(fraction)
            return True

        print('already in VR')

    def remove_fraction(self, fraction):
        if fraction in self.fractions:
            print(f'Fraction {fraction.name} has been removed from VR')
            self.fractions.remove(fraction)
            return True

        print(f'Fraction {fraction.name} not in the list.')
        return False

    def print_all_fractions(self):
        print('List of all fractions:')
        for fr in self.fractions:
            print(fr)

    @staticmethod
    def print_fraction(fraction):
        print(fraction)

    @staticmethod
    def add_deputy_to_fraction(deputy, fraction):
        print(f'Adding deputy: {deputy} ...')
        fraction.add_deputy(deputy)

    def remove_deputy_from_fraction(self, fraction, deputy):
        print(f'Removing deputy: {deputy} ...')
        for fr in self.fractions:
            if fraction == fr:
                fr.remove_deputy(deputy)
                return

    def print_all_deputies(self):
        for fraction in self.fractions:
            print('{}: '.format(fraction.name))
            for deputy in fraction.deputies:
                print(''.rjust(len(fraction.name)), deputy)

    def is_present_in_vr(self, deputy):
        for fraction in self.fractions:
            if deputy in fraction:
                print('True')
        print('False')

    def update_deputy(self, deputy):
        for fraction in self.fractions:
            for dp in fraction.deputies:
                if deputy == dp:
                    dp.bribe_amount = deputy.bribe_amount


class UkraineVerkhovnaRada(VerkhovnaRada):
    name = 'Verkhovna Rada Ukraine'

    def __init__(self):
        super(UkraineVerkhovnaRada, self).__init__()

    def print_all_bribe_takers(self):
        print('Printing all bribe takers in VR')
        for fraction in self.fractions:
            for deputy in fraction.deputies:
                if deputy.bribe_taker:
                    print(deputy, 'grivnjas taken: {}'.format(deputy.bribe_amount))

    def higher_bribe_taker(self):
        bribe_takers = []
        for fraction in self.fractions:
            for deputy in fraction.deputies:
                if deputy.bribe_taker:
                    bribe_takers.append(deputy)

        bribe_takers.sort(key=Sorting('bribe_amount'))
        print(bribe_takers[-1], 'grivnjas taken: {}'.format(bribe_takers[-1].bribe_amount))

    def update_deputy(self, deputy):
        for fraction in self.fractions:
            for dp in fraction.deputies:
                if deputy == dp:
                    dp.bribe_amount = deputy.bribe_amount

    def add_spiker(self, spiker):
        if not getattr(self, "spiker", None):
            self.spiker = spiker
            print("spiker was added")
        


class PolandVerkhovnaRada(VerkhovnaRada):
    name = 'Verkhovna Rada Poland'

    def __init__(self):
        super(PolandVerkhovnaRada, self).__init__()

