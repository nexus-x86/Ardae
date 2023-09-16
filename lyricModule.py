from lyricsgenius import Genius

genius = Genius("WWQ6XEPsXOOYFVJmdQFwc3ibP9ugv_pQ1f6Lxp6WV_MX6rRZAIfPOk2pRuYR6Cvq")

def refine(lyrics):
    new = str(lyrics).lower()
    new.replace("\n", "")

    firstlineend = new.find("]") + 1
    new = new[firstlineend:len(new)]

    while new.find("[") != -1:
        open = new.find("[")
        close = new.find("]")
        
        new = new[0:open] + new[close+1:len(new)]
    return new

def songContains(song, key):
    lyrics = refine(str(genius.lyrics(song)))
    if(lyrics.find(key) != -1):
        return True
    else:
        return False