from decorator import input_error, validation_exists_name
from show_help import show_help
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
def add_name(name, phone=None, birthday=None):
    name = Name(name)
    if name.value not in contacts and phone is None and birthday is None:
        record = Record(name)
        contacts.add_record(record)
        return f"Name << {name} >> succefully added"
    else:
        raise ValueError(f"Phone book is already contain this name!!!")
    
@input_error
def add_contact(name, phone, birthday=None):
    name = Name(name)
    phone = Phone(phone)
    if name.value not in contacts:
        if birthday is not None:
            birthday = Birthday(birthday)
            record = Record(name, phones=[phone], birthday=birthday)
        else:
            record = Record(name, phones=[phone])
        contacts.add_record(record)
        return f"<< Contact {name} >> has been added to the phone book"
    else:
        raise ValueError(f"Phone book is already contain this name!!!")
    
@input_error
@validation_exists_name(contacts)
def add_phone(name, phone):
    phone = Phone(phone)
    name = Name(name)
    contact = contacts[name.value]
    contact.add_phone(str(phone.value))
    return f"<< Number {phone} >> has been added to the contact << {name} >>"

@input_error
@validation_exists_name(contacts)
def add_bd(name, birthday, phone=None):
    name = Name(name)
    birthday = Birthday(birthday)
    if phone is None:
        record = contacts.data[name.value]
        record.add_birthday(birthday) 
        return f"<< Birthday >> has been added to the contact << {name} >>"
    if birthday.value in contacts:
        raise ValueError(f"<< Contact {name.value} >> is already have {birthday.value}")
    
@input_error
@validation_exists_name(contacts)
def del_contact(name):
    name = Name(name)
    contacts.delete_record(name)
    return f"<< {name} >> has been removed from phone book"

@input_error
@validation_exists_name(contacts)
def del_phone(name, phone):
    phone = Phone(phone)
    name = Name(name)
    contact = contacts[name.value]
    contact.delete_phone(phone)
    return f"<< Number {phone} >> has been removed from phone book"

@input_error
@validation_exists_name(contacts)
def del_bd(name):
    name = Name(name)
    record = contacts.data[name.value]
    record.delete_birthday()
    return f"<< Birthday >> succefully deleted from contact << {name} >>"
        
@input_error
@validation_exists_name(contacts)
def change_name(name, new_name):
    name = Name(name)
    new_name = Name(new_name)
    contacts.update_record(name, new_name)
    return f"Name for << {name.value} >> has been updated to << {new_name.value} >>"

@input_error
@validation_exists_name(contacts)
def change_phone(name, phone):
    name = Name(name)
    phone = Phone(phone)
    record = contacts.data[name.value]
    record.edit_phone(record.phones[0], phone)
    return f"Phone number for << contact {name.value} >> has been updated"

@input_error
@validation_exists_name(contacts)
def upd_bd(name, birthday, phone=None):
    name = Name(name)
    birthday = Birthday(birthday)
    if phone is None:        
        record = contacts.data[name.value]
        record.update_birthday(birthday) 
        return f"<< Birthday >> succefuly updated to contact << {name} >>"
        
@input_error
@validation_exists_name(contacts)
def get_bd(name, birthday):
    name = Name(name)
    birthday = Birthday(birthday)
    record = Record(name, birthday=birthday)
    days_to_bd = record.days_to_birthday(birthday)
    return days_to_bd
    
@input_error
def search_by_name(name):
    name_obj = Name(name)
    find_name = contacts.find_records(name=name_obj)
    if find_name:
        return find_name
    else:
        print("No records found with name: ", name_obj)

@input_error
def search_by_phone(phone):
    phone_obj = Phone(phone)
    find_phone = contacts.find_records(phone=phone_obj)
    if find_phone:
        return find_phone
    else:
        print("No records found with phone number: ", phone_obj)

@input_error
def show_all():
    # print(contacts)
    usr_input = input("\nEnter number of records: ")
    if usr_input == "":
        contacts.print_records(sorted(contacts.items()))
        return ""
    else:
        n = int(usr_input)
        for records in sorted(contacts.iterator(n)):
            contacts.print_records(records)
            usr_input = input("\nPress enter to show more records or 'q' to quit: ")
            if usr_input == "q":
                return "Done!"
    return "No more records"
