
import json
import click

def encrypt(key, s):
    b = bytearray(str(s).encode("gbk"))
    n = len(b) # 求出 b 的字节数
    c = bytearray(n*2)
    j = 0
    for i in range(0, n):
        b1 = b[i]
        b2 = b1 ^ key # b1 = b2^ key
        c1 = b2 % 16
        c2 = b2 // 16 # b2 = c2*16 + c1
        c1 = c1 + 65
        c2 = c2 + 65 # c1,c2都是0~15之间的数,加上65就变成了A-P 的字符的编码
        c[j] = c1
        c[j+1] = c2
        j = j+2
    return c.decode("gbk")
 
def decrypt(key, s):
    c = bytearray(str(s).encode("gbk"))
    n = len(c)  # 计算 b 的字节数
    if n % 2 != 0:
        return ""
    n = n // 2
    b = bytearray(n)
    j = 0
    for i in range(0, n):
        c1 = c[j]
        c2 = c[j+1]
        j = j+2
        c1 = c1 - 65
        c2 = c2 - 65
        b2 = c2*16 + c1
        b1 = b2 ^ key
        b[i] = b1
    return b.decode("gbk")

g_keywork = 2
json_filename = 'sensitive-text.json'

@click.group()
def app():
    pass

@app.command()
@click.option("--json_filename", type=click.Path(),default=json_filename)
def encode_file(json_filename):
    pop_data = {}
    incressNum = 0
    with open(json_filename) as f:
        pop_data = json.load(f)
        for key in pop_data:
            print(key,pop_data[key])
            pop_data[key] = str(incressNum)+'_'+encrypt(g_keywork, key)
            incressNum += 1
        print(pop_data)
    with open(json_filename, 'w') as f:
        json.dump(pop_data, f)

@app.command()
@click.option("--json_filename", type=click.Path(),default=json_filename)
def decode_file(json_filename):
    with open(json_filename) as f:
        pop_data = json.load(f)
        for key in pop_data:
            dec = decrypt(g_keywork,pop_data[key].split("_")[1])
            print(key,dec,pop_data[key])
            assert key == dec

@app.command()
@click.Argument("text", type=str)
@click.option("--json_filename", type=click.Path(),default=json_filename)
def add_text(json_filename,text):
    with open(json_filename) as f:
        pop_data = json.load(f)
        pop_data[text] = ""
        encode_file(json_filename)

if __name__ == "__main__":
    app()
