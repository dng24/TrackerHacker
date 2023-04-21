# Tracker Hacker project

## Installation/Setup

1. Install python3.11 and add Python to your PATH variable
2. Install dependencies: `pip3 install -r requirements.txt`
3. Install and launch mitmproxy, go to mitm.it, download the certs, and install according to the directions
4. Install the latest version of any browsers you would like to use to load URLs

For more detail or if you run into errors, see the user manual for more detailed instructions.

## Run
To run TrackerHacker, navigate to the TrackerHacker folder (NOT the trackerhacker subfolder) and run "python main.py".
Running in this way launches the GUI, with menus for each selection you can make.

The first selection is datapoints, which lets you choose what information TrackerHacker will collect about the requests made
while loading the URLs. You can sequentially enter a, b, c, or d to choose additional points one at a time, e to select
all datapoints, or any other letter to move on after your first selection.

The next selection is which browser(s) to use to load your URLs. Each selected browser will be used to load each URL.
You can sequentially enter a, b, c, or d to choose additional browsers, e to choose all browsers, or any other 
letter to move on after your first selection.

Next it will ask for how you would like to enter your URLs. If you choose manual entry, you will be asked to provide
properly formatted URLs one by one. If you choose file upload, you must pass in a valid filepath containing a list of URLs,
one on each line. Incorrectly formatted URLs will be discarded.

The last two selections are whether you want to run in headless mode (yes/no), meaning that there is no visible browser window
as it loads the URLs, and whether you would like the output directory to remain the default (out/ folder in the TrackerHacker
directory) or a custom directory which you may input.

Once all of these choices have been made, the program will run. Upon completion, it will output a series of HTML files and one
CSV file, all of which contain information on the ads and trackers that were queried as the passed in URLs were being loaded

## Command Line Interface
The other way to run TrackerHacker is through the CLI. You can run "python main.py -h" to view the help screen, as below:

usage: main.py [-h] [-d [{a,b,c,d,e} ...]] [-b [{1,2,3,4,5} ...]] [-uf URLFILE] [-u [URLS ...]] [-hl] [-o OUTPUT_DIRECTORY]

options:
  -h, --help            show this help message and exit
  -d [{a,b,c,d,e} ...], --data [{a,b,c,d,e} ...]
                        Data types to output. 

                        a: Server Location
                        b: Server Location Coordinates
                        c: Domain Information
                        d: Owner Information
                        e: All data choices

                        For multiple choices, enter them space delimited, eg: -d a b for Server Location and Server Location Coordinates.
  -b [{1,2,3,4,5} ...], --browser [{1,2,3,4,5} ...]
                        Which browser to use.

                        1: Chrome
                        2: Firefox
                        3: Edge
                        4: Brave
                        5: All browsers

                        For multiple choices, enter them space delimited, eg: 1 2 for Chrome and Firefox
  -uf URLFILE, --urlfile URLFILE
                        File of URLs to analyze. Provide the path of a .txt file with a list of urls, with only a single url per line.
  -u [URLS ...], --urls [URLS ...]
                        URLs to analyze. Manually type urls to analyze, space delimited.
  -hl, --headless       Run program in headless mode. No interface for selenium browser will be launched. Default is non-headless
  -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
                        The output directory to save outputs (Default: out/)

Using the CLI for TrackerHacker allows you to make each choice in one line by running something like:
"python main.py -d e -b 2 -uf urlfile.txt -hl"