Type "python scrape.py -h" for help, usage instructions and examples.

Usage: scrape.py -s <startyear> -e <endyear>

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

Additional libraries required:

    requests
    bs4
    pandas

Scraped data is exported as a CSV file.