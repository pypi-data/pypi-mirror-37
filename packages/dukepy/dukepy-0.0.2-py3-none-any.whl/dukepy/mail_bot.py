import win32com.client
import pythoncom


class Handler_Class(object):
	def OnNewMailEx(self, receivedItemsIDs):
		for ID in receivedItemsIDs.split(","):
			# Microsoft.Office.Interop.Outlook _MailItem properties:
			# https://msdn.microsoft.com/en-us/library/microsoft.office.interop.outlook._mailitem_properties.aspx
			mailItem = MailBot.outlookHandled.Session.GetItemFromID(ID)
			print "Subj: " + mailItem.Subject
			print "Body: " + mailItem.Body.encode('ascii', 'ignore')
			print "========"


class MailBot():
	outlookHandled = win32com.client.DispatchWithEvents("Outlook.Application", Handler_Class)

	def __init__(self):
		self.outlook = win32com.client.Dispatch(
			"Outlook.Application")  # https://msdn.microsoft.com/en-us/vba/outlook-vba/articles/application-object-outlook#
		self.application = self.outlook.Application
		self.namespace = self.application.GetNamespace("MAPI")
		self.inbox = self.namespace.GetDefaultFolder(6)

	def eval(self, object, param):
		res = None
		try:
			res = eval("object.%s" % (param))
		except AttributeError as e:
			pass

		return res

	def BuildMailItem(self, message):
		resItem = dict()
		resItem["message"] = message
		resItem["Subject"] = self.eval(message, "Subject")
		resItem["Body"] = self.eval(message, "Body")
		resItem["HTMLBody"] = self.eval(message, "HTMLBody")
		resItem["Importance"] = self.eval(message, "Importance")
		resItem["Recipients"] = self.eval(message, "Recipients")
		resItem["Sender"] = self.eval(message, "Sender")
		resItem["To"] = self.eval(message, "To")
		resItem["CC"] = self.eval(message, "CC")
		resItem["BCC"] = self.eval(message, "BCC")
		resItem["SenderEmailAddress"] = self.eval(message, "SenderEmailAddress")
		resItem["SenderName"] = self.eval(message, "SenderName")
		resItem["SentOn"] = self.eval(message, "SentOn")
		resItem["Size"] = self.eval(message, "Size")
		resItem["UnRead"] = self.eval(message, "UnRead")
		resItem["VotingOption"] = self.eval(message, "VotingOption")
		resItem["VotingResponse"] = self.eval(message, "VotingResponse")
		resItem["Attachments"] = self.eval(message, "Attachments")
		return resItem

	def GetAllMails(self):
		"""
		# Reference: https://stackoverflow.com/questions/22813814/clearly-documented-reading-of-emails-functionality-with-python-win32com-outlook
		:return: all the mails in the inbox
		"""
		messages = self.inbox.Items

		res = []
		for message in messages:
			resItem = self.BuildMailItem(message)
			res.append(resItem)
		return res

	def GetLastMail(self):
		message = self.inbox.Items.GetLast()
		res = self.BuildMailItem(message)
		return res

	def GetAllFolders(self):
		for i in range(50):
			try:
				box = self.namespace.GetDefaultFolder(i)
				name = box.Name
				print(i, name)
			except:
				pass

	def Search(self, query):
		strF = "urn:schemas:mailheader:subject = '%s'" % (query)
		strS = "Inbox"
		results = self.application.AdvancedSearch(strS, strF).Results
		for result in [results.Item(i) for i in range(1, results.Count)]:
			print(result)
		return results

	def SendMail(self, mail=None, To=None, CC=None, BCC=None, Subject=None,
				 Body=None, Attachments=None,
				 draft=True):
		"""
		Reference: https://stackoverflow.com/questions/17449184/sending-outlook-email-with-body-as-contents-of-a-text-file
		:param mail: Mail object to reply to.
		:param BCC:
		:param CC:
		:param Attachments: List of attachments
		:param To:
		:param Subject:
		:param Body:
		:param draft: Set it to false if the mail is to be sent automatically.
		:return:
		"""
		if mail is None:
			mail = self.application.CreateItem(0)

		if To is None:
			To = ["user@user.com", "user2@user.com"]
		if Attachments is None:
			Attachments = []

		if To:
			for toItem in To:
				recipient = mail.Recipients.Add(toItem)
				recipient.Type = 1
		if CC:
			for ccItem in CC:
				recipient = mail.Recipients.Add(ccItem)
				recipient.Type = 2
		if BCC:
			for bccItem in BCC:
				recipient = mail.Recipients.Add(bccItem)
				recipient.Type = 3
		if Subject:
			mail.Subject = Subject
		if Body:
			mail.Body = Body
		if Attachments:
			for attachment in Attachments:
				mail.Attachments.Add(attachment)
		if draft:
			mail.Display()
		else:
			mail.Send()

	def ReplyToMail(self, mail, replyToAll=False, To=None, CC=None, BCC=None,
					Body=None, Attachments=None,
					draft=True):
		"""
		:param mail: Mail object to reply to.
		:param BCC:
		:param CC:
		:param Attachments: List of attachments
		:param To:
		:param Body:
		:param draft: Set it to false if the mail is to be sent automatically.
		:return:
		"""
		if replyToAll:
			newMail = mail.ReplyAll()
		else:
			newMail = mail.Reply()
		Body = Body + "\n" + newMail.Body
		self.SendMail(newMail, To=To, CC=CC, BCC=BCC, Body=Body, Attachments=Attachments, draft=draft)

	def ForwardMail(self, mail, To=None, CC=None, BCC=None,
					Body=None, Attachments=None,
					draft=True):
		"""
		:param mail: Mail object to be forwarded
		:param BCC:
		:param CC:
		:param Attachments: List of attachments
		:param To:
		:param Body:
		:param draft: Set it to false if the mail is to be sent automatically.
		:return:
		"""
		newMail = mail.Forward()
		Body = Body + "\n" + newMail.Body
		self.SendMail(newMail, To=To, CC=CC, BCC=BCC, Body=Body, Attachments=Attachments, draft=draft)

	def SwitchUnread(self, mail):
		if mail.UnRead == True:
			mail.UnRead = False
		else:
			mail.UnRead = True


if __name__ == "__main__":
	last = MailBot().GetLastMail()
	# MailBot().SendMail(
	# 	Subject="Test mail",
	# 	Body="This is the test body.\n \ncan go multiline",
	# 	To=["xyz@abc.com", "xyz@abc.com"],
	# 	CC=["xyz@abc.com", "xyz@abc.com"],
	# 	BCC=["xyz@abc.com", "xyz@abc.com"],
	# 	Attachments=["D:\xyz\abc\foo.txt"]
	# )

	MailBot().ReplyToMail(
		mail=last["message"],
		# replyToAll=True,
		Body="This is the test body.\n \ncan go multiline",
		To=["xyz@abc.com", "xyz@abc.com"],
		CC=["xyz@abc.com", "xyz@abc.com"],
		BCC=["xyz@abc.com", "xyz@abc.com"],
		Attachments=["D:\xyz\abc\foo.txt"]
	)

	# MailBot().ForwardMail(
	# 	mail=last["message"],
	# 	Body="This is the test body.\n \ncan go multiline",
	# 	To=["xyz@abc.com", "xyz@abc.com"],
	# 	CC=["xyz@abc.com", "xyz@abc.com"],
	# 	BCC=["xyz@abc.com", "xyz@abc.com"],
	# 	Attachments=["D:\xyz\abc\foo.py"]
	# )

	# search = MailBot().Search("Test")
	# folders = MailBot().GetAllFolders()
	# mails = MailBot().GetAllMails()
	pass
