import os
import io
import requests
import json

class Collect:
    def __init__(self, docs_folder_github, folder_to_collect=None) -> None:
        docs_folder_github = docs_folder_github.replace('https://', '').replace('http://', '')
        docs_folder_github = docs_folder_github.split('/')
        self.branch = docs_folder_github[docs_folder_github.index('tree')+1]
        [docs_folder_github.remove(i) for i in ['github.com', 'tree', self.branch] if i in docs_folder_github]
        self.maintainer = docs_folder_github[0]
        self.repository_name = docs_folder_github[1]
        self.docslocate = '/'.join(docs_folder_github[2:])
        self.folders = []
        self.files = []
        self.folder_to_collect = self.repository_name if not folder_to_collect else folder_to_collect
        self.subpath = '/'.join(['collected', self.repository_name])
        try:
            os.makedirs(self.subpath)
        except FileExistsError:
            pass
        print('Downloading '+self.repository_name+' docs...')
        self.collect_all()
        print('Complete!')

    def collect_all(self, folder_name='', url=None):
        for file in self.collect_by_type(_type='file', folder_name=folder_name, url=url):
            try:
                content = requests.get(file['download_url']).text
                tocreatepath = os.path.join(self.subpath, file['path']).replace('\\', '/')
                if not os.path.isdir('/'.join(tocreatepath.split('/')[:-1])):
                    os.makedirs('/'.join(tocreatepath.split('/')[:-1]))
                with io.open(tocreatepath, 'w+', encoding='UTF-8') as f:
                    f.write(content)
            except:
                pass
        
        
        for directory in self.collect_by_type(_type='dir', folder_name=folder_name):
            try:
                tocreatepath = os.path.join(self.subpath, directory['path']).replace('\\', '/')
                os.makedirs(tocreatepath)
                if self.dir_empty(tocreatepath):
                    self.collect_all(url=directory['_links']['self'])
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
        return [i for i in j if i['type'] == _type]

    
    def dir_empty(self, path):
        return True if not os.listdir(path) else False 


