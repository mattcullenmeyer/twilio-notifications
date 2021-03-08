import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from twilio.rest import Client
import os


# SendGrid account info
api_key = os.environ.get('SENDGRID_API_KEY')
sg = sendgrid.SendGridAPIClient(api_key=api_key)

# Twilio account info
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

# Dummy data of new positions
new_positions = [
    ['#1', 'Financial Analyst', 'Finance'],
    ['#2', 'Data Analyst', 'Business Intelligence'],
    ['#3', 'Staff Accountant', 'Accounting'],
]


''' SEND EMAIL VIA SENDGRID AND SMS VIA TWILIO '''

# Sender's email
sender_email = 'me@example.com'

# List of addresses to send Email
email_addresses = ['you@example.com',]

# Sender's number (provided through Twilio)
sender_number = '+12345678910'

# List of numbers to send SMS
phone_numbers = ['+19999999999',]

# Subject line of Email
subject = 'New positions were approved for recruiting in Anaplan'

# Body of Email message
body = '''<p>The following positions were recently approved for recruiting in Anaplan. 
    Please add these Unique IDs to Greenhouse when creating the new jobs.</p><p></p>'''
    
# Table header for new positions
html_table = '''
    <table style="border: 1px solid #ddd;text-align: left;border-collapse: collapse;">
    <tr>
      <th style="border: 1px solid #ddd;text-align: left;padding: 15px;">Unique ID</th>
      <th style="border: 1px solid #ddd;text-align: left;padding: 15px;">Position Title</th>
      <th style="border: 1px solid #ddd;text-align: left;padding: 15px;">Department</th>
    </tr>'''
    
# Function to generate row for each position in table
def update_table(i, unique_id, title, department):
	# Alternate background color of rows for legibility    
	if i % 2 != 0:
    		return '''
    		<tr>
    			<td style="border: 1px solid #ddd;text-align: left;padding: 15px; 
                background-color: #f2f2f2">{}</td>
    			<td style="border: 1px solid #ddd;text-align: left;padding: 15px; 
                background-color: #f2f2f2">{}</td>
    			<td style="border: 1px solid #ddd;text-align: left;padding: 15px; 
                background-color: #f2f2f2">{}</td>
    		</tr>'''.format(unique_id, title, department)
	else:
    		return '''
    		<tr>
    			<td style="border: 1px solid #ddd;text-align: left;padding: 15px;">{}</td>
    			<td style="border: 1px solid #ddd;text-align: left;padding: 15px;">{}</td>
    			<td style="border: 1px solid #ddd;text-align: left;padding: 15px;">{}</td>
    		</tr>'''.format(unique_id, title, department)

i = 0
for unique_id, title, department in new_positions:
    html_table += update_table(i, unique_id, title, department)
    i += 1

html_table += '</table>'

end = '<p></p><p></p><em>* This email notification was sent to all recruiters & HRBPs.</em>' 
    
content = Content('text/html', body + html_table + end)
    
# Send emails via SendGrid
for email_address in email_addresses:
    from_email = Email(sender_email)
    to_email = To(email_address)
    mail = Mail(from_email, to_email, subject, content)
    mail_json = mail.get()
    response = sg.client.mail.send.post(request_body=mail_json)
    print(response.status_code)

# Function for creating text message body
def create_sms(new_positions):
	text_body = ''
	for unique_id, title, _ in new_positions:
		text_body += unique_id + ' | ' + title + '\n'
	return text_body

# Create text message content
sms_text = subject + '\n' + create_sms(new_positions)

# Send SMS via Twilio
for phone_number in phone_numbers:
    message = client.messages.create(
        	body=sms_text,
        	from_= sender_number,
        	to=phone_number
    )
    print(message.sid)
