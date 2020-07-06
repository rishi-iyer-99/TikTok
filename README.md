# TikTok

This is the code used to scrape TikTok daily and gather information about specifc sounds to track their growth through multiple metrics.  
The information is then used for promotional purposes, to show artists the potential growth and outreach possible if they paid famous TikTokers to make videos using their songs.  

The daily pipeline proceeds as follows:

 - `jawa_scrape.py`, scrapes the @ad_hok user page, building a .txt file containing the sound ids of all videos on the page
 - `tiktok.py`, takes the .txt file containing sound ids as inputs, and returns a json containing relevant data for all the sounds
 - `database.py`, reads the daily json as input and writes the data to a SQLite database
 - `flask_test.py`, a preliminary attempt at developing a website to display charts of certain metrics such as total plays and comments over time


