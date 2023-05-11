from decorator import input_error
from show_help import show_help
from show_contacts import show_contacts
from classes import AddressBook, Name, Phone, Birthday, Record


# Processing input commands

contacts = AddressBook()

@input_error
def hello():
    return "\nHow can I help you?"

@input_error
def good_bye():
    print("\nBye bye!")
    exit()

@input_error
def helper():
    return show_help()

@input_error
def error_func():
    raise ValueError(f"Command not found. Please, try again!")

@input_error
def add_contact(name, phone, birthday=None):
    name = Name(name)
    phone = Phone(phone)
    if birthday is not None:
        birthday = Birthday(birthday)
        record = Record(name, phones=[phone], birthday=birthday)
    else:
        record = Record(name, phones=[phone])
    contacts.add_record(record)
    return f"<< Contact {name} >> has been added to the phone book"

@input_error
def add_phone(name, phone):
    phone = Phone(phone)
    name = Name(name)
    if name.value not in contacts:
        raise ValueError(f"<< Contact {name.value} >> not found in phone book")
    contact = contacts[name.value]
    contact.add_phone(phone.value)
    return f"<< Number {phone} >> has been added to the contact << {name} >>"

@input_error
def del_contact(name):
    name = Name(name)
    contacts.delete_record(name)
    return f"<< {name} >> has been removed from phone book"

@input_error
def del_phone(name, phone):
    phone = Phone(phone)
    name = Name(name)
    record = contacts.data[name.value]
    if name.value not in contacts:
        if phone.value not in record.phones:
            raise ValueError(f"<< Number {phone.value} >> not found in phone book")
        raise ValueError(f"<< Number {phone.value} >> not found in << {name.value} >> contact")
    record.delete_phone(phone.value)
    return f"<< Number {phone.value} >> has been removed from phone book"

@input_error
def change_phone(name, phone):
    name = Name(name)
    phone = Phone(phone)
    if name.value not in contacts:
        raise ValueError(f"<< Contact {name.value} >> not found in phone book")
    record = contacts.data[name.value]
    record.edit_phone(record.phones[0], phone)
    return f"Phone number for << contact {name.value} >> has been updated"

@input_error
def change_name(name, new_name):
    name = Name(name)
    new_name = Name(new_name)
    contacts.update_record(name, new_name)
    return f"Name for << {name.value} >> has been updated to << {new_name.value} >>"


@input_error
def show_phone(name):
    name = Name(name)
    if name.value not in contacts:
        raise ValueError(f"<< {name.value} >> not found in phone book")
    record = contacts.data[name.value]
    return record

@input_error
def show_all():
    usr_input = input("Enter number of records: ")
    if usr_input == "":
        records = contacts.find_records()
        for record in records:
            print(record)
        return ""
    else:
        n = int(usr_input)
        for records in contacts.iterator(n):
            for record in records:
                print(record)
            usr_input = input("Press enter to show more records or 'q' to quit: ")
            if usr_input == "q":
                return "Done!"
    return "No more records"

@input_error
def add_bd(name, birthday, phone=None):
    name = Name(name)
    birthday = Birthday(birthday)
    if phone is None:
        record = Record(name, birthday=birthday)
        contacts.add_record(record)

@input_error
def get_bd(name, birthday):
    name = Name(name)
    birthday = Birthday(birthday)
    bd = Record(name, birthday=birthday)
    s = bd.days_to_birthday(birthday)
    return s

@input_error    
def search_by_name(name):
    name = Name(name)
    records = contacts.find_records(name)
    return records

def search_by_phone(phone):
    phone_obj = Phone(phone)
    return contacts.find_records(phone_obj.value)

def search_by_bd(birthday):
    birthday = Birthday(birthday)
    records = contacts.find_records(birthday)
    return records