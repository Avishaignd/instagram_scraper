from scraper import Scraper 

# First we initialize the scraper with our username and password in case we need to login to instagram
scraper = Scraper()

# Then we use the get data function with the account we want to scrape
scraper.get_data()