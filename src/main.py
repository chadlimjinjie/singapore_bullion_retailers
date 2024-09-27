import getpass
import asyncio

from bullion import bullion

# bullionstar_client = bullion.BullionStar()
# data = bullionstar_client.login("chadlimjinjie@gmail.com", "Ch@dlim98")


while True:
    retailer = input("Enter retailer (bullionstar, silverbullion, stargrams): ")
    retailer = retailer if retailer != "" else "bullionstar"
    email = input("Enter your email: ")
    password = getpass.getpass("Enter your password: ")
    login_data = asyncio.run(bullion.login(email, password, retailer))
    if login_data["success"]:
        break
    


