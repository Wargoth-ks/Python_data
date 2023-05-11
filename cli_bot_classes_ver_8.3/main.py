from termcolor import colored
from show_greeting import greet
from datetime import datetime
from commands import hello, helper, add_contact, del_contact, del_phone, error_func
from commands import change_phone, show_all, show_phone, good_bye, add_phone, change_name, add_bd, get_bd,  search_by_name, search_by_phone, search_by_bd

cmds = {
    "hello": hello,
    "help": helper,
    "add": add_contact,
    "add_phone": add_phone,
    "del": del_contact,
    "del_phone": del_phone,
    "change": change_name,
    "change_phone": change_phone,
    "phone": show_phone,
    "show all": show_all,
    "add_bd": add_bd,
    "get_bd": get_bd,
    "by_name":  search_by_name,
    "by_phone": search_by_phone,
    "by_bd": search_by_bd, 
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    ".": good_bye
}

list_cmds = ["show all", "good bye", "close", "exit", ".", "help", "hello"]


def main():
    while True:
        usr_inp = input(colored("\nEnter command: ", "green"))
        if usr_inp in list_cmds:
            s_func = cmds[usr_inp.strip()]
            print(s_func())
        elif not usr_inp or usr_inp.split()[0] not in cmds.keys():
            print(error_func())
        else:
            if usr_inp.split()[0] in cmds.keys() and len(usr_inp.split()) > 1:
                command, *data = usr_inp.strip().split(' ', 1)
                handler = cmds[command]
                args = data[0].split(" ")
                print(command, args)
                if not data:
                    print(error_func())
                if len(data[0].split(", ")) == 2:
                    arg_1, arg_2 = data[0].split(", ")
                    print(handler(arg_1, arg_2))
                    continue
                if len(args) >= 2:
                    if all(symb.isdigit() or symb in ['+', '-'] for symb in args[-2]):
                        date_arg = args[-1]
                        d_arg = datetime.strptime(date_arg, '%d.%m.%Y').date()
                        dig_arg = str(args[-2])
                        list_args = [" ".join(args[:-2]), dig_arg, d_arg]
                        print(handler(*list_args))
                        continue
                    elif all(symb.isdigit() or symb in ['+', '-'] for symb in args[-1]):
                        dig_arg = str(args[-1])
                        list_args = [" ".join(args[:-1]), dig_arg]
                        print(handler(*list_args))
                        continue
                if handler and len(args) == 2 and datetime.strptime(args[-1], '%d.%m.%Y').date(): 
                    date_arg = datetime.strptime(args[-1], '%d.%m.%Y').date()
                    list_args = [" ".join(args[:-1]), date_arg]
                    print(handler(*list_args))
                    continue
                if len(data) == 1:
                    print(data)
                    print(handler(*data))
            else:
                print(
                    "Type Error: " + colored(f"Command << {usr_inp} >> must have any arguments !!!", "red"))


if __name__ == "__main__":
    greet()
    main()
