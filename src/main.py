import getpass

from bullion import bullion


# while True:
#     retailer = input("Enter retailer (bullionstar, silverbullion, stargrams): ")
#     retailer = retailer if retailer != "" else "bullionstar"
#     email = input("Enter your email: ")
#     password = getpass.getpass("Enter your password: ")
#     login_data = asyncio.run(bullion.login(email, password, retailer))
#     if login_data["success"]:
#         break

email = input("Enter your email: ")
password = getpass.getpass("Enter your password: ")

bullionstar_client = bullion.BullionStar(locationId=1, development=False)

bullionstar_client.login(email, password)

'''
480: 1 Gram of Gold - Bullion Savings Program (BSP)
481: 1 Gram of Silver - Bullion Savings Program (BSP)
'''
print(bullionstar_client.add_to_shopping_cart(481, "1"))

print(bullionstar_client.update_shopping_cart(481, "10"))

print(bullionstar_client.cartString)

# bullionstar_client.remove_from_shopping_cart(481)

# print(bullionstar_client.load_all_shopping_carts())

# bullionstar_client.refresh_shopping_cart(1)
# print(bullionstar_client.cartString)
