import click
import os, shutil
import dirUtil

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
    files = dirUtil.list_all_files(path)
    files = [x for x in files if x.endswith(suffix)]
    for f in files:
        print(f)

if __name__ == "__main__":
    replace_lib()
    app()
