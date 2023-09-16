from lyricsgenius import Genius

genius = Genius("WWQ6XEPsXOOYFVJmdQFwc3ibP9ugv_pQ1f6Lxp6WV_MX6rRZAIfPOk2pRuYR6Cvq")

def refine(lyrics):
    new = lyrics.lower()
    new.replace("[Chorus]", "")
    new.replace("[Refrain]", "")
    new.replace("[Bridge]", "")
    new.replace("[Post-Chorus]", "")
    new.replace("[Intro]", "")
    new.replace("[Verse ", "")

    return new

def songContains(song, key):
    lyrics = refine(genius.lyrics(song_url=song))
    if(lyrics.find(key) != -1):
        return True
    else:
        return False