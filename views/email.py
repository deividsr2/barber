import win32com.client

try:
    outlook = win32com.client.Dispatch("Outlook.Application")
    email = outlook.CreateItem(0)
    email.To = "deividsr.rodrigues@gmail.com"  # Altere para um e-mail válido de teste
    email.Subject = "Teste de Envio de E-mail via Outlook"
    email.Body = "Este é um e-mail de teste enviado via Python e Outlook."
    email.Send()
    print("✅ E-mail enviado com sucesso!")
except Exception as e:
    print(f"❌ Erro ao enviar e-mail: {e}")
