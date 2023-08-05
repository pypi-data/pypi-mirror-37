# encoding: utf-8


def command_confirm(prompt="Do you want to do the fix? [Y/n]: "):
    """Get confirm from command.
    
     Y|y: returns True
     N|n: returns False"""

    prompt_w = "Can't recognize, please retry. [Y/n]: "

    answer = raw_input(prompt)
    while answer not in ['Y', 'y', 'N', 'n']:
        answer = raw_input(prompt_w)

    if answer in ['Y', 'y']:
        return True
    else:
        return False


if __name__ == '__main__':
    res = command_confirm()
    print(res)
