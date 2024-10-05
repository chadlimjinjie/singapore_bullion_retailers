  # Singapore Bullion Retailers API

Programmatic functions for accessing Singapore bullion retailers API


BullionStar Singapore https://www.bullionstar.com/developer/docs/api/

BullionStar Object

```python
from bullion import BullionStar

# Creates a http session
bullionstar_client = bullion.BullionStar(cuurency='SGD', locationId=1)
```

Authentication API
- Initialize Authentication
```python
data_initialize = bullionstar_client.initialize('example@example.com') # TODO: authToken, salt = bullionstar_client.initialize('example@example.com')
```
- Perform Authentication
```python
data_authenticate = bullionstar_client.authenticate(data_initialize['authToken'], BullionStar.encryptPassword(data_initialize['salt'], BullionStar.hashPassword(password))) 
# TODO: data_authenticate = bullionstar_client.authenticate(authToken, BullionStar.encryptPassword(salt, BullionStar.hashPassword(password)))
```
- Perform Two-factor Authentication
- Resend Two-factor Authentication Code
- Invalidate Access Token

Shopping Cart API
- Refresh Shopping Cart
- Add to Shopping Cart
- Update Shopping Cart
- Remove from Shopping Cart
- Load All Shopping Carts

(Development on hold)
Silver Bullion Singapore Stargrams
- Login function

(Development on hold)
Silver Bullion Singapore
- Login function (TODO)

Roadmap
- Retailers onboarding
- To release as a python package on PyPi
- Looking for passionate maintainers
