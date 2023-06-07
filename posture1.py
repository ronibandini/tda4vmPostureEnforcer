# TDA4vm Edge Impulse posture enforcer
# Roni Bandini @RoniBandini June 2023
# MIT License
# https://bandini.medium.com

import subprocess
import time
import RPi.GPIO as GPIO
import requests
import json

# Relay output pin
output_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(output_pin, GPIO.OUT)

# Runner output file
output_file = open('output.txt', 'w')

print("Posture enforcer with Texas Instruments TDA4VM and Edge Impulse")
print("Roni Bandini, June 2023, Argentina, @RoniBandini")
print("")

print("Testing relay")
GPIO.output(output_pin, GPIO.HIGH)
time.sleep(3)
GPIO.output(output_pin, GPIO.LOW)

print("Stop with CTRL-C")

# Launch Impulse Runner with parameters using subprocess, output to file
subprocess.Popen(["edge-impulse-linux-runner", "--force-engine tidl", "-force-target", "runner-linux-aarch64-tda4vm"], stdout=output_file)


with open("output.txt", "r") as f:
    lines_seen = set()
    while True:
        line = f.readline()
        if not line:
            time.sleep(1)
            continue

        if ("[]" in line):
            print("No posture detected")

        if ("height" in line):

            if ("notok" in line) and line not in lines_seen:
                print("Incorrect posture")
                #print("Complete line: "+line)
                parts = line.split()
                myLine = parts[2][1:-1]
                #print("Json part: "+str(myLine))
                myJson = json.loads(myLine)
                print("Confidence: "+str(myJson["value"]))
                print(" At X: "+str(myJson["x"])+ " Y: "+str(myJson["y"]))

                lines_seen.add(line)

                # Disable machine
                GPIO.output(output_pin, GPIO.LOW)


            if ("ok" in line) and line not in lines_seen:
                print("Correct posture")
                parts = line.split()
                myLine = parts[2][1:-1]
                myJson = json.loads(myLine)
                print("Confidence: "+str(myJson["value"]))
                print(" At X: "+str(myJson["x"])+ " Y: "+str(myJson["y"]))
                lines_seen.add(line)

                # Enable machine
                curr_value = GPIO.HIGH
                GPIO.output(output_pin, curr_value)
