import csv
import os
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
#import seaborn as sns

from trackerhacker.userinput import DataChoices

LIST_DELIMITATOR = ","

class Output:
    def __init__(self, logger, analysis_results: dict, output_choices: list[DataChoices], output_dir: str) -> None:
        #sns.set()
        self.logger = logger
        self.analysis_results = analysis_results
        self.output_choices = output_choices
        self.output_dir = output_dir
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            #TODO error checking

    def make_heatmap(self) -> None:
        self.logger.info("Making heatmap output...")
        fig = go.Figure(go.Scattergeo())
        fig.update_geos(
            visible=False, resolution=50,
            showcountries=True, countrycolor="RebeccaPurple"
        )
        fig.update_layout(height=300, margin={"r":0,"t":0,"l":0,"b":0})
        fig.show()
        
    def make_brower_comparison(self) -> None:
        self.logger.info("Making browser comparison output...")
        
        browser_nums = {}

        for source_url, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                if browser not in browser_nums.keys():
                    browser_nums[browser] = 0
                for fqdn, fqdn_info in browser_info.items():
                    browser_nums[browser] += fqdn_info["ad_tracker_count"]

        df_browser_ad_tracker_totals = pd.DataFrame()
        for browser, num_ad_trackers in browser_nums.items():
            browser_ad_tracker_series = pd.Series(dtype="object")
            browser_ad_tracker_series["Browser"] = browser
            browser_ad_tracker_series["Number of ads/trackers"] = num_ad_trackers
            df_browser_ad_tracker_totals = df_browser_ad_tracker_totals.append(browser_ad_tracker_series, ignore_index=True)

        data_represent = px.bar(df_browser_ad_tracker_totals, x="Browser", y="Number of ads/trackers")
        plotly.offline.plot(data_represent, filename=os.path.join(self.output_dir, "browser_comparison.html"))


    def make_top_sites_graph(self) -> None:
        self.logger.info("Making top sites comparison output...")

        url_ranked_by_browser = {}

        url_ranked_by_browser = {}
        for source_url, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                if browser not in url_ranked_by_browser:
                    url_ranked_by_browser[browser] = {}

                if source_url not in url_ranked_by_browser[browser]:
                    url_ranked_by_browser[browser][source_url] = 0
                
                for _, fqdn_info in browser_info.items():
                    url_ranked_by_browser[browser][source_url] += fqdn_info["ad_tracker_count"]



        for browser, unranked_urls in url_ranked_by_browser.items():
            df_browser_ad_tracker_rankings = pd.DataFrame()
            ranked_urls = dict(sorted(unranked_urls.items(), key=lambda item: item[1]))
            print(ranked_urls)
            count = 0
            for u, val in ranked_urls.items():
                browser_ad_tracker_series = pd.Series(dtype="object")
                #print("Printing ranked items")
                #print(u)
                #print(val)
                if count > 9:
                    break
                browser_ad_tracker_series["Source URL"] = u
                browser_ad_tracker_series["Number of ads/trackers"] = val
                
                #browser_ad_tracker_series[u] = ranked_urls[u]
                df_browser_ad_tracker_rankings = df_browser_ad_tracker_rankings.append(browser_ad_tracker_series, ignore_index=True)
                count += 1
            
            data_represent = px.bar(df_browser_ad_tracker_rankings, x="Source URL", y="Number of ads/trackers")
            plotly.offline.plot(data_represent, filename=os.path.join(self.output_dir, f"{browser}_top_ten.html"))

        
    def make_top_ads_trackers_graph(self) -> None:
        self.logger.info("Making top 10 ads/trackers graph...")

        adt_ranked_by_browser = {}

        for _, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                if browser not in adt_ranked_by_browser:
                    adt_ranked_by_browser[browser] = {}

                for fqdn, fqdn_info in browser_info.items():
                    if fqdn not in adt_ranked_by_browser[browser]:
                        adt_ranked_by_browser[browser][fqdn] = fqdn_info["ad_tracker_count"]
                    else:
                        adt_ranked_by_browser[browser][fqdn] += fqdn_info["ad_tracker_count"]

        for browser, unranked_fqdns in adt_ranked_by_browser.items():
            df_browser_ad_tracker_rankings = pd.DataFrame()
            ranked_adts = dict(sorted(unranked_fqdns.items(), key=lambda item: item[1]))

            count = 0
            for u, val in ranked_adts.items():
                browser_ad_tracker_series = pd.Series(dtype="object")
                #print("Printing ranked items")
                #print(u)
                #print(val)
                if count > 9:
                    break
                browser_ad_tracker_series["Ad/Tracker"] = u
                browser_ad_tracker_series["Frequency"] = val

                #browser_ad_tracker_series[u] = ranked_urls[u]
                df_browser_ad_tracker_rankings = df_browser_ad_tracker_rankings.append(browser_ad_tracker_series, ignore_index=True)
                count += 1

            data_represent = px.bar(df_browser_ad_tracker_rankings, x="Ad/Tracker", y="Frequency")
            plotly.offline.plot(data_represent, filename=os.path.join(self.output_dir, f"{browser}_top_ten_adstrackers.html"))


    def make_csv_output(self) -> None:
        self.logger.info("Making CSV output...")
        output_csv = []
        header_row = ["source_url", "browser", "ad_tracker_fqdn", "ad_tracker_count", "ip"]
        for output_choice in self.output_choices:
            header_row.append(output_choice.value["output_name"])

        output_csv.append(header_row)

        for source_url, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, fqdn_info in browser_info.items():
                    for ip in fqdn_info["ips"]:
                        row = [source_url, browser, fqdn, fqdn_info["ad_tracker_count"], ip]
                        for server_location_dict in fqdn_info["server_location"]:
                            if server_location_dict["IPv4"] == ip:
                                current_server_dict = server_location_dict

                        for output_choice in self.output_choices:
                            analysis_field_name = output_choice.value["analysis_name"]
                            output_field_name = output_choice.value["output_name"]
                            if output_field_name.startswith("server:"):
                                row.append(current_server_dict[analysis_field_name])
                            elif output_field_name.startswith("whois:"):
                                row.append(fqdn_info["whois"][analysis_field_name])

                        output_csv.append(row)

        output_csv_filename = os.path.join(self.output_dir, "output.csv")
        with open(output_csv_filename, "w", newline="") as f:
            csv_writer = csv.writer(f)
            print(output_csv)
            csv_writer.writerows(output_csv)
            #TODO error checking
            self.logger.info("CSV written to '%s'" % output_csv_filename)
            
                        
    def make_html_output(self) -> None:
        self.logger.info("Making HTML output...")
