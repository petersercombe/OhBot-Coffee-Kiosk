# Import required libraries
from ohbot import ohbot
from random import *
from fuzzywuzzy import process
import threading, keyboard, datetime

# Import custom modules
from menu import *
from config import *
from faceDetection import faceDetection
from dbUtils import *

# Configure Ohbot Settings for this app
ohbot.setVoice("-vzira")
soundDelay = 0  # -0.5


def say(msg):
    ohbot.say(msg, True, soundDelay=soundDelay)


# Configure custom phrase lists to improve
# menu item recognition in the Speech SDK
phrase_list_grammar = speechsdk.PhraseListGrammar.from_recognizer(speech_recognizer)
for choice in drinks:
    phrase_list_grammar.addPhrase(choice[0])
for option in milk:
    phrase_list_grammar.addPhrase(option)
for option in shots:
    phrase_list_grammar.addPhrase(option)


# Function to handle voice input
def voiceInput():
    while True:
        menuText.set(menuText.get() + "\nListening...")
        msg = fromMic()
        # msg = input("Input: ")
        if msg:
            if "joke" in msg.lower():
                tellJoke()
            elif "sugar" in msg.lower():
                say("You can add your own sugar on the table beside the coffee machine")
                return msg
            else:
                return msg
        else:
            say(repeatPhrase())


# Select a repeat phrase
def repeatPhrase():
    phrases = ["Could you repeat that?",
               "Say that again?",
               "Pardon?",
               "Sorry, I didn't catch that?",
               "I'm a bit hard of hearing. Could you repeat that?",
               "Could you say it again, a bit slower?",
               "Sorry, I was just day dreaming. What was that you said?"]
    select = randint(0, len(phrases) - 1)
    return phrases[select]


# Define compliments:
def compliment():
    compliments = ["May I say that you are simply glowing today.",
                   "May I say that you look great today.",
                   "May I say, that color is perfect on you.",
                   "May I say that your hair looks stunning.",
                   "May I say that your voice is magnificent.",
                   "May I say that I love your sense of style.",
                   "That name suits you to a T."
                   ]
    return compliments[randint(0, len(compliments) - 1)]


# Define jokes:
def tellJoke():
    jokes = ["No, but have you seen Sarah Connor by any chance? A friend of mine is looking for her.",
             "What do you call sad coffee? Depresso",
             "How does Moses have his coffee? He brews it",
             "How did the hipster burn his tongue? He drank his coffee before it was cool",
             "I drink so much coffee at work, I consider it part of my daily grind",
             "How does a robot drink coffee? She installs Java",
             "Ok, I've got a joke. Half strength dee calf caramel latte on soy",
             "What’s the technical name for a pot of coffee at work? Break fluid",
             "Why should you be wary of a 50 cent espresso? It's a cheap shot"]
    joke = randint(0, len(jokes) - 1)
    say(jokes[joke])
    ohbot.wait(1)
    say("Now, what was it you wanted?")


# Event listener to initiate an order
def startOrder():
    while True:
        keyboard.wait('`') # Order function will trigger when the ` key is pressed
        order()


def order():
    menuText.set("Hello. May I start with your name? ")
    say("Hello. May I start with your name?")
    name = voiceInput()
    say("Hi " + name + ". " + compliment())
    orderText.set("Name: " + name)
    cost = 0

    # Loop for drink order:
    while True:
        # Coffee Selection
        while True:
            menuText.set("Order one drink at a time. \nMenu Options:\n" + menuString())
            say("What would you like to order today?")
            msg = voiceInput()
            drinkChoice = process.extractOne(msg, drinks)
            if drinkChoice[1] < 60: # If match confidence is less than 60%
                say("Oh, I didn't quite catch that.")
                continue
            else:
                shotChoice = process.extractOne(msg, shots)
                milkChoice = process.extractOne(msg, milk)
                break

        orderText.set(orderText.get() + "\nOrder: " + drinkChoice[0][0])
        cost += drinkChoice[0][1]
        say(drinkChoice[0][0])

        # Number of shots
        if drinkChoice[0][0] in isCoffee:
            if shotChoice[1] < 70: # If match confidence is less than 70%
                menuText.set("Shot Options:\n" + shotsString())
                say("How many shots would you like in that?")
                msg = voiceInput()
                shotChoice = process.extractOne(msg, shots)
            orderText.set(orderText.get() + " (" + shotChoice[0] + ")")
            say(shotChoice[0])

        # Milk selection
        if milkChoice[1] < 70: # If match confidence is less than 70%
            menuText.set("Menu Options:\n" + milkString())
            say("What milk would you like that on? ")
            msg = voiceInput()
            milkChoice = process.extractOne(msg, milk)
        orderText.set(orderText.get() + " with " + milkChoice[0])
        say(milkChoice[0])

        # Order another item loop
        menuText.set('Would you like another drink? \n \n'
                     'Say "yes" or "no"\n')
        say("Would you like another drink?")
        repeat = voiceInput()
        if "yes" in repeat.lower() or "yeah" in repeat.lower() or "yep" in repeat.lower():
            continue
        else:
            break

    # Special requests/modifications
    menuText.set("Do you have any special requests or \n"
                 "modifications to your order?")
    say("Do you have any special requests or modifications to your order?")
    special = voiceInput()
    orderText.set(orderText.get() + "\nSpecial Requests: " + special)

    # Prepare order for DB entry and process
    orderString = orderText.get().replace('\n', '\r\n')
    orderID, orderTime = processOrder(orderString, cost)

    # Final greeting, reset GUI
    finalGreeting = '''Thanks {}. 

That comes to a total of ${}

Your order ID is {}.

It should be ready in about {} minutes.

If there are any issues with your order 
please let a human know.
'''.format(name, cost, orderID, orderTime)
    menuText.set(finalGreeting)
    say(finalGreeting)
    ohbot.wait(3)
    total = getTotal()
    menuText.set("Coral, the Covid-Safe Kiosk"
                 "\n \nCurrent wait time is about {} minutes"
                 "\n \nTotal funds raised today: ${}".format(orderTime, total[0][0]))
    orderText.set("")


def processOrder(order, cost): # Commit voice order to database
    paid = "No"
    currentDT = datetime.datetime.now()
    data = (order,
            cost,
            paid,
            currentDT
            )
    runQuery(insertOrder, data)
    orderID = getQuery(getOrderID, ("orders",))
    # Calculate order wait times by averaging the time the last 5 orders took to fill
    orderTimes = getQuery(getOrderTimes, ("orderID",))
    delta = 0
    for i, times in enumerate(orderTimes):
        if i >= len(orderTimes) - 5:
            times = list(times)
            delta += (datetime.datetime.strptime(times[2], "%Y-%m-%d %H:%M:%S.%f") - datetime.datetime.strptime(
                times[1], "%Y-%m-%d %H:%M:%S.%f")).seconds
        else:
            pass
    orderTime = round((delta / 60) / 5)
    # Return OrderID and OrderTime
    return orderID[0][0], orderTime


def blinking(): # Randomly blink Ohbot's eyes
    while True:
        ohbot.move(ohbot.LIDBLINK, 1, 10)
        ohbot.wait(random() / 3)
        ohbot.move(ohbot.LIDBLINK, 10, 10)
        ohbot.wait(randint(2, 6))


# Start 'em up:
ohbot.reset()
ohbot.move(ohbot.EYETURN, 2)

t = threading.Thread(target=faceDetection, args=())
t2 = threading.Thread(target=blinking, args=())
t3 = threading.Thread(target=startOrder, args=())

t.start()
ohbot.wait(1)
t2.start()
ohbot.wait(1)
t3.start()

# Start GUI mainloop
win.mainloop()

# Close ohbot at the end.
ohbot.close()
