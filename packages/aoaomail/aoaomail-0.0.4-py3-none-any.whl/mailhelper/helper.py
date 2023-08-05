from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from email.header import Header
import smtplib


class MailHelper():
	def __init__(self,host,username,password):
		self.host = host
		self.username = username
		self.password = password

	def qq_sender(self,email_from, recipient, subject, message):
		message = MIMEText(message,'plain','utf-8')
		message['From'] = Header(email_from, 'utf-8')
		message['To'] = Header(recipient, 'utf-8')
		message['Subject'] = Header(subject, 'utf-8')

		try:
			server = smtplib.SMTP_SSL(smtp_server, 465)
			server.login(self.username, self.password)
			server.sendmail(email_from,recipient, message.as_string())
			server.quit()
		except smtplib.SMTPException:
			raise Exception("Email Send Failed")