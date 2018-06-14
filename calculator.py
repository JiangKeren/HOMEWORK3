def readNumber(line, index):
    number = 0
    flag = 0
    keta = 1
    while index < len(line) and (line[index].isdigit() or line[index] == '.'):
        if line[index] == '.':
            flag = 1
        else:
            number = number * 10 + int(line[index])
            if flag == 1:
                keta *= 0.1
        index += 1
    token = {'type': 'NUMBER', 'number': number * keta}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readMul(line, index):
    token = {'type': 'MUL'}
    return token, index + 1

def readDiv(line, index):
    token = {'type': 'DIV'}
    return token, index + 1

def readLParen(line, index):
    token = {'type': 'LPAREN'}
    return token, index + 1

def readRParen(line, index):
    token = {'type': 'RPAREN'}
    return token, index + 1

def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMul(line, index)
        elif line[index] == '/':
            (token, index) = readDiv(line, index)
        elif line[index] == '(':
            (token, index) = readLParen(line, index)
        elif line[index] == ')':
            (token, index) = readRParen(line, index)
        else:
            print 'Invalid character found: ' + line[index]
            exit(1)
        tokens.append(token)
    return tokens
            
def evaluate_Bracket(tokens):
    index=0
    ex=[]
    while index<len(tokens):
        if tokens[index]['type']=='LPAREN':
            ex.append(index)  #store all left brackets' positions
        elif tokens[index]['type']=='RPAREN':
            temp_answer=0
            sub=tokens[ex[len(ex)-1]+1:index]  #find the tokens inside smallest pair of brackets
            temp_answer=final_evaluate(sub)   
            del tokens[ex[len(ex)-1]:index+1]  #delate this pair brackets and the tokens inside them
            tokens.insert(ex[len(ex)-1],{'type':'NUMBER','number':temp_answer})
            index=ex[len(ex)-1]
            ex.pop()
        index += 1
    return tokens

#calculate *,/
def evaluate_MulDiv(tokens):
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'MUL':
            mul_value= tokens[index-1]['number'] * tokens[index+1]['number']
            tokens.insert(index-1,{'type':'NUMBER','number':mul_value})
            print(tokens)
            del tokens[index:index+3]
            print(tokens)
        elif tokens[index]['type'] == 'DIV':
            div_value= float(tokens[index-1]['number'])/tokens[index+1]['number']
            tokens.insert(index-1,{'type':'NUMBER','number':div_value})
            del tokens[index:index+3]
        else:
             index +=1
    return tokens

#calculate +,-
def evaluate_PlusMinus(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print 'Invalid syntax'
        index += 1
    return answer


def final_evaluate(tokens):
    tokens=evaluate_Bracket(tokens)
    tokens=evaluate_MulDiv(tokens)
    answer=evaluate_PlusMinus(tokens)
    return answer

def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer =final_evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print "PASS! (%s = %f)" % (line, expectedAnswer)
    else:
        print "FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer)


# Add more tests to this function :)
def runTest():
    print "==== Test started! ===="
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("1+2*5-2",9)
    test("1*2+2",4)
   # test("1*5+5/2+2*5/2",12.5)
   # test("2*(2-1)",2)
   # test("((1+2)+3)+4", 10)
   # test("1+(2+(3+4))", 10)
   # test("(1+1)+(1+1)", 4)
   # test("(1+2)*3", 9)
   # test("(3.0+4*(2-1))/5", 1.4)
   #test("2*(2+3)*(2+4)",60)
   # test("(3.0+4*(2-1))/5",1.4)
   # test("3*(4+50)-((100+40)*5/2-3*2*2/4+9)*(((3+4)-4)-4)",518)
    print "==== Test finished! ====\n"

runTest()

while True:
    print '> ',
    line = raw_input()
    tokens = tokenize(line)
    answer = final_evaluate(tokens)
    print "answer = %f\n" % answer
