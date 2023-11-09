import PySimpleGUI as sg

# Defining the font
textFont = ('Helvetica',40)
buttonsTextFont = ('Helvetica',32)
smallTextFont = ('Helvetica',16)

# Defining the layout
layout = [
    # Layout elements here
    [sg.Column([
        [sg.Text("Expresion: ",font=smallTextFont),sg.Text("",font=smallTextFont,key = "expresion")]
        ], justification = 'center')
    ],
    [sg.Input(" ",key="textBox", disabled=True, font=textFont, justification='right')],
    [sg.Column([
        [
        sg.Button("+",key="+",size=(3,1),font=buttonsTextFont, button_color=("white",'gray23')),
        sg.Button("1",key="1",size=(3,1),font=buttonsTextFont),
        sg.Button("2",key="2",size=(3,1),font=buttonsTextFont),
        sg.Button("3",key="3",size=(3,1),font=buttonsTextFont)],
        ],justification = 'center')
    ],
    [sg.Column([
        [
        sg.Button("-",key="-",size=(3,1),font=buttonsTextFont, button_color=("white",'gray23')),
        sg.Button("4",key="4",size=(3,1),font=buttonsTextFont),
        sg.Button("5",key="5",size=(3,1),font=buttonsTextFont),
        sg.Button("6",key="6",size=(3,1),font=buttonsTextFont)],
        ],justification = 'center')
    ],
    [sg.Column([
        [
        sg.Button("*",key="*",size=(3,1),font=buttonsTextFont, button_color=("white",'gray23')),
        sg.Button("7",key="7",size=(3,1),font=buttonsTextFont),
        sg.Button("8",key="8",size=(3,1),font=buttonsTextFont),
        sg.Button("9",key="9",size=(3,1),font=buttonsTextFont)],
        ],justification = 'center')
    ],
    [sg.Column([
        [
        sg.Button("/",key="/",size=(3,1),font=buttonsTextFont, button_color=("white",'gray23')),
        sg.Button(".",key=".",size=(3,1),font=buttonsTextFont, button_color=("white", 'DarkSlateGray')),
        sg.Button("0",key="0",size=(3,1),font=buttonsTextFont),
        sg.Button("N",key="N",size=(3,1),font=buttonsTextFont, button_color=("white",'DarkSlateGray'))],
        ],justification = 'center')
    ],
    [sg.Column([
        [
        sg.Button("C",key="C",size=(3,1),font=buttonsTextFont, button_color=("white", 'IndianRed1')),    
        sg.Button("=",key="=",size=(6,1),font=buttonsTextFont, button_color=("black", 'SeaGreen1')),
        sg.Button("<-",key="<-",size=(3,1),font=buttonsTextFont, button_color=("white",'gray20'))],
        ],justification = 'center')
    ]
]

## CONSTANTS
DIGITS = [str(i) for i in range(10)] # Define the digits list
FUNCTIONS = ["C","<-","=",".","N"]
OPERATORS = ["+","-","*","/"]
MAX_LENGTH = 10
WINDOW_SIZE = (400,600)

## OTHER VARIABLES
class Calculator:
    firstNumber:float = 0
    secondNumber:float = 0
    result:float = 0
    curOperator:str = ''
    expresionText:str = ''

    # Sets to 'True' when the first number was entered
    firstNumberEntered:bool = False 
    # Is set to 'True' when the result of an operation is shown
    resShowed:bool = False 

# Create the window
window = sg.Window("Simple Calculator", layout,size=WINDOW_SIZE,finalize=True)
window["textBox"].update(value='')

def ClearTextBox():
    window['textBox'].update(value='')
    if Calculator.resShowed == True:
        Calculator.resShowed = False
        # Update expresion text
        Calculator.expresionText = ''
        window["expresion"].update(Calculator.expresionText)
    print("Input box cleared.")

def HandleDigits(event,values):
    # Check if the input key is a digit
    if event not in DIGITS:
        return

    # Gets the text from inside the text box
    textBoxText = values["textBox"]

    if Calculator.resShowed == True:
        textBoxText = ''
        Calculator.resShowed = False

    # Checks if it reached the max length
    if len(textBoxText) < MAX_LENGTH:
        newText = textBoxText + event
        window['textBox'].update(value=newText)

    # Prints the key of the pressed button in the console
    if len(textBoxText) < MAX_LENGTH:
        print(f"Digit entered: {event}")
    else:
        print("Max reached.")

def ResetVariables():
    Calculator.firstNumberEntered = False
    Calculator.firstNumber = 0
    Calculator.secondNumber = 0
    Calculator.curOperator = ''
    Calculator.result = 0
    Calculator.resShowed = True

def HandleSolve(values):
    Calculator.textBoxText = values["textBox"]
    if Calculator.textBoxText == '' or Calculator.textBoxText == '-':
        print('Empty input.')
        return

    if Calculator.resShowed:
        print("Already solved.")
        return

    if Calculator.firstNumberEntered == False:
        print("First number not entered yet.")
        return

    Calculator.secondNumber = float(Calculator.textBoxText.strip())

    # Solve the result
    if Calculator.curOperator == "+":
        Calculator.result = Calculator.firstNumber + Calculator.secondNumber
    elif Calculator.curOperator == "-":
        Calculator.result = Calculator.firstNumber - Calculator.secondNumber
    elif Calculator.curOperator == "*":
        Calculator.result = Calculator.firstNumber * Calculator.secondNumber
    elif Calculator.curOperator == "/":
        # Check for zero division
        try:
            Calculator.result = Calculator.firstNumber / Calculator.secondNumber
        except ZeroDivisionError:
            print("ZERO DIVISION ERROR")
            Calculator.result = 0
            window['textBox'].update(value='ERROR')
            ResetVariables()
            return

    # Get rid of the '.0' at the end of the float
    formatNumber = lambda n: n if n%1 else int(n)
    Calculator.result = formatNumber(Calculator.result)
    newText = str(Calculator.result)
    window['textBox'].update(value=newText)
    print ("Result: "+newText)
    # Update expresion text
    # Get rid of the '.0' at the end of the float for second number
    Calculator.secondNumber = formatNumber(Calculator.secondNumber)
    Calculator.expresionText = Calculator.expresionText + " " + str(Calculator.secondNumber) + " ="
    window["expresion"].update(Calculator.expresionText)
    #
    ResetVariables()

def HandleFunctions(event,values):
    # Check if the input key is a function
    if event not in FUNCTIONS:
        return

    if event == "C":
        ClearTextBox()
        return
    elif event == "<-":
        # Handle digit deletion
        # Gets the text from inside the text box
        textBoxText = values["textBox"]
        # If the result was already shown it will clear the text box
        if Calculator.resShowed == True:
            ClearTextBox()
            return
        # Checks if it reached the min length
        if len(textBoxText) > 0:
            # Deletes the last character
            newText = textBoxText[:-1]
            window['textBox'].update(value=newText)
            print("Deleted one digit.")
            return
        else:
            print("No digit to clear.")
    elif event == "=":
        HandleSolve(values)
    elif event == "N":
        # Minus sign
        textBoxText = values["textBox"]
        if Calculator.resShowed == True:
            textBoxText = ''
            ClearTextBox()
        if textBoxText == '':
            textBoxText = '-'
            print("Negated.")
        else:
            if textBoxText[0] == '-':
                textBoxText = textBoxText[1:]
                print("Negated.")
            else:
                textBoxText = '-' + textBoxText
                print("Denegated.")
        window['textBox'].update(value=textBoxText)
    elif event == ".":
        # Dot
        if Calculator.resShowed == True:
            return
        textBoxText = values["textBox"]
        if textBoxText == '':
            print("Empty input.")
            return
        if textBoxText[-1] in DIGITS and textBoxText.count('.') == 0:
            textBoxText = textBoxText + '.'
            window['textBox'].update(value=textBoxText)
            print("Added dot.")

def HandleOperators(event,values):
    if event not in OPERATORS:
        return
    
    if Calculator.resShowed == True:
        return

    textBoxText = values["textBox"]
    if (textBoxText == '' and Calculator.firstNumberEntered == False) or textBoxText == '-':
        print('Empty input.')
        return
    
    if Calculator.firstNumberEntered == False:
        Calculator.firstNumber = float(textBoxText.strip())
        # Get rid of the '.0' at the end of the float for second number
        formatNumber = lambda n: n if n%1 else int(n)
        Calculator.firstNumber = formatNumber(Calculator.firstNumber)
        print("First number: "+str(Calculator.firstNumber))
        Calculator.firstNumberEntered = True
        ClearTextBox()
        # Change expresion text
        Calculator.expresionText = str(Calculator.firstNumber) + "  "
        
    Calculator.curOperator = event
    # Update expresion text
    Calculator.expresionText = Calculator.expresionText[:-1] + Calculator.curOperator
    window["expresion"].update(Calculator.expresionText)
    # DEBUG
    print("Operator changed to: "+event)

## EVENT LOOP
while True:
    event, values = window.read()

    # The mandatory check if 'x' button of the window is pressed
    if event == sg.WINDOW_CLOSED:
        break
    # Other event logic here
    HandleDigits(event,values)
    HandleFunctions(event,values)
    HandleOperators(event,values)
        
# Close the window when the loop ends
window.close()