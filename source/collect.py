import os
import io
import requests
import json
from colorama import Fore
from . import tabs
import tqdm

class APILimited(Exception):
    __note__ = "Connection error(API rate limit)"

class Collect:
    def __init__(self, docs_folder_github, folder_to_collect=None) -> None:
        docs_folder_github = docs_folder_github.replace('https://', '').replace('http://', '')
        docs_folder_github = docs_folder_github.split('/')

        if 'tree' not in docs_folder_github: #If documents has own repository like laravel
            self.branch = ''
        else:
            self.branch = docs_folder_github[docs_folder_github.index('tree')+1]

        [docs_folder_github.remove(i) for i in ['github.com', 'tree', self.branch] if i in docs_folder_github]

        self.maintainer = docs_folder_github[0]
        self.repository_name = docs_folder_github[1]
        self.docslocate = '/'.join(docs_folder_github[2:])
        self.folders = []
        self.files = []
        self.folder_to_collect = self.repository_name if not folder_to_collect else folder_to_collect
        self.subpath = '/'.join(['collected',self.repository_name] if self.branch else ['collected', self.maintainer, self.repository_name])
  
        try:
            os.makedirs(self.subpath)
        except FileExistsError:
            pass

        print(tabs+Fore.LIGHTGREEN_EX+'Downloading '+Fore.GREEN+ (self.repository_name if self.branch else self.maintainer) + Fore.LIGHTGREEN_EX+' docs...')
        print(Fore.LIGHTBLUE_EX)


        self.collect_all()


        print(Fore.LIGHTGREEN_EX)
        print(tabs+'Complete!')

    def collect_all(self, folder_name='', url=None):
        try:
            collect_by_file_type = self.collect_by_type(_type='file', folder_name=folder_name, url=url)
            collect_by_dir_type = self.collect_by_type(_type='dir', folder_name=folder_name, url=url)
            with tqdm.tqdm(total=len(collect_by_file_type)) as pbar:
                for file in collect_by_file_type:
                    try:
                        tocreatepath = os.path.join(self.subpath, file['path']).replace('\\', '/')
                        pbar.set_description('Writing '+ tocreatepath)
                        content = requests.get(file['download_url']).text
                        try:
                            if self.is_limited(json.loads(content)):
                                raise APILimited
                        except json.JSONDecodeError:
                            pass

                        if not os.path.isdir('/'.join(tocreatepath.split('/')[:-1])):
                            os.makedirs('/'.join(tocreatepath.split('/')[:-1]))
                        with io.open(tocreatepath, 'w+', encoding='UTF-8') as f:
                            f.write(content)
                        
                        pbar.update(1)
                    
                    except APILimited as e:
                        print(tabs+Fore.RED+ f'{e.__note__}, Failed to write {tocreatepath} !{Fore.LIGHTBLUE_EX}')
                        print('\n'*2)

        except (ConnectionError, requests.exceptions.RequestException):
            raise ConnectionError

        except KeyboardInterrupt:
            raise KeyboardInterrupt("Close")
        
        except APILimited:
            raise APILimited

        except:
            pass

        for directory in collect_by_dir_type:
            try:
                tocreatepath = os.path.join(self.subpath, directory['path']).replace('\\', '/')
                os.makedirs(tocreatepath)
                if self.dir_empty(tocreatepath):
                    self.collect_all(url=directory['_links']['self'])

            except APILimited as e:
                print(tabs+Fore.RED+ f'{e.__note__}, Failed to catch \n{tabs}{directory['_links']['self']} !{Fore.LIGHTBLUE_EX}')
                print('\n'*2)
                continue
            except:
                pass

        
    def collect_by_type(self, folder_name='', _type='dir', url=None):
        if url:
            j = json.loads(requests.get(url).text)
        else:
            j = json.loads(requests.get('https://api.github.com/repos/{}/{}/contents/{}{}?ref={}'.format(
                self.maintainer,
                self.repository_name,
                self.docslocate,
                '/'+folder_name if folder_name else '',
                self.branch
            )).text)

        if self.is_limited(j):
            raise APILimited

        return [i for i in j if i['type'] == _type]

    
    def dir_empty(self, path):
        return not os.listdir(path)

    @staticmethod
    def is_limited(content):
        return isinstance(content, dict) and content.get("message").startswith("API rate limit exceeded for")
    