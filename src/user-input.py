#!/usr/bin/env python3.11

import socket
import urllib.request
import sys
import os
import requests

def help():
    print("\n\nWelcome to tracker hacker, a convenient tool to show what trackers are spying on you when you visit a webpage. Usage of the tool is easy!\n\nFirst, enter the types of FINISH")

def user_input():

    print("Welcome to tracker hacker!\n")
    print("To begin, select your datapoints and url inputs. (Type help for manual, q to quit)\n")


    #Desired data points
    datapoints = []
    while True:
        print("\nPlease select what data points you want tracker hacker to ouptut:\n")
        print("a)    Whois\n")
        print("b)    IP geolocation\n")
        print("c)    Owner\n")

        try:
            data_choice = input("--->  ")
           
            if (data_choice == "help") or (data_choice == "Help") or (data_choice == 'h'):
                help()
                continue

            if data_choice == 'q':
                return

        except:
            print("\nOops, something went wrong with your input. Please try again")
            continue
        
        if (data_choice == 'a' or data_choice == 'b' or data_choice == 'c'):
            if data_choice not in datapoints:
                datapoints.append(data_choice)
            else:
                print("\nPlease enter a choice that you have not selected yet.")
                continue
        else:
            print("\nSomething went wrong, please try retyping your input\n")
            continue

        if len(datapoints) != 3:
            c = input("\nWould you like to select another datapoint? (y or any other key):")

            if c == 'y':
                continue
            if c == 'q':
                return
            else:
                break
        else:
            break

    #Browser Choice
    browser = 'a' #Chrome is default, value set at 'a'
    while True:
        print("\n Please select the browser for tracker hacker to query\n")
        print("a)    Chrome\n")
        print("b)    Firefox\n")

        try:
            browser_choice = input("--->   ")

            if (browser_choice == "help") or (browser_choice == "Help") or (browser_choice == 'h'):
                help()
                continue

            if browser_choice == 'q':
                return
        except:
            print("\nOops! Something went wrong with your input. Please try again")
            continue

        if browser_choice == 'a':
            break
        elif browser_choice == 'b':
            browser = 'b'
            break
        else:
            print("\nPlease enter a valid choice for browser")
            continue
    

    #Url input
    urls = []
    url_input_type = 'a' #Default is manual entry

    while True:

        print("\nPlease enter what type of url input you will use.\n")
        print("a)    Manual entry\n")
        print("b)    File upload\n")
       
        try:
            url_input_type = input("\nPlease enter what type of url input you will use:  ")
        except:
            print("\nOops! There was a problem with your input, please try again.")

        if (url_input_type == "help") or (url_input_type == "Help") or (url_input_type == 'h'):
            help()
            continue

        if url_input_type == 'q':
            return

        if url_input_type == 'a' or url_input_type == 'b':
            break
        else:
            print("\nPlease enter a valid input.")


    if url_input_type == 'a':
        while True:
            try:
                user_input = input("Enter the desired URL: ")

                if (user_input == "help") or (user_input == "Help") or (user_input == 'h'):
                    help()
                    continue

                if user_input == 'q':
                    return

                #socket.gethostbyname(user_input)
                #urllib.request.urlopen(user_input)
                get = urllib.request.urlopen(str(user_input))
                print(get.getcode())
                if get.getcode() == 200:
                    urls.append(user_input)
                    c = input("Valid url entered! Would you like to enter another url (y or any other key)?\n")

                    if c == 'y':
                        continue
                    
                    if (c == "help") or (c == "Help") or (c == 'h'):
                        help()
                        continue

                    if c == 'q':
                        return

                    print("Starting tracker analysis...\n")    
                    break
            except:
                print("Malformed URL entered, please type your desired url again\n")
                continue

            break

    if url_input_type == 'b':
        while True:
            try:
                filepath = input("\nPlease enter the filepath of a txt file containing your list of urls:   ")
            except:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
                continue
                
            if (filepath == "help") or (filepath == "Help") or (filepath == 'h'):
                help()
                continue

            if filepath == 'q':
                return

            try:
                f = open(filepath, "r")
            except:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
                continue


            count = 0
            malformed = 0
            for url in f:
                try:
                    get = urllib.request.urlopen(str(url.strip()))
                    if get.getcode() == 200:
                        print("[{}]: {}".format(count, url.strip()))
                        urls.append(url.strip())
                        count += 1
                except:
                    print("[X]: {}".format(url.strip()))
                    malformed += 1

            f.close()

            if malformed > 0:
                print("\n{} Malformed urls included in your file. Added {} valid urls, continuing...\n".format(malformed, count))


            print("Starting tracker analysis...\n")
            break

    print("Datapoints: ", datapoints)
    print("Browser: " + browser)
    print("urls ", urls)



user_input()




