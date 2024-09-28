import hashlib
import requests
from requests.sessions import Session

'''
https://services.bullionstar.com/product/filter/desktop?locationId=1&page=1&name=root&currency=SGD&apg=-1
'''

class BullionStar:
    def __init__(self, apiKey: str = "", development: bool = True) -> None:
        self.uri = "testapi.bullionstar.com" if development else "services.bullionstar.com" # services.bullionstar.com/api.bullionstar.com
        self.session: Session = requests.Session()
        self.apiKey: str = apiKey
        self.accessToken: str = ""
        self.cartString: str = ""
        pass


    # Authentication API: https://www.bullionstar.com/developer/docs/api/resources/auth.html
    def login(self, email: str, password: str):
        data = self.initialize(email)
        data = self.authenticate(data["authToken"], self.encryptPassword(data["salt"], self.hashPassword(password)))
        return data


    def initialize(self, email: str):
        body_initialize = {
            "email": email,
            "machineId": "EMV93wOBXXOUg04IOsKY",
            "ignoreWarning": "false",
            "device": "D"
        }

        resp = self.session.post(f'https://{self.uri}/auth/v1/initialize', data=body_initialize)
        data = resp.json()
        
        print(resp.status_code, data)
        
        return data


    def hashPassword(self, password: str):
        hashedPassword = hashlib.md5(str.encode(password)).hexdigest()
        return hashedPassword


    def encryptPassword(self, salt: str, hashedPassword: str):
        encryptedPassword = hashlib.md5(str.encode(salt + hashedPassword)).hexdigest()
        return encryptedPassword


    def authenticate(self, authToken: str, encryptedPassword: str):
        body_authenticate = {
            "authToken": authToken,
            "encryptedPassword": encryptedPassword,
            "valuation": "buy",
            "locationId": "1",
            "ignoreWarning": "false",
            "device": "D"
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticate', data=body_authenticate) 
        data = resp.json()
        print(resp.status_code, data)
        
        if data:
            self.accessToken = data["accessToken"]
        
        return data


    async def authenticate_2fa(self, twoFactorToken: str, code: str):
        body_authenticate_2fa = {
            "twoFactorToken": twoFactorToken,
            "code": code,
            # "valuation": "buy",
            # "locationId": "1",
            # "ignoreWarning": "false",
            # "device": "D"
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticateTwoFactor', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)
        return data


    async def authenticateTwoFactorResendCode(self, twoFactorToken: str):
        body_authenticate_2fa = {
            "twoFactorToken": twoFactorToken,
            # "valuation": "buy",
            # "locationId": "1",
            # "ignoreWarning": "false",
            # "device": "D"
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticateTwoFactorResendCode', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)

        return data


    async def invalidate(self):
        body_invalidate = {
            "accessToken": self.accessToken,
            # "valuation": "buy",
            # "locationId": "1",
            # "ignoreWarning": "false",
            # "device": "D"
        }
        
        
        resp = self.session.post(f'https://{self.uri}/auth/v1/invalidate', data=body_invalidate)
        data = resp.json()
        print(resp.status_code, data)
        self.accessToken = ""
        return data

    
    def product_prices(self, currency: str, locationId: int, productIds: str):
        resp = self.session.get(f'https://{self.uri}/product/v1/prices?currency={currency}&locationId={locationId}&productIds={productIds}')
        data = resp.json()
        print(resp.status_code, data)
        return data
    
    
    # Shopping Cart API: https://www.bullionstar.com/developer/docs/api/resources/shopping-cart.html
    # Refresh Shopping Cart
    def refresh_shopping_cart(self, locationId: int):
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "locationId": locationId,
            "cartString": self.cartString
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart', headers=headers, json=body_cart)
        data = resp.json()
        return data
    
    # Add to Shopping Cart
    def add_to_cart(self, productId: int, quantity: str, locationId: int):
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "productId": productId,
            "quantity": quantity,
            "locationId": locationId,
            "cartString": self.cartString,
            "accessToken" : self.accessToken,
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart/item', headers=headers, json=body_cart)
        data = resp.json()
        self.cartString = data["cartString"]
        return data


    # Remove from Shopping Cart
    '''
    480: 1 Gram of Gold - Bullion Savings Program (BSP)
    481: 1 Gram of Silver - Bullion Savings Program (BSP)
    '''
    def remove_from_cart(self, productId: int, locationId: int):
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "locationId": locationId,
            "cartString": self.cartString,
            "accessToken" : self.accessToken,
        }
        resp = self.session.delete(f'https://{self.uri}/product/v1/shoppingcart/item/{productId}', headers=headers, json=body_cart)
        data = resp.json()
        self.cartString = data["cartString"]
        return data


    def load_all_shopping_carts(self, locationId: int):
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "locationId": locationId,
            # "cartString": self.cartString
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart/all', headers=headers, json=body_cart)
        data = resp.json()
        return data
