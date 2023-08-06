#coding=utf-8
#autor:yangpeng
#date: 2018-10-25 15:42
def chengfa():
    for i in range(1,10):
        for j in range(1,i+1):
            print('%d*%d=%d' %(i,j,i*j),end=' ')
        print(' ')
if __name__ == '__main__':
    chengfa()