def decoder(url):
    
    try:
        import urllib
        decoded_url = urllib.unquote(url)
        decoded_url = urllib.unquote(decoded_url)
    except AttributeError:
        """working on while python 3.x"""
        import urllib.parse 
        decoded_url = urllib.parse.unquote(url)
        decoded_url = urllib.parse.unquote(decoded_url)
    return decoded_url  
