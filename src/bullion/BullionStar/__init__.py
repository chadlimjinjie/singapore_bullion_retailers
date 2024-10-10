import hashlib
from requests import Session

'''
https://services.bullionstar.com/product/filter/desktop?locationId=1&page=1&name=root&currency=SGD&apg=-1
'''

class BullionStar:
    def __init__(self, currency: str, locationId: int = None, apiKey: str = None, development: bool = True) -> None:
        '''
        cuurency: SGD USD EUR GBP AUD NZD SEK JPY BTC BCH ETH LTC

        locationId: {1: Singapore, 3: New Zealand}

        apiKey (optional): 

        development: 
        '''
        self.uri = 'testapi.bullionstar.com' if development else 'services.bullionstar.com' # services.bullionstar.com/api.bullionstar.com
        self.session: Session = Session()
        self.apiKey: str = apiKey
        self.accessToken: str = ''
        self.cartEntries: list = []
        self.cartString: str = ''
        self.locationId: int = locationId
        pass
    
    def shopping_cart_api_headers(self):
        return {
            'Authorization': self.accessToken,
            'Content-Type': 'application/json; charset=UTF-8'
        }
    
    def login(self, email: str, password: str):
        authToken, salt = self.initialize(email)
        data_authenticate = self.authenticate(authToken, self.encryptPassword(salt, self.hashPassword(password)))
        data_load_all_shopping_carts = self.load_all_shopping_carts()
        # print(data_load_all_shopping_carts)
        if data_load_all_shopping_carts:
            self.cartEntries = data_load_all_shopping_carts['response']['cartEntries']
            self.cartString = data_load_all_shopping_carts['response']['cartString']
        return data_authenticate


    # Authentication API: https://www.bullionstar.com/developer/docs/api/resources/auth.html
    # Initialize Authentication
    def initialize(self, email: str):
        '''
        Use this API to initialize the authentication process.
        '''
        body_initialize = {
            'email': email,
            'machineId': 'EMV93wOBXXOUg04IOsKY',
            # 'ignoreWarning': 'false',
            # 'device': 'D'
        }

        resp = self.session.post(f'https://{self.uri}/auth/v1/initialize', data=body_initialize)
        data = resp.json()
        
        # print(resp.status_code, data)
        
        return (data['authToken'], data['salt'])


    def hashPassword(self, password: str):
        hashedPassword = hashlib.md5(str.encode(password)).hexdigest()
        return hashedPassword


    def encryptPassword(self, salt: str, hashedPassword: str):
        encryptedPassword = hashlib.md5(str.encode(salt + hashedPassword)).hexdigest()
        return encryptedPassword

    # Perform Authentication
    def authenticate(self, authToken: str, encryptedPassword: str):
        '''
        Use this API to perform authentication to generate an access token.
        The authToken response item from the /auth/v1/initialize endpoint are required as inputs to this API.
        '''
        body_authenticate = {
            'authToken': authToken,
            'encryptedPassword': encryptedPassword,
            # 'valuation': 'buy',
            # 'locationId': '1',
            'ignoreWarning': 'false',
            'device': 'D'
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticate', data=body_authenticate) 
        data = resp.json()
        print(resp.status_code, data)
            
        self.accessToken = data['accessToken']
        return data


    async def authenticate_2fa(self, twoFactorToken: str, code: str):
        '''
        Use this API to perform SMS-based two-factor authentication (2FA) to generate an access token. This must be preceded by the /auth/v1/authenticate API.
        '''
        body_authenticate_2fa = {
            'twoFactorToken': twoFactorToken,
            'code': code
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticateTwoFactor', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)
        return data


    async def authenticateTwoFactorResendCode(self, twoFactorToken: str):
        body_authenticate_2fa = {
            'twoFactorToken': twoFactorToken
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticateTwoFactorResendCode', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)

        return data


    async def invalidate(self):
        body_invalidate = {
            'accessToken': self.accessToken
        }
        
        
        resp = self.session.post(f'https://{self.uri}/auth/v1/invalidate', data=body_invalidate)
        data = resp.json()
        print(resp.status_code, data)
        self.accessToken = ''
        return data

    
    def product_prices(self, currency: str, locationId: int, productIds: str):
        resp = self.session.get(f'https://{self.uri}/product/v1/prices?currency={currency}&locationId={locationId}&productIds={productIds}')
        data = resp.json()
        print(resp.status_code, data)
        return data
    
    
    # Shopping Cart API: https://www.bullionstar.com/developer/docs/api/resources/shopping-cart.html
    # Refresh Shopping Cart
    def refresh_shopping_cart(self):
        '''
        Use this API to refresh the user's shopping cart contents; usually required when updating the product prices and quantity.
        '''
        headers = self.shopping_cart_api_headers()
        body_cart = {
            'locationId': self.locationId,
            'cartString': self.cartString
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart', headers=headers, json=body_cart)
        data = resp.json()
        return data
    
    # Add to Shopping Cart
    def add_to_shopping_cart(self, productId: int, quantity: int):
        '''
        Use this API to add a product to the user's shopping cart.
        '''
        headers = self.shopping_cart_api_headers()
        body_cart = {
            'productId': productId,
            'quantity': quantity,
            'locationId': self.locationId,
            'cartString': self.cartString,
            'accessToken' : self.accessToken,
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart/item', headers=headers, json=body_cart)
        data = resp.json()
        if data:
            self.cartEntries = data['cartEntries']
            self.cartString = data['cartString']
            
        return data
    
    # Update Shopping Cart
    def update_shopping_cart(self, productId: int, quantity: int):
        '''
        Use this API to update the user's shopping cart contents; usually required when updating the quantity for products that have already been added to the shopping cart.
        '''
        headers = self.shopping_cart_api_headers()

        
        for entry in self.cartEntries:
            if str(productId) == entry['productId']:
                entry['quantity'] = quantity

        cartString = ','.join([f'{entry['productId']},{entry['quantity']}' for entry in self.cartEntries])
        
        body_cart = {
            'locationId': self.locationId,
            'cartString': cartString
        }
        
        resp = self.session.put(f'https://{self.uri}/product/v1/shoppingcart/item/{productId}', headers=headers, json=body_cart)
        print(resp)
        print(resp.text, resp.content)
        data = resp.json()
        if data:
            self.cartString = data['cartString']
        
        return data
    
    # Remove from Shopping Cart
    def remove_from_shopping_cart(self, productId: int):
        '''
        Use this API to remove a product from the user's shopping cart.
        '''
        headers = self.shopping_cart_api_headers()
        body_cart = {
            'locationId': self.locationId,
            'cartString': self.cartString,
            'accessToken' : self.accessToken,
        }
        resp = self.session.delete(f'https://{self.uri}/product/v1/shoppingcart/item/{productId}', headers=headers, json=body_cart)
        data = resp.json()
        if data:
            self.cartEntries = data['cartEntries']
            self.cartString = data['cartString']
        return data
    
    # Load All Shopping Carts
    def load_all_shopping_carts(self):
        headers = self.shopping_cart_api_headers()
        body_cart = {
            'locationId': self.locationId,
            # 'cartString': self.cartString
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart/all', headers=headers, json=body_cart)
        data = resp.json()
        return data

    def display_shopping_cart(self):
        print(f'productId title quantity')
        for entry in self.cartEntries:
            print(f'{entry['productId']} {entry['title']} {entry['quantity']}')
    

    # Buy Checkout API: https://www.bullionstar.com/developer/docs/api/resources/buy-checkout.html
    '''
    The Buy Checkout API allows you to lock in on the Buy price and place a Buy order

    1. Call the /api/v3/buycheckout/init API to get the retrieve the current product price, and to lock in on the current buy price before confirming the order. 
    The API returns a priceLockToken which can be used to update the order in Step 2.
    2. Call the /api/v2/buycheckout/update API to specify the bullion and BSP products to buy, update the payment method, 
    and to lock in on the current price before confirming the order.
    3. Call the /api/v2/buycheckout/confirm API to confirm the order with the latest priceLockToken (if any) obtained from the previous steps.

    '''
    # Initialize Order
    def initialize_order(self, currency: str, shippingMethodId: int, paymentMethodId: int):
        '''
        Use this API to initialize a Buy order. Get the total order price, and obtain a priceLockToken to lock in on the order price before placing the order. This API also returns shipping and payment methods that are available for the order.
        The priceLockToken is currently valid for three minutes; however this limit is subject to change.
        '''

        resp = self.session.post(f'https://{self.uri}/checkout/buycheckout/init?currency={currency}&shippingMethodId={shippingMethodId}&paymentMethodId={paymentMethodId}&locationId=1&productsString={self.cartString}')
        data = resp.json()
        print(data['address'])
        print(data['costs'])
        
        return data

    # Affiliate API
    def affiliate(self):
        '''
        Use this API to retrieve transaction and balance information for the Affiliate Program. Only applicable to affiliate accounts.
        '''
        resp = self.session.get(f'https://{self.uri}/api/v1/referral/info')
        data = resp.text
        print(data)
        return data

    # Announcements API
    def latest_announcements(self, visitedDays: int, geoCountry: str, dismissed: int):
        '''
        Use this API to get relevant announcements from BullionStar.
        '''
        resp = self.session.get(f'https://{self.uri}/account/v1/announcement')
        data = resp.text
        print(data)
        return data

