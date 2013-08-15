import fedmsg
from urlparse import urlparse
import requests
from os.path import basename
import os
from gi.repository import Notify, GLib

Notify.init("Fedora Badges")

image_url = urlparse("https://badges.fedoraproject.org/pngs/tagger-02.png")
f = open("badges/"+basename(image_url.path),'wb')
f.write(requests.get('https://badges.fedoraproject.org/pngs/tagger-02.png').content)
f.close()

config = fedmsg.config.load_config([], None)
config['mute'] = True
config['timeout'] = 0

for name, endpoint, topic, msg in fedmsg.tail_messages(**config):	
	if topic.find("fedbadges.badge.award") > 0:
		username = msg["msg"]["user"]["username"]
		badgename = msg["msg"]["badge"]["name"]
		image_url = msg["msg"]["badge"]["image_url"]
		filename = "badges/"+basename(urlparse(image_url).path)
		f = open(filename,'wb')
		f.write(requests.get(image_url).content)
		f.close()
		print username+ " got the "+badgename+" badge"
		Hello=Notify.Notification.new (username+ " got the "+badgename+" badge",msg["msg"]["badge"]["description"],os.getcwd()+"/icon.png")
		Notify.Notification.set_hint(Hello,"image-path", GLib.Variant.new_string(os.getcwd()+"/"+filename))
		Hello.show()
		
