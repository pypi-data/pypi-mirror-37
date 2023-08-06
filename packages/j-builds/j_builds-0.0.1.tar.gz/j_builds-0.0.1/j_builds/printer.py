from termcolor import colored


class Printer:
    @staticmethod
    def __print_color(cmd, color, status):
        cmd_text = colored(f'[{cmd}] -->', color, attrs=['bold'])
        status_text = colored(status, color)
        print(f'{cmd_text} {status_text}')

    def scheduled(self, cmd):
        self.__print_color(cmd, 'yellow', 'SCHEDULED')

    def success(self, cmd):
        self.__print_color(cmd, 'green', 'SUCCESS')

    def error(self, cmd):
        self.__print_color(cmd, 'red', 'ERROR')


printer = Printer()
