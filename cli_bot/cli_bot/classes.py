import atexit
import pickle
import os
import re

from collections import UserDict
from termcolor import colored
from datetime import date

FILENAME = "contacts_saved.pickle"


class Field:
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        return self.value == other.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return f"{self.value}"

    @property
    def value(self):
        parent = Field.value.fget(self)
        return parent

    @value.setter
    def value(self, value):
        if not re.match(r"^[A-Za-z\s]+$", value):
            raise ValueError(
                f"The name should not contain digits or special characters!!!"
            )
        Field.value.fset(self, value)


class Phone(Field):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    @property
    def value(self):
        parent = Field.value.fget(self)
        return parent

    @value.setter
    def value(self, value):
        if 10 <= len(str(value)) <= 17:
            Field.value.fset(self, value)
        else:
            raise ValueError(f"Lenght of phone number must be 10-17 symbols")


class Birthday(Field):
    def __init__(self, value: date):
        self.value = value

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

    @property
    def value(self):
        parent = Field.value.fget(self)
        return parent

    @value.setter
    def value(self, value):
        if isinstance(value, date):
            Field.value.fset(self, value)
        else:
            raise ValueError("Date of BD must be in format << dd.mm.yyyy >>")


class Record:
    def __init__(self, name: Name, phones: list[Phone] = [], birthday=None):
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __getitem__(self, key):
        if key == "name":
            return self.name
        if key == "phones":
            return self.phones
        elif key == "birthday":
            return self.birthday
        else:
            raise KeyError(key)

    def add_phone(self, phone: Phone):
        self.phones.insert(0, Phone(phone))

    def edit_phone(self, phone: Phone, new_phone: Phone):
        if self.phones != []:
            self.phones.remove(phone)
            self.phones.append(new_phone)

    def delete_phone(self, phone: Phone):
        if phone not in self.phones:
            raise ValueError(
                f"<< {self.name.value} >> doesn't have << phone: {phone} >>"
            )
        self.phones.remove(phone)

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def delete_birthday(self):
        self.birthday = None

    def update_birthday(self, new_birthday: Birthday):
        self.birthday = new_birthday

    def days_to_birthday(self, birthday):
        self.birthday = birthday
        if self.birthday is None:
            return "No BD"
        today = date.today()
        next_bd = date(today.year, self.birthday.value.month, self.birthday.value.day)
        if next_bd < today:
            next_bd = next_bd.replace(year=today.year + 1)
        delta = next_bd - today
        return colored("\nDays until birthday: ", "blue") + f"{delta.days}"

    def __str__(self) -> str:
        phones_str = ", ".join(sorted(str(p) for p in self.phones))
        return f"Name: {self.name} \nPhone(s): {phones_str} \nBirthday: {self.birthday}"


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

        if os.path.exists(FILENAME):
            with open(FILENAME, "rb") as f:
                loaded_data = pickle.load(f)
                self.data.update(loaded_data)
        atexit.register(self.save_contacts_on_exit)

    def save_contacts_on_exit(self):
        with open(FILENAME, "wb") as f:
            pickle.dump(self.data, f)

    def add_record(self, record: Record):
        if record.name.value not in self.data:  # Record(name,phone,birth)
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
            pattern = r"\b\w{3,}"
            patt_name = re.findall(pattern, name.value, re.IGNORECASE)
            records = (
                [
                    str(rec)
                    for rec in self.data.values()
                    if any(
                        word.lower().startswith(patt_name[0].lower())
                        for word in rec.name.value.split()
                    )
                ]
                if patt_name
                else []
            )
            str_rec = "\n\n".join(records)
            return str_rec

        elif phone is not None:
            records = []
            for record in self.data.values():
                for p in record.phones:
                    matches = re.findall(r"\+?\d{1,3}(?:-?\d{1,3}){3,}", p.value)
                    if any(phone.value in match for match in matches):
                        records.append(str(record))
                        break
            str_rec = "\n\n".join(records)
            return str_rec

    def print_records(self, records):
        for record in records:
            name, info = record
            print(colored("\nName: ", "cyan") + f"{name}")
            phones = [str(phone) for phone in info["phones"]]
            print(colored("Phone(s): ", "white") + f"{', '.join(phones)}")
            if info["birthday"]:
                print(
                    colored("Birthday: ", "yellow")
                    + f"{info['birthday'].value.strftime('%d.%m.%Y')}"
                )
            else:
                print(colored("Birthday: ", "yellow") + f"No info")
            print()

    def iterator(self, n: int):
        records = sorted(list(self.data.items()))
        i = 0
        while i < len(records):
            yield records[i : i + n]
