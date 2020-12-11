# GSMLS Parser

**GSMLS** is a great place to find properties, often before they are posted on other real estate websites.

Unfortunately, the website is not user friendly.
There is no easy way of determining which listings are new and which were removed since your last visit.
There is no way to save properties.

This is my way around those short comings.

**V1** was a simple script that took command line arguments.
Data was parsed naively by using selenium to navigate the GSMLS website and scrape property data.
Properties were stored in Property objects, and serialized using Pickle.
When the script was executed, previously viewed Properties were unpickled.
Data was parsed and compared to previously viewed properties to identify new or removed listings and price changes

**V2** Rebuild has begun.
I am working to reverse engineer the API in order to fetch raw data.
For now, I am making requests to a single endpoint with query data.  The response is the HTML string which is parsed for data.
TO DO:
* Implement database to store previously viewed properties.
Choices:
    * SQLite - easy queries, minimal in-app storage utilization
    * CSV - human readable
* Pull photos
* Generate reports
* Analyze previous sale data
