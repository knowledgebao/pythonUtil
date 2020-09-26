import os, shutil
import dirUtil
import re
import numpy as np
import matplotlib.pyplot as plt

def drawline(index,v1,v2,v1Name,v2Name):
    l1=plt.plot(index,v1,'r--',label=v1Name)
    # l2=plt.plot(index,v2,'g--',label=v2Name)
    plt.title(v1Name+v2Name)
    plt.xlabel('index')
    plt.ylabel('count')
    plt.legend()
    plt.show()
    
def train_log_process(path, file):
    files = dirUtil.list_all_files(path)
    files = [x for x in files if file in x]

    # text = "[32m07:41:20 [D]LocalCapture_StartTrainCollect:772  LocalCapture_StartTrainCollect, run_second=21600,temper1=35.600000,temper2=33.600000,threshold=37.400000[0m"
    pattern3para = ".*LocalCapture_StartTrainCollect, run_second=(?P<run_second>[0-9]*),temper1=(?P<temper1>[\d\.]*),temper2=(?P<temper2>[\d\.]*),threshold=(?P<threshold>[\d\.]*).*"
    prog3para = re.compile(pattern3para)

    # text = "[34m13:41:24 [I]process_train_collect:215 train_3 get para.lou_bao_lv:fn=0.019652(342/17403),wu_bao_lv:fp=0.000000(0/17402)[0m"
    pattern3 = ".*lou_bao_lv:fn=(?P<fn>[0-9\.]*)\((?P<fnNum>\d*)/(?P<fnAll>\d*)\),wu_bao_lv:fp=(?P<fp>[0-9\.]*)\((?P<fpNum>\d*)/(?P<fpAll>\d*)\).*"
    prog3 = re.compile(pattern3)

    fnCounts = {}
    fpCounts = {}
    for f in files:
        print("-------------------------------------------------------------------------------------")
        print(f)
        with open(f) as fd:
            for line in fd:
                result = prog3para.match(line)
                if result:
                    d = result.groupdict()
                    print(d)#"time={},temper1={},temper2={},threshold={}".format(d["run_second"],d["temper1"],d["temper2"],d["threshold"])

                result = prog3.match(line)
                if result:
                    d = result.groupdict()
                    print("漏报:{}={}/{},误报:{}={}/{}".format(d["fn"],d["fnNum"],d["fnAll"],d["fp"],d["fpNum"],d["fpAll"]))
                    fnCounts[f]=d["fnAll"]
                    fpCounts[f]=d["fpAll"]
    index = [x for x in range(0,len(fpCounts))]
    vfp = [int(fpCounts[x]) for x in fpCounts]
    vfn = [int(fnCounts[x]) for x in fnCounts]
    print(index)
    print(vfp)
    print(vfn)
    plt.plot(index,vfp)
    plt.plot(index,vfn)
    plt.show()

if __name__ == "__main__":
    train_log_process("C:\\Users\\guoxingbao\\Desktop\\0703_产线测试文档\\data\\0909","download_file.txt")
    # train_log_process("C:\\Users\\guoxingbao\\Desktop\\0703_产线测试文档\\data\\0909\\M014001762006010061 - 合格","download_file.txt")
