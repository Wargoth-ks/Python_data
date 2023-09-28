from termcolor import colored


def greet():
    frame_width = 28
    title = "Welcome to phone book!"

    # Borders
    top_border = "+" + "-" * (frame_width - 2) + "+"
    side_border = "|" + " " * (frame_width - 2) + "|"

    # Titles
    title_len = len(title)
    title_side_spaces = (frame_width - title_len - 2) // 2
    title_line = (
        "|"
        + " " * title_side_spaces
        + title
        + " " * (frame_width - title_side_spaces - title_len - 2)
        + "|"
    )

    # Print
    print(colored(top_border, "cyan"))
    print(colored(side_border, "cyan"))
    print(colored(title_line, "cyan"))
    print(colored(side_border, "cyan"))
    print(colored(top_border, "cyan"))
    print('\nTo get help on the commands, please type "help"')
