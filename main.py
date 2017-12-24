import sys
import datetime
import certstream

file = open('domains.txt', 'a+')
def print_callback(message, context):
	if message['message_type'] == "heartbeat":
		return
	if message['message_type'] == "certificate_update":
		all_domains = message['data']['leaf_cert']['all_domains']
		if len(all_domains) == 0:
			return
		for domain in all_domains:
			if len(domain.split('.')) != 2:
				return
			file.write(domain + '\n')
		

certstream.listen_for_events(print_callback)

