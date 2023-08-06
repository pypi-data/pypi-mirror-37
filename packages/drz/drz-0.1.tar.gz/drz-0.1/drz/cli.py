import sys


# FIRST YOU HANDLE ARG
def entrypoint():
    commands = {
        'deploy': deploy
    }

    command = sys.argv[1]
    if command in commands:
        commands[command]()
    else:
        print("Unknown argument '%s'" % command)


def deploy():
    print("DEPLOYING NOW!")
