import sys

sys.path.insert(0, '/home/pi/server/wakerspace')

activate_this = '/home/pi/server/env/bin/activate_this.py'
with open(activate_this) as file_:
	exec(file_.read(), dict(__file__=activate_this))

from wakerspace import app as application

