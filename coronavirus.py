#this code uses data from Google's own COVID map at
#https://google.com/covid19-map/?hl=en
#This data changes rapidly, so what’s shown may be out of date. Table totals may not always represent an accurate sum. Information about reported cases is also available on the World Health Organization site.

import subprocess
import sys
#use this install() function to pip-install modules
def install(package):
    subprocess.run([
        sys.executable, "-m", "pip", "-q", "install", package
    ])
install("bs4")


from urllib.request import urlopen
from bs4 import BeautifulSoup


m = str(urlopen("https://google.com/covid19-map/?hl=en").read())
page = BeautifulSoup(m,"html.parser")


lis = list(filter(lambda x:x.string!=None and "Updated" in x.string,page.find_all("div")))
print(lis[0].string)

#Parsing all the data
def parse(entry):
    region = entry.find_all("span")[0].string
    stats = list(map(lambda x:x.string,entry.find_all("td")))
    stats = [stats[1]]+stats[3:]
    return [region.string]+stats


data = page.find_all("tbody")[0]
entr = data.find_all("tr")
full_list = list(map(parse,entr))

print("-"*61)
print("|    Location     |  Confirmed  |  Recovered  |    Deaths   |")
print("-"*61)
for i in full_list:
    print(("|{:<17}"+"|{:<13}"*3+"|").format(*i))
print("-"*61)