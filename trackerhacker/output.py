import csv
import os
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go

from datetime import datetime
from enum import Enum
from logging import Logger
from typing import Any

from whois import WhoisEntry

from trackerhacker.userinput import DataChoices


class Entity(Enum):
    COUNTRY = ["country", "countries"]
    STATE = ["state", "states"]


# Produces CSV and graph outputs
class Output:
    def __init__(self, logger: Logger, tracker_hacker_root: str, analysis_results: dict[str, dict[str, dict[str, dict[str, list[str] | int | WhoisEntry | list[dict[str, str | None]]]]]], output_choices: list[DataChoices], output_dir: str) -> None:
        self._logger = logger
        self.analysis_results = analysis_results
        self.output_choices = output_choices
        self.output_dir = output_dir
        self.country_codes_iso2to3 = self._make_csv_mapping(os.path.join(tracker_hacker_root, "res/iso2to3.csv"))
        self.state_codes_mapping = self._make_csv_mapping(os.path.join(tracker_hacker_root, "res/stateNamesToCodes.csv"))
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            #TODO error checking

    # read in CSV mapping from col A to col B into memory
    def _make_csv_mapping(self, csv_filename: str) -> dict[str, str]:
        mapping = {}
        with open(csv_filename, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                mapping[row[0]] = row[1]

        return mapping
    
    # retrieve information from analysis results needed to make heat map
    def _get_info_for_heatmap(self, entities: set[str], entity_type: Entity, fqdn: str, fqdn_info: dict[str, list[str] | int | WhoisEntry | list[dict[str, str | None]]], map_info: dict) -> dict[str, dict[str, int | dict[str, int]]]:
        if len(entities) > 1:
            self._logger.warning("'%s' has servers in multiple %s. Double counting for %d ad/trackers for %s" % (fqdn, entity_type.value[1], fqdn_info["ad_tracker_count"], entities))
        
        # calculate total number of ad/trackers for each state/country and fqdn in each state/country
        for entity in entities:
            if entity not in map_info.keys():
                map_info[entity] = {"total_ad_trackers": 0, "fqdns": {}}

            map_info[entity]["total_ad_trackers"] += fqdn_info["ad_tracker_count"]
            if fqdn not in map_info[entity]["fqdns"].keys():
                map_info[entity]["fqdns"][fqdn] = fqdn_info["ad_tracker_count"]
            else:
                map_info[entity]["fqdns"][fqdn] += fqdn_info["ad_tracker_count"]

        return map_info
    
    # given data for a heatmap, generate the plot
    def _make_heatmap_figure(self, map_info: dict[str, dict[str, int | dict[str, int]]], location_mode: str) -> go.Figure:
        locations = []
        ad_tracker_count = []
        ad_tracker_fqdns = []
        for entity, entity_data in map_info.items():
            locations.append(entity)
            ad_tracker_count.append(entity_data["total_ad_trackers"])
            # sort fqdns for current entity by number of ad/tracker requests made
            entity_fqdns_sorted = {k: v for k, v in sorted(entity_data["fqdns"].items(), key=lambda item: item[1], reverse=True)}
            hover_text_fqnds = []
            i = 0
            fqdn_list_len = 40
            # make the hover text for each country - limit number of fqdns in the hover text to 40
            for fqdn, num_requests in entity_fqdns_sorted.items():
                if i == fqdn_list_len:
                    extra_fqdns = len(entity_fqdns_sorted) - fqdn_list_len
                    plural = "s" if extra_fqdns != 1 else ""
                    hover_text_fqnds.append("%d more FQDN%s....." % (extra_fqdns, plural))
                    break

                plural = "s" if num_requests != 1 else ""
                hover_text_fqnds.append("%s: %d ad/tracker request%s" % (fqdn, num_requests, plural))
                i += 1

            ad_tracker_fqdns.append("<br>".join(hover_text_fqnds))

        # generate the heatmap object
        fig = go.Figure(data=go.Choropleth(
            locations=locations,
            z=ad_tracker_count,
            text=ad_tracker_fqdns, # hover text
            locationmode=location_mode,
            reversescale=True,
            marker_line_color='darkgray',
            colorbar_title="Number<br>ads/trackers",
        ))

        return fig

    # make a heatmap
    def make_heatmap(self) -> None:
        self._logger.info("Making heatmap output...")
       
        map_country_info = {}
        map_state_info = {}
        for source_url_info in self.analysis_results.values():
            for browser, browser_info in source_url_info.items():
                if browser not in map_country_info.keys():
                    map_country_info[browser] = {}

                if browser not in map_state_info.keys():
                    map_state_info[browser] = {}

                for fqdn, fqdn_info in browser_info.items():
                    countries: set[str] = set()
                    states: set[str] = set()
                    # geolocation-db uses 2 letter country/state codes, whereas the plotting software uses 3 letter codes, convert them here
                    for server_location_dict in fqdn_info["server_location"]:
                        try:
                            iso3_country_code = self.country_codes_iso2to3[server_location_dict["country_code"]]
                            countries.add(iso3_country_code)
                            if iso3_country_code == "USA" and server_location_dict["state"] is not None:
                                try:
                                    state_code = self.state_codes_mapping[server_location_dict["state"]]
                                    states.add(state_code)
                                except KeyError:
                                    self._logger.warning("'%s' (location of %s) not a valid state code. Skipping....." % (server_location_dict["state"], server_location_dict["IPv4"]))
                        except KeyError:
                            self._logger.warning("'%s' (location of %s) not a valid country code. Skipping....." % (server_location_dict["country_code"], server_location_dict["IPv4"]))

                    # extract the data from the analysis data needed to make the heatmaps
                    map_country_info[browser] = self._get_info_for_heatmap(countries, Entity.COUNTRY, fqdn, fqdn_info, map_country_info[browser])
                    map_state_info[browser] = self._get_info_for_heatmap(states, Entity.STATE, fqdn, fqdn_info, map_state_info[browser])

        # generate country heatmaps
        for browser, heatmap_data in map_country_info.items():
            fig = self._make_heatmap_figure(heatmap_data, "ISO-3")
            fig.update_layout(
                title_text="World Heatmap of Ads/Trackers for %s" % browser,
                title_x=0.5,
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    showcountries=True,
                    countrywidth=1,
                    projection_type='equirectangular'
                )
            )

            output_path = os.path.join(self.output_dir, "%s_ad_tracker_world_map.html" % browser)
            plotly.offline.plot(fig, filename=output_path)
            self._logger.info("Map written to '%s'" % output_path)

        # generate state heatmaps
        for browser, heatmap_data in map_state_info.items():
            fig = self._make_heatmap_figure(heatmap_data, "USA-states")
            fig.update_layout(
                title_text="USA Heatmap of Ads/Trackers for %s" % browser,
                title_x=0.5,
                geo = dict(
                    scope="usa",
                    projection=go.layout.geo.Projection(type="albers usa")
                )
            )

            output_path = os.path.join(self.output_dir, "%s_ad_tracker_usa_map.html" % browser)
            plotly.offline.plot(fig, filename=output_path)
            self._logger.info("Map written to '%s'" % output_path)
        
    # generate bar graph that compares number of ad/tracker requests sent to each browser
    def make_brower_comparison(self) -> None:
        self._logger.info("Making browser comparison output...")
        
        # get data from analysis results
        browser_nums = {}
        for _, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                if browser not in browser_nums.keys():
                    browser_nums[browser] = 0
                for _, fqdn_info in browser_info.items():
                    browser_nums[browser] += fqdn_info["ad_tracker_count"]

        # add the data to a pandas object
        df_browser_ad_tracker_totals = pd.DataFrame()
        for browser, num_ad_trackers in browser_nums.items():
            browser_ad_tracker_series = pd.Series(dtype="object")
            browser_ad_tracker_series["Browser"] = browser
            browser_ad_tracker_series["Number of Ad/Tracker Requests"] = num_ad_trackers
            df_browser_ad_tracker_totals = pd.concat([df_browser_ad_tracker_totals, browser_ad_tracker_series.to_frame().T], ignore_index=True)

        # generate the plot
        data = px.bar(df_browser_ad_tracker_totals, x="Browser", y="Number of Ad/Tracker Requests")
        data.update_layout(title_text="Number of Ad/Tracker Requests Per Browser", title_x=0.5)
        output_path = os.path.join(self.output_dir, "browser_comparison.html")
        plotly.offline.plot(data, filename=output_path)
        self._logger.info("Plot written to '%s'" % output_path)

    # generate plots for top user-requestesd URLs with most ad/tracker requests
    def make_top_sites_graph(self) -> None:
        self._logger.info("Making top sites comparison output...")

        # get the data from the analysis results
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
            ranked_urls = dict(sorted(unranked_urls.items(), key=lambda item: item[1], reverse=True))
            count = 0
            # add the top ten user-requested URLs with the most ad/tracker requests to the plot
            for u, val in ranked_urls.items():
                browser_ad_tracker_series = pd.Series(dtype="object")
                if count > 9:
                    break

                browser_ad_tracker_series["Source URL"] = u
                browser_ad_tracker_series["Number of Ad/Tracker Requests"] = val
                df_browser_ad_tracker_rankings = pd.concat([df_browser_ad_tracker_rankings, browser_ad_tracker_series.to_frame().T], ignore_index=True)
                count += 1
            
            data = px.bar(df_browser_ad_tracker_rankings, x="Source URL", y="Number of Ad/Tracker Requests")
            data.update_layout(title_text=f"{browser} Sites With the Most Ads/Trackers Requests", title_x=0.5)
            
            # long user-requested URLs make the plots look funny - limit URLs to 30 characters
            x_axis_labels = []
            for url in df_browser_ad_tracker_rankings["Source URL"]:
                if len(url) > 30:
                    x_axis_labels.append(url[:30] + "...")
                else:
                    x_axis_labels.append(url)

            data.update_xaxes(tickvals=list(range(10)), ticktext=x_axis_labels)
            output_path = os.path.join(self.output_dir, f"{browser}_top_ten.html")
            plotly.offline.plot(data, filename=output_path)
            self._logger.info("Plot written to '%s'" % output_path)

    # make plot to display the top ten ad and tracker fqdns where requests were made
    def make_top_ads_trackers_graph(self) -> None:
        self._logger.info("Making top 10 ads/trackers graph...")

        # get the data from the analysis results
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
            ranked_adts = dict(sorted(unranked_fqdns.items(), key=lambda item: item[1], reverse=True))

            # add the top ten ad/tracker fqdns to the plot
            count = 0
            for u, val in ranked_adts.items():
                browser_ad_tracker_series = pd.Series(dtype="object")
                if count > 9:
                    break

                browser_ad_tracker_series["Ad/Tracker Domain"] = u
                browser_ad_tracker_series["Number of Requests"] = val
                df_browser_ad_tracker_rankings = pd.concat([df_browser_ad_tracker_rankings, browser_ad_tracker_series.to_frame().T], ignore_index=True)
                count += 1

            data = px.bar(df_browser_ad_tracker_rankings, x="Ad/Tracker Domain", y="Number of Requests")
            data.update_layout(title_text=f"{browser} Top Ten Most Prevalent Ads/Trackers Domains by Number of Requests", title_x=0.5)
            output_path = os.path.join(self.output_dir, f"{browser}_top_ten_adstrackers.html")
            plotly.offline.plot(data, filename=output_path)
            self._logger.info("Plot written to '%s'" % output_path)

    # prettify the output to place into the CSV
    def _prettify_output(self, output: Any) -> str | None:
        if output is None:
            prettified_output = None
        elif type(output) == list:
            prettified_output = ",".join([self._prettify_output(item) for item in output])
        elif type(output) == datetime:
            prettified_output = output.strftime("%Y-%m-%d %H:%M:%S%z")
        else:
            prettified_output = str(output)

        return prettified_output
    
    # make one row of the CSV
    def _make_csv_row(self, source_url: str, browser: str, fqdn: str, fqdn_info: dict[str, list[str] | int | WhoisEntry | list[dict[str, str | None]]], ip: str, first_instance: bool) -> list[str]:
        row = []
        # an FQDN might resolve to more than one IP address; each IP gets a row; the first row will have the FQDN as well, and all subsequent rows will have a "-" to signify that
        # the IP in the current row maps to a FQDN in one of the rows above
        if first_instance:
            row = [source_url, browser, fqdn, fqdn_info["ad_tracker_count"], ip]
        else:
            row = ['-', '-', '-', '-', ip]

        # find the correct dict in the analysis results to populate the CSV
        current_server_dict = {}
        for server_location_dict in fqdn_info["server_location"]:
            if server_location_dict["IPv4"] == ip:
                current_server_dict = server_location_dict
                break

        # retrieve the items for each row
        for output_choice in self.output_choices:
            analysis_field_name = output_choice.value["analysis_name"]
            output_field_name = output_choice.value["output_name"]
            if output_field_name.startswith("server:"):
                try:
                    row.append(self._prettify_output(current_server_dict[analysis_field_name]))
                except KeyError:
                    row.append(None)
                    self._logger.warning("No server location key named '%s' in [%s][%s][%s]. Skipping..." %  (analysis_field_name, source_url, browser, fqdn))
            elif output_field_name.startswith("whois:"):
                try:
                    row.append(self._prettify_output(fqdn_info["whois"][analysis_field_name]))
                except KeyError:
                    row.append(None)
                    self._logger.warning("No whois key named '%s' in [%s][%s][%s]. Skipping..." %  (analysis_field_name, source_url, browser, fqdn))

        return row

    # make the CSV output and write to file
    def make_csv_output(self) -> None:
        self._logger.info("Making CSV output...")
        output_csv = []
        header_row = ["source_url", "browser", "ad_tracker_fqdn", "ad_tracker_count", "ip"]
        # get the output choices requested by the user
        for output_choice in self.output_choices:
            header_row.append(output_choice.value["output_name"])

        output_csv.append(header_row)

        # build output
        for source_url, source_url_info in self.analysis_results.items():
            for browser, browser_info in source_url_info.items():
                for fqdn, fqdn_info in browser_info.items():
                    first_instance = True
                    if len(fqdn_info["ips"]) == 0:
                        output_csv.append(self._make_csv_row(source_url, browser, fqdn, fqdn_info, None, first_instance))

                    for ip in fqdn_info["ips"]:
                        output_csv.append(self._make_csv_row(source_url, browser, fqdn, fqdn_info, ip, first_instance))
                        first_instance = False

        # write the CSV file
        output_csv_filepath = os.path.join(self.output_dir, "output.csv")
        try:
            with open(output_csv_filepath, "w", encoding="utf-8", newline="") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(output_csv)
                #TODO error checking
                self._logger.info("CSV written to '%s'" % output_csv_filepath)
        except PermissionError:
            self._logger.error("Permission denied: '%s'. Unable to open CSV for writing." % output_csv_filepath)
