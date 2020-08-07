import os

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

if __name__ == "__main__":
    f = '../../knowledgebao.github.io/_posts/2019-06-28-待整理列表.md'
    assert(os.path.exists(f))
    assert(os.path.isfile(f))
    print(os.path.dirname(f))
    print(os.path.basename(f))
    print(os.path.splitext(os.path.basename(f))[0])
    print(os.path.splitext(f))
    print(os.path.splitext(f)[-1])
