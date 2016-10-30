# coding=utf-8
import uniout #打印中文用的
import sys
sys.setrecursionlimit(100000)


class llgrammarparser:
    def __init__(self):
        self.grammar = []
        self.grammarindex = []
        self.finishsymbol = []
        self.notfinishsymbol = []#test
        self.first = {}
        self.follow = {}
        self.tonone = []
        self.index = {}

    def pretodumpgrammar(self):#准备文法
        '''
        #flag = False  # flag为true时一直加入设定为一个推导组
        eachreduce = []
        finish = []
        with open('grammar.txt') as f:
            for strs in f:
                if strs.startswith('/*'):
                    self.grammarindex.append(strs.replace('\n',''))
                    self.grammar.append(eachreduce)
                    self.finishsymbol.append(finish)
                    eachreduce = []
                    finish = []
                    notfinish = []
                elif strs.startswith('@'):
                    for str in strs:
                        if str == '@' or str == ' ':
                            continue
                        else:
                            if str == 't': #终结符
                                tersymbolslice = strs.split(':')
                                print tersymbolslice
                                if len(tersymbolslice) > 1:
                                    for i in map(lambda x: x.replace(' ', ''), tersymbolslice[1].split('|')):
                                        self.finishsymbol.append(i)
                                break
                            elif str == 'n':
                                ntersymbolslice = strs.split(':')
                                if len(ntersymbolslice) > 1:
                                    for i in map(lambda x: x.replace(' ', ''), ntersymbolslice[1].split('|')):
                                        self.notfinishsymbol.append(i)
                                break
                            else:
                                pass
                else:
                    strsline = strs.split('->')
                    # k = map(lambda x:x.replace(' ',''),strsline)
                    temp = {}
                    if len(strsline) > 1:
                        tobereduced = map(lambda x: x.replace('\n', ''), strsline[1].split('|'))
                        left = strsline[0]
                        temp[left] = tobereduced
                        eachreduce.append(temp)
            self.grammar.pop(0)
            self.grammar.append(eachreduce)
            self.finishsymbol.pop(0)
            #终结符怎么搞?现在看大概只能搞个symboltable进行对比了
            #
    #计算first集
    '''
        i = 0
        with open('grammarex.txt') as f:
            for strs in f:
                temp = {}
                dictrightvector = []
                grammarlist = strs.split('->')
                if len(grammarlist) > 1:
                    left = grammarlist[0].strip()
                    right = grammarlist[1].strip()
                    rightlist = right.split(' | ')
                    for item in rightlist:
                        itemlist = item.split(' ')
                        dictrightvector.append(itemlist)
                    temp[left] = dictrightvector
                    self.grammar.append(temp)
                    if left not in self.notfinishsymbol:
                        self.notfinishsymbol.append(left)
                        self.index[left] = i
                        i += 1
                else:
                    pass
            for index in self.grammar:
                values = index.values()
                for value in values:
                    for item in value:
                        for str in item:
                            if str not in self.notfinishsymbol:
                                if str not in self.finishsymbol:
                                    self.finishsymbol.append(str)

    def first(self):
        # 首先计算终结符的first集合
        for nter in self.finishsymbol:
            self.first[nter] = nter #终结符的first集等于其本身
        for eachrecgroup in self.grammar:
            #for
            pass


    def iftonone(self,ch): #ch 是否能推导出none
        if ch in self.tonone:
            return True
        elif ch == '$':
            return True
        elif ch in self.finishsymbol and ch != '$':
            return False
        else:
            flag = True
            rank = self.index[ch]
            for i in self.grammar[rank][ch]:
                if '$' in i:
                    self.tonone.append(ch)
                    return True
                else:
                    for item in i:
                        if not self.iftonone(item):
                            flag = False
            return flag
        #递归爆炸,不仅要判断出ch是否能推导出'$'同时还要将self.tonone列表填充完毕




if __name__ == '__main__':
    s = llgrammarparser()
    s.pretodumpgrammar()
    print s.grammar
    print s.notfinishsymbol
    print s.finishsymbol
    print sorted(s.index.items(), key=lambda d: d[1])
    print len(s.index)
    print s.iftonone("E'")
    #print s.tonone