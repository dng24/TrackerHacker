import argparse
import os
import pathlib
import sys
import validators

from argparse import RawTextHelpFormatter


from trackerhacker.browsermanager import WebBrowsers
from trackerhacker import TrackerObject
from trackerhacker.TrackerObject import DataChoices


DATA_CHOICES_MAPPING = {
    "a": [DataChoices.SERVER_COUNTRY_CODE, DataChoices.SERVER_COUNTRY_NAME, DataChoices.SERVER_STATE, DataChoices.SERVER_CITY, DataChoices.SERVER_POSTAL_CODE],
    "b": [DataChoices.SERVER_LATITUTE, DataChoices.SERVER_LONGITUDE],
    "c": [DataChoices.DOMAIN_NAME, DataChoices.REGISTRAR, DataChoices.WHOIS_SERVER, DataChoices.REFERRAL_URL, DataChoices.UPDATED_DATE, DataChoices.CREATION_DATE, DataChoices.EXPIRATION_DATE, DataChoices.NAME_SERVERS, DataChoices.STATUS, DataChoices.DNSSEC],
    "d": [DataChoices.NAME, DataChoices.ORG, DataChoices.ADDRESS, DataChoices.WHOIS_CITY, DataChoices.WHOIS_STATE, DataChoices.WHOIS_COUNTRY, DataChoices.WHOIS_REGISTRANT_POSTAL_CODE, DataChoices.EMAILS]
}


# Checks the adlist directory for files
def check_adlists(adlists_dir):
    dir = os.listdir(adlists_dir)
    if len(dir) == 0:
        print("There was a problem with referencing ad list files in '%s'. Please make sure the directory is not empty." % adlists_dir)
        return None
    else:
        x = len(dir)
        print(f"Num files: {x}")
        return 1


# Help function
def help():
    print("\n\nWelcome to tracker hacker, a convenient tool to show what trackers are spying on you when you visit a webpage. Usage of the tool is easy!\n\nFirst, enter the types of data you want to find out about the adstrackers, then supply which browsers you want the program to run on. Following, supply either a list of manually entered urls (make sure to type them in the correct format: https://<valid url>.<valid url type>, or supply a list of urls in a txt file. You can then supply a custom list of ads/tracker to look for, or you can use the default lists. You can also choose to run the program headless, which means the selenium gui will not launch. Finally, you can specify the type of output and directory for the output.\n\n\nHelpful tips:\n - At any time, you can provide h, H, or help to the input field to bring up this help menu.\n - At any time, you can type q or quit to end the program\n - If you enter a value or entry wrong, no worries, the program will pick up on it and prompt you to re-enter it.\n")


# Method to retrieve the user supplied information from the cli run 
def get_userinput_cli(adlists_dir, default_output_dir):
    datapoints = []
    browsers = []
    urls = []
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter)
    headless = False

    parser.add_argument("-d", "--data", nargs='*', help="Data types to output. \n\na: Server Location \nb: Server Location Coordinates \nc: Domain Information \nd: Owner Information \ne: All data choices\n\nFor multipe choices, enter them space delimited, eg: -d a b for Server Location and Server Location Coordinates.", type=str, choices=['a','b','c', 'd', 'e'])
    parser.add_argument("-b", "--browser", nargs='*', help="Which browser to use. \n\n1: Chrome \n2: Firefox \n3: Edge \n4: Brave \n5: All browsers\n\nFor multiple choices, enter them space delimited, eg: 1 2 for Chrome and Firefox", type=int, choices=[1,2,3,4,5])
    parser.add_argument("-uf", "--urlfile", help="File of URLs to analyze. Provide the path of a .txt file with a list of urls, with only a single url per line.")
    parser.add_argument("-u", "--urls", nargs='*', help="URLs to analyze. Manually type urls to analyze, space delimited.")
    parser.add_argument("-hl", "--headless", help="Run program in headless mode. No interface for selenium browser will be launched. Default is non-headless", action='store_true')
    parser.add_argument("-o", "--output-directory", nargs=1, default=default_output_dir, help="The output directory to save outputs (Default: %s/)" % default_output_dir)
    
    # Parses user command line args
    args = parser.parse_args()

    # Determines what types of data points the user supplied for -d argument
    if args.data:
        data_choices = []
        if 'e' in args.data:
            for choice in DATA_CHOICES_MAPPING.values():
                datapoints.extend(choice)
        else:
            for choice in args.data:
                if choice in data_choices:
                    continue
                data_choices.append(choice)
                datapoints.extend(DATA_CHOICES_MAPPING[choice])
    else:
        for choices in DATA_CHOICES_MAPPING.values():
            datapoints.extend(choices)
    
    # Determines what browsers to run the program on
    if args.browser:
        count = 0
        browsers = []
        if 5 in args.browser:
            browsers.append(WebBrowsers.CHROME)
            browsers.append(WebBrowsers.FIREFOX)
            browsers.append(WebBrowsers.EDGE)
            browsers.append(WebBrowsers.BRAVE)
        else:
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

    # Loads the user specificed file for url lists
    if args.urlfile:
        # Determines if the supplied filepath is valid
        if pathlib.Path(args.urlfile).suffix.lower() != '.txt':
            print("\nOops! Looks like there was a problem loading your urls file. Please make sure that it is a valid path and a correctly formatted TXT file.")          
        else:    
            count = 0
            malformed = 0
            print("Loading urls:")
            #try:
            f = open(args.urlfile, "r")
            #except:
            
            # Iterates through the lines of the user supplied file and collects each url, stripping the extra characters off until left with only url
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

            print("\n{} malformed urls included in your file. Added {} valid urls, continuing...\n".format(malformed, count))

    # Load individual urls provided by the user in the commnd line
    if args.urls:
        count = 0
        malformed = 0
        print("Loading urls:")

        # Iterates through each url and formats it to be readable by the rest of the program
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

    # If there are no URLs entered, quits out
    if len(urls) == 0:
        print("Please enter at least 1 valid URL.")
        quit()

    # Determines if the program will run headless
    if args.headless:
        headless = True

    # Checks the adlists
    if check_adlists(adlists_dir) == None:
        return None

    # Constructs tracker object to pass to main
    trackerQuery = TrackerObject.TrackerObject(datapoints, browsers, urls, headless, args.output_directory)
    return trackerQuery


# Determines user requested datapoints to query for the supplied urls
def datapoints():
    #Desired data points
    datapoints = []
    data_choices = []

    # Collects and analyzes user input
    while True:
        print("\nPlease select a data point you want Tracker Hacker to ouptut:\n")
        print("a)    Server location\n")
        print("b)    Server location coordinates\n")
        print("c)    Domain information\n")
        print("d)    Owner information\n")
        print("e)    All of the Above\n")

        # Prompts user, and gets valid input
        try:
            data_choice = input("--->  ").lower()
            if data_choice in ["h", "help"]:
                help()
                continue
            elif data_choice in ["q", "quit"]:
                return None

        except Exception:
            print("\nOops, something went wrong with your input. Please try again.")
            continue

        if data_choice == 'e':
            for choice, value in DATA_CHOICES_MAPPING.items():
                data_choices.append(choice)
                datapoints.extend(value)

            break

        try:
            data_choice_items = DATA_CHOICES_MAPPING[data_choice]
        except KeyError:
            print("'%s' is not a valid choice. Please try again.\n" % data_choice)
            continue

        if data_choice not in data_choices:
            data_choices.append(data_choice)
            datapoints.extend(data_choice_items)
        else:
            print("\nPlease enter a choice that you have not selected yet.")
            continue

        if len(data_choices) != 4:
            while True:
                c = input("\nWould you like to select another datapoint? [y/N/h/q] ").lower()
                if c in ["y", "yes"]:
                    break
                elif c in ["h", "help"]:
                    help()
                elif c in ["q", "quit"]:
                    return None
                else:
                    return datapoints
                
        else:
            break

    return datapoints


# Determines which browsers to run the program through
def browser_choice():
    #Browser Choice
    browser = []
    while True:
        print("\nPlease select the browser for Tracker Hacker to query:\n")
        print("a)    Chrome\n")
        print("b)    Firefox\n")
        print("c)    Edge\n")
        print("d)    Brave\n")
        print("e)    All of the Above\n")

        try:
            browser_choice = input("--->   ").lower()
            if browser_choice in ["h", "help"]:
                help()
                continue
            elif browser_choice in ["q", "quit"]:
                return None
            
        except Exception:
            print("\nOops! Something went wrong with your input. Please try again.")
            continue

        if browser_choice == 'a':
            browser.append(WebBrowsers.CHROME)
        elif browser_choice == 'b':
            browser.append(WebBrowsers.FIREFOX)
        elif browser_choice == 'c':
            browser.append(WebBrowsers.EDGE)
        elif browser_choice == 'd':
            browser.append(WebBrowsers.BRAVE)
        elif browser_choice == 'e':
            browser.append(WebBrowsers.CHROME)
            browser.append(WebBrowsers.FIREFOX)
            browser.append(WebBrowsers.EDGE)
            browser.append(WebBrowsers.BRAVE)
        else:
            print("'%s' is not a valid choice. Please try again.\n" % browser_choice)
            continue

        if len(browser) != 4:
             while True:
                c = input("\nWould you like to select another browser? [y/N/h/q] ").lower()
                if c in ["y", "yes"]:
                    break
                elif c in ["h", "help"]:
                    help()
                elif c in ["q", "quit"]:
                    return None
                else:
                    return browser
                
        else:
            break

    return browser


# Determines what urls to run the program against
def urls():
    #Url input
    urls = []
    url_input_type = ""

    while True:
        print("\nPlease enter what type of url input you will use.\n")
        print("a)    Manual entry\n")
        print("b)    File upload\n")
       
        try:
            url_input_type = input("--->   ").lower()
        except Exception:
            print("\nOops! There was a problem with your input, please try again.")

        if url_input_type in ["h", "help"]:
            help()
            continue
        elif url_input_type in ["q", "quit"]:
            return None
        elif url_input_type in ["a", "b"]:
            break
        else:
            print("\nPlease enter a valid input.")

    if url_input_type == 'a':
        while True:
            try:
                print("\nEnter the desired URL:\n")
                user_input = input("--->   ")
                if user_input.lower() in ["h", "help"]:
                    help()
                    continue
                elif user_input.lower() in ["q", "quit"]:
                    return None

                if validators.url(str(user_input)):
                    urls.append(user_input)
                    print("Valid URL entered!")
                    while True:
                        c = input("\nWould you like to enter another URL? [y/N/h/q] ").lower()
                        if c in ["y", "yes"]:
                            break
                        elif c in ["h", "help"]:
                            help()
                            continue
                        elif c in ["q", "quit"]:
                            return None
                        else:
                            return urls
                else:
                    print("Malformed URL entered, please type your desired URL again.\n")
                    continue

            except Exception:
                print("Malformed URL entered, please type your desired url again\n")
                continue

    if url_input_type == 'b':
        while True:
            try:
                print("\nEnter the filepath of a TXT file containing your list of URLs:\n")
                filepath = input("--->   ")
                
                if filepath.lower() in ["h", "help"]:
                    help()
                    continue
                elif filepath.lower() in ["q", "quit"]:
                    return None
           
                if pathlib.Path(filepath.lower()).suffix != '.txt':
                    print("error")
                    raise ValueError
            except Exception:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a TXT file.")
                continue

            try:
                f = open(filepath, "r")
            except Exception:
                print("\nOops! Looks like there was a problem referencing the file. Make sure you entered the path correctly and the file is a TXT file.")
                continue

            count = 0
            malformed = 0
            for url in f:
                try:
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
                print("\n{} malformed urls included in your file. Added {} valid urls, continuing...\n".format(malformed, count))

            break

        if len(urls) == 0:
            print("Your URL file must contain at least one valid URL. Please try again.")
            quit(0)

    return urls

    
# Determines if the program will run headless, or if it will launch the selenium visual browser
def headless_run():
    headless = False
    while True:
        try:
            headless_choice = input("\nWould you like to collect data in headless mode (GUI of browsers will not appear)? [y/N/h/q] ").lower()
            if headless_choice in ["h", "help"]:
                help()
                continue
            elif headless_choice in ["q", "quit"]:
                return None 
            elif headless_choice in ["y", "yes"]:
                headless = True

            break

        except Exception:
            print("\nOops, something went wrong with your input. Please try again.")
            continue

    return headless


# Determines the ouptut directory where the output graphics and csv will be put
def get_output_dir(default_output_dir):
    output_dir = default_output_dir
    while True:
        try:
            use_default_output_dir = input("\nWould you like to use the default output directory (out/)? [Y/n/h/q] ").lower()
            if use_default_output_dir in ["h", "help"]:
                help()
                continue
            elif use_default_output_dir in ["q", "quit"]:
                return None 
            elif use_default_output_dir not in ["", "y", "yes"]:
                while True:
                    print("\nEnter your output directory:\n")
                    output_dir = input("--->   ")
                    if output_dir.lower() in ["h", "help"]:
                        help()
                        continue
                    elif output_dir.lower() in ["q", "quit"]:
                        return None
                    else:
                        break

            break
        except Exception:
            print("\nOops, something went wrong with your input. Please try again")
            continue

    return output_dir


# Runs all the UI components and prompts user
def get_user_input_gui(adlists_dir: str, default_output_dir: str) -> TrackerObject.TrackerObject:
    print("Welcome to Tracker Hacker!\n")
    print("To begin, follow the prompts to select your inputs (Type h/help for the manual, q/quit to quit).\n")

    d = datapoints()
    if d is None:
        return None
    
    b = browser_choice()
    if b is None:
        return None
    
    u = urls()
    if u is None:
        return None
    
    if check_adlists(adlists_dir) is None:
        return None

    headless = headless_run()
    if headless is None:
        return None
    
    output_dir = get_output_dir(default_output_dir)
    if output_dir is None:
        return None

    trackerQuery = TrackerObject.TrackerObject(d, b, u, headless, output_dir)
    return trackerQuery


if __name__ == "__main__":
    if len(sys.argv) > 1:
        get_userinput_cli()
    else:
        get_user_input_gui()
