  # Singapore Bullion Retailers API

Programmatic functions for accessing Singapore bullion retailers API


BullionStar Singapore https://www.bullionstar.com/developer/docs/api/

BullionStar Object

```python
# Creates a http session
bullionstar_client = bullion.BullionStar(cuurency='SGD', locationId=1)
```

Authentication API
- Initialize Authentication
```python
bullionstar_client.initialize('example@example.com')
```
- Perform Authentication
```python
data_initialize = bullionstar_client.initialize('example@example.com') # authToken, salt = bullionstar_client.initialize('example@example.com')
data_authenticate = bullionstar_client.authenticate(data_initialize['authToken'], bullion.BullionStar.encryptPassword(data_initialize['salt'], bullion.BullionStar.hashPassword(password))) # data_authenticate = bullionstar_client.authenticate(authToken, bullion.BullionStar.encryptPassword(salt, bullion.BullionStar.hashPassword(password)))
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


Silver Bullion Singapore Stargrams
- Login function


(Development on hold)
Silver Bullion Singapore
- Login function (TODO)



Roadmap
- Retailers onboarding
- To release as a python package on PyPi
