import socket
import urllib.request
import sys
import os
import requests
import pathlib
import validators
import argparse

from browsers import WebBrowsers

def help():
    print("\n\nWelcome to tracker hacker, a convenient tool to show what trackers are spying on you when you visit a webpage. Usage of the tool is easy!\n\nFirst, enter the types of FINISH")

def get_userinput_args():
    print("args")
    

    datapoints = []
    browsers = []
    urls = []
    adlist_urls = []
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d", "--data", nargs='*', help="Data types to output. 1: Whois, 2: IP geolocation, 3: Owner. For multipe choices, enter them space delimited, eg: -d 1 2 for whois and IP geolocation.", type=int)
    parser.add_argument("-b", "--browser", nargs='*', help="Which browser to use. 1: Chrome, 2: Firefox. For multiple choices, enter them space delimited, eg: 1 2 for Chrome and Firefox", type=int)
    parser.add_argument("-u", "--urls", help="URLs to analyze. Provide the path of a .txt file with a list of urls, with only a single url per line.")
    parser.add_argument("-l", "--list", help="List of ads/trackers. Please either enter \'default\' to use the default list of ads/trackers, or provide the path of a .txt file with a list of custom ad/tracker urls, with only a single url per line.")
    
    args = parser.parse_args()
    
    if args.data:
        count = 0
        print("URL Args:", args.data)
        datapoints = args.data
        for choice in args.data:
            if choice == 1 or choice == 2 or choice == 3:
                continue
            else:
                datapoints.remove(choice)
    else:
        datapoints = [1,2,3]

    if args.browser:
        count = 0
        browsers = args.browser
        for choice in args.browser:
            if choice == 1 or choice == 2:
                continue
            else:
                browsers.remove(choice)
    else:
        browsers = [1,2]

    
    if args.urls:
        
        if pathlib.Path(args.urls).suffix != '.txt':
            print("\nOops! Looks like there was a problem loading your urls file. Please make sure that it is a valid path and a correctly formatted .txt file")          
        else:    
            count = 0
            malformed = 0
            f = open(args.urls, "r")
            for url in f:
                try:
                    if validators.url(url.strip()):
                        print("[{}]: {}".format(count, url.strip()))
                        urls.append(url.strip())
                        count += 1
                    else:
                        print("[X]: {}".format(url.strip()))
                        malformed += 1
                except:
                    print("[X]: {}".format(url.strip()))
                    malformed += 1 
            f.close()

    if args.list:
        if pathlib.Path(args.list).suffix != '.txt':
            print("\nOops! Looks like there was a problem loading your urls file. Please make sure that it is a valid path and a correctly formatted .txt file")
        else:
            f = open(args.list, "r")
            for ad in f:
                adlist_urls.append(ad.strip())
            f.close()

    print("Choices", datapoints)
    print("Browsers", browsers)
    print("Urls", urls)
    print("Adlist", adlist_urls)



def get_user_input():

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
                #NOTE: set to verify unittest mock inputs, might want to keep
                return 0

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
            browser = WebBrowsers.CHROME
            break
        elif browser_choice == 'b':
            browser = WebBrowsers.FIREFOX
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
                #get = urllib.request.urlopen(str(user_input))
                #print(get.getcode())
                #if get.getcode() == 200:
                if validators.url(str(user_input)):
                    urls.append(user_input)
                    c = input("Valid url entered! Would you like to enter another url (y or any other key)?\n")

                    if c == 'y':
                        continue
                    
                    if c == 'q':
                        return
                else:
                    print("Malformed URL entered, please type your desired url again")
                    continue

                break
            except:
                print("Malformed URL entered, please type your desired url again\n")
                continue

            break

    if url_input_type == 'b':
        while True:
            try:
                filepath = input("\nPlease enter the filepath of a txt file containing your list of urls:   ")
                
                if (filepath == "help") or (filepath == "Help") or (filepath == 'h'):
                    help()
                    continue

                if filepath == 'q':
                    return
           
                if pathlib.Path(filepath).suffix != '.txt':
                    print("error")
                    raise ValueError
            except:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
                continue

            try:
                f = open(filepath, "r")
            except:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
                continue


            count = 0
            malformed = 0
            for url in f:
                try:
                    #get = urllib.request.urlopen(str(url.strip()))
                    #if get.getcode() == 200:
                    if validators.url(str(url.strip())):
                        print("[{}]: {}".format(count, url.strip()))
                        urls.append(url.strip())
                        count += 1
                    else:
                        print("[X]: {}".format(url.strip()))
                        malformed += 1
                except:
                    print("[X]: {}".format(url.strip()))
                    malformed += 1

            f.close()

            if malformed > 0:
                print("\n{} Malformed urls included in your file. Added {} valid urls, continuing...\n".format(malformed, count))


            break

    #Default list or manual list entry
    blocklist_urls = []
    blocklist_url_input_type = 'a' #Default

    while True:

        print("\nPlease select if you want to supply a custom ad/tracker list or if you would like to use the default list.\n")
        print("a)    Default list\n")
        print("b)    Custom list\n")

        try:
            blocklist_url_input_type = input("\nPlease enter what type of url input you will use:  ")
        except:
            print("\nOops! There was a problem with your input, please try again.")

        if (blocklist_url_input_type == "help") or (blocklist_url_input_type == "Help") or (blocklist_url_input_type == 'h'):
            help()
            continue

        if blocklist_url_input_type == 'q':
            return

        if blocklist_url_input_type == 'a' or blocklist_url_input_type == 'b':
            break
        else:
            print("\nPlease enter a valid input.")


    if blocklist_url_input_type == 'a':
        try:
            f= open("default_list.txt", "r")
            for url in f:
                blocklist_urls.append(url.strip())
        except:
            print("Oops, looks like something is wrong with the default list file. Please make sure it is in the proper directory and the right format. Aborting program.\n")
            return
        f.close()
        


    if blocklist_url_input_type == 'b':
        while True:
            try:
                filepath = input("\nPlease enter the filepath of a txt file containing your list of ad/tracker urls:   ")

                if (filepath == "help") or (filepath == "Help") or (filepath == 'h'):
                    help()
                    continue

                if filepath == 'q':
                    return

                if pathlib.Path(filepath).suffix != '.txt':
                    raise ValueError

            except:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
                continue

            try:
                f = open(filepath, "r")
            except:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
                continue

            for url in f:
                try:
                    blocklist_urls.append(url.strip())
                except:
                    print("Oops, looks like something is wrong with the default list file, and an error occured when processing it. Please make sure it is in the proper directory and the right format.\n")
                    continue
            f.close()

            break

    print("Datapoints: ", datapoints)
    print("Browser: " + str(browser))
    print("urls ", urls)
    print("blocklist urls", blocklist_urls)

    print("Starting analysis")

    return datapoints,browser,urls,blocklist_urls


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_userinput_args()
    else:
        get_user_input()
