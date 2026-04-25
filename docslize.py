import os, random
from source import CATEGORIES, collect, tabs
from colorama import Fore
from requests.exceptions import RequestException
from time import sleep
clear_command = 'cls' if os.name == 'nt' else 'clear'

class Main:
    def __init__(self) -> None:

        self.unique_ids = {}
        self.colors = [Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX]

        logo = """██████╗░░█████╗░░█████╗░░██████╗██╗░░░░░██╗███████╗███████╗
                  ██╔══██╗██╔══██╗██╔══██╗██╔════╝██║░░░░░██║╚════██║██╔════╝
                  ██║░░██║██║░░██║██║░░╚═╝╚█████╗░██║░░░░░██║░░███╔═╝█████╗░░
                  ██║░░██║██║░░██║██║░░██╗░╚═══██╗██║░░░░░██║██╔══╝░░██╔══╝░░
                  ██████╔╝╚█████╔╝╚█████╔╝██████╔╝███████╗██║███████╗███████╗
                  ╚═════╝░░╚════╝░░╚════╝░╚═════╝░╚══════╝╚═╝╚══════╝╚══════╝"""
        print('\n'.join([random.choice(self.colors)+tabs+i.strip() for i in logo.splitlines()])+'\n')
        print(tabs+Fore.LIGHTRED_EX+'Please choice and enter the id of document you want to download : ')
        print()
        for cat, subs in CATEGORIES.items():
            print(tabs+Fore.LIGHTCYAN_EX+(' '*2)+'[*] '+cat)
            for s, v in subs.items():
                uniqueid = str(random.randint(111, 999))
                print(tabs+Fore.LIGHTBLUE_EX+(' '*5)+'|--['+Fore.BLUE+uniqueid+Fore.LIGHTBLUE_EX+'] '+ s)
                self.unique_ids[uniqueid] = v
            print()

        first_time_alert = False
        try:
            while True:     
                i = input(tabs+Fore.LIGHTYELLOW_EX+"[ID] >> "+Fore.LIGHTWHITE_EX)
                if i not in self.unique_ids:
                    continue
                if not first_time_alert:
                    print(tabs+Fore.LIGHTRED_EX+(' '*2)+'Note: documents are download in "collected" folder.')
                    first_time_alert = True
                try:
                    collect.Collect(self.unique_ids[i])
                except (ConnectionError, RequestException):
                    print(tabs+Fore.RED+'Connection error !\a')
                
                except collect.APILimited as e:
                    print(tabs+Fore.RED+ f'{e.__note__}, check the link blow, try again later !\a')
                    print(tabs+Fore.LIGHTCYAN_EX + 'https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api#rate-limiting')
                
                except PermissionError as e:
                    print(tabs+Fore.RED+ f'An error occurred({e}) !\a')
                    
                except:
                    print(tabs+Fore.RED+'An error occurred !\a')

        except KeyboardInterrupt as e:
            os.system(clear_command)
            if str(e) == "Close":
                try:
                    print(f'\r{tabs}{Fore.RED}Download process was failed, try again!\a')
                    sleep(1.25)
                    return self.__init__()
                except KeyboardInterrupt:
                    return self.__init__()
            else:
                return self.__init__()
        except:
            pass


os.system(clear_command)
print('\n'*4)
app = Main()
