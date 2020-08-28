
import json
import click
import hashlib
import os
import codec_my

'''
1. sensitive_word.json文件是加密文件，解密后是一个json文件
2. 解密后的json文件，key是原字符，value是对源字符进行加密。
3. key和value是一一对应关系，可以相互转换
'''

g_keywork = 18
g_json_filename = 'sensitive_word.json'
g_splitKey = '-kktwh-'

def enc(val):
    en = codec_my.encrypt(g_keywork,val)
    return g_splitKey+en+g_splitKey

def dec(val):
    en = val.replace(g_splitKey,'',-1)
    return codec_my.decrypt(g_keywork,en)

def read_json():
    '''
    读取加密文件，解码后返回对应的json串(dict)
    '''
    pop_data = {}
    with open(g_json_filename) as f:
        text = f.read()
        text = dec(text)
        pop_data = json.loads(text)

    return pop_data

@click.group()
def app():
    pass

# def encode_file(file):
#     '''
#     1. 编码整个file文件，编码后重新写入file中
#     '''
#     with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
#         text = f1.read()
#         text = enc(text)
#         f2.write(text)

#     os.remove(file)
#     os.rename("%s.bak" % file, file)

@app.command()
@click.option("--file", type=click.Path(),default=g_json_filename)
def decode_file(file):
    '''
    1. 解码file文件整个内容，解码后重新写入file中
    '''
    
    with open(file, 'r') as f:
        try:
            json.load(f)
            print("file is json,not need decode.")
            return
        except json.JSONDecodeError as err:
            print("ok,start decode.")

    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        text = f1.read()
        text = dec(text)
        f2.write(text)

    os.remove(file)
    os.rename("%s.bak" % file, file)

@app.command()
@click.option("--json_filename", type=click.Path(),default=g_json_filename)
@click.option("--add", type=str,default='')
@click.option("--remove", type=str,default='')
def encode_json(json_filename,add,remove):
    '''
    1. 对json文件进行编码，可以增加和删除关键字字段。
    2. 输入文件必须是decode_fiel解码后的json文件。
    3. 完成后对文件进行加密重新加密。
    用法：python sensitive_encode.py encode_json --add ... --remove ...
    '''
    pop_data = {}
    with open(json_filename, 'r') as f:
        pop_data = json.load(f)
    if len(add):
        pop_data[add] = ''
    if len(remove) and remove in pop_data.keys():
        pop_data.pop(remove)
    for key in pop_data:
        pop_data[key] = enc(key)
    print(pop_data)
    with open(json_filename, 'w') as f:
        text = json.dumps(pop_data)
        f.write(enc(text))
        # json.dump(pop_data, f)
    # encode_file(json_filename)

@app.command()
def demo():
    '''
    测试方法
    '''
    print("demo start")
    s=['test1','test2']
    for i in s:
        e = enc(i)
        d = dec(e)
        print(i,e,d)

if __name__ == "__main__":
    app()
