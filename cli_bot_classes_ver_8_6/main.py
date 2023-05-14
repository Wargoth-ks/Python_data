from termcolor import colored
from show_greeting import greet
from datetime import datetime
from commands import hello, helper, add_contact, del_contact, del_phone, error_func, get_bd, del_bd, upd_bd
from commands import change_phone, show_all, good_bye, add_phone, change_name, search_by_name, search_by_phone, add_bd 
import re

cmds = {
    "hello": hello,
    "help": helper,
    "add": add_contact, # >= 2 arg name phone (bd) +
    "add_phone": add_phone, # 2 arg name phone +
    "del": del_contact, # 1 arg name +
    "del_bd": del_bd, # 1 arg +
    "upd_bd": upd_bd, # 2 arg +
    "del_phone": del_phone, # 2 arg name phone +
    "change": change_name, # 2 arg old_name new_name
    "change_phone": change_phone, # 2 arg name new_phone + digits +
    "show all": show_all, # +
    "add_bd": add_bd, # >= 2 arg name bd + dates +
    "get_bd": get_bd, # >= 1 arg + 
    "by_name":  search_by_name, # 1 or 2 arg +
    "by_phone": search_by_phone, # 1 or 2 arg +
    "good bye": good_bye, # +
    "close": good_bye, # +
    "exit": good_bye, # +
    ".": good_bye # +
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
                args = data[0].split(" ") # data[0]
                #print(command, args)
                if not data:
                    print(error_func())
                    continue
                if len(data[0].split(", ")) == 2: # old_name new_name
                    arg_1, arg_2 = data[0].split(", ")
                    print(handler(arg_1, arg_2))
                    continue
                if len(args) >= 2:
                    if re.match(r'^[+\-\d]+$', args[-2]) and re.match(r'^\d{2}\.\d{2}\.\d{4}$',args[-1]): # add name phone birthday
                        date_arg = args[-1] # birthday
                        d_arg = datetime.strptime(date_arg, '%d.%m.%Y').date()
                        dig_arg = str(args[-2]) # phone
                        list_args = [" ".join(args[:-2]), dig_arg, d_arg] # [phone, birthday]
                        print(handler(*list_args))
                        continue
                    elif re.match(r'^[+\-\d]+$', args[-1]): # add name phone; change_phone name phone; del_phone name phone;
                        dig_arg = str(args[-1]) # phone
                        list_args = [" ".join(args[:-1]), dig_arg]
                        print(handler(*list_args))
                        continue
                if len(args) >= 1 and re.match(r'^\d{2}\.\d{2}\.\d{4}$',args[-1]) is None: # by_phone, by_name
                    #print(data)
                    print(handler(*data))
                    continue
                if re.match(r'^\d{2}\.\d{2}\.\d{4}$',args[-1]):
                    date_arg = datetime.strptime(args[-1], '%d.%m.%Y').date()
                    list_args = [" ".join(args[:-1]), date_arg] # get_bd
                    #print(list_args)
                    print(handler(*list_args))
                else:
                    print(error_func)
            else:
                print("Type Error: " + colored(f"Command << {usr_inp} >> must have any arguments !!!", "red"))


if __name__ == "__main__":
    greet()
    main()
