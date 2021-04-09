from discord.ext import commands, tasks
from colorama import Fore, init
import os, discord, json


class Console():
    def __init__(self):
        init()

    def print_logo(self):
        os.system('cls && title [Its-Vichy] Rankup' if os.name == 'nt' else 'clear')

        print('''
                ██████╗  █████╗ ███╗   ██╗██╗  ██╗██╗   ██╗██████╗
                ██╔══██╗██╔══██╗████╗  ██║██║ ██╔╝██║   ██║██╔══██╗
                ██████╔╝███████║██╔██╗ ██║█████╔╝ ██║   ██║██████╔╝
                ██╔══██╗██╔══██║██║╚██╗██║██╔═██╗ ██║   ██║██╔═══╝
                ██║  ██║██║  ██║██║ ╚████║██║  ██╗╚██████╔╝██║
                ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝ ╚═════╝ ╚═╝
             '''.replace('█', f'{Fore.MAGENTA}█{Fore.WHITE}'))

    def log(self, color, past, text, finish= '.'):
        print(f'{Fore.WHITE}[{color}{past}{Fore.WHITE}] {text}{finish}')


class Rankup():
    def __init__(self, config):
        self.prefix = config['PREFIX']
        self.token = config['TOKEN']
        self.console = Console()

        rankup_client = commands.Bot(command_prefix= self.prefix)
        self.rankup_client = rankup_client


        @tasks.loop(hours= config['TIMEOUT'])
        async def stonks():
            pub = ''

            with open('./pub.txt', 'r', encoding="utf8", errors="ignore") as pub_file:
                for line in pub_file:
                    pub += line

            for channel in config['DBUMP_CHANNELS']:
                self.console.log(Fore.YELLOW, '+', f'Dbump: {channel}')
                await rankup_client.get_channel(channel).send('!d bump')

            for channel in config['PUB_CHANNELS']:
                self.console.log(Fore.YELLOW, '+', f'Sent pub to {channel}')
                await rankup_client.get_channel(channel).send(pub)

        @rankup_client.event
        async def on_ready():
            self.console.log(Fore.GREEN, '*', f'Connected to {rankup_client.user}')
            await stonks.start()

    def start(self):
        self.rankup_client.run(self.token, bot= False)

if __name__ == '__main__':
    with open('./config.json', 'r') as config:
        Console().print_logo()
        Rankup(json.load(config)).start()