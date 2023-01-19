#!/usr/bin/env python3

import json
import urllib.request
import time
import datetime
import urwid
from time import sleep
from math import pow
import matplotlib.pyplot as plt

#------------------# Settings #------------------#
# MAC of the tag you want to track 
tag = "ac233fa34190"
# Set the threshold for the update time in seconds
threshold = 10
# Variable ajustement n=obstacle   a=calibration distance
n=2
a=-55
# Position of each antenna
x1,y1 = 2,2         # Antenna 001bc509408201a6/1
x2,y2 = 4.5,2       # Antenna 001bc509408200b5/1
x3,y3 = 1,5.5         # Antenna 001bc509408200ae/1


capteurs = {}

# Class for the rssi, contain the rssi and the last time it was updated
class Rssi:
    def __init__(self, rssi, update_time=None):
        self.rssi = rssi
        self.update_time = update_time or time.time()
        self.distance = pow(10,((rssi-a)/(-10*n)))
        
# Calculate where the position using trilateration
def trilateration(x1,y1,r1,x2,y2,r2,x3,y3,r3):
  A = 2*x2 - 2*x1
  B = 2*y2 - 2*y1
  C = r1**2 - r2**2 - x1**2 + x2**2 - y1**2 + y2**2
  D = 2*x3 - 2*x2
  E = 2*y3 - 2*y2
  F = r2**2 - r3**2 - x2**2 + x3**2 - y2**2 + y3**2
  x = (C*E - F*B) / (E*A - B*D)
  y = (C*D - A*F) / (B*D - A*E)
  return x,y

figure, axes = plt.subplots()
plt.show(block=False)

while True:
    
    with urllib.request.urlopen('http://localhost:3001/context/device/' + tag + '/2') as response:
        try:
            html = response.read()
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")
        #print(html)
        htmlobj = json.loads(html)
        i = 0
        while i < len(htmlobj["devices"]["ac233fa34190/2"]["nearest"]):
            capteurs.update({htmlobj["devices"]["ac233fa34190/2"]["nearest"][i]["device"]:Rssi(htmlobj["devices"]["ac233fa34190/2"]["nearest"][i]["rssi"])})
            i += 1
        print("Number of active antenna : ",i)


        # Create a list of antenna to delete
        antenna_to_delete = []

        for key, value in capteurs.items():
            # If the time difference is greater than the threshold, add the key to the list of keys to delete
            if (time.time() - value.update_time) > threshold:
                antenna_to_delete.append(key)

        # Delete the values from the dictionary capteurs
        for key in antenna_to_delete:
            print("WARNING! The key \"{}\" is too old and will be deleted!".format(key))
            del capteurs[key]    
        
        # If all the antenna have been found
        if all(key in capteurs for key in ['001bc509408201a6/1', '001bc509408200b5/1', '001bc509408200ae/1']):
            print("All three keys are in the dictionary.")
            dist_1 = capteurs['001bc509408201a6/1'].distance
            dist_2 = capteurs['001bc509408200b5/1'].distance
            dist_3 = capteurs['001bc509408200ae/1'].distance
            x,y = trilateration(2,2,dist_1,10,10,dist_2,10,2,dist_3)
            print(x,y)
            plt.clf()
            axes.cla()
            # figure, axes = plt.subplots()
            Drawing_antenne1 = plt.Circle( (x1,y1 ), dist_1, fill = True )
            Drawing_antenne2 = plt.Circle( (x2,y2 ), dist_2, fill = True )
            Drawing_antenne3 = plt.Circle( (x3,y3 ), dist_3, fill = True )
            plt.scatter([x], [y], color="black") # plotting single point
            plt.scatter([x1], [y1], color="blue") # plotting single point
            plt.scatter([x2], [y2], color="red") # plotting single point
            plt.scatter([x3], [y3], color="green",) # plotting single point
            plt.xlim(0, 15)
            plt.ylim(0, 15)
            axes.set_aspect('equal')  # <-- set aspect ratio to 'equal'
            axes.add_artist(Drawing_antenne1)  # <-- add Circle objects to axes
            axes.add_artist(Drawing_antenne2)  # <-- add Circle objects to axes
            axes.add_artist(Drawing_antenne3)  # <-- add Circle objects to axes
            plt.title( 'CoolCowTracker.exe' )
            current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            figure.suptitle("Last updated : " + current_time)
            plt.show(block=False)
        
            figure.canvas.draw()  # <-- use this line instead of plt.draw()
            #plt.draw()
            plt.pause(0.001)
            
        missing_antenna = [key for key in ['001bc509408201a6/1', '001bc509408200b5/1', '001bc509408200ae/1'] if key not in capteurs or capteurs[key] is None]

        if missing_antenna:
            print("Howl-In-One missing : {}".format(', '.join(missing_antenna)))

        for key, value in capteurs.items():
            print("Key: {}, Rssi: {}, Distance: {}, Last time updated: {}".format(key, value.rssi, value.distance, value.update_time))

        sleep(1)