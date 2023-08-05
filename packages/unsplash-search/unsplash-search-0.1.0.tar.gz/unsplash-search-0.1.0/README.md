# unsplash-search

Unsplash-search is small python library to search for photos from the Unsplash photograph hosting website.

# Install

    pip install unsplash-search


# Usage

First and foremost, you must get an access key from the Unsplash Deverloper API website.

You must then instantiate the UnsplashSearch Class with your key to use the program.

    unsplash = UnsplashSearch(YOUR_KEY)

## Search using queries
The unsplash search method takes in a query as an argument for what kind of photos you
want to get.

If successful, it will return a random image dictionary.

    img = unsplash.search('mountains') #=> dict

The image dictionary object has two keys: The url of the image, and the author's instagram username.

So if you simply want to get a random image matching the query just do

    img['img']

