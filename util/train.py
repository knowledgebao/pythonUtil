import os, shutil
import dirUtil
import re
import numpy as np
import matplotlib.pyplot as plt

# text = "[34m09:00:48 [I]Track_TrackPush:554 guoxb,track_id=2,rect=(872,400,72,72)[0m"
patterntrack = ".*guoxb,track_id=(?P<track_id>[0-9]*),rect=\((?P<x>[\d]*),(?P<y>[\d]*),(?P<w>[\d]*),(?P<h>[\d]*)\).*"
progtrack = re.compile(patterntrack)

# text="[33m09:00:34 [W]LocalCapture_PushCapture:327 train_3 exist add trackID=2(2)---size(2)--2--35.800000[0m"
# text="[33m09:00:32 [W]LocalCapture_PushCapture:334 train_3 not exist add trackID=2---0--35.800000[0m"
patterntempertrack = ".*exist add trackID=(?P<track_id>[0-9]*).*"
progtempertrack = re.compile(patterntempertrack)

# text = "[32m07:41:20 [D]LocalCapture_StartTrainCollect:772  LocalCapture_StartTrainCollect, run_second=21600,temper1=35.600000,temper2=33.600000,threshold=37.400000[0m"
pattern3para = ".*LocalCapture_StartTrainCollect, run_second=(?P<run_second>[0-9]*),temper1=(?P<temper1>[\d\.]*),temper2=(?P<temper2>[\d\.]*),threshold=(?P<threshold>[\d\.]*).*"
prog3para = re.compile(pattern3para)

# text = "[34m13:41:24 [I]process_train_collect:215 train_3 get para.lou_bao_lv:fn=0.019652(342/17403),wu_bao_lv:fp=0.000000(0/17402)[0m"
pattern3 = ".*lou_bao_lv:fn=(?P<fn>[0-9\.]*)\((?P<fnNum>\d*)/(?P<fnAll>\d*)\),wu_bao_lv:fp=(?P<fp>[0-9\.]*)\((?P<fpNum>\d*)/(?P<fpAll>\d*)\).*"
prog3 = re.compile(pattern3)

def drawTrack(tracks,temper_tracks):
    newtracks = []
    newttemper_tracks = []
    for i in range(len(tracks)):
        if len(tracks[i]) == 2:
            for k in tracks[i].keys():
                newtracks.append(tracks[i][k])
                newttemper_tracks.append(temper_tracks[i][k])
        else:
            newtracks.append(0)
            newtracks.append(0)
            newttemper_tracks.append(0)
            newttemper_tracks.append(0)
    print("原始track",newtracks)
    print("推送track",newttemper_tracks)

    index2 = [x for x in range(0,len(newtracks))]
    print(len(index2),len(newtracks),len(newttemper_tracks))
    plt.plot(index2,newtracks,label="原始track",marker='*')
    plt.plot(index2,newttemper_tracks,label="推送track",marker='^')
    plt.legend(('原始track', '推送track'), loc='upper right')  
    plt.show()

def processFolder(path,file):
    files = dirUtil.list_all_files(path)
    files = [x for x in files if file in x]
    for src in files:
        pre,ext = os.path.splitext(src)
        dst = pre + "_back" + ext
        start = False
        with open(src) as f:
            with open(dst,mode='a') as f2:
                for line in f:
                    result = prog3para.match(line)
                    if result:
                        start = True
                        print(result.group())
                        f2.seek(0)
                        f2.truncate()
                    if start:
                        f2.write(line)
    
def train_log_process(path, file):
    files = dirUtil.list_all_files(path)
    files = [x for x in files if file in x]

    trainLogInfo = {}
    for f in files:
        print("-------------------------------------------------------------------------------------")
        print(f)
        tracks = {}
        tempertracks = {}
        with open(f) as fd:
            trainLogInfo[f]={
                "track":{},
                "temper_track":{},
                "fnAll":0,
                "fpAll":0,
                "fn":0,
                "fp":0,
                "fnNum":0,
                "fpNum":0,
                "run_second":0,
                "temper1":0,
                "temper2":0,
                "threshold":0,
                "stats":1
            }
            for line in fd:
                result = progtrack.match(line)
                if result:
                    d = result.groupdict()
                    tid=int(d["track_id"])
                    # print(tid,tracks)
                    trainLogInfo[f]["track"][tid] = 1 if tid not in trainLogInfo[f]["track"].keys() else trainLogInfo[f]["track"][tid]+1

                result = progtempertrack.match(line)
                if result:
                    d = result.groupdict()
                    tid=int(d["track_id"])
                    # print(tid,tracks)
                    trainLogInfo[f]["temper_track"][tid] = 1 if tid not in trainLogInfo[f]["temper_track"].keys() else trainLogInfo[f]["temper_track"][tid]+1

                result = prog3para.match(line)
                if result:
                    d = result.groupdict()
                    print(d)
                    trainLogInfo[f]["run_second"]=d["run_second"]
                    trainLogInfo[f]["temper1"]=d["temper1"]
                    trainLogInfo[f]["temper2"]=d["temper2"]
                    trainLogInfo[f]["threshold"]=d["threshold"]
                    trainLogInfo[f]["track"] = {}
                    trainLogInfo[f]["temper_track"] = {}

                result = prog3.match(line)
                if result:
                    d = result.groupdict()
                    print(u"误报:{}={}/{},漏报:{}={}/{}".format(d["fn"],d["fnNum"],d["fnAll"],d["fp"],d["fpNum"],d["fpAll"]))
                    trainLogInfo[f]["fnAll"]=d["fnAll"]
                    trainLogInfo[f]["fpAll"]=d["fpAll"]
                    trainLogInfo[f]["stats"]= (0 if "合格" in f else 1)
                    trainLogInfo[f]["fn"]= d["fn"]
                    trainLogInfo[f]["fnNum"]= d["fnNum"]
                    trainLogInfo[f]["fp"]= d["fp"]
                    trainLogInfo[f]["fpNum"]= d["fpNum"]
    index = [x for x in range(0,len(trainLogInfo))]
    statss = [trainLogInfo[x]["stats"] for x in trainLogInfo]
    fns = [trainLogInfo[x]["fn"] for x in trainLogInfo]
    fps = [trainLogInfo[x]["fp"] for x in trainLogInfo]
    fpNums = [trainLogInfo[x]["fpNum"] for x in trainLogInfo]
    fnNums = [trainLogInfo[x]["fnNum"] for x in trainLogInfo]
    fpAlls = [trainLogInfo[x]["fpAll"] for x in trainLogInfo]
    fnAlls = [trainLogInfo[x]["fnAll"] for x in trainLogInfo]
    tracks = [trainLogInfo[x]["track"] for x in trainLogInfo]
    temper_tracks = [trainLogInfo[x]["temper_track"] for x in trainLogInfo]
    print("=======================================================")
    for i in index:
        print(i,files[i])
    print(index)
    print("状态",statss)
    print("误报",fpAlls)
    print("漏报",fnAlls)
    print("原始track",tracks)
    print("推送track",temper_tracks)
    drawTrack(tracks,temper_tracks)

if __name__ == "__main__":
    # processFolder("C:\\Users\\Administrator\\Desktop\\0909","download_file.txt")
    train_log_process("C:\\Users\\Administrator\\Desktop\\0910","txt")
