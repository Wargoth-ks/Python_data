
from decorator.decorator import input_error
from display_help.display_help import display_help
from contacts.display_contacts import display_contacts
#from contacts.save_contacts import contacts
from classes import *

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
    return display_help()

@input_error
def error_func():
    raise ValueError(f"Command not found. Please, try again!")

@input_error
def add_contact(name, phone):
    name = Name(name)
    phone = Phone(phone)
    record = Record(name, phones=[phone])
    contacts.add_record(record)
    return f"<< {name} >> has been added to the phone book"

@input_error
def add_phone(name, phone):
    phone = Phone(phone)
    if name not in contacts:
        contacts.add_record(Record(name, [phone]))
        return f"<< {name} >> and {phone} have been added to phone book"
    else:
        contact = contacts[name]
        contact.add_phone(phone)
        return f"<< {phone} >> has been added to the contact {name} in phone book"
    
@input_error
def del_contact(name):
    name = Name(name)
    if name.value not in contacts:
        return f"<< {name.value} >> not found in phone book"
    contacts.delete_record(Name(name.value))
    return f"<< {name} >> has been removed from phone book"

@input_error
def del_phone(name, phone):
    phone = Phone(phone)
    name = Name(name)
    if name.value not in contacts:
        return f"<< {phone.value} >> not found in phone book"
    record = contacts.data[name.value]
    record.delete_phone(phone)
    return f"<< {phone.value} >> has been removed from phone book"

@input_error
def change_phone(name, phone):
    name = Name(name)
    phone = Phone(phone)
    if name.value not in contacts:
        return f"<< {name.value} >> not found in phone book"
    record = contacts.data[name.value]
    record.edit_phone(record.phones[0], phone)
    return f"Phone number for << {name.value} >> has been updated"

@input_error
def change_name(name, new_name):
    name = Name(name)
    new_name = Name(new_name)
    if name.value not in contacts:
        return f"<< {name.value} >> not found in phone book"
    contacts.update_record(name, new_name)
    return f"Name for << {name.value} >> has been updated to << {new_name.value} >>"



@input_error
def show_phone(name):
    name = Name(name)
    if name.value not in contacts:
        raise ValueError(f"<< {name.value} >> not found in phone book")
    record = contacts.data[name.value]
    return record.phones


@input_error
def show_all():
    records = contacts.find_records()
    if not records:
        return "<< You have no contacts saved >>"
    data = {str(record.name): record.phones for record in records}
    return display_contacts(data)