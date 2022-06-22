# Farfetch_crawler
This programs is designed to crawling data automatically from Farfetch using Selenium. Note that since it visits components by X-path, if the grammer of the x-path is changed, you have to modify the x-path in the codes.

## Farfetch.com
![image](https://user-images.githubusercontent.com/89527573/175085281-6f88eaa7-213c-48b1-ae2b-097c089d2d7c.png)
![image](https://user-images.githubusercontent.com/89527573/175086146-48efbf4c-1235-4153-813f-b0b412b1c49e.png)


### main.py
  Gather the price, brand, item name, img url, and item attributes url.


### img_save
save images from saved image urls.

### item_properties
save item attributes from saved urls.


### Data
---
![image](https://user-images.githubusercontent.com/89527573/175087068-3a5bb9bc-b63e-4fc3-91f3-ef43c8e81be2.png)
##### Item attributes & Composition
by running item_properties.py
###### ['aged black ', 'cotton blend ', 'skinny cut ', 'ripped detailing ', 'paint splatter detail ', 'mid-rise ', 'belt loops ', 'front button fastening ', 'classic five pockets ']
###### Cotton 92%, Polyester 6%, Spandex/Elastane 2%
