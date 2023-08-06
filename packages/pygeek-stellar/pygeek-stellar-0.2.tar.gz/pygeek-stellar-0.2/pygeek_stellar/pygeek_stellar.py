# Local imports
from .geek_stellar_cmd import GeekStellarCmd
from .cli_session import *


def main():
    """
    Entry point of pygeek-stellar tool. Prints the banner, initializes a
    CLI session and starts the pygeek-stellar CMD interpreter.
    """
    print_banner()

    session = init_cli_session()
    if not session:
        print("No session could be initialized. Exiting..")
        return

    cmd = GeekStellarCmd(session)
    print_current_session_details(session)
    cmd.do_help(None)
    cmd.cmdloop()


def print_banner():
    """
    Prints the a pygeek-stellar banner in the Command Line Interface.
    """
    ch = '#'
    length = len(CLI_BANNER_TEXT) + 8
    spaced_text = ' %s ' % CLI_BANNER_TEXT
    banner = spaced_text.center(length, ch)
    print('\n' + ch * length)
    print(banner)
    print(ch * length + '\n')


def print_current_session_details(session):
    """
    Prints information regarding the selected account for a given CLI session.
    :param CliSession session: Current CLI session.
    """
    print('\nThe following account was chosen: {}\n'.format(session.to_str()))


if __name__ == "__main__":
    main()
