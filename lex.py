import collections
class Lexer:
    def __init__(self):
        self.keywords = ['int', 'float', 'bool', 'if', 'else', 'return', 'do', 'while', 'return', 'def']
        self.operator = ['+', '-', '*', '/', '|', '&', '^','!','%','>','<']
        self.edgeop = ['=', ';', '[', ']', '.','{','}','(',')']
        self.noteDFA = [['^/', '/', '#', '#', '#'], ['^/*', '/', '*', '#', '#'],
                   ['#', '#', '^*', '*', '#'], ['#', '#', '^/*', '*', '/'],
                   ['#', '#', '#', '#', '#']]
        self.digitDFA = {0: {'d': 1}, 1: {'d': 1, '.': 2, 'e': 4}, 2: {'d': 3},
                    3: {'d': 3, 'e': 4}, 4: {'+-': 5, 'd': 6}, 5: {'d': 6}, 6: {'d': 6,}}
        self.stringDFA = ["#\\b#", "##a#", "#\\b\"", "####"]
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
                            if token in self.keywords:
                                self.symboltable[(token,self.symbol_pos)] = (token.upper(), '_')
                                self.symbol_pos += 1
                            else:
                                self.symboltable[(token,self.symbol_pos)] = ('IDN', token)
                                self.symbol_pos += 1
                            token = ""
                        if strs[i] == '/':
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
                                self.errortable[token] = 'note error~'
                            state = 0
                            token = ''
                        if i < len(strs) and (strs[i] in self.operator or strs[i] in self.edgeop):
                            self.symboltable[(strs[i],self.symbol_pos)] = (strs[i], '_')
                            self.symbol_pos += 1
                        #const number
                        if i < len(strs) and self.isdigit(strs[i]):
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
                                self.errortable[token] = 'error on const number~'
                            token = ''
                            i -= 1
                            state = 0
                        i += 1

    def islegalprefix(self, ch):
        return ch == '_' or ch in [chr(i) for i in range(ord("a"), ord("z")+1)]

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

    def printtoconsole(self):
        for (item, pos) in self.symboltable:
            print "%s %d <%s, %s>" % (item, pos, self.symboltable[(item,pos)][0], self.symboltable[(item,pos)][1])

    def printerror(self):
        for item in self.errortable:
            print "%s   <%s, %s>" % (item, self.errortable[item][0], self.errortable[item][1])

if __name__ == '__main__':
    lex = Lexer()
    lex.anylisis('test.c')
    lex.printtoconsole()
    #lex.printerror()



