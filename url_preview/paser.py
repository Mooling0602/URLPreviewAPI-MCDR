import requests
from bs4 import BeautifulSoup
from typing import Optional
from urllib.parse import urlparse
import socket
import ipaddress


# 最大响应体大小（字节），例如 5MB
MAX_BYTES = 5 * 1024 * 1024

def is_private_hostname(hostname: str) -> bool:
    # 移除可能存在的协议前缀
    if hostname.startswith("http://"):
        hostname = hostname[7:]
    elif hostname.startswith("https://"):
        hostname = hostname[8:]
    # 去掉可能附带的路径，只保留域名部分
    hostname = hostname.split('/')[0]
    
    try:
        infos = socket.getaddrinfo(hostname, None)
        # 收集所有解析得到的 IP 地址
        resolved_ips = {sockaddr[0] for _, _, _, _, sockaddr in infos}
        # 如果所有解析到的 IP 都属于内部地址，则认为此主机名为内部地址
        for ip in resolved_ips:
            ip_obj = ipaddress.ip_address(ip)
            if not (ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved or ip_obj.is_link_local):
                return False
        return True
    except socket.gaierror:
        # DNS 解析失败则返回 True，提示存在风险
        return True
    except Exception:
        return True

def parse_url_info(url: str, locale: Optional[str] = None):
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ['http', 'https']:
        return {'error': 'URL scheme must be http or https!'}
    if not parsed_url.hostname or is_private_hostname(parsed_url.hostname):
        return {'error': 'Access to internal network resources or invalid hostname is forbidden!'}

    try:
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
            )
        }
        if locale:
            headers['Accept-Language'] = locale

        # 启用流式请求，避免一次性加载全部内容
        response = requests.get(url, headers=headers, stream=True, timeout=10)
        response.raise_for_status()

        # 检查响应头中的 Content-Length 是否超过限制
        if 'Content-Length' in response.headers:
            if int(response.headers['Content-Length']) > MAX_BYTES:
                return {'error': 'Content length too long!'}

        # 分块读取响应内容，防止 OOM
        content = b""
        for chunk in response.iter_content(chunk_size=1024):
            content += chunk
            if len(content) > MAX_BYTES:
                return {'error': 'Content length too long!'}
        html_text = content.decode('utf-8', errors='replace')

        soup = BeautifulSoup(html_text, 'html.parser')
        title = soup.title.string.strip() if soup.title and soup.title.string else None

        summary = ''
        meta_desc = soup.find('meta', attrs={'name': 'description', 'lang': 'zh-CN'})
        if not meta_desc:
            meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            summary = meta_desc.get('content').strip()
        else:
            paragraphs = soup.find_all('p')
            chinese_text = []
            for p in paragraphs[:5]:
                text = p.get_text().strip()
                if any('\u4e00' <= c <= '\u9fff' for c in text):
                    chinese_text.append(text)
                    if len(chinese_text) >= 2:
                        break
            summary = (' '.join(chinese_text)[:200] + '...')

        return {'title': title, 'summary': summary}

    except requests.exceptions.RequestException:
        return {'error': 'Failed to request!'}
    except Exception:
        return {'error': 'Failed to parse!'}
