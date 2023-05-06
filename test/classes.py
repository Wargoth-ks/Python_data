from collections import UserDict


class Field:

    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.value == other.value


class Name(Field):
    pass


class Phone(Field):
    pass


class Record:

    def __init__(self, name: Name, phones: list):
        self.name = name
        self.phones = phones or []

    def add_phone(self, phone: Phone):
        self.phones.insert(0, phone)

    def edit_phone(self, phone: Phone, new_value):
        for p in self.phones:
            if p == phone:
                p.value = new_value
                break

    def delete_phone(self, phone: Phone):
        self.phones = [p for p in self.phones if p != phone]

    def __str__(self):
        phones_str = ", ".join(str(p) for p in self.phones)
        return f"{self.name}: {phones_str}"

    def __repr__(self):
        return str(self)

    def __format__(self, format_spec):
        return format(str(self.phones), format_spec)


class AddressBook(UserDict):

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def delete_record(self, name: Name):
        del self.data[name.value]

    def update_record(self, old_name: Name, new_name):
        record = self.data.pop(old_name.value)
        record.name = new_name
        self.data[new_name.value] = record

    def find_records(self):
        return list(self.data.values())


