import collections
class Lexer:
    def __init__(self):
        self.keywords = ['int', 'float', 'bool','char','if', 'else', 'return', 'do', 'while', 'return', 'def']
        self.operator = ['+', '-', '*', '/', '|', '&', '^','!','%','>','<']
        self.edgeop = ['=', ';', '[', ']', '.','{','}','(',')']
        self.noteDFA = [['^/', '/', '#', '#', '#'], ['^/*', '/', '*', '#', '#'],
                   ['#', '#', '^*', '*', '#'], ['#', '#', '^/*', '*', '/'],
                   ['#', '#', '#', '#', '#']]
        self.digitDFA = {0: {'d': 1}, 1: {'d': 1, '.': 2, 'e': 4}, 2: {'d': 3},
                    3: {'d': 3, 'e': 4}, 4: {'+-': 5, 'd': 6}, 5: {'d': 6}, 6: {'d': 6,}}
        #self.stringDFA = ["#\\b#", "##a#", "#\\b\"", "####"]
        self.stringdfa = {0: {'\"': 1}, 1: {'a': 1, '\"': 2}}
        self.escapech = ['\a','\b','\f','\n','\r','\t','\v','\\','\'','\"','\?','\0']
        #self.state = 0
        self.symboltable = collections.OrderedDict()
        self.errortable = collections.OrderedDict()
        self.symbol_pos = 1
        self.linenum = 1

    def anylisis(self, src):
        state = 0
        token = ""
        hasmistake = False
        with open(src, 'r') as f:
            for strs in f:
                if strs == "":
                    pass
                else:
                    i = 0
                    while i < len(strs): #identifier
                        if self.islegalprefix(strs[i]):
                            while self.islegalprefix(strs[i]) or self.isdigit(strs[i]):
                                token += strs[i]
                                i += 1
                                if i >= len(strs):
                                    break
                            if token in self.keywords:
                                self.symboltable[(token,self.symbol_pos)] = (token.upper(), '_')
                                self.symbol_pos += 1
                            else:
                                self.symboltable[(token,self.symbol_pos)] = ('IDN', token)
                                self.symbol_pos += 1
                            token = ""
                            i -= 1
                        elif strs[i] == '/':
                            #temp = i
                            if self.isdigit(strs[i + 1]) or (self.islegalprefix(strs[i + 1]) and strs[i + 1] != '_'):
                                self.symboltable[(strs[i], self.symbol_pos)] = ('/', '_')
                                self.symbol_pos += 1
                                #i += 1
                            elif strs[i + 1] == '/':
                                while (i < len(strs)):
                                    token += strs[i]
                                    i += 1
                                self.symboltable[(token, self.symbol_pos)] = ("Note", token)
                                token = ''
                            else:
                                while 1:
                                    if i >= len(strs):
                                        break
                                    token += strs[i]
                                    res = self.in_notedfa(strs[i], state)
                                    if res[0] is False:
                                        break;
                                    else:
                                        state = res[1]
                                    i += 1
                                if state == 4:
                                    self.symboltable[(token, self.symbol_pos)] = ("Note", token)
                                    self.symbol_pos += 1
                                else:
                                    self.errortable[(token,self.linenum)] = 'note error~'
                                state = 0
                                token = ''
                        elif i < len(strs) and (strs[i] in self.operator or strs[i] in self.edgeop):
                            self.symboltable[(strs[i],self.symbol_pos)] = (strs[i], '_')
                            self.symbol_pos += 1
                        #const number
                        elif i < len(strs) and self.isdigit(strs[i]):
                            while i < len(strs) and (strs[i] == 'e' or strs[i] == '.' or self.isdigit(strs[i]) or strs[i] == '+' or strs[i] == '-'):
                                if i >= len(strs):
                                    break
                                res = self.in_digitdfa(strs[i], state)
                                if res[0] is False:
                                    break;
                                else:
                                    state = res[1]
                                    token += strs[i]
                                    i += 1
                            #print state
                            if state == 1 or state == 3 or state == 6:
                                self.symboltable[(token,self.symbol_pos)] = ('CONST NUM', token)
                                self.symbol_pos += 1
                            else:
                                # hasmistake = True
                                while strs[i] != '\0' and strs[i] != ',' and strs[i] != ';' and strs[i] != ' ':
                                    token += strs[i]
                                    i += 1
                                    if i >= len(strs):
                                        break
                                self.errortable[(token,self.linenum)] = 'error on const number~'
                            token = ''
                            i -= 1
                            state = 0
                        elif i < len(strs) and strs[i] == '\"':
                            while 1:
                                if i >= len(strs):
                                    break
                                if state == 2:
                                    break;
                                res = self.in_stringdfa(strs[i], state)
                                if not res[0]:
                                    break
                                else:
                                    state = res[1]
                                    token += strs[i]
                                i += 1

                            if state == 2:
                                self.symboltable[(token, self.symbol_pos)] = (token, 'CONST STRING')
                                self.symbol_pos += 1
                            elif state == 1:
                                self.errortable[(token, self.linenum)] = 'string not blocked~'
                            state = 0
                            token = ''
                        i += 1
                    self.linenum += 1

    def islegalprefix(self, ch):
        return ch == '_' or ch in [chr(i) for i in range(ord("a"), ord("z")+1)] or\
        ch in [chr(i) for i in range(ord("A"), ord("Z")+1)]

    def isdigit(self, ch):
        return ch in map(str, range(10))

    def in_notedfa(self,ch,curstate):
        for i in range(5):
            if self.noteDFA[curstate][i] == '^/*' and ch != '/' and ch != '*':
                return True, i
            if self.noteDFA[curstate][i] == '^/'and ch != '/':
                return True, i
            if self.noteDFA[curstate][i] == '/' and ch == '/':
                return True, i
            if self.noteDFA[curstate][i] == '*' and ch == '*':
                return True, i
            if self.noteDFA[curstate][i] == '^*'and ch != '*':
                return True, i
        return False, '_'

    def in_digitdfa(self,ch,curstate):
        if ch == '.':
            ch = '.'
        elif ch == 'e':
            ch = 'e'
        elif ch == '+' or ch == '-':
            ch == '+-'
        elif self.isdigit(ch):
            ch = 'd'
        if curstate in self.digitDFA and ch in self.digitDFA[curstate]:
            return True, self.digitDFA[curstate][ch]
        return False, '_'

    def in_stringdfa(self,ch,curstate):
        if ch == '\"' :
            ch = '\"'
        else:
            ch = 'a'
        if curstate in self.stringdfa and ch in self.stringdfa[curstate]:
            return True, self.stringdfa[curstate][ch]
        return False,'_'


    def printtoconsole(self):
        for (item, pos) in self.symboltable:
            print "%s %d <%s, %s>" % (item, pos, self.symboltable[(item,pos)][0], self.symboltable[(item,pos)][1])

    def printerror(self):
        for (item,linenum) in self.errortable:
            print "%s line : %d  <%s>" % (item,linenum,self.errortable[(item,linenum)])

if __name__ == '__main__':
    lex = Lexer()
    lex.anylisis('test.c')
    lex.printtoconsole()
    print '-----------------------error-------------------------'
    lex.printerror()


