Robotic Coffee ordering system using the Ohbot (though it will work without the robot). Created for our school fete.

Robot will allow users to place a coffee order through speech recognition. Inputs are matched using fuzzy logic to menu items. E.g. an order for "Double-shot Cappucino on Full Cream" will pick out the selected items from the menu. If confidence of the match is low, it will ask the user for input again for the specific portion of the order (e.g. "Which milk would you like".)

Another neat little feature is that if you have a webcam placed on top of the ohbot's head, it will use face detection to follow the user's face (i.e. move the head to centralise the face within the image)

Run generateDB.py once to create database file and required tables.

Update the menu.py file to suit your menu.

Python library requirements may be found in the requirements.txt file.

Additionally, an Azure cognitive services subscription/service is required for the speech recognition. Rename config-dist.py file to config.py and replace the sections indicated by square brackets [] with your cognitive services details.

To run the system, you'll need to run both the coffee.py and htmlPOS.py files. Html order tracker can be accessed on the local machine at http://localhost:5000, or on a remote machine by replacing 'localhost' with the host machine's IP address on the network.

As this was created for an educational purpose, I cannot guarantee I have not infringed on copyright in this work. There are significant issues/bugs with the code, and it comes with no warranty.

I'll slap a CC BY-SA license on it. As I've said though, I'm not sure that all the work is mine to share.

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.