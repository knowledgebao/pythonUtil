import click
import json
import os
import dirUtil
import sensitive_codec

json_filename = 'sensitive-text.json'

def process_replace(file, data):
    change = False
    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
                for key in data:
                    if key in line:
                        change = True
                        line = line.replace(key,data[key])
                f2.write(line)
    if change:
        os.remove(file)
        os.rename("%s.bak" % file, file)
    else:
        os.remove("%s.bak" % file)

@click.group()
def app():
    '''
    入口
    '''
    pass

@app.command()
@click.option("--dir", type=click.Path(),default="../../knowledgebao.github.io/_posts/3rd")
def replace_root(dir):
    '''
    1. 替换指定目录 dir 下所有文件内容的关键字key
    2. key对应的value是加密字段
    3. 可以反向将value转换回key
    '''
    data = sensitive_codec.read_json()
    if len(data):
        files = dirUtil.list_all_files(dir)
        extern = ['.md','.py','.c','.c++','.go']
        for f in files:
            if os.path.splitext(f)[-1] in extern:
                process_replace(f,data)

        print('total:', len(files))

if __name__ == "__main__":
    app()
