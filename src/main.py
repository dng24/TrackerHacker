import userinput
import datacollection
import sys

def main():
    print("init")
    # 1. parse args
    
    # Determines what interface to use
    if len(sys.argv) > 1:
        datapoints, browsers, urls, blocklist_urls, headless = userinput.get_userinput_cli()
    else:
        datapoints, browsers, urls, blocklist_urls, headless = userinput.get_user_input_gui()

    # 2. open urls with selenium and capture traffic with web proxy
    # TODO: add absolute timeout and support for browser paths
    print(browsers)
    fqdns = datacollection.collect_fqdns(urls, browsers, headless=headless)

    # 3. separate ad/tracking domains from other domains

    # 4. use ad/tracking domain names to get data we want

    # 5. make visualizations/reports

if __name__ == "__main__":
    main()
