import requests

class JWCClient:
    """
    教务系统客户端：封装登录和抓取 HTML
    """
    def __init__(self, username:str, password: str):
        self.username:str = username
        self.password:str = password
        self.session:requests.Session = requests.Session()
        self.logged_in:bool = False
        
    def login(self) -> bool:
        """
        登录教务系统，保存 session
        """
        
        
        return True