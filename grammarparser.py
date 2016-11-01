# coding=utf-8
import uniout  # 打印中文用的

import sys
from collections import namedtuple

sys.setrecursionlimit(10000)

item = namedtuple('item', 'left tolist dotindex') #项集中每一个状态的定义

#暂时写成SLR(1)的，以后再改吧
class llgrammarparser:
    def __init__(self):
        self.grammar = []
        self.grammarindex = []
        self.finishsymbol = []
        self.notfinishsymbol = []  # test
        self.first = {}
        self.follow = {}
        self.tonone = []
        self.index = {}
        self.itemfamiy = []#LR(0)项集族，是一个列表，列表中的每一项都是一个列表，其值为一个字典，字典键为每个推导的左部，值为一个包含右部推导的一个
                            #列表与项集的点的位置构成的二元组
    def pretodumpgrammar(self):  # 准备文法
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

    def makefirst(self):
        # 首先计算终结符的first集合
        # for nter in self.finishsymbol:
        #    self.first[nter] = nter #终结符的first集等于其本身
        # eachfirstset = {}
        # for ter in self.notfinishsymbol:
        #    rank = self.index[ter]
        # 本身递归很简单，但python递归支持实在太差
        '''
        for symbol in (self.finishsymbol + self.notfinishsymbol):
            if symbol in self.finishsymbol:
                self.first[symbol] = symbol  # 终结符的first集合等于他本身
            else:
                rank = self.index[symbol]
                golist = map(lambda l: l[0], self.grammar[rank][symbol])
                golist = list(set(golist))
                stack = []
                for item in golist:
                    if item in self.finishsymbol:
                        self.first[symbol].append(item)
                    elif item in self.notfinishsymbol:
                        stack.append(item)
                while len(stack) != 0:
                    pickone = stack.pop(0)
                    pickitem = self.index[pickone]
                    itemgolist = map(lambda l: l[0], self.grammar[pickitem][pickone])
                    golist = list(set(golist))
                    for i in golist:
                        if i in self.finishsymbol:
                            self.first[symbol].append(i)
                        elif i in self.notfinishsymbol:
                            stack.append(i)
            '''
            #naive的算法完全跑不了，尝试一下从后向前记忆化搜索估计会快很多
        for ter in self.finishsymbol:
            self.first[ter] = [ter]
        for nter in self.notfinishsymbol:
            self.first[nter] = []
        haschange = True
        while(haschange):
            haschange = False
            for nter in self.notfinishsymbol:
                items = self.hasLeft(nter)
                for item in items:
                    changed = self.combine(self.first[nter], self.first[item])
                    if changed:
                        haschange = True
            '''
            rank = self.index[nter]
            for item in map(lambda x: x[0],self.grammar[rank][nter]):
                if item == nter:
                    continue
                self.first[nter] += self.first[item]
            self.first[nter] = list(set(self.first[nter]))
            '''
            
    '''
    def iftonone(self,ch): #ch 是否能推导出none
        if ch in self.finishsymbol and ch != '$':
            return False
        elif ch in self.notfinishsymbol:
            #flag = True
            rank = self.index[ch]
            if ['$'] in self.grammar[rank][ch]:
                return True
            return False
        #递归爆炸,不仅要判断出ch是否能推导出'$'同时还要将self.tonone列表填充完毕,这里非常难处理
        #只能考虑利用文法本身的特点予以简化,只比较ch所对应字典的值(二维数组)中是否存在['$']的数组
        #例如K = x1x2x3x4 比较精确的判断是只有非终结符x1x2x3x4都可以推导为空的情况才可以说K可以
        #推导为空，只能牺牲一定精确度
        #好吧，shachale
    '''

    #计算非终结符的follow集
    def makefollow(self):
        if len(self.first) == 0:
            self.makefirst()
        for nter in self.notfinishsymbol:
            self.follow[nter] = []
        self.follow["E'"].append('$')
        haschange = True
        while haschange:
            haschange = False
            for nter in self.notfinishsymbol:
                if nter == "E'":
                    continue
                items = self.getleft(nter)
                for item in items:#可以在哪种推导中发现它
                    rank = self.index[item]
                    l = filter(lambda x: nter in x, self.grammar[rank][item])#nter 在哪种右部推导中
                    for i in l:
                        idx = i.index(nter)
                        if idx < len(i) - 1:
                            changed = self.combine(self.follow[nter],self.first[i[idx + 1]])
                            if changed:
                                haschange = True
                        elif idx == len(i) - 1:
                            changed = self.combine(self.follow[nter],self.follow[item])
                            if changed:
                                haschange = True

    def hasLeft(self,symbol):
        rank = self.index[symbol]
        return map(lambda x: x[0],self.grammar[rank][symbol])

    def combine(self,l1,l2):
        haschange = False
        for c in l2:
            if c not in l1:
                l1.append(c)
                haschange = True
        return haschange

    #这个符号能从哪个非终结符推出?
    def getleft(self,symbol):
        res = []
        for nter in self.notfinishsymbol:
            rank = self.index[nter]
            if symbol in reduce(lambda x,y:x+y,self.grammar[rank][nter]):
                res.append(nter)
        return res


    def getitemfamily(self):
        pass

    def closure(self,statelist): #传入一个项集　list[item]
        res = []
        temp = []
        haschange = True
        res += statelist
        while haschange:
            haschange = False
            for items in res:
                if items.dotindex != len(items.tolist) and items.tolist[items.dotindex] in self.notfinishsymbol:
                    a = items.dotindex
                    rank = self.index[items.tolist[a]]
                    for eachlist in self.grammar[rank][items.tolist[a]]:
                        state = item(items.tolist[a],eachlist,0)
                        temp.append(state)
                    changed = self.combine(res,temp)
                    if changed:
                        haschange = True
        return res


    def goto(self,statelist,symbol):#statelist 项集　symbol 文法符号 返回一个项集
        res = []
        for state in statelist:
            a = state.dotindex
            if state.dotindex != len(state.tolist) and state.tolist[a] == symbol:
                aftershift = item(state.left,state.tolist,a + 1)
                res.append(aftershift)
        print res
        return self.closure(res)

if __name__ == '__main__':
    s = llgrammarparser()
    s.pretodumpgrammar()
    print s.grammar
    print s.notfinishsymbol
    print s.finishsymbol
    print sorted(s.index.items(), key=lambda d: d[1])
    #print s.index
    # print s.iftonone('relational_expression')
    # print s.grammar[43]
    # print s.tonone
    #print s.hasLeft('Px')
    s.makefirst()
    print s.first
    s.makefollow()
    print s.follow
    print len(s.follow)
    print len(s.notfinishsymbol)
    #print s.getleft('E')
    print s.closure([item("E'",['E'],0)])
    print s.goto([item("E'",['E'],1),item("E",['E','+','T'],1)],'+')