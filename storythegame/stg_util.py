import inspect
import os.path


def keypress():
    """keypress function modified form code.activestate.com/recipes/...

    Waits for the user to press a key. Returns the ascii code
    for the key pressed or zero for a function key pressed.
    Aborts function with CTL-C
    """
    import time
    import msvcrt

    while 1:
        if msvcrt.kbhit():
            a = ord(msvcrt.getch())
            # is it a function key?
            if a == 0 or a == 224:
                # discard second byte of key scan code
                msvcrt.getch()
                return 0
            else:
                return a

        # TODO implement keypress as an animation
        # for dot in ['.', '..', '...']:
        # print dot
        # time.sleep(0.5)

        # TODO: Validate that time.sleep effects performance
        # reduce CPU workload during while execution
        time.sleep(0.5)


def prompt(custom_prompt="--> "):
    """
    Simple raw_input with custom prompt.
    Returns the raw_input
    """
    answer = raw_input(custom_prompt).lower()
    return answer


def get_file_path(current_file='', sub_dir=''):
    util_path = os.path.dirname(inspect.getabsfile(inspect.currentframe()))
    if current_file == '':
        return util_path + "\\"
    elif sub_dir == '':
        current_file = os.path.join(util_path, current_file) + "\\"
    else:
        current_file = os.path.join(util_path, sub_dir, current_file) + "\\"

    return current_file
