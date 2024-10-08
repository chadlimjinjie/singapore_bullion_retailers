# import requests
from requests import Session
'''
<form action="/Account/Login" class="login-form" method="post"><input name="__RequestVerificationToken" type="hidden" value="qwU6mmU8Ja_MZE0x0xaeDW0Ezbbz3CIBYraW_E6bg6V2aFSxmfWW89QyKNY8YL5MAlI8-xaSAP29KuFtIP1Reqe96jo1" /><input id="CaptchaToken" name="CaptchaToken" type="hidden" value="" />                        <div class="form-group">
                            <input class="form-control" id="inputEmail3" name="UsernameEmail" placeholder="Username or e-mail" type="text" value="" />
                        </div>
                        <div class="form-group">
                            <input class="form-control" id="inputPassword3" name="Password" placeholder="Password" type="password" value="" />
                        </div>
                        <div class="form-group">
                            <div class="checkbox">
                                <span class="forgot_pwd">
                                    <a href="/Password/Forgot">Forgot your password?</a>
                                </span>
                            </div>
                        </div>
                        <div class="form-group">
                            <button type="submit" class="btn btn-primary">Log in</button>
                        </div>
</form>
https://www.silverbullion.com.sg/Account/Login
__RequestVerificationToken: PuXNCzCEMh0cv0vl7ZF18UUtLO5WYH2iZ6OPMJmjNS7St2i0dLTey9M24gcfC6-izRkrWS6DUsqiAfIDQDF6cuLkDrU1
ReturnUrl: /
CopyCart: False
TokenCode: 
CaptchaToken: 
VerifyMethod: 
UsernameEmail: example@example.com
Password: 123456789
'''

class SilverBullion():
    def __init__(self) -> None:
        self.session: Session = Session()
        
        pass


    def login(self, email, password):
        
        # body_login = {
        #     "__RequestVerificationToken": "W7tAtfw6c-U5oHBwU37MqEW-xbw1etttu3RSzpNE_65Gh9DPdUmJjr6cMW90aVrMDv_2BcQURdhuZywfZfmLT127rM81",
        #     "ReturnUrl": "/",
        #     "CopyCart": "False",
        #     "TokenCode": "",
        #     "CaptchaToken": "",
        #     "VerifyMethod": "",
        #     "UsernameEmail": email,
        #     "Password": password
        # }
        response = self.session.post('https://www.silverbullion.com.sg/Account/Login', data=f'UsernameEmail={email}&Password={password}')
        data = response.text
        print(data)
        return data


