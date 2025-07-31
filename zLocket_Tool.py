import requests

class zLocket:
    API_LOCKET_URL = "https://api.locket.com/v1"  # Sửa URL này lại nếu bạn dùng endpoint khác!

    def __init__(self, target_friend_uid=None):
        self.target_friend_uid = target_friend_uid

    def headers_locket(self):
        return {
            "Content-Type": "application/json",
            # Thêm các headers khác nếu cần (Authorization, Cookie...)
        }

    def excute(self, url, headers, payload, proxies_dict):
        try:
            res = requests.post(url, headers=headers, json=payload, proxies=proxies_dict, timeout=10)
            if res.ok:
                return res.json()
            else:
                return None
        except Exception as e:
            return None

def format_proxy(proxy_str):
    return {
        "http": f"http://{proxy_str}",
        "https": f"http://{proxy_str}"
    }
