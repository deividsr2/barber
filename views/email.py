import win32.client as win32

#integracao
outlook = win32.Dispatch('outlook.application')

#criar email
email = outlook.CreateItem(0)

#config
email.To = 'deividmib17@hotmail.com'
email.Subject = 'email python'
email.HTMLBody = """
olá mundo
"""

email.Send()