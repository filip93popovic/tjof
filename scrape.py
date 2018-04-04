# -*- coding: utf-8 -*-

"""Usage: scrape.py -s <startyear> -e <endyear>

<startyear> and <endyear> should be integers between 1946 and current year.
    Examples:
        1958, 2001, 2017, 1948

-s: Start year of the scrape range. Defaults to 1946.
-e: End year of the scrape range. Defaults to datetime.datetime.now().year
    which stands for current year.

This script scrapes the 'The Journal of Finance - Wiley Online Library' for
articles data in specified age range.

Script can be invoked with start year and/or end year options.
If no options are specified script will scrape the whole website.
In order to scrape only one year type same argument for start and end years.

    Examples:
        python scrape.py
            (scrapes whole website)
        python scrape.py -s 2016
            (scrapes from 2016 till present)
        python scrape.py -e 1950
            (scrapes from 1946 till 1950 - inclusive)
        python scrape.py -s 2016 -e 2017
            (scrapes from 2016 till 2017-inclusive)
        python scrape.py -s 2010 -e 2010
            (scrapes only one year)

Scraped data is exported as a CSV file.
"""

# Loading libraries
import sys
import getopt
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd

opts, args = getopt.getopt(sys.argv[1:], 'hs:e:')

maxyear = datetime.datetime.now().year

dictContainer = []


# Scrape function
def scrape(startyear, endyear):
    """
    Funcion crawls through 'The Journal of Finance - Wiley Online Library'
    website and scrapes data.
    """

    urlvol = startyear - 1946 + 1
    urlissue = 1

    while startyear <= endyear:
        url = "http://onlinelibrary.wiley.com/doi/10.1111/jofi.{}.{}.issue-{}/issuetoc".format(startyear, urlvol, urlissue)
        r = requests.get(url)
        print(url)

        if r.status_code == 200:
            c = r.content
            urlissue += 1

            soup = BeautifulSoup(c, "html.parser")
            # Finding HTML elements that contain Release Date, Volume number, Issue number
            # Release Date, Volume number, Issue number are shown once per page
            all_1 = soup.find_all("div", {"id": "metaData"})

            # Extracting release date
            try:
                release_date = all_1[0].find("h2", {"class": "noMargin"}).text
            except:
                release_date = None

            # Extracting Volume number
            try:
                volume_number = all_1[0].find("span", {"class": "issueTocVolume"}).text
                volume_number = volume_number[-2:]
            except:
                volume_number = None
            # Extracting Issue number
            try:
                issue_number = all_1[0].find("span", {"class": "issueTocIssue"}).text
                issue_number = issue_number[-1]
            except:
                issue_number = None

            # Finding HTML elements that contain Titles and Authors
            all_2 = soup.find_all("div", {"class": "citation tocArticle"})
            # There are multiple elements on page so that is the reason to iterate
            for item in all_2:
                d = {}

                # Titles with number of pages
                try:
                    t = item.find("a").text
                    # Title
                    c = t.find("(")
                    L = len(t)
                    title = t.replace(t[c-1:], "")
                    # Page numbers
                    page_num = t[c+1:L-1]
                    x = page_num.find("(pages ")
                    page_numbers = page_num.replace(page_num[:x+7], "")
                    d["Title"] = title
                    d["Page numbers"] = page_numbers
                except:
                    t = None

                # Authors and DOI
                # Authdoi is list of <p> elements - Index is used for selecting particular
                # No class or ID was defined so we had to find them manually
                authdoi = item.find_all("p")
                try:
                    author = authdoi[0].text
                    d["Author"] = author
                except:
                    author = None

                    # Code that exports required URL of other pages we want information from
                    # And also code that scrapes that information
                    # Embeded scrape into the main one - it has dependecies in main scrape
                try:
                    doi = authdoi[1].text
                    # Extracing link from DOI
                    # This is the dependecy we mentioned before
                    ind = doi.index("DOI: ")
                    rDOI = doi[ind+5:]
                    lk = "http://onlinelibrary.wiley.com/wol1/doi/" + rDOI + "/abstract"
                    d["Link"] = "http://onlinelibrary.wiley.com/wol1/doi/" + rDOI + "/abstract"
                except:
                    doi = None
                try:
                    req = requests.get(lk)
                    ctt = req.content
                    supa = BeautifulSoup(ctt, "html.parser")
                except:
                    doi = None
                try:
                    affiliation = supa.find("li", {"class": "affiliation"})
                    d["affiliation"] = affiliation.find("p").text
                except:
                    affiliation = None
                try:
                    author = supa.find("div", {"class": "text"}).text
                    d["authinfo"] = author
                except:
                    author = None

                # Adding info from all_1 since we do not iterate through that for every article
                # But we would like to have that information next to each of articles
                d["Rel Month/Year"] = release_date
                d["Volume number"] = volume_number
                d["Issue number"] = issue_number

                dictContainer.append(d)

            print('Number of scraped records: ', len(dictContainer))

        elif r.status_code == 404:
            startyear += 1
            urlvol += 1
            urlissue = 1


if __name__ == '__main__':
    if len(sys.argv[1:]) == 0:
        scrape(1946, maxyear)
    elif len(sys.argv[1:]) == 1:
        for opt, arg in opts:
            if opt == '-h':
                print(__doc__)
    elif len(sys.argv[1:]) == 2:
        for opt, arg in opts:
            if opt == '-s':
                scrape(int(arg), maxyear)
            elif opt == '-e':
                scrape(1946, int(arg))
    elif len(sys.argv[1:]) == 4:
            scrape(int(opts[0][1]), int(opts[1][1]))

    # Exporting data
    data = pd.DataFrame(dictContainer)
    data.to_csv('data.csv')

    # End notes
    print('\n', 36*'~', 'END', 36*'~')
