from collections import UserDict
from collections.abc import Iterator, Generator
from datetime import date, timedelta
import atexit
import pickle
import os


FILENAME = 'contacts_saved.pickle'


class Field:

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):

    def __init__(self, value) -> None:
        super().__init__(value)
        self._private_name = value

    def __repr__(self) -> str:
        return f"{self.value}"

    @property
    def value(self):
        return self._private_name
    
    @value.setter
    def value(self, arg_name):
        if 3 <= len(arg_name) <= 22:
            self._private_name = arg_name
        else:
            raise ValueError(f"Name must have more then 2 symbols and less the 22 symbols")
        

class Phone(Field):

    def __init__(self, value) -> None:
        super().__init__(value)
        self._private_phone = value

    def __repr__(self) -> str:
        return f"{self.value}"

    @property
    def value(self):
        return self._private_phone
    
    @value.setter
    def value(self, arg_phone):
        if 10 <= len(arg_phone) <= 17:
            self._private_phone = arg_phone
        else:
            raise ValueError(f"Lenght of phone number must be 10-17 symbols")


class Birthday(Field):
    
    def __init__(self, value):
        super.__init__(value)
        self._private_bd = value

    def __repr__(self) -> str:
        return f"{self.value}"
    
    @property
    def value(self):
        return self._private_bd
    
    @value.setter
    def value(self, arg_bd: date):
        if isinstance(arg_bd, date):
            self._private_bd = arg_bd
        else:
            raise ValueError("Date of BD must be in format << dd.mm.yyyy >>")


class Record:

    def __init__(self, name: Name, phones: list[Phone], birthday=None):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        self.phones.insert(0, phone)

    def edit_phone(self, phone: Phone, new_value: Phone):
        for p in self.phones:
            if p == phone:
                p.value = new_value
                break

    def delete_phone(self, phone: Phone):
        self.phones.remove(phone)

    def days_to_birthday(self, name, bd):

        self.name = name
        self.bd = bd

        bd_dict = {}

        if self.birthday is None:
            return "No BD"

        today = date.today()
        next_bd = date(today.year, self.birthday.value.month, self.birthday.value.day)

        if next_bd < today:
            next_bd = next_bd.replace(year=today.year + 1)

        delta = next_bd - today

        return delta.days

    def __repr__(self) -> str:
        return f"Record({self.name!r}: {self.phones!r})"

    def __format__(self, format_spec):
        return format(str(self.phones), format_spec)


class AddressBook(UserDict):

    def __init__(self):

        self.data = {}

        if os.path.exists(FILENAME):
            with open(FILENAME, 'rb') as f:
                loaded_data = pickle.load(f)
                self.data.update(loaded_data)

        atexit.register(self.save_contacts_on_exit)

    def save_contacts_on_exit(self):
        with open(FILENAME, 'wb') as f:
            pickle.dump(self.data, f)

    def __iter__(self) -> Iterator:
        ...
    
    def __next__(self):
        ...
    
    def __getstate__(self):
        return self.data
    
    def __setstate__(self, state):
        self.data = state

    def add_record(self, record: Record):
        self.data[record.name.value] = record
        
    def delete_record(self, name: Name):
        del self.data[name.value]
    
    def update_record(self, old_name: Name, new_name: Name):
        record = self.data.pop(old_name.value)
        record.name = new_name
        self.data[new_name.value] = record

    def find_records(self):
        return list(self.data.values())
    


