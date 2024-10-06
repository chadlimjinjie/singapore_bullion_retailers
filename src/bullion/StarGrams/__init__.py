import requests
from requests import Session

class StarGrams:
    def __init__(self) -> None:
        self.session: Session = requests.Session()
        self.access_token: str = ''
        self.expires_in: int = ''
        self.refresh_token: str = ''
        self.token_type: str = ''
        # implement function to refresh token
        pass
    
    
    '''
    200 Response
    access_token: ""
    expires_in: 3600
    refresh_token: ""
    token_type: "Bearer"
    '''
    def login(self, email: str, password: str):
        '''
        
        '''
        body_login = {
            'username': email,
            'password': password
        }
        resp = self.session.post('https://www.stargrams.app/api/login', data=body_login)
        
        data = resp.json()
        print(data)
        
        self.access_token = data['access_token']
        return data

    def authenticate_2fa(self, token):
        '''
        
        '''
        # body_2fa = {
        #     "token": token
        # }

        # resp = self.session.post('https://www.stargrams.app/api/user/2fa/phone', data=body_2fa)
        # data = resp.json()
        # print(data)
        return
    
    def user(self):
        '''
        Use this API to get login user details.
        '''
        headers = {
            'Authorization': f'{self.token_type} {self.access_token}'
        }
        resp = self.session.post(f'https://www.stargrams.app/api/user')
        data = resp.json()
        
        # print(resp.status_code, data)
        
        return data



