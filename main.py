from scraper import Scraper 

# First we initialize the scraper with our username and password in case we need to login to instagram
scraper = Scraper('example@example.com', '123456')

# Then we use the get data function with the account we want to scrape and number of posts
scraper.get_data('some-IG-account', 10)