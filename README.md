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
hashedPassword = BullionStar.hashPassword(password)
encryptedPassword = BullionStar.encryptPassword(salt, hashedPassword)
authenticate_response = bullionstar_client.authenticate(authToken, encryptedPassword)
```
- Perform Two-factor Authentication
- Resend Two-factor Authentication Code
- Invalidate Access Token
```python
invalidate_response = bullionstar_client.invalidate()
```

Shopping Cart API
- Refresh Shopping Cart
- Add to Shopping Cart
- Update Shopping Cart (unstable)
- Remove from Shopping Cart (unstable)
- Load All Shopping Carts

Buy Checkout API (in-development)
- Initialize Order
- Update Order
- Confirm Order
- Confirm Order and Create Account


Silver Bullion Singapore Stargrams (development on hold)
```python
# import the module
from bullion import StarGrams
```
StarGrams Object
```python
# Creates a http session
stargrams_client = StarGrams()
```
- Login
```python
login_response = stargrams_client.login('example@example.com', 'some_password')
```
- 2FA
<!-- ```python
``` -->
- User
<!-- ```python
``` -->


Silver Bullion Singapore (development on hold)
- Login function


