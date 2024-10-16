'''
https://www.bullionstar.com/developer/docs/api/resources/buy-checkout.html#buy-checkout-init-post
'''

from typing import Any


class InitializedOrder:
    '''
    
    '''

    def __init__(self, data: dict) -> None:
        # self.shippingMethods: list
        # self.shippingMethodId: int
        # self.paymentMethods: list
        # self.paymentMethodId: int
        # self.cart: dict
        # self.costs: dict
        # self.expectedReleaseDate: str
        # self.priceLockToken: str
        for key, val in data.items():
            self.__setattr__(key, val)
        pass
    
    # def __str__(self) -> str:
    #     pass
    
    
        
# class InitializedOrder:
#     '''
    
#     '''
#     def __init__(self, shippingMethods: list, shippingMethodId: int, paymentMethods: list, 
#                  paymentMethodId: int, cart: dict, costs: dict, expectedReleaseDate: str,
#                  priceLockToken: str) -> None:
#         self.shippingMethods: list = shippingMethods
#         self.shippingMethodId: int = shippingMethodId
#         self.paymentMethods: list = paymentMethods
#         self.paymentMethodId: int = paymentMethodId
#         self.cart: dict = cart
#         self.costs: dict = costs
#         self.expectedReleaseDate: str = expectedReleaseDate
#         self.priceLockToken: str = priceLockToken
#         pass
    
    
    
    
    
    