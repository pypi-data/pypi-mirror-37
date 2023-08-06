#!/bin/python

"""A download a video from arte.tv website."""

from bs4 import BeautifulSoup
from urllib.request import urlopen, unquote, urlretrieve
import re, json, sys

def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print("    "+sys.argv[0]+" <arte.tv_link>")
        print("Example:")
        print("    "+sys.argv[0]+" https://www.arte.tv/fr/videos/051868-000-A/liberte-egalite-indemnites-vers-un-revenu-universel/")
        sys.exit(0)

    url = sys.argv[1]

    content = urlopen(url)

    soup = BeautifulSoup(content, "lxml")

    iframes = soup.find_all("iframe")

    url = ""

    for iframe in iframes:
        url = unquote(iframe['src'])

    url = re.split("url=",url)[1]
    url = re.split("\?autostart", url)[0]

    content = urlopen(url)
    json_data = json.loads(content.read().decode())
    name = json_data['videoJsonPlayer']['VTI']
    url = json_data['videoJsonPlayer']['VSR']['HTTPS_SQ_1']['url']

    name=name.replace('/', '-')+".mp4"
    try:
        print("Downloading '"+name+"'...")
        urlretrieve(url, name)
        print("\nDownload completed")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
