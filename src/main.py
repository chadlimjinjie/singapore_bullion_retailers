import getpass
import asyncio

from bullion import bullion

# bullionstar_client = bullion.BullionStar()
# data = bullionstar_client.login("chadlimjinjie@gmail.com", "Ch@dlim98")


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

bullionstar_client = bullion.BullionStar(development=False)

bullionstar_client.login(email, password)
bullionstar_client.add_to_cart(2934, "1", 1)
# bullionstar_client.refresh_shopping_cart(1, "")
