from termcolor import colored
from show_greeting import greet

from commands import hello, helper, add_contact, del_contact, del_phone, error_func
from commands import change_phone, show_all, show_phone, good_bye, add_phone, change_name

dict_cmd = {
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
    "good bye": good_bye,
    "close": good_bye,
    "exit": good_bye,
    ".": good_bye
}

simple_cmds = ["show all", "good bye", "close", "exit", ".", "help", "hello"]


def main():
    while True:
        user_input = input(colored("\nEnter command: ", "green"))
        if user_input in simple_cmds:
            simple_func = dict_cmd[user_input.strip()]
            print(simple_func())
        elif not user_input or user_input.split()[0] not in dict_cmd.keys():
            print(error_func())
        else:
            if user_input.split()[0] in dict_cmd.keys() and len(user_input.split()) > 1:
                command, *data = user_input.strip().split(' ', 1)
                handler = dict_cmd[command]
                args = data[0].split(" ")
                # print(command, args)
                if not data:
                    print(error_func())
                if len(data[0].split(", ")) == 2:
                    old_name, new_name = data[0].split(", ")
                    print(handler(old_name, new_name))
                    continue
                if len(args) >= 2:
                    if all(symb.isdigit() or symb in ['+', '-'] for symb in args[-1]):
                        dig_arg = str(args[-1])
                        list_args = [" ".join(args[:-1]), dig_arg]
                        print(handler(*list_args))
                        continue
                if len(data) == 1:
                    print(handler(*data))
            else:
                print(
                    "Type Error: " + colored(f"Command << {user_input} >> must have any arguments !!!", "red"))


if __name__ == "__main__":
    greet()
    main()
