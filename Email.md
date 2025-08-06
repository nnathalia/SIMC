## EMAILS

### 🔧 **1. Pré-requisitos**

Antes de tudo, você precisa garantir algumas configurações para que o envio de e-mails funcione:

#### ✅ Configurar variáveis de ambiente:

No seu arquivo `.env` (ou onde você define suas variáveis de ambiente), adicione:

```env
EMAIL_HOST_USER=seuemail@gmail.com
EMAIL_TOKEN=sua_senha_de_aplicativo_ou_token
```

> ⚠️ Se você estiver usando Gmail, é necessário gerar uma **senha de app** em vez de usar sua senha normal, pois o Gmail não permite logins inseguros diretamente com senha.

---

#### ✅ Ativar o envio de e-mails no Gmail:

1. Acesse sua conta Google.
2. Ative a verificação em duas etapas.
3. Vá até **Segurança > Senhas de app**.
4. Gere uma senha para "Mail" com "Outro (nome personalizado)".
5. Use essa senha no lugar da `EMAIL_TOKEN`.

---

### ✉️ **Dicas importantes**

* Verifique sempre se o e-mail foi realmente enviado com sucesso (pode envolver tratamento de exceções).
* Evite colocar senhas diretamente no código.
* Nunca envie e-mails em ambientes de produção sem um sistema de monitoramento/log.
* Em produção, use serviços de envio de e-mail dedicados (ex: SendGrid, Amazon SES, etc.), se necessário.

---

