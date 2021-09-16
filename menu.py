drinks = [["Cappuccino", 4],
           ["Flat white", 4],
           ["Latte", 4],
           ["Hot Chocolate", 4],
           ["Chai", 4],
           ["Long Black", 3]
           ]


isCoffee = ["Cappuccino",
            "Flat white",
            "Latte",
            "Long Black"
            ]


shots = ["Single",
        "Double",
        "Half Strength"
        ]


milk = ["Full Cream/Normal",
        "Skim/Skinny",
        "Lactose Free/Zymil",
        "Almond",
        "None"
        ]

# Convert lists into strings for display in the GUI
def menuString():
    text = ""
    for choice in drinks:
        text = text + "   > " + str(choice[0]) + " - $" + str(choice[1]) + "\n"
    return text


def shotsString():
    text = ""
    for choice in shots:
        text = text + "   > " + choice + "\n"
    return text


def milkString():
    text = ""
    for choice in milk:
        text = text + "   > " + choice + "\n"
    return text