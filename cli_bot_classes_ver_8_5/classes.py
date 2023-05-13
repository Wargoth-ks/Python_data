from collections import UserDict

from datetime import date
import atexit
import pickle
import os

FILENAME = 'contacts_saved.pickle'

class Field:

    def __init__(self, value=None):
        self.value = value

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
        if 10 <= len(str(arg_phone)) <= 17:
            self._private_phone = arg_phone
        else:
            raise ValueError(f"Lenght of phone number must be 10-17 symbols")


class Birthday(Field):
    
    def __init__(self, value):
        super().__init__(value)
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
    

class Record(Field):

    def __init__(self, name: Name, phones: list[Phone]=[], birthday=None):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __getitem__(self, key):
        if key == 'phones':
            return self.phones
        elif key == 'birthday':
            return self.birthday
        else:
            raise KeyError(key)

    def add_phone(self, phone: Phone):
        self.phones.insert(0, phone)

    def edit_phone(self, phone: Phone, new_value: Phone):
        for p in self.phones:
            if p == phone:
                p.value = new_value
                break

    def delete_phone(self, phone: Phone):
        if phone not in self.phones:
            raise ValueError(f"<< {self.name} >> doesn't have << phone: {phone} >>")
        self.phones.remove(phone)

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
    
    def delete_birthday(self, name: Name):
        self.birthday = None
        self.name = name

    def update_birthday(self, new_birthday: Birthday):
        self.birthday = new_birthday

    def days_to_birthday(self, birthday):
        self.birthday = birthday
        if self.birthday is None:
            return "No BD"
        today = date.today()
        print(today)
        next_bd = date(today.year, self.birthday.value.month, self.birthday.value.day)
        if next_bd < today:
            next_bd = next_bd.replace(year=today.year + 1)
        delta = next_bd - today
        return f"Days until birthday: {delta.days}"
    
    def __repr__(self) -> str:
        return f"{self.name!r}: {self.phones!r}, {(self.birthday)}"

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

    def add_record(self, record: Record):
        if record.name.value not in self.data: # Record(name,phone,birth)
            self.data[record.name.value] = record

    def delete_record(self, name: Name):
        if name.value not in self.data:
            raise ValueError(f"<< {name.value} >> not found in phone book")
        del self.data[name.value]

    def update_record(self, old_name, new_name):
        if old_name.value not in self.data:
            raise ValueError(f"<< {old_name.value} >> not found in phone book")
        record = self.data.pop(old_name.value)
        record.name = new_name
        self.data[new_name.value] = record

    def find_records(self, name=None, phone=None):
        if name is not None:
            return self.data.get(name)
        elif phone is not None:
            found_records = []
            for record in self.data.values():
                for p in record.phones:
                    if p.value == phone.value:
                        found_records.append(record)
                        break
            return found_records[0]
    
    def print_records(self, records):
        for record in records:
            name, info = record
            print(f"Name: {name}")
            phones = [str(phone) for phone in info['phones']]
            print(f"Phone: {', '.join(phones)}")
            if info['birthday']:
                print(f"Birthday: {info['birthday'].value.strftime('%d.%m.%Y')}")
            else:
                print("Birthday: No info")
            print()

    def iterator(self, n: int):
        records = sorted(list(self.data.items()))
        i = 0
        while i < len(records):
            yield records[i:i+n]
            i += n

    