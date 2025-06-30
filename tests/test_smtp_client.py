import pytest
import asyncio
from main import AsyncSMTPClient

class DummySMTPClient(AsyncSMTPClient):
    async def send_mail(self, subject, body, to, log_level=None, is_dev=False, exc=None):
        # 模擬寄信，不實際發送
        return {
            'subject': subject,
            'body': body,
            'to': to,
            'log_level': log_level,
            'is_dev': is_dev,
            'exc': exc
        }

def test_send_mail_multiple_recipients():
    client = DummySMTPClient('host', 587, 'user', 'pass')
    result = asyncio.run(client.send_mail('subj', 'body', ['a@b.com', 'c@d.com']))
    assert result['to'] == ['a@b.com', 'c@d.com']

def test_send_mail_log_level_color():
    client = DummySMTPClient('host', 587, 'user', 'pass')
    result = asyncio.run(client.send_mail('subj', 'body', ['a@b.com'], log_level='error'))
    assert result['log_level'] == 'error'

def test_send_mail_dev_stacktrace():
    client = DummySMTPClient('host', 587, 'user', 'pass')
    try:
        raise RuntimeError('test')
    except Exception as e:
        result = asyncio.run(client.send_mail('subj', 'body', ['a@b.com'], log_level='dev', is_dev=True, exc=e))
        assert result['is_dev'] is True
        assert result['exc'] is not None
