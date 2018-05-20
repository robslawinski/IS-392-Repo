from threading import Thread
    import urllib.request
    import urllib.error
    from bs4 import BeautifulSoup
    import time
seedUrls =  ['https://en.wikipedia.org/wiki/Steve_Jobs','https://en.wikipedia.org/wiki/Apple_Inc.']
relWords = ['apple', 'steve jobs', 'ipod', 'ipad', 'iphone', 'steve wozniak', 'pixar', 'mac', 'macbook', 'siri']
def linkCrawler(seed_url, wordlist):
    crawl_queue = list(seed_url)
    total = 0
    # keep track which URL's have seen before
    seen = list(crawl_queue)
        #keep crawling until you hit at least 500, and write links to crawl_queue.text
        #retrieve first link in queue and save to url
    while crawl_queue:
        if total > 500:
            with open("crawl_queue.txt", 'w') as f:
                f.write(crawl_queue)
            break
        url = crawl_queue.pop(0)
        html = download(url)
       
        if pageCheck(wordlist, html):
            savePage(url, html)
            total +=1
        for href in get_links(html):
            try:
                if href.find('/wiki/') == 0 and href.find('/File:') == -1:
                    link = "https://en.wikipedia.org"+href
                    if link not in seen and link.find("#") == -1:
                        seen.append(link)
                        crawl_queue.append(link)

            except Exception as e:
                print (e)
def pageCheck(word,text):
    soup = BeautifulSoup(text,"lxml")
    stoup = soup.get_text().lower()
    relCount = 0
    for x in word:
        x = x.lower()
        if x in stoup.lower():
            relCount += 1
        if relCount >=2:
            return True
        return False
def download(url, numRetries=2):
    time.sleep(1)
    print ('Downloading:', url)
    with open("crawled_pages.txt", 'a+') as fil:
        fil.write(url+"\n")
    try:
        html = urlopen(url).read()
    except urllib.error.URLError as e:
        print ('Download error:', e.reason)
        html = None
        if numRetries > 0:
            if hasattr(e, 'code') and 500 <= e.code < 600:
                # retry 5XX HTTP errors
                html = download(url, numRetries-1)
    return html
def savePage(url, text):
    name = url[url.rfind("/"):]
    with open("websites/"+name+".html", 'w+') as file:
        file.write(text)
    file.closed
    with open("crawled_pages.txt", 'a+') as tile:
        tile.write(url+"\n")
    tile.closed
def get_links(html):
    try:
        soup = BeautifulSoup(html,"lxml")
        return [link.get('href') for link in soup.find_all('a') ]
    except Exception as e:
        print (e)