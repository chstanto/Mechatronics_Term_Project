'''
@file       Lab_01.py

@brief      This lab simulates the Vendotron machine.

@details    A finite state machine first requests that the user input
            change using number keys 0 - 7, and at any point the user
            can request one of the four drinks by inputting the appropriate
            letter. The FSM then checks that the inputted funds are 
            sufficient and either asks for more money or dispenses the
            requested drink. The machine then initializes again and prints
            the welcome message.

@image      html Lab_1_Transition_Diagram.PNG width=1000px

'''

import keyboard
import math

change = 0
order = 0
state = 0

def on_keypress(key):
    """ 
    @brief Callback function which is called when a key has been pressed.
    """
    global last_key
    last_key = key.name
    
keyboard.on_release_key("C", callback = on_keypress)
keyboard.on_release_key("P", callback = on_keypress)
keyboard.on_release_key("S", callback = on_keypress)
keyboard.on_release_key("D", callback = on_keypress)
keyboard.on_release_key("E", callback = on_keypress)
keyboard.on_release_key("0", callback = on_keypress)
keyboard.on_release_key("1", callback = on_keypress)
keyboard.on_release_key("2", callback = on_keypress)
keyboard.on_release_key("3", callback = on_keypress)
keyboard.on_release_key("4", callback = on_keypress)
keyboard.on_release_key("5", callback = on_keypress)
keyboard.on_release_key("6", callback = on_keypress)
keyboard.on_release_key("7", callback = on_keypress)

while True:
    
#    keyboard.on_press(on_keypress)
    
    if(state == 0):
        print('Welcome to Vendotron')
        print('  Input money using #s 0 - 7')
        print('  Press C for Cuke ($1.10)')
        print('  Press P for Popsi ($1.20)')
        print('  Press S for Spryte ($1.30)')
        print('  Press D for Dr. Pupper ($1.40)')
        print('  Press E to eject change')
        
        last_key = None
        keyboard.on_release(on_keypress)
        state = 1
        
    elif(state == 1):
        if(last_key == '0'):
            change += 1
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == '1'):
            change += 5
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == '2'):
            change += 10
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == '3'):
            change += 25
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == '4'):
            change += 100
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == '5'):
            change += 500
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == '6'):
            change += 1000
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == '7'):
            change += 2000
            print('Current Funds = ' , change , 'cents')
            last_key = None
            
        elif(last_key == 'C'):
            order = 1
            state = 2
            last_key = None
        
        elif(last_key == 'P'):
            order = 2
            state = 2
            last_key = None
        
        elif(last_key == 'S'):
            order = 3
            state = 2
            last_key = None
        
        elif(last_key == 'D'):
            order = 4
            state = 2
            last_key = None
        
        elif(last_key == 'E'):
            state = 3
            last_key = None
        
        else:
            pass
        
    elif(state == 2):
        if(order == 1):
            if(change >= 110):
                print('Dispensing Cuke')
                change -= 110
                state = 3
            else:
                print('Not Enough Funds, Please Input More')
                state = 1
     
        elif(order == 2):
            if(change >= 120):
                print('Dispensing Popsi')
                change -= 120
                state = 3
            else:
                print('Not Enough Funds, Please Input More')
                state = 1
        
        elif(order == 3):
            if(change >= 130):
                print('Dispensing Spryte')
                change -= 130
                state = 3
            else:
                print('Not Enough Funds, Please Input More')
                state = 1
        
        elif(order == 4):
            if(change >= 140):
                print('Dispensing Dr. Pupper')
                change -= 140
                state = 3
            else:
                print('Not Enough Funds, Please Input More')
                state = 1
    
    elif(state == 3):
        
        ## Variable defining number of twenties to return
        twenty = math.floor(change/(20*100))
        change -= twenty*20*100
        
        ## Variable defining number of tens to return
        ten = math.floor(change/(10*100))
        change -= ten*10*100
        
        ## Variable defining number of fives to return
        five = math.floor(change/(5*100))
        change -= five*5*100
        
        ## Variable defining number of ones to return
        one = math.floor(change/(100))
        change -= one*100
        
        ## Variable defining number of quarters to return
        quarter = math.floor(change/(25))
        change -= quarter*25
        
        ## Variable defining number of dimes to return
        dime = math.floor(change/(10))
        change -= dime*10
        
        ## Variable defining number of nickels to return
        nickel = math.floor(change/(5))
        change -= nickel*5
        
        ## Variable defining number of pennies to return
        penny = math.floor(change)
        
        change_tuple = (penny , nickel , dime , quarter , one , five , ten , twenty)
        
        print('Change Returned: ' , change_tuple)
        print('Format: (penny , nickel , dime , quarter , one , five , ten , twenty)')
        change = 0
        order = 0
        state = 0
        pass
    
    else:
    # Invalid state code (error handling)
        pass
    
    #last_key = ''

    
    
    