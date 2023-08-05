from abc import ABC, abstractmethod


class Console(ABC):
    def __init__(self, rada, fraction_class, deputat_class, db_class, spiker_class = None):
        self.rada = rada
        self.fraction_class = fraction_class
        self.deputat_class = deputat_class
        self.db = db_class
        if spiker_class:
            self.spiker_class = spiker_class
    
    @abstractmethod
    def run(self):
        pass
    
    
class UkraineConsole(Console):
    
    def __init__(self, rada, fraction_class, deputat_class, db_class, spiker_class):
        super(UkraineConsole, self).__init__(rada, fraction_class, deputat_class, db_class, spiker_class)
        self.help_text = """
                Введіть 1, щоб додати фракцію
                Введіть 2, щоб видалити фракцію
                Введіть 3, щоб очистити фракцію
                Введіть 4, щоб вивести фракції
                Введіть 5, щоб видалити фракцію з ВР
                Введіть 6, щоб додати депутата у фракцію
                Введіть 7, щоб видалити депутата із фракції
                Введіть 8, щоб вивести список хабарників у фракції
                Введіть 9, щоб вивести список  хабарників у раді
                Введіть 10, щоб вивести найбільшого хабарника у раді
                Введіть 11, щоб вивести найбільшого хабарника у фракції.
                Введіть 12, щоб перевірити чи є дупутат у фракції
                Введіть 13, щоб перевірити чи є депутат у раді
                Введіть 14, дати хабара депутату!
                Введіть 15, вивести всіх депутатів у ВР
                Введіть 16, записати у БД
                Введіть 17, зчитати з БД
                Введіть 18, додати спикера
                Введіть 19, повидомити хабарникив


                Введіть 0, щоб вийти із програми.
                : """

    def run(self):

        while True:

            choice = input(self.help_text)
            try:
                choice = int(choice)
            except ValueError:
                print('Enter a number from the list')
                continue

            if choice == 1:
                fr_name = input('Please enter a fraction name: ')
                self.rada.add_fraction(self.fraction_class(fr_name, self.deputat_class))
            elif choice == 2:
                fr_name = input('Please enter a fraction name to be deleted: ')
                self.rada.remove_fraction(self.fraction_class(fr_name, self.deputat_class))
            elif choice == 3:
                fr_name = input('Please enter fraction name to work with: ')
                self.fraction_class(fr_name, self.deputat_class).clean_out_deputies()
            elif choice == 4:
                self.rada.print_all_fractions()
            elif choice == 5:
                fr_name = input('Please enter a fraction name to be deleted: ')
                self.rada.remove_fraction(self.fraction_class(fr_name, self.deputat_class))
            elif choice == 6:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)
                if fr not in self.rada.fractions:
                    self.rada.fractions.add(fr)
                for fraction in self.rada.fractions:
                    if fraction == fr:
                        fraction.add_deputy()
            elif choice == 7:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)
                dp = fr.add_deputy()

                self.rada.remove_deputy_from_fraction(fr, dp)
            elif choice == 8:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)

                if fr in self.rada.fractions:
                    for fraction in self.rada.fractions:
                        if fraction == fr:
                            fraction.find_all_bribe_takers()
            elif choice == 9:
                self.rada.print_all_bribe_takers()
            elif choice == 10:
                self.rada.higher_bribe_taker()
            elif choice == 11:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)

                if fr in self.rada.fractions:
                    for fraction in self.rada.fractions:
                        if fraction == fr:
                            fraction.find_highest_bribe_taker()

            elif choice == 12:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)
                dp = self.deputat_class.describe_deputy()
                if dp:
                    fr.is_participant(self.rada, dp)
            elif choice == 13:
                dp = self.deputat_class.describe_deputy()
                if dp:
                    self.rada.is_present_in_self.rada(dp)
            elif choice == 14:
                dp = self.deputat_class.describe_deputy()
                if dp:
                    dp.give_tribute()
                    self.rada.update_deputy(dp)
            elif choice == 15:
                self.rada.print_all_deputies()
            elif choice == 16:
                self.db.save_to_db(self.rada)
            elif choice == 17:
                self.rada = self.db.load_from_db()
            elif choice == 18:
                spiker_info = input ("Please enter a spiker info: weight, height, last_name, first_name, age ")
                spiker_info = spiker_info.split()
                spiker = self.spiker_class(*spiker_info)
                self.rada.add_spiker(spiker)
            elif choice == 19:
                self.rada.spiker.notify_all_habarnikiv(self.rada)  
            elif choice == 0:
                break
    
    
class PolandConsole(Console):

    def __init__(self, rada, fraction_class, deputat_class, db_class):
        super(PolandConsole, self).__init__(rada, fraction_class, deputat_class, db_class)
        self.help_text = """
                Введіть 1, щоб додати фракцію
                Введіть 2, щоб видалити фракцію
                Введіть 3, щоб очистити фракцію
                Введіть 4, щоб вивести фракції
                Введіть 5, щоб видалити фракцію з ВР
                Введіть 6, щоб додати депутата у фракцію
                Введіть 7, щоб видалити депутата із фракції
                Введіть 12, щоб перевірити чи є дупутат у фракції
                Введіть 13, щоб перевірити чи є депутат у раді
                Введіть 15, вивести всіх депутатів у ВР
                Введіть 16, записати у БД
                Введіть 17, зчитати з БД

                Введіть 0, щоб вийти із програми.
                : """

    def run(self):

        while True:

            choice = input(self.help_text)
            try:
                choice = int(choice)
            except ValueError:
                print('Enter a number from the list')
                continue

            if choice == 1:
                fr_name = input('Please enter a fraction name: ')
                self.rada.add_fraction(self.fraction_class(fr_name, self.deputat_class))
            elif choice == 2:
                fr_name = input('Please enter a fraction name to be deleted: ')
                self.rada.remove_fraction(self.fraction_class(fr_name, self.deputat_class))
            elif choice == 3:
                fr_name = input('Please enter fraction name to work with: ')
                self.fraction_class(fr_name, self.deputat_class).clean_out_deputies()
            elif choice == 4:
                self.rada.print_all_fractions()
            elif choice == 5:
                fr_name = input('Please enter a fraction name to be deleted: ')
                self.rada.remove_fraction(self.fraction_class(fr_name, self.deputat_class))
            elif choice == 6:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)
                if fr not in self.rada.fractions:
                    self.rada.fractions.add(fr)
                for fraction in self.rada.fractions:
                    if fraction == fr:
                        fraction.add_deputy()
            elif choice == 7:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)
                dp = fr.add_deputy()

                self.rada.remove_deputy_from_fraction(fr, dp)
            elif choice == 12:
                fr_name = input('Please enter fraction name to work with: ')
                fr = self.fraction_class(fr_name, self.deputat_class)
                dp = self.deputat_class.describe_deputy()
                if dp:
                    fr.is_participant(self.rada, dp)
            elif choice == 13:
                dp = self.deputat_class.describe_deputy()
                if dp:
                    self.rada.is_present_in_self.rada(dp)
            elif choice == 15:
                self.rada.print_all_deputies()
            elif choice == 16:
                self.db.save_to_db(self.rada)
            elif choice == 17:
                self.rada = self.db.load_from_db()
            elif choice == 0:
                break
