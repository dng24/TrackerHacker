import userinput
import datacollection

def main():
    print("init")
    # 1. parse args
    datapoints, browsers, urls, blocklist_urls = userinput.get_user_input()

    # 2. open urls with selenium and capture traffic with web proxy
    print(browsers)
    fqdns = datacollection.collect_fqdns(urls, [browsers])

    # 3. separate ad/tracking domains from other domains

    # 4. use ad/tracking domain names to get data we want

    # 5. make visualizations/reports

if __name__ == "__main__":
    main()
