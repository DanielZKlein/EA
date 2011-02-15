from datetime import datetime
import pprint

def dbug(text):
	pp = pprint.PrettyPrinter()
	fh = open("debuglog.txt", "a")
	now = datetime.now().strftime("%H:%M:%S")
	if isinstance(text, str) or isinstance(text, unicode):
		fh.write(now + " " + text + "\n")
	else:
		fh.write(now + ":\n" + pp.pformat(text) + "\n------------\n")
	fh.close()
	