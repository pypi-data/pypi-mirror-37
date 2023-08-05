import pickle


class DataBase:
    @classmethod
    def save_to_db(cls, vr):
        confirmance = input('Are you sure? press yes/no: ')
        if confirmance == 'yes':
            with open(cls.db_file, 'wb') as f:
                pickle.dump(vr, f, pickle.HIGHEST_PROTOCOL)
                print('DATA has been recorded!')

    @classmethod
    def load_from_db(cls):
        with open(cls.db_file, 'rb') as f:
            VR = pickle.load(f)
        return VR


class UkraineDataBase(DataBase):
    db_file = 'ukraine.pickle'


class PolandDataBase(DataBase):
    db_file = 'poland.pickle'