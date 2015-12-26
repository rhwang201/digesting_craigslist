#!/usr/bin/python

import requests
root_url = 'http://sfbay.craigslist.org'
url = root_url + '/search/sfc/zip?postedToday=1&search_distance_type=mi&nh=4&nh=18&nh=25&nh=1'
response = requests.get(url)


from bs4 import BeautifulSoup as bs
soup = bs(response.text)


content = soup.find(class_='content')
listings = content.find_all('p')


location_listings = {}

for l in listings:
    link = root_url + l.a['href']
    title = l.find(class_='pl').a.text
    location = l.find(class_='l2').small.text

    ll = (link, title)

    if location not in location_listings:
        location_listings[location] = [ll]
    else:
        location_listings[location].append(ll)


from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

f = open('/Users/richardhuang/sandbox/email_digest/email.txt')
username = f.readline().strip()
password = f.readline().strip()


msg = MIMEMultipart('alternative')
msg['Subject'] = "SF Craigslist Free Digest"
msg['From'] = username
msg['To'] = username

text = ''

from html import HTML
h = HTML()

with h.ul as l:
    for location, listings in location_listings.iteritems():
        l.h2(location.strip().strip('()').title())
        text += location.strip('()').title() + '\n'

        for pair in listings:
            link, title = pair
            with l.li as li:
                l.a(title, href=link) 
                text += title + ' ' + link + '\n'

html = str(h)

part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

msg.attach(part1)
msg.attach(part2)


import smtplib
server = smtplib.SMTP('smtp.gmail.com:587')
server.starttls()
server.login(username,password)
server.sendmail(username, username, msg.as_string())
server.quit()
