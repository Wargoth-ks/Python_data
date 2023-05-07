from termcolor import colored

def show_contacts(data):
    if not data:
        return "You have no contacts saved."
    
    # sort names alphabetically
    sorted_names = sorted(data.keys())
    
    # find max length of name and phone number
    max_name_len = max(len(name) for name in sorted_names)
    max_phone_len = max(len(str(phone)) for phones in data.values() for phone in phones)
    
    # generate table
    table = ''
    for name in sorted_names:
        phones = ', '.join(str(phone) for phone in data[name])
        table += colored("Name: ", "cyan") + colored(f"{name:<{max_name_len}}", "white") + " " + colored("Phone: ", "yellow") + colored(f"{phones:>{max_phone_len}}\n", "white")
    
    return table



