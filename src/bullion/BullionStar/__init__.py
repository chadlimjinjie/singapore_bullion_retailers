import hashlib
from requests import Session

'''
https://services.bullionstar.com/product/filter/desktop?locationId=1&page=1&name=root&currency=SGD&apg=-1
'''

class BullionStar:
    def __init__(self, cuurency: str, locationId: int = None, apiKey: str = None, development: bool = True) -> None:
        '''
        cuurency: SGD USD EUR GBP AUD NZD SEK JPY BTC BCH ETH LTC

        locationId: {1: Singapore, 3: New Zealand}

        apiKey (optional): 

        development: 
        '''
        self.uri = 'testapi.bullionstar.com' if development else 'api.bullionstar.com' # services.bullionstar.com/api.bullionstar.com
        self.session: Session = Session()
        self.apiKey: str = apiKey
        self.accessToken: str = ''
        self.cartEntries: list = []
        self.cartString: str = ''
        self.locationId: int = locationId
        pass

    
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
            "email": email,
            "machineId": "EMV93wOBXXOUg04IOsKY",
            # "ignoreWarning": "false",
            # "device": "D"
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
            "authToken": authToken,
            "encryptedPassword": encryptedPassword,
            # "valuation": "buy",
            # "locationId": "1",
            "ignoreWarning": "false",
            "device": "D"
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticate', data=body_authenticate) 
        data = resp.json()
        print(resp.status_code, data)
            
        self.accessToken = data["accessToken"]
        return data


    async def authenticate_2fa(self, twoFactorToken: str, code: str):
        '''
        Use this API to perform SMS-based two-factor authentication (2FA) to generate an access token. This must be preceded by the /auth/v1/authenticate API.
        '''
        body_authenticate_2fa = {
            "twoFactorToken": twoFactorToken,
            "code": code
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticateTwoFactor', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)
        return data


    async def authenticateTwoFactorResendCode(self, twoFactorToken: str):
        body_authenticate_2fa = {
            "twoFactorToken": twoFactorToken
        }
        resp = self.session.post(f'https://{self.uri}/auth/v1/authenticateTwoFactorResendCode', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)

        return data


    async def invalidate(self):
        body_invalidate = {
            "accessToken": self.accessToken
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
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "locationId": self.locationId,
            "cartString": self.cartString
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart', headers=headers, json=body_cart)
        data = resp.json()
        return data
    
    # Add to Shopping Cart
    def add_to_shopping_cart(self, productId: int, quantity: int):
        '''
        Use this API to add a product to the user's shopping cart.
        '''
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "productId": productId,
            "quantity": quantity,
            "locationId": self.locationId,
            "cartString": self.cartString,
            "accessToken" : self.accessToken,
        }
        resp = self.session.post(f'https://{self.uri}/product/v1/shoppingcart/item', headers=headers, json=body_cart)
        data = resp.json()
        if data:
            self.cartEntries = data["cartEntries"]
            self.cartString = data["cartString"]
            
        return data
    
    # Update Shopping Cart
    def update_shopping_cart(self, productId: int, quantity: int):
        '''
        Use this API to update the user's shopping cart contents; usually required when updating the quantity for products that have already been added to the shopping cart.
        '''
        headers = {
            ':authority:': 'services.bullionstar.com',
            'Authorization': self.accessToken,
            'Content-Type': 'application/json; charset=UTF-8',
            
        }

        
        for entry in self.cartEntries:
            if str(productId) == entry['productId']:
                entry['quantity'] = quantity

        cartString = ",".join([f"{entry['productId']},{entry['quantity']}" for entry in self.cartEntries])
        
        body_cart = {
            "locationId": self.locationId,
            "cartString": cartString
        }
        
        resp = self.session.put(f'https://{self.uri}/product/v1/shoppingcart/item/{productId}', headers=headers, json=body_cart)
        print(resp)
        print(resp.text, resp.content)
        data = resp.json()
        if data:
            self.cartString = data["cartString"]
        
        return data
    
    # Remove from Shopping Cart
    def remove_from_shopping_cart(self, productId: int):
        '''
        Use this API to remove a product from the user's shopping cart.
        '''
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "locationId": self.locationId,
            "cartString": self.cartString,
            "accessToken" : self.accessToken,
        }
        resp = self.session.delete(f'https://{self.uri}/product/v1/shoppingcart/item/{productId}', headers=headers, json=body_cart)
        data = resp.json()
        if data:
            self.cartEntries = data["cartEntries"]
            self.cartString = data["cartString"]
        return data
    
    # Load All Shopping Carts
    def load_all_shopping_carts(self):
        headers = {
            "Authorization": self.accessToken,
            "Content-Type": "application/json; charset=UTF-8"
        }
        body_cart = {
            "locationId": self.locationId,
            # "cartString": self.cartString
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
        # print(currency, shippingMethodId, paymentMethodId)
        # headers = {
        #     "Authorization": self.accessToken,
        #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        # }
        body_order = {
            "currency": currency,
            # "productsString": self.cartString,
            # "shippingMethodId": shippingMethodId,
            # "paymentMethodId": paymentMethodId
        }
        resp = self.session.post(f'https://{self.uri}/checkout/buycheckout/init', data=body_order)
        data = resp.text
        print(data)
        return data


    '''
    "shippingMethods": [
        {
            "id": 2,
            "title": "Vault Storage Singapore",
            "description": "Store bullion safely with BullionStar as your Vault Storage provider. You can sell or withdraw your bullion by placing online orders 24/7.",
            "descriptionMobile": "Vault Storage with BullionStar. You can sell or withdraw stored bullion anytime by placing online orders."
        },
        {
            "id": 3,
            "title": "Personal Collection (Pick-up) Singapore",
            "description": "You will receive an e-mail payment confirmation from us once your payment has been processed. After you have received the payment confirmation, you may proceed to our bullion center at the following location to pick up your bullion. Please bring your ID. No appointment is necessary.<br /><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" style=\"padding: 0;margin-bottom: 12px;margin-top: 12px;\"><tbody><tr><td style=\"text-align: center;\" width=\"50px\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: block\"><img alt=\"\" src=\"https://static.bullionstar.com/img/email/google-map.png\" style=\"height: 40px;\" width=\"28\"></a></td><td style=\"text-align: left;\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: inline-block; font-size: 14px; line-height: 17px; font-weight: bold; text-decoration: none; color: black;\">45 New Bridge Road<br>Singapore 059398</a></td></tr></tbody></table><table><tbody><tr><td style=\"padding:0;font-family:Arial,sans-serif;\"><p style=\"font-weight: bold; margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Opening Hours:</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Mondays - Saturdays: 11 am to 7 pm</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Closed on Sundays and Public Holidays</p></td></tr></tbody></table>",
            "descriptionMobile": "You will receive an e-mail payment confirmation from us once your payment has been processed. After you have received the payment confirmation, you may proceed to our bullion center at 45 New Bridge Road to pick up your bullion. Please bring your ID. No appointment is necessary."
        },
        {
            "id": 1,
            "title": "Shipping by Courier from Singapore",
            "description": "Shipping by Courier to your delivery address.<br /><br />The shipping rates are based on your shipping destination country. Your current shipping country is: <span class=\"shippingDestinationCountryAnchor\"></span>. <span class=\"cc-condition\">To change shipping address/country, please check the checkbox for \"Ship to a Different Address\" under \"Customer Information\" and fill in your shipping address and country.</span>",
            "descriptionMobile": "The shipping cost will be visible on the next page and is based on your shipping destination country. Your current shipping country is: <span class=\"shippingDestinationCountryAnchor\"></span>. <span class=\"cc-condition\">To change shipping address/country, please check the checkbox for \"Ship to a Different Address\" below and fill in your shipping address and country.</span>"
        }
    ],
    "paymentMethods": [
        {
            "id": 37,
            "title": "PayNow Payment",
            "description": "The QR code and the Unique Entity Number - UEN will be visible on the order confirmation page and in the order confirmation e-mail. Maximum amount: SGD 200,000.",
            "descriptionMobile": "The QR code and the Unique Entity Number - UEN will be visible on the order confirmation page and in the order confirmation e-mail. Maximum amount: SGD 200,000.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 24,
            "title": "SGD Bank Transfer - OCBC",
            "description": "The bank account details will be visible on the order confirmation page and in the order confirmation e-mail.",
            "descriptionMobile": "The bank account details will be visible on the order confirmation page and in the order confirmation e-mail.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 13,
            "title": "SGD Bank Transfer - DBS Bank",
            "description": "The bank account details will be visible on the order confirmation page and in the order confirmation e-mail.",
            "descriptionMobile": "The bank account details will be visible on the order confirmation page and in the order confirmation e-mail.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 2,
            "title": "SGD Bank Transfer - UOB",
            "description": "The bank account details will be visible on the order confirmation page and in the order confirmation e-mail.",
            "descriptionMobile": "The bank account details will be visible on the order confirmation page and in the order confirmation e-mail.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 20,
            "title": "SGD BullionStar Account",
            "description": "Funds for your order will be debited from your BullionStar account. Your current BullionStar account balance is S$0.00.",
            "descriptionMobile": "Funds for your order will be debited from your BullionStar account. Your current BullionStar account balance is S$0.00.",
            "forceToCurrency": "",
            "accountPayment": true
        },
        {
            "id": 5,
            "title": "SGD Cash Payment",
            "description": "The payment has to be settled within one business day of the order confirmation.  <br /><br />Please proceed to our shop at the following location to make payment. No appointment is necessary. <br /><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" style=\"padding: 0;margin-bottom: 12px;margin-top: 12px;\"><tbody><tr><td style=\"text-align: center;\" width=\"50px\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: block\"><img alt=\"\" src=\"https://static.bullionstar.com/img/email/google-map.png\" style=\"height: 40px;\" width=\"28\"></a></td><td style=\"text-align: left;\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: inline-block; font-size: 14px; line-height: 17px; font-weight: bold; text-decoration: none; color: black;\">45 New Bridge Road<br>Singapore 059398</a></td></tr></tbody></table><table><tbody><tr><td style=\"padding:0;font-family:Arial,sans-serif;\"><p style=\"font-weight: bold; margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Opening Hours:</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Mondays - Saturdays: 11 am to 7 pm</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Closed on Sundays and Public Holidays</p></td></tr></tbody></table>",
            "descriptionMobile": "Please proceed to our shop at 45 New Bridge Road to make payment within one business day of placing your order.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 10,
            "title": "NETS",
            "description": "Please note that the product price is 1% higher when you select NETS payment. If you would like to avoid the extra cost, please choose another payment method such as bank transfer, PayNow or SGD cash payment. The default payment limit for most NETS cardholders is SGD 2000. Enquire with your bank to check or raise your limit. The payment has to be settled within one business day of the order confirmation.<br /><br />Please proceed to our shop at the following location to make payment. No appointment is necessary. <br /><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" style=\"padding: 0;margin-bottom: 12px;margin-top: 12px;\"><tbody><tr><td style=\"text-align: center;\" width=\"50px\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: block\"><img alt=\"\" src=\"https://static.bullionstar.com/img/email/google-map.png\" style=\"height: 40px;\" width=\"28\"></a></td><td style=\"text-align: left;\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: inline-block; font-size: 14px; line-height: 17px; font-weight: bold; text-decoration: none; color: black;\">45 New Bridge Road<br>Singapore 059398</a></td></tr></tbody></table><table><tbody><tr><td style=\"padding:0;font-family:Arial,sans-serif;\"><p style=\"font-weight: bold; margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Opening Hours:</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Mondays - Saturdays: 11 am to 7 pm</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Closed on Sundays and Public Holidays</p></td></tr></tbody></table>",
            "descriptionMobile": "Please note that the product price is 1% higher when you select NETS payment. If you would like to avoid the extra cost, please choose another payment method such as bank transfer, PayNow or SGD cash payment. The default payment limit for most NETS cardholders is SGD 2000. Enquire with your bank to check or raise your limit. Please proceed to our shop at 45 New Bridge Road to make payment within one business day of placing your order.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 49,
            "title": "Online Credit/Debit Card Payment in SGD",
            "description": "We accept Mastercard, VISA, JCB and UnionPay. Maximum amount: SGD 75,000. Please note that the price is 4% higher when you select online card payment. If you would like to avoid the extra cost, please choose another payment method such as bank transfer, PayNow or SGD cash payment.<br /><br />Please allow up to 24 hours for the card transaction to be processed. ",
            "descriptionMobile": "We accept Mastercard, VISA, JCB and UnionPay. Maximum amount: SGD 75,000. Please note that the price is 4% higher when you select online card payment. If you would like to avoid the extra cost, please choose another payment method such as bank transfer, PayNow or SGD cash payment.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 25,
            "title": "Retail Shop Credit/Debit Card Payment in SGD (Settlement in retail shop)",
            "description": "We accept Visa, Mastercard and UnionPay. Please note that the price is 3.3% higher when you select card payment. If you would like to avoid the extra cost, please choose another payment method such as bank transfer, PayNow or SGD cash payment. The payment has to be settled within one business day of the order confirmation. <br /><br />Please proceed to our shop at the following location to make payment with your credit/debit card.<br /><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" style=\"padding: 0;margin-bottom: 12px;margin-top: 12px;\"><tbody><tr><td style=\"text-align: center;\" width=\"50px\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: block\"><img alt=\"\" src=\"https://static.bullionstar.com/img/email/google-map.png\" style=\"height: 40px;\" width=\"28\"></a></td><td style=\"text-align: left;\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: inline-block; font-size: 14px; line-height: 17px; font-weight: bold; text-decoration: none; color: black;\">45 New Bridge Road<br>Singapore 059398</a></td></tr></tbody></table><table><tbody><tr><td style=\"padding:0;font-family:Arial,sans-serif;\"><p style=\"font-weight: bold; margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Opening Hours:</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Mondays - Saturdays: 11 am to 7 pm</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Closed on Sundays and Public Holidays</p></td></tr></tbody></table>",
            "descriptionMobile": "We accept Visa, Mastercard and UnionPay. Please note that the price is 3.3% higher when you select card payment. If you would like to avoid the extra cost, please choose another payment method such as bank transfer, PayNow or SGD cash payment. Please proceed to our shop at 45 New Bridge Road to make your card payment within one business day of placing your order. We accept Visa, Mastercard or UnionPay.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 6,
            "title": "SGD Cheque Payment ",
            "description": "Please make your cheque payable to: BullionStar Pte Ltd.<br /><br />Please hand over the cheque to us within one business day of the order confirmation. If you mail the cheque, it has to be mailed to us within one business day. Please note that only cheques issued by Singaporean banks are accepted and that all orders paid by cheque are subject to a holding period until the cheque has cleared.<br /><br />To hand over your cheque, please proceed to our shop at the below location. No appointment is necessary. If you mail your cheque, send it to the address as stated below: <br /><table border=\"0\" cellpadding=\"0\" cellspacing=\"0\" style=\"padding: 0;margin-bottom: 12px;margin-top: 12px;\"><tbody><tr><td style=\"text-align: center;\" width=\"50px\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: block\"><img alt=\"\" src=\"https://static.bullionstar.com/img/email/google-map.png\" style=\"height: 40px;\" width=\"28\"></a></td><td style=\"text-align: left;\"><a href=\"https://www.google.com/maps/place/45+New+Bridge+Rd,+BullionStar,+Singapore+059398/@1.2882241,103.8467937,17z/data=!4m2!3m1!1s0x31da19102f0905d1:0x84514482d11d3320\" target=\"_blank\" style=\"display: inline-block; font-size: 14px; line-height: 17px; font-weight: bold; text-decoration: none; color: black;\">BullionStar Pte Ltd<br>45 New Bridge Road<br>Singapore 059398</a></td></tr></tbody></table><table><tbody><tr><td style=\"padding:0;font-family:Arial,sans-serif;\"><p style=\"font-weight: bold; margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Opening Hours:</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Mondays - Saturdays: 11 am to 7 pm</p><p style=\"margin: 0 0 2px; font-size: 14px; line-height: 17px;\">Closed on Sundays and Public Holidays</p></td></tr></tbody></table>",
            "descriptionMobile": "Please proceed to our shop at 45 New Bridge Road to hand over the cheque to us within one business day of placing your order.",
            "forceToCurrency": "",
            "accountPayment": false
        },
        {
            "id": 17,
            "title": "Bitcoin",
            "description": "You will receive the bitcoin address, to which you send your bitcoin payment, on the order confirmation page after placing your order.  <br /><br />The bitcoin payment must be initiated within 20 minutes of the order confirmation.<br /><br />You will receive an e-mail when we have processed your payment. We will thereafter handle your order.",
            "descriptionMobile": "You will receive the bitcoin address, to which you send your bitcoin payment, on the order confirmation page after placing your order. The bitcoin payment must be initiated within 20 minutes of the order confirmation.",
            "forceToCurrency": "BTC",
            "accountPayment": false
        },
        {
            "id": 34,
            "title": "Bitcoin Cash",
            "description": "You will receive the Bitcoin Cash address, to which you send your Bitcoin Cash payment, on the order confirmation page after placing your order. Only send coins from Bitcoin Cash (Node). Do NOT send coins from the Bitcoin Cash ABC and Bitcoin Cash SV chain to BullionStar as they are not accepted.<br /><br />The Bitcoin Cash payment must be initiated within 20 minutes of the order confirmation.<br /><br />You will receive an e-mail when we have processed your payment. We will thereafter handle your order.",
            "descriptionMobile": "You will receive the Bitcoin Cash address, to which you send your Bitcoin Cash payment, on the order confirmation page after placing your order. Only send coins from Bitcoin Cash (Node). Do NOT send coins from the Bitcoin Cash ABC and Bitcoin Cash SV chain to BullionStar as they are not accepted. The Bitcoin Cash payment must be initiated within 20 minutes of the order confirmation.",
            "forceToCurrency": "BCH",
            "accountPayment": false
        },
        {
            "id": 35,
            "title": "Ethereum",
            "description": "You will receive the ethereum address, to which you send your ethereum payment, on the order confirmation page after placing your order. <br /><br />The Ethereum payment must be initiated within 20 minutes of the order confirmation through the Ethereum Mainnet.<br /><br />You will receive an e-mail when we have processed your payment. We will thereafter handle your order.",
            "descriptionMobile": "You will receive the ethereum address, to which you send your ethereum payment, on the order confirmation page after placing your order. The Ethereum payment must be initiated within 20 minutes of the order confirmation through the Ethereum Mainnet.",
            "forceToCurrency": "ETH",
            "accountPayment": false
        },
        {
            "id": 36,
            "title": "Litecoin",
            "description": "You will receive the litecoin address, to which you send your litecoin payment, on the order confirmation page after placing your order. <br /><br />The litecoin payment must be initiated within 20 minutes of the order confirmation.<br /><br />You will receive an e-mail when we have processed your payment. We will thereafter handle your order.",
            "descriptionMobile": "You will receive the litecoin address, to which you send your litecoin payment, on the order confirmation page after placing your order. The litecoin payment must be initiated within 20 minutes of the order confirmation.",
            "forceToCurrency": "LTC",
            "accountPayment": false
        }
    ],    
    '''
    