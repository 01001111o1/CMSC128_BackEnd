def request_approved_template(name, queue_number):
	content = f'Hello {name}, <br><br> Your request with order number {queue_number} has been approved.'
	return content

def documents_approved_template(name, queue_number):
	content = f'Hello {name}, <br><br> The documents you submitted for order number {queue_number} has been verified and approved.'
	return content

def documents_available_template(name, queue_number):
	content = f'Hello {name}, <br><br> The documents you requested for order number {queue_number} is available for claiming. Please proceed to the OUR to claim it'
	return content
#NOTE: CONTENT CAN BE FORMATTED USING HTML!