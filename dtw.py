
import numpy
import librosa
from basic_operator import *

import matplotlib.pyplot as plt

yes1 = "yes1.wav"
no2  =  "no2.wav"
yes3 =  "yes3.wav"
def mfcc(path):
    data,fs=librosa.load(path)
    # print(data)
    # print(data.shape)
    # print(fs)
    step1   =   pre_emphasis(data) 
    # print(step1)
    # print(step1.shape)
    step2   =   framing(step1,fs) 
    # print(step2)
    # print(step2.shape)
    step3   =   add_window(step2,fs)
    # print(step3)
    # print(step3.shape)
    step4   =   stft(step3) 
    # print(step4)
    # print(step4.shape)
    step5   =   mel_filter(step4, fs) 
    # print(step5)
    # print(step5.shape)
    fbank   =   log_pow(step5) 
    # print(fbank)
    # print(fbank.shape)
    mfcc  = discrete_cosine_transform(fbank)
    return mfcc
    # print(mfcc)
    # print(mfcc.shape)

def fbank(path):
    data,fs=librosa.load(path)
    # print(data)
    # print(data.shape)
    # print(fs)
    step1   =   pre_emphasis(data) 
    # print(step1)
    # print(step1.shape)
    step2   =   framing(step1,fs) 
    # print(step2)
    # print(step2.shape)
    step3   =   add_window(step2,fs)
    # print(step3)
    # print(step3.shape)
    step4   =   stft(step3) 
    # print(step4)
    # print(step4.shape)
    step5   =   mel_filter(step4, fs) 
    # print(step5)
    # print(step5.shape)
    fbank   =   log_pow(step5) 
    # print(fbank)
    # print(fbank.shape)
    
    return fbank
    # print(mfcc)
    # print(mfcc.shape)

"""
DTWDistance(s1, s2) is copied from:
http://alexminnaar.com/2014/04/16/Time-Series-Classification-and-Clustering-with-Python.html
"""
 
def DTWDistance(s1, s2,getpath=False):
    DTW={}
    len1=s1.shape[0]
    len2=s2.shape[0]
    dist = np.zeros((len1,len2))
  
    for i in range(len1):
        for j in range(len2):
            dist[i][j]=(sum((s1[i][:]-s2[j][:])*(s1[i][:]-s2[j][:])))

 
    for i in range(len1):
        DTW[(i, -1)] = float('inf')
    for i in range(len2):
        DTW[(-1, i)] = float('inf')
    DTW[(-1, -1)] = 0

    path = {}
 
    for i in range(len1):
        for j in range(len2):
            # TODO1
            # 理解dtw算法，此处写入递推公式
            DTW[(i, j)] = dist[i][j] + min(DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)])
            path_from = np.argmin([DTW[(i - 1, j)], DTW[(i, j - 1)], DTW[(i - 1, j - 1)]])
            if path_from == 0:
                path[(i, j)] = (i - 1, j)
            elif path_from == 1:
                path[(i, j)] = (i, j - 1)
            else:
                path[(i, j)] = (i - 1, j - 1)
    reversed_path = []
    i = len1 - 1
    j = len2 - 1
    while i != -1 and j != -1:
        reversed_path.append((i, j))
        i, j = path[(i, j)]

    final_path = list(reversed(reversed_path))

    return np.sqrt(DTW[len1 - 1, len2 - 1]), final_path


# TODO2
# 导入wav文件，计算mfcc，用mfcc计算两个wav文件的dtw距离
# 提示：导入文件可以使用 librosa.load('文件路径')

yes1_mfcc = mfcc('./yes1.wav')
no2_mfcc = mfcc('./no2.wav')
yes3_mfcc = mfcc('./yes3.wav')

# TODO3
# 将yes1和yes3两个音频，每一帧之间的对应关系用图表的形式画出来
# yes1作为x轴，yes3作为y轴
# 提示：在动态规划算法之中，保存算入最终dtw距离的两帧的索引index1和index2，以index1为x轴，index2为y轴画图
yes1_no2, path1 = DTWDistance(yes1_mfcc, no2_mfcc, getpath=True)
yes1_yes3, path2 = DTWDistance(yes1_mfcc, yes3_mfcc, getpath=True)
print(yes1_no2)
print(yes1_yes3)
# plot the path1
plt.plot([x[0] for x in path1], [x[1] for x in path1], 'b')
plt.title("yes1_no2")
plt.show()
# plot the path2
plt.plot([x[0] for x in path2], [x[1] for x in path2], 'r')
plt.title("yes1_yes3")
plt.show()