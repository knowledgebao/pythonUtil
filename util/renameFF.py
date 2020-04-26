'''
1. 查找制定目录下以 lib 开头，以 .a 结尾的文件名 libName.a
2. 查找是否有对应的 Name.lib 命名的文件，如果有 则在前边加 lib
比如：文件夹下存在 libavcodec.a 和 avcodec.lib ，则将 avcodec.lib 重命名为 libavcodec.lib
'''
import click
import os, shutil

@click.group()
def app():
    pass

@app.command()
@click.option("--prefix", type=str, default="lib")
@click.option("--suffix", type=str, default="a")
@click.argument("process_dir", type=click.Path())
def rename_lib(process_dir, prefix,suffix):
    '''example: python renameFF.py rename_lib C:\work\local\ssn-deps-v1-msvc-debug-x86_64\lib'''
    dictFile = {}
    for parent, dirnames, filenames in os.walk(process_dir,  followlinks=True):
        for filename in filenames:
            dictFile[filename] = parent
    
    for key in dictFile:
        if key.startswith(prefix) and key.endswith(suffix):
            findStr = key[len(prefix):-1*len(suffix)]+"lib"
            if findStr in dictFile:
                dst = os.path.join(dictFile[findStr],prefix+findStr)
                print(findStr,dst)
                os.rename(os.path.join(dictFile[findStr],findStr),dst)
    print(dictFile.keys())

if __name__ == "__main__":
    app()
