#------------------------------------------webcrawler--------------------------------------------------------
#imports libraries
def get_page( url ):
    try:
        import urllib
        return urllib.urlopen( url ).read()
    except:
        return "" #everything is inserted in quotes
 
 
#looking at the "" (denotes URL) for next URL, tells you where to stop and move to the next url
def get_next_target( page ):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find( '"', start_link )
    end_quote = page.find('"', start_quote + 1)
    url = page[ start_quote + 1:end_quote ]
    return url, end_quote

    
#starts with empty list, appending url to end of page    
def get_all_links( page ):
    links = []
    while True:
        url, endpos = get_next_target( page )
        if url:
            links.append( url )
            page = page[ endpos: ]
        else:
            break
    return links

#
def union( a, b ):
    for e in b:
        if e not in a:
            a.append( e )

            
#uses dictionary structure; 
# basically a list thats structured like a hash table. easier to find text
#they have keys, which is set to some value, and thats how it searches
#index, key, and value compose a dictionary            
def crawl_web( seed ): # returns index, graph of inlinks
    tocrawl = [ seed ]
    crawled = []
    graph = {}  # <url>, [list of pages it links to]
    index = {}
    while tocrawl:
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page( page )
            add_page_to_index( index, page, content )
            graph[ page ] = get_all_links( content )
            union(tocrawl, get_all_links( content ))
            crawled.append( page )
    return index, graph

#--------------------------------------------------Indexing---------------------------------------------------------
# adds page to index, takes a string object, makes its into bunch of substrings, and manipulation is easier
# adds the specific url to index
def add_page_to_index( index, url, content ):
    words = content.split()
    for word in words:
        add_to_index( index, word, url )


# adds the keyword off that url
def add_to_index( index, keyword, url ):
    if keyword in index:
        index[ keyword ].append( url )
    else:
        index[ keyword ] = [ url ]
        
        
#looks for keyword youre looking for
def lookup( index, keyword ):
    if keyword in index:
       return index[ keyword ]
    else:
        return None

#--------------------------------------------------------------Ranking------------------------------------------   
#algorithm
#page rank algorithm 
def compute_ranks( graph ):
    d = 0.8 # damping factor
    q = 10

    ranks = {}
    npages = len( graph )
    for page in graph:
        ranks[ page ] = 1.0 / npages

    for i in range(0, q):
        newranks = {}
        for page in graph:
            newrank = ( 1 - d ) / npages
            for node in graph:
                if page in graph[ node ]:
                    newrank = newrank + d * ( ranks[ node ] / len( graph[ node ] ) )
            newranks[ page ] = newrank
        ranks = newranks
    return ranks

    
#recursive algorithm    
# O(n^2) runtime
def quick_sort( url_lst,ranks ):
    url_sorted_worse=[]
    url_sorted_better=[]
    if len( url_lst )<=1:
        return url_lst
    pivot=url_lst[ 0 ]
    for url in url_lst[ 1: ]:
        if ranks[ url ]<=ranks[ pivot ]:
            url_sorted_worse.append( url )
        else:
            url_sorted_better.append( url )
    return quick_sort( url_sorted_better,ranks )+[ pivot ]+quick_sort( url_sorted_worse,ranks )

#orders by index        
def ordered_search( index, ranks, keyword ):
    if keyword in index:
        all_urls=index[keyword]
    else:
        return None
    return quick_sort(all_urls,ranks)

#------------------------------------------------------Test-----------------------------------------------
#test    
kword = raw_input("Enter Keyword: ")
index, graph = crawl_web( 'https://developers.openshift.com/en/getting-started-overview.html' )
ranks = compute_ranks( graph )
print ordered_search( index, ranks, kword )
