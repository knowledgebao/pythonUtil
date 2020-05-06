import click
import os, shutil

def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files

@click.group()
def app():
    pass

@app.command()
@click.option("--config", type=click.Path(),default="./config.json")
@click.option("--path", type=click.Path(), default="C:\gwork\knowledgebao\knowledgebao.github.io\_posts")
@click.option("--suffix", type=str, default="md")
def replace_lib(config, path, suffix):
    '''
    example: python renameFF.py rename_lib C:\work\local\ssn-deps-v1-msvc-debug-x86_64\lib
    '''
    files = list_all_files(path)
    files = [x for x in files if x.endswith(suffix)]
    for f in files:
        print(f)

if __name__ == "__main__":
    replace_lib()
    app()
