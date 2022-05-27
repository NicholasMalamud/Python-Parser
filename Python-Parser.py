#HW7 Python Project -- parser

from tkinter import *
import re

class MyLexicalGUI:  # class definition

    def __init__(self, root):
        # Master is the default prarent object of all widgets.
        # You can think of it as the window that pops up when you run the GUI code.
        self.master = root
        self.master.title("Lexical Analyzer for TinyPie")

        self.inputLabel = Label(self.master, text="Source Code Input: ", padx = 50)
        self.inputLabel.grid(row=0, column=0, sticky=E)

        self.outputLabel = Label(self.master, text="Lexical Analyzed Result: ", padx = 70)
        self.outputLabel.grid(row=0, column=1, sticky=E)

        self.outputLabel2 = Label(self.master, text="Parse Tree: ", padx=150)
        self.outputLabel2.grid(row=0, column=2, sticky=E)

        self.inputText = Text(self.master, width = 25, height = 10)
        self.inputText.grid(row=1, column=0, sticky=E)

        self.outputText = Text(self.master, width=25, height=10)
        self.outputText.grid(row=1, column=1, padx = 40, sticky=E)

        self.outputText2 = Text(self.master, width=50, height=10)
        self.outputText2.grid(row=1, column=2, sticky=E)

        self.currentLine_Label = Label(self.master, text="Current Processing Line: " , padx = 70 )
        self.currentLine_Label.grid(row=2, column=0, sticky=E)

        self.currentInputLine = 0;
        self.currentLine_Label2 = Label(self.master, text= 0)
        self.currentLine_Label2.grid(row=2, column=0, sticky=E, padx = 50)

        self.nextLine_Button = Button(self.master, text="Next Line", command=self.analyzeResult)
        self.nextLine_Button.grid(row=3, column=0, sticky=E)

        self.quitButton = Button(self.master, text="Quit", command=self.closeGui, width = 8)
        self.quitButton.grid(row=3, column=1, sticky=E, padx = 40)


    def analyzeResult(self):
        text = self.inputText.get('1.0', END).splitlines() #turn inputbox text into list
        if self.currentInputLine <= len(text): #avoid index out of range error
            TokenOutputList = CutOneLineTokens(text[self.currentInputLine])
            ParserTokenList = []
            for T in TokenOutputList:
                self.outputText.insert(END, T + "\n" ) #insert line into output
                T = T.replace("<", "", 1)
                T = T.replace(">", "", 1)
                ParserTokenList.append(tuple(T.split (",")))

            self.currentInputLine += 1 #increment input line
            self.currentLine_Label2.configure(text = self.currentInputLine) #update count in currentLine label
            print(str(ParserTokenList))
            parser(self.currentInputLine, self.outputText2 , ParserTokenList)


    def closeGui(self):
        self.master.destroy() #close Gui


        # HW3 Lexer stuff

def Match(code, word):
    result = re.match(code, word)
    if (result != None):
        return result.group(0)
    else:
        return False

def Search(code, word):
    result = re.search(code, word)
    if (result != None):
        return result.group(0)
    else:
        return False


def CutOneLineTokens(line):
    output = []
    linewithspace = line
    line = line.replace(" ", "") #spaces mess with them for some reason
    while(line != ""): #while just in case there are multiple instances of the same type of token

        key = Match(r'if|else|int|float', line)
        if key != False:
            output.append("<key," + key + ">")
            line = re.sub(r'if|else|int|float', "", line, 1)

        id = Match(r'[A-z]+\d+|[A-z]+', line)
        if id != False:
            output.append("<id," + id + ">")
            line = re.sub(r'[A-z]+\d+|[A-z]+', "", line, 1)

        sep = Match(r'\(|\)|"|:|;', line)
        if sep != False:
            output.append("<sep," + sep + ">")
            line = re.sub(r'\(|\)|"|:|;', "", line, 1)

        op = Match(r'=|\+|>|\*', line)
        if op != False:
            output.append("<op," + op + ">")
            line = re.sub(r'=|\+|>|\*', "", line, 1)

        #literals
        flolit = Match(r'\d*\.\d+', line)  # float
        if flolit != False:
            output.append("<flo_lit," + flolit + ">")
            line = re.sub(r'\d*\.\d+', "", line, 1)
        intlit = Match(r'\d+', line)  # int
        if intlit != False:
            output.append("<int_lit," + intlit + ">")
            line = re.sub(r'\d+', "", line, 1)
        strlit = Search(r'".*"', linewithspace)  # string
        if strlit != False:
            #need to save the string to literal and "" to seperators
            strlit = re.sub(r'"',"",strlit);
            output.append("<sep," + '"' + ">");
            output.append("<str_lit," + strlit + ">")
            output.append("<sep," + '"' + ">");
            line = re.sub(r'".*"', "", line, 1)
            linewithspace = re.sub(r'".*"', "", linewithspace, 1)

    return output


            #Parser

Mytokens = []
TreeBox = []
inToken = ("empty", "empty")


def accept_token():
    global inToken
    TreeBox.insert(END, "     accept token from the list:" + inToken[1] + "\n")
    print("     accept token from the list:" + inToken[1])
    inToken = Mytokens.pop(0)


def math():
    TreeBox.insert(END, "\n----parent node math, finding children nodes:" + "\n")
    print("\n----parent node math, finding children nodes:")
    global inToken

    multi()
    if (inToken[1] == "+"):
        TreeBox.insert(END, "\nchild node (token):" + inToken[1] + "\n")
        print("\nchild node (token):" + inToken[1])
        accept_token()
        TreeBox.insert(END, "child node (internal): multi" + "\n")
        print("child node (internal): multi")
        multi()


def multi():
    TreeBox.insert(END, "\n----parent node multi, finding children nodes:" + "\n")
    print("\n----parent node multi, finding children nodes:")
    global inToken

    if (inToken[0] == "int_lit"):
        TreeBox.insert(END, "child node (internal): int" + "\n")
        print("child node (internal): int")
        TreeBox.insert(END, "   int has child node (token):" + inToken[1] + "\n")
        print("   int has child node (token):" + inToken[1])
        accept_token()
    elif (inToken[0] == "flo_lit"):
        TreeBox.insert(END, "child node (internal): float" + inToken[1] + "\n")
        print("child node (internal): float")
        TreeBox.insert(END, "   float has child node (token):" + inToken[1] + "\n")
        print("   float has child node (token):" + inToken[1])
        accept_token()

    if (inToken[1] == "*"):
        TreeBox.insert(END, "child node (token):" + inToken[1] + "\n")
        print("child node (token):" + inToken[1])
        accept_token()
        TreeBox.insert(END, "child node (internal): multi" + "\n")
        print("child node (internal): multi")
        multi()


def exp():
    TreeBox.insert(END, "\n----parent node exp, finding children nodes:" + "\n")
    print("\n----parent node exp, finding children nodes:")
    global inToken;
    typeT, token = inToken;
    if (typeT == "key"):
        TreeBox.insert(END, "child node (internal): key" + "\n")
        print("child node (internal): key")
        TreeBox.insert(END, "   key has child node (token):" + token + "\n")
        print("   key has child node (token):" + token)
        accept_token()
    else:
        print("expect key as the first element of the expression!\n")
        return

    if (inToken[0] == "id"):
        TreeBox.insert(END, "child node (internal): identifier" + "\n")
        print("child node (internal): identifier")
        TreeBox.insert(END, "   identifier has child node (token):" + inToken[1] + "\n")
        print("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect identifier as the second element of the expression!\n")
        return

    if (inToken[1] == "="):
        TreeBox.insert(END, "child node (token):" + inToken[1] + "\n")
        print("child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect = as the third element of the expression!")
        return

    TreeBox.insert(END, "Child node (internal): math" + "\n")
    print("Child node (internal): math")
    math()


def if_exp():
    TreeBox.insert(END, "\n----parent node if_exp, finding children nodes:" + "\n")
    print("\n----parent node if_exp, finding children nodes:")
    global inToken;
    typeT, token = inToken;
    if (typeT == "key"):
        TreeBox.insert(END, "child node (internal): key" + "\n")
        print("child node (internal): key")
        TreeBox.insert(END, "   key has child node (token):" + token + "\n")
        print("   key has child node (token):" + token)
        accept_token()
    else:
        print("expect key as the first element of the expression!\n")
        return

    if (inToken[1] == "("):
        TreeBox.insert(END, "child node (internal): separator" + "\n")
        print("child node (internal): separator")
        TreeBox.insert(END, "   separator has child node (token):" + inToken[1] + "\n")
        print("   separator has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect separator as the second element of the expression!\n")
        return

    comparison_exp()

    if (inToken[1] == ")"):
        TreeBox.insert(END, "child node (internal): separator" + "\n")
        print("child node (internal): separator")
        TreeBox.insert(END, "   separator has child node (token):" + inToken[1] + "\n")
        print("   separator has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect separator as the six element of the expression!\n")
        return

def comparison_exp():
    TreeBox.insert(END, "\n----parent node comparison_exp, finding children nodes:" + "\n")
    print("\n----parent node comparison_exp, finding children nodes:")
    global inToken

    if (inToken[0] == "id"):
        TreeBox.insert(END, "child node (internal): identifier" + "\n")
        print("child node (internal): identifier")
        TreeBox.insert(END, "   identifier has child node (token):" + inToken[1] + "\n")
        print("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect identifier as the third element of the expression!\n")
        return

    if (inToken[1] == ">"):
        TreeBox.insert(END, "child node (token):" + inToken[1] + "\n")
        print("child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect > as the fourth element of the expression!")
        return

    if (inToken[0] == "id"):
        TreeBox.insert(END, "child node (internal): identifier" + "\n")
        print("child node (internal): identifier")
        TreeBox.insert(END, "   identifier has child node (token):" + inToken[1] + "\n")
        print("   identifier has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect identifier as the fifth element of the expression!\n")
        return


def print_exp():
    TreeBox.insert(END, "\n----parent node print_exp, finding children nodes:" + "\n")
    print("\n----parent node print_exp, finding children nodes:")
    global inToken;
    typeT, token = inToken;
    if (typeT == "id"):
        TreeBox.insert(END, "child node (internal): identifier" + "\n")
        print("child node (internal): identifier")
        TreeBox.insert(END, "   identifier has child node (token):" + token + "\n")
        print("   identifier has child node (token):" + token)
        accept_token()
    else:
        print("expect identifier as the first element of the expression!\n")
        return

    if (inToken[1] == "("):
        TreeBox.insert(END, "child node (internal): separator" + "\n")
        print("child node (internal): separator")
        TreeBox.insert(END, "   separator has child node (token):" + inToken[1] + "\n")
        print("   separator has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect separator as the second element of the expression!\n")
        return

    if (inToken[1] == '"'):
        TreeBox.insert(END, "child node (internal): separator" + "\n")
        print("child node (internal): separator")
        TreeBox.insert(END, "   separator has child node (token):" + inToken[1] + "\n")
        print("   separator has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect separator as the third element of the expression!\n")
        return

    if (inToken[0] == "str_lit"):
        TreeBox.insert(END, "child node (internal): string" + "\n")
        print("child node (internal): string")
        TreeBox.insert(END, "   string has child node (token):" + inToken[1] + "\n")
        print("   string has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect string literal as the fourth element of the expression!\n")
        return

    if (inToken[1] == '"'):
        TreeBox.insert(END, "child node (internal): separator" + "\n")
        print("child node (internal): separator")
        TreeBox.insert(END, "   separator has child node (token):" + inToken[1] + "\n")
        print("   separator has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect separator as the fifth element of the expression!\n")
        return

    if (inToken[1] == ")"):
        TreeBox.insert(END, "child node (internal): separator" + "\n")
        print("child node (internal): separator")
        TreeBox.insert(END, "   separator has child node (token):" + inToken[1] + "\n")
        print("   separator has child node (token):" + inToken[1])
        accept_token()
    else:
        print("expect separator as the six element of the expression!\n")
        return



def parser(LineNum,OutputBox,TokenList):
    global Mytokens
    global inToken
    global TreeBox

    Mytokens = TokenList
    inToken = Mytokens.pop(0)
    TreeBox = OutputBox

    if(LineNum == 1 or LineNum == 2):
        TreeBox.insert(END, "\n####Parse tree for line " + str(LineNum) + "###" + "\n")
        print("####Parse tree for line " + str(LineNum) + "###" + "\n")
        exp()
        if (inToken[1] == ";"):
            TreeBox.insert(END, "\nparse tree building success!" + "\n")
            print("\nparse tree building success!")
    elif(LineNum == 3):
        TreeBox.insert(END, "\n####Parse tree for line " + str(LineNum) + "###" + "\n")
        print("####Parse tree for line " + str(LineNum) + "###" + "\n")
        if_exp()
        if (inToken[1] == ":"):
            TreeBox.insert(END, "\nparse tree building success!" + "\n")
            print("\nparse tree building success!")
    elif(LineNum == 4):
        TreeBox.insert(END, "\n####Parse tree for line " + str(LineNum) + "###" + "\n")
        print("####Parse tree for line " + str(LineNum) + "###" + "\n")
        print_exp()
        if (inToken[1] == ";"):
            TreeBox.insert(END, "\nparse tree building success!" + "\n")
            print("\nparse tree building success!")
    else:
        print("error: too many lines")

    return



if __name__ == '__main__':
    myTkRoot = Tk()
    my_gui = MyLexicalGUI(myTkRoot)
    myTkRoot.mainloop()

