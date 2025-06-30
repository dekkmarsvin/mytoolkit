import asyncio
import traceback
from email.message import EmailMessage
from typing import List, Optional
import aiosmtplib

LOG_LEVELS = {
    'dev': {'color': '#e0e0e0'},
    'info': {'color': '#d9edf7'},
    'warn': {'color': '#fcf8e3'},
    'error': {'color': '#f2dede'},
    'critical': {'color': '#f44336'},
}

class AsyncSMTPClient:
    """
    非同步 SMTP client，支援多收件人與 log level 標示顏色。
    """
    def __init__(self, host: str, port: int, username: Optional[str] = None, password: Optional[str] = None, use_tls: bool = True):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.service_name = 'RCSA'  # 可根據需要修改服務名稱

    async def send_mail(self, subject: str, body: str, to: List[str], log_level: Optional[str] = None, is_dev: bool = False, exc: Optional[Exception] = None):
        msg = EmailMessage()
        msg["From"] = self.username if self.username else "noreply@example.com"
        msg["To"] = ', '.join(to)
        msg["Subject"] = subject
        html_body = self._format_body(body, log_level, is_dev, exc)
        msg.set_content(body)
        msg.add_alternative(html_body, subtype='html')
        smtp_kwargs = {
            'hostname': self.host,
            'port': self.port,
            'start_tls': self.use_tls
        }
        if self.username:
            smtp_kwargs['username'] = self.username
        if self.password:
            smtp_kwargs['password'] = self.password
        try:
            await aiosmtplib.send(
                msg,
                **smtp_kwargs
            )
        except Exception as e:
            # SMTP 連線異常時開啟 debuglevel 並捕捉詳細錯誤
            import sys
            from aiosmtplib import SMTP
            smtp = SMTP(**smtp_kwargs)
            try:
                await smtp.connect()
                await smtp.send_message(msg)
            except Exception as debug_exc:
                print("SMTP debug error:", debug_exc, file=sys.stderr)
                raise debug_exc from e
            finally:
                await smtp.quit()

    def _format_body(self, body: str, log_level: Optional[str], is_dev: bool, exc: Optional[Exception]) -> str:
        import datetime
        color = LOG_LEVELS.get(log_level or '', {}).get('color', '#ffffff')
        html = f'<div style="background-color:{color};padding:16px;">'
        html += f'<p>{body}</p>'
        if is_dev and exc:
            stack = traceback.format_exception(type(exc), exc, exc.__traceback__)
            html += '<pre style="color:#333;background:#fafafa;border:1px solid #ccc;padding:8px;">'
            html += ''.join(stack)
            html += '</pre>'
        now = datetime.datetime.now().strftime('%Y%m%d %H%M%S')
        html += f'<div style="font-size:12px;color:#888;margin-top:16px;">此郵件為{self.service_name}服務自動發送 {now}</div>'
        html += '</div>'
        return html

# 範例用法
async def main():
    client = AsyncSMTPClient(
        host='smtp.example.com',
        port=587,
        username='your@email.com',
        password='yourpassword',
        use_tls=True
    )
    try:
        await client.send_mail(
            subject='測試信件',
            body='這是一封測試信件',
            to=['to1@example.com', 'to2@example.com'],
            log_level='warn',
            is_dev=True,
            exc=ValueError('測試錯誤')
        )
    except Exception as e:
        print('寄信失敗:', e)

if __name__ == "__main__":
    asyncio.run(main())
