# coding=utf-8
import uniout #打印中文用的
class llgrammarparser:
    def __init__(self):
        self.grammar = []
        self.grammarindex = []

    def pretodumpleftrec(self):  # 准备文法并消除左递归
        #flag = False  # flag为true时一直加入设定为一个推导组
        eachreduce = []
        with open('grammar.txt') as f:
            for strs in f:
                if strs.startswith('/*'):
                    self.grammarindex.append(strs.replace('\n',''))
                    self.grammar.append(eachreduce)
                    eachreduce = []
                else:
                    strsline = strs.split('->')
                    # k = map(lambda x:x.replace(' ',''),strsline)
                    temp = {}
                    if len(strsline) > 1:
                        tobereduced = map(lambda x: x.replace('\n',''),strsline[1].split('|'))
                        left = strsline[0]
                        temp[left] = tobereduced
                        eachreduce.append(temp)
            self.grammar.append(eachreduce)
            self.grammar.pop(0)
        #消除左递归
