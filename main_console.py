import os


def clear():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)


def main():
    pass


if __name__ == '__main__':
    main()
