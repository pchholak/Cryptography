def get_page_source(url):
    from urllib.request import urlopen
    with urlopen(url) as f:
        html = f.read().decode('utf8')
    return html

def open_url(url):
    import webbrowser
    webbrowser.open_new_tab(url)
    return None

def write_string_to_txt(string, fname):
    # Previously known as write_html_to_txt(html, fname)
    file = open(fname, "w")
    file.write(string)
    file.close()
    return None

def read_txt_file(fname):
    file = open(fname, "r")
    chars = file.read()
    return chars

def get_page_source_object(url):
    from urllib.request import urlopen
    html_object = urlopen(url)
    return html_object
