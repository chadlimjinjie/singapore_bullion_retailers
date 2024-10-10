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
                
        get_page = self.session.get('https://www.silverbullion.com.sg/Account/Login')
        page_cookies = get_page.cookies
        __RequestVerificationToken = page_cookies.get('__RequestVerificationToken')
        print(__RequestVerificationToken)
        response = self.session.post('https://www.silverbullion.com.sg/Account/Login', data=f'__RequestVerificationToken={__RequestVerificationToken}&ReturnUrl=&CopyCart=False&TokenCode=&CaptchaToken=&VerifyMethod=&UsernameEmail={email}&Password={password}')
        
        data = response.text
        print(data)
        return data


# fetch("https://www.silverbullion.com.sg/Account/Login", {
#   "headers": {
#     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
#     "accept-language": "en-US,en;q=0.9",
#     "cache-control": "max-age=0",
#     "content-type": "application/x-www-form-urlencoded",
#     "priority": "u=0, i",
#     "sec-ch-ua": "\"Brave\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Windows\"",
#     "sec-fetch-dest": "document",
#     "sec-fetch-mode": "navigate",
#     "sec-fetch-site": "same-origin",
#     "sec-fetch-user": "?1",
#     "sec-gpc": "1",
#     "upgrade-insecure-requests": "1",
#     "cookie": ".ASPXANONYMOUS=nLpQb8GDJOgUw-q5NmN6Jo1dfd6A1IxxveZR5XhZMM8PEmnoxOHnKfEk5zzqPmW_Jl4f2DAyD4e35xZpS3UPgymB9qxRoDkiommlGoBiwgpk4fejiMiX57EKyJVJ8L6hIMJLtQ2; PreferredCurrency=SGD; ASP.NET_SessionId=wtqubuvw03bwica5txpiljtf; __RequestVerificationToken=StEYfeuB-1V3rfNGg-zALQ5ShhNC6h7NP97aNfMhfsUFarN4ZQe3h9IlT9mnEwfVu7xBiYz2KlyLwe00sq1pN9PFHBs1",
#     "Referer": "https://www.silverbullion.com.sg/Account/Login",
#     "Referrer-Policy": "strict-origin-when-cross-origin"
#   },
#   "body": "__RequestVerificationToken=jQG-gHTlQx4j2rcbW94meA5T3Z8ow_GwnbV7W_84XEj7V2XgwA29kFVl9udgbmGDEJHyPdvdUubk0CTJ5273YqCakog1&ReturnUrl=&CopyCart=False&TokenCode=&CaptchaToken=&VerifyMethod=&UsernameEmail=123&Password=123",
#   "method": "POST"
# });