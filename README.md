  # Singapore Bullion Retailers API

An open-source Python library for accessing Singapore bullion retailers API

Designed for retail investors and businesses, this package streamlines the process of integrating with the bullion marketplace by abstracting complex API calls and providing intuitive functions to manage investments in gold, silver, and other precious metals.

BullionStar Singapore https://www.bullionstar.com/developer/docs/api/


```python
# import the module
from bullion import BullionStar
```

BullionStar Object

| locationId | Country |
| -------- | ------- |
| 1 | Singapore |
| 3 | New Zealand |

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

| ID | Item |
| -------- | ------- |
| 480 | 1 Gram of Gold - Bullion Savings Program (BSP) |
| 481 | 1 Gram of Silver - Bullion Savings Program (BSP) |

IMPORTANT!!! Product ID are different across location
```python
cart_response = bullionstar_client.add_to_shopping_cart(productId=481, quantity=32)
```
- Update Shopping Cart
- Remove from Shopping Cart
- Load All Shopping Carts

Buy Checkout API
- Initialize Order
- Update Order (in-development)
- Confirm Order (in-development)
- Confirm Order and Create Account (in-development)


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


