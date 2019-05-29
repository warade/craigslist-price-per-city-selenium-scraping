# Introduction
To quote...
> As for desired requirements:
> 1. Generate a list of all the US Craigslist cities (https://www.craigslist.org/about/sites) and how much it costs to post a job ad. All cities have different prices for job posts, some are free. This might require some scraping. 

# How to use
1. Install the requirements.
```
pip3 install -r requirements.txt
```

2. You need to have your driver for browser. I used chromedriver, a chromedriver should be same as your chrome version.
List of chromedrivers - http://chromedriver.chromium.org/downloads you can download it from here and put it into assets/ folder.

3. You also need to have a list of URL for cities you want to find a price per job post. In this post all the US cities are extracted.

- Go to this site https://www.craigslist.org/about/sites
- Download the html page.
- Name it as a.html
- Open it in a editor and remove lines outside the US div, keep only <li> tags of US cities.
- Run the following code.
  
```
cat a.html | grep "href=" | cut -d'>' -f2 | cut -d'=' -f2 | tr -d '"' > input_cities.txt
```
- This will generate a input_cities.txt file which contains all the url for US cities.

3. Run the crawler.py file.
```
python3 crawler.py -d assets/chromedriver
```

4. Output file will be generated in output.txt

Note: other csv files in the folder are created using the final_output.txt. I already ran this on a server, and output is stored in final_output.txt. All the urls for US cities are in US_cities.txt. You have to mention URLs those you want to search price for in input_cities.txt and output will be in output.txt
