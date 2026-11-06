# Order completion email notifications

When staff changes an order to **Completed**, XeroEasy emails the student once for that transition. Changing an already-completed order to **Completed** again does not send another message. The staff dashboard reports whether the email was sent, SMTP is not configured, or delivery failed.

Configure the SMTP server in the environment that starts Flask:

| Variable | Purpose | Default |
| --- | --- | --- |
| `XEROEASY_SMTP_HOST` | SMTP server hostname | unset |
| `XEROEASY_SMTP_PORT` | SMTP server port | `587` |
| `XEROEASY_SMTP_FROM` | Sender email address | unset |
| `XEROEASY_SMTP_USERNAME` | SMTP username; optional | unset |
| `XEROEASY_SMTP_PASSWORD` | SMTP password; optional, required with username | unset |
| `XEROEASY_SMTP_USE_TLS` | Use STARTTLS | `true` |
| `XEROEASY_SMTP_USE_SSL` | Use implicit SSL, e.g. port 465 | `false` |

For example, set these in PowerShell before starting the app (replace the example values with your mail provider's settings):

```powershell
$env:XEROEASY_SMTP_HOST = "smtp.example.com"
$env:XEROEASY_SMTP_PORT = "587"
$env:XEROEASY_SMTP_FROM = "xerox@example.com"
$env:XEROEASY_SMTP_USERNAME = "xerox@example.com"
$env:XEROEASY_SMTP_PASSWORD = "your-provider-issued-app-password"
$env:XEROEASY_SMTP_USE_TLS = "true"
$env:XEROEASY_SMTP_USE_SSL = "false"
& ".\venv\Scripts\python.exe" ".\app.py"
```

Use the SMTP credentials or app password issued by your email provider. Do not commit real credentials to the project. Restart Flask after changing environment variables.
