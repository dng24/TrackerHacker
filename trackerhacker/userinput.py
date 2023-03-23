import socket
import urllib.request
import sys
import os
import requests
import pathlib
import validators
import argparse

from enum import Enum

from trackerhacker.browsermanager import WebBrowsers
from trackerhacker import TrackerObject

class DataChoices(Enum):
    SERVER_LOCATION = "server_location"
    DOMAIN_NAME = "whois:domain_name"
    REGISTRAR = "whois:registrar"
    WHOIS_SERVER = "whois:whois_server"
    REFERRAL_URL = "whois:referral_url"
    UPDATED_DATE = "whois:updated_date"
    CREATION_DATE = "whois:creation_date"
    EXPIRATION_DATE = "whois:expiration_date"
    NAME_SERVERS = "whois:name_servers"
    STATUS = "whois:status"
    EMAILS = "whois:emails"
    DNSSEC = "whois:dnssec"
    NAME = "whois:name"
    ORG = "whois:org"
    ADDRESS = "whois:address"
    WHOIS_CITY = "whois:city"
    WHOIS_STATE = "whois:state"
    WHOIS_REGISTRANT_POSTAL_CODE = "whois:registrant_postal_code"
    WHOIS_COUNTRY = "whois:country"
    

def check_adlists(adlists_dir):
    dir = os.listdir(adlists_dir)
    if len(dir) == 0:
        print("There was a problem with referencing files in the adlists dir. Please make sure the directory is not empty.")
    else:
        x = len(dir)
        print(f"Num files: {x}")
        return 1
    return None

def help():
    print("\n\nWelcome to tracker hacker, a convenient tool to show what trackers are spying on you when you visit a webpage. Usage of the tool is easy!\n\nFirst, enter the types of FINISH")

def get_userinput_cli(adlists_dir):
    print("args")
    

    datapoints = []
    browsers = []
    urls = []
    adlist_path = ""
    parser = argparse.ArgumentParser()
    headless = False
    default_flag = True

    parser.add_argument("-d", "--data", nargs='*', help="Data types to output. a: Whois, b: IP geolocation, c: Owner. For multipe choices, enter them space delimited, eg: -d a b for whois and IP geolocation.", type=str, choices=['a','b','c'])
    parser.add_argument("-b", "--browser", nargs='*', help="Which browser to use. 1: Chrome, 2: Firefox, 3: Edge, 4: Brave. For multiple choices, enter them space delimited, eg: 1 2 for Chrome and Firefox", type=int, choices=[1,2,3,4])
    parser.add_argument("-uf", "--urlfile", help="File of URLs to analyze. Provide the path of a .txt file with a list of urls, with only a single url per line.")
    parser.add_argument("-u", "--urls", nargs='*', help="URLs to analyze. Manually type urls to analyze, space delimited.")
    #parser.add_argument("-l", "--list", help="List of ads/trackers. This program by default uses a set of premade ad/tracker lists. If you would like to add a custom ad/tracker list, please provide the path of a .txt file with a list of custom ad/tracker urls, with only a single url per line.")
    #parser.add_argument("-e", "--exclude", help="Use this flag to tell the program to EXCLUDE the default ad/track list referenced during run.", action='store_true')
    parser.add_argument("-hl", "--headless", help="Run program in headless mode. No interface for selenium browser will be launched. Default is non-headless", action='store_true')
    


    args = parser.parse_args()
    
    if args.data:
        for choice in args.data:
            if choice in datapoints:
                continue
            datapoints.append(choice)
    else:
        datapoints = ['a','b','c'] #Gui outputs chars, in order to make it more streamlined, num choices are converted 
            
    

    if args.browser:
        count = 0
        browsers = []
        for choice in args.browser:
            if choice == 1:
                browsers.append(WebBrowsers.CHROME)
            if choice == 2:
                browsers.append(WebBrowsers.FIREFOX)
            if choice == 3:
                browsers.append(WebBrowsers.EDGE)
            if choice == 4:
                browsers.append(WebBrowsers.BRAVE)
    else:
        browsers.append(WebBrowsers.FIREFOX)

    
    if args.urlfile:
        if pathlib.Path(args.urls).suffix != '.txt':
            print("\nOops! Looks like there was a problem loading your urls file. Please make sure that it is a valid path and a correctly formatted .txt file")          
        else:    
            count = 0
            malformed = 0
            print("Loading urls:")
            #try:
            f = open(args.urls, "r")
            #except:
            #    print("Oops, looks like there was a problem reading your url file! Please make sure it is the correct format/file type and the path is correct")
            for url in f:
                try:
                    if validators.url(url.strip()):
                        print("[{}]: {}".format(count, url.strip()))
                        urls.append(url.strip())
                        count += 1
                    else:
                        print("[X]: {}".format(url.strip()))
                        malformed += 1
                except Exception:
                    print("[X]: {}".format(url.strip()))
                    malformed += 1 
            f.close()

            print("\n{} Malformed urls included in your file. Added {} valid urls, continuing...\n".format(malformed, count))

    if args.urls:
        count = 0
        malformed = 0
        print("Loading urls:")
        for url in args.urls:
            try:
                if validators.url(url.strip()):
                    print("[{}]: {}".format(count, url.strip()))
                    urls.append(url.strip())
                    count += 1
                else:
                    print("[X]: {}".format(url.strip()))
                    malformed += 1
            except Exception:
                print("[X]: {}".format(url.strip()))
                malformed += 1

        print("\n{} Malformed urls included in your file. Added {} valid urls, continuing...\n".format(malformed, count))

    #if args.list:
    #    if pathlib.Path(args.list).suffix != '.txt':
    #        print("\nOops! Looks like there was a problem loading your urls file. Please make sure that it is a valid path and a correctly formatted .txt file")
    #    else:
    #        adlist_path = args.list

    #if args.exclude:
    #    default_flag = False

    if args.headless:
        headless = True


    if check_adlists(adlists_dir) == None:
        exit()

    #print("Choices", datapoints)
    #print("Browsers", browsers)
    #print("Urls", urls)
    #print("Adlist", adlist_urls)

    trackerQuery = TrackerObject.TrackerObject(datapoints, browsers, urls, headless)

    return trackerQuery

def datapoints():

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
                return None

        except Exception:
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
                return None
            else:
                break
        else:
            break

    return datapoints


def browser_choice():

    #Browser Choice
    browser = [] #Chrome is default, value set at 'a'
    while True:
        print("\n Please select the browser for tracker hacker to query\n")
        print("a)    Chrome\n")
        print("b)    Firefox\n")
        print("c)    Edge\n")
        print("d)    Brave\n")

        try:
            browser_choice = input("--->   ")

            if (browser_choice == "help") or (browser_choice == "Help") or (browser_choice == 'h'):
                help()
                continue

            if browser_choice == 'q':
                return None
        except Exception:
            print("\nOops! Something went wrong with your input. Please try again")
            continue


        if browser_choice == 'a':
            browser.append(WebBrowsers.CHROME)
        elif browser_choice == 'b':
            browser.append(WebBrowsers.FIREFOX)
        elif browser_choice == 'c':
            browser.append(WebBrowsers.EDGE)
        elif browser_choice == 'd':
            browser.append(WebBrowsers.BRAVE)
        else:
            print("\nPlease enter a valid choice for browser")
            continue

        if len(browser) != 4:
            c = input("\nWould you like to select another browser? (y or any other key):")

            if c == 'y':
                continue
            if c == 'q':
                return None
            else:
                break
        else:
            break



    return browser


def urls():
    #Url input
    urls = []
    url_input_type = 'a' #Default is manual entry

    while True:

        print("\nPlease enter what type of url input you will use.\n")
        print("a)    Manual entry\n")
        print("b)    File upload\n")
       
        try:
            url_input_type = input("\nPlease enter what type of url input you will use:  ")
        except Exception:
            print("\nOops! There was a problem with your input, please try again.")

        if (url_input_type == "help") or (url_input_type == "Help") or (url_input_type == 'h'):
            help()
            continue

        if url_input_type == 'q':
            return None

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
                    return None

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
                        return None
                else:
                    print("Malformed URL entered, please type your desired url again")
                    continue

                break
            except Exception:
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
                    return None
           
                if pathlib.Path(filepath).suffix != '.txt':
                    print("error")
                    raise ValueError
            except:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a txt file.")
                continue

            try:
                f = open(filepath, "r")
            except Exception:
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
                except Exception:
                    print("[X]: {}".format(url.strip()))
                    malformed += 1

            f.close()

            if malformed > 0:
                print("\n{} Malformed urls included in your file. Added {} valid urls, continuing...\n".format(malformed, count))


            break

    return urls


def adtrack_list():

    #Default list or manual list entry
    custom_list = ""
    default_flag = True

    while True:

        #print("\nPlease select if you want to supply a custom ad/tracker list or if you would like to use the default list.\n")
        #print("a)    Default list\n")
        #print("b)    Custom list\n")

        try:
            default_choice = input("\nTracker Hacker uses a default ad/tracker list to query your results against. If you would like to use the default list, press any key to continue. If you do not want to use the default list, please enter n/no\n")
        except Exception:
            print("error")
            continue

        if (default_choice == "help") or (default_choice == "Help") or (default_choice == 'h'):
            help()
            continue

        if default_choice == 'q':
            return None, None

        if default_choice == 'n' or default_choice == "no":
            default_flag = False

        break


    while True:
        if default_flag:
            try:
                c_lists = input("\nWould you like to enter a custom ad/tracker list (y or yes, any other key for no):  ")
            except Exception:
                print("error")
                continue

            if (c_lists == "help") or (c_lists == "Help") or (c_lists == 'h'):
                help()
                continue

            if c_lists == 'q':
                return None, None

            if (c_lists == 'y') or (c_lists == "yes"):
                print("yes")
            else:
                break

        try:
            filepath = input("\nPlease enter the path to a txt file containing your ad/tracker list:   ")
            
            if (filepath == "help") or (filepath == "Help") or (filepath == 'h'):
                help()
                continue

            if filepath == 'q':
                return None, None

            if pathlib.Path(filepath):
                custom_list = filepath
            else:
                raise ValueError

        except Exception:
            print("error in processing filepath")
            continue
            
        break
        

    return default_flag, custom_list
    

def headless_run():
    headless = False
    while True:
        try:
            headless_choice = input("\nPlease select if you would like to run this program headless (without the selenium web browser visual interface running). Enter y/yes for yes, any other key for no.")
            
            if (headless_choice == "help") or (headless_choice == "Help") or (headless_choice == 'h'):
                help()
                continue

            if headless_choice == 'q':
                return None 

            break

        except Exception:
            print("\nOops, something went wrong with your input. Please try again")
            continue

    if (headless_choice == 'y') or (headless_choice == "yes"):
        headless = True


    return headless




def get_user_input_gui(adlists_dir):

    print("Welcome to tracker hacker!\n")
    print("To begin, select your datapoints and url inputs. (Type help for manual, q to quit)\n")

    d = datapoints()
    if d is None:
        exit()

    b = browser_choice()
    if b is None:
        exit()

    u = urls()
    if u is None:
        exit()

    #flag, customlist = adtrack_list()
    #if flag is None or customlist is None:  
    #    exit()

    if check_adlists(adlists_dir) == None:
        exit()
    

    headless = headless_run()
    if headless is None:
        exit()

    # TODO: do we want to allow headless on gui input?
    trackerQuery = TrackerObject.TrackerObject(d, b, u, headless)

    return trackerQuery


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_userinput_cli()
    else:
        get_user_input_gui()
