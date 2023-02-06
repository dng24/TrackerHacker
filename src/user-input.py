#!/usr/bin/env python3.11

import socket
import urllib.request

import requests

def user_input():


    



    #User initial input
    while True:
        try:
            user_input = input("Enter the desired URL: ")
            #socket.gethostbyname(user_input)
            #urllib.request.urlopen(user_input)
            get = urllib.request.urlopen(str(user_input))
            print(get.getcode())
            if get.getcode() == 200:
                print("Starting tracker analysis...\n")    
                break
        except:
            print("Malformed URL entered, please type your desired url again\n")
            print("An error occured, please try again\n")
        print(user_input)
        break
user_input()




