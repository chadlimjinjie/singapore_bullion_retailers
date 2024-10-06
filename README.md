  # Singapore Bullion Retailers API

Programmatic functions for accessing Singapore bullion retailers API


BullionStar Singapore https://www.bullionstar.com/developer/docs/api/


```python
# import the module
from bullion import BullionStar
```

BullionStar Object

```python
# Creates a http session
bullionstar_client = BullionStar(cuurency='SGD', locationId=1)
```

Authentication API
- Initialize Authentication
```python
authToken, salt = bullionstar_client.initialize('example@example.com')
```
- Perform Authentication
```python
data_authenticate = bullionstar_client.authenticate(authToken, BullionStar.encryptPassword(salt, BullionStar.hashPassword(password)))
```
- Perform Two-factor Authentication
- Resend Two-factor Authentication Code
- Invalidate Access Token
```python
data_invalidate = bullionstar_client.invalidate()
```

Shopping Cart API
- Refresh Shopping Cart
- Add to Shopping Cart
- Update Shopping Cart
- Remove from Shopping Cart
- Load All Shopping Carts

Silver Bullion Singapore Stargrams (Development on hold)
- Login function

Silver Bullion Singapore (Development on hold)
- Login function (TODO)

Roadmap
- Retailers onboarding
- To release as a python package on PyPi
- Looking for passionate maintainers
