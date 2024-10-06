import requests

class StarGrams:
    def __init__(self) -> None:
        self.session = requests.Session()
        pass
    
    

    def login(self, email: str, password: str):
        
        body_login = {
            "username": email,
            "password": password
        }
        resp = self.session.post('https://www.stargrams.app/api/login', data=body_login)

        data = resp.json()
        print(data)

        token = input("Enter 2FA: ")

        body_2fa = {
            "token": token
        }

        resp = self.session.post('https://www.stargrams.app/api/user/2fa/phone', data=body_2fa)


        data = resp.json()
        print(data)
        
        return


