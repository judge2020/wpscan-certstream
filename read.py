import os
import sys
import subprocess
import requests
import re
from random import randint

def check(blabla):
        datafile = open('scanned.txt', 'r')
        found = False #this isn't really necessary 
        for line in datafile:
            if blabla in line:
                #found = True #not necessary 
                return True
        return False #because you finished the search without finding anything

def is_wpscan3():
	process = subprocess.Popen(['wpscan', '-v'], stdout=subprocess.PIPE)
	out, err = process.communicate()
	return 'v3' in out

def random_agent():
	with open('user-agents.txt','r') as f:
		uas = f.read()
		uas = re.sub("#.*","", uas)
		uas = uas.replace("\n\n","")
		uas = uas.split('\n')
	random = randint(0, 40)
	return uas[random]

def is_wordpress(url):
	url = 'http://' + url
	try:
		d = requests.get(url, headers={"User-Agent":random_agent()}, timeout=10)
		return 'wp-' in d.text
	except Exception as e:
		print(str(e))
		return False

def write_is_interesting(url):
	interestingfile = open('interesting.txt', 'a+')
	interestingfile.write(url + '\n')
	interestingfile.close()

def do_main():
	file = open('domains.txt', 'r')
	fwrite = open('scanned.txt', 'a+')
	alreadyscanned = 0
	for line in file:
		line = line.replace('\n', '')
		fwrite.write(line + '\n')
		if check(line):
			alreadyscanned += 1
			continue
		print('Scanning %s' % line)
		print('Already scanned %s hosts' % alreadyscanned)
		if is_wordpress(line):
			print('Website most likely is wordpress: %s' % line)
			write_is_interesting(line)
			os.system('wpscan --random-agent --follow-redirection --update --url ' + line)
			return 0
		else:
			print('Website most likely is not wordpress.')
			return 2

def main():
	if do_main() == 2:
		main()
	else:
		os._exit(0)
if __name__ == "__main__":
	main()
