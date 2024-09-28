import getpass

import bullion

# while True:
#     retailer = input("Enter retailer (bullionstar, silverbullion, stargrams): ")
#     retailer = retailer if retailer != "" else "bullionstar"
#     email = input("Enter your email: ")
#     password = getpass.getpass("Enter your password: ")
#     login_data = asyncio.run(bullion.login(email, password, retailer))
#     if login_data["success"]:
#         break


'''
480: 1 Gram of Gold - Bullion Savings Program (BSP)
481: 1 Gram of Silver - Bullion Savings Program (BSP)
'''

email = input("Enter your email: ")
password = getpass.getpass("Enter your password: ")
bullionstar_client = bullion.BullionStar(locationId=1, development=False)
bullionstar_client.login(email, password)
print("1. Add to Shopping Cart")
print("2. Update Shopping Cart")
print("3. Remove from Shopping Cart")
print("4. Refresh Shopping Cart")
print("5. Load All Shopping Carts")
while True:
    option = int(input("Enter option: "))
    print()
    if option == 1:
        productId = int(input("Enter productId: "))
        quantity = int(input("Enter quantity: "))
        add_to_shopping_cart = bullionstar_client.add_to_shopping_cart(productId, quantity)
    elif option == 2:
        productId = int(input("Enter productId: "))
        quantity = int(input("Enter quantity: "))
        update_shopping_cart = bullionstar_client.update_shopping_cart(productId, quantity)
    elif option == 3:
        productId = int(input("Enter productId: "))
        bullionstar_client.remove_from_shopping_cart()
    elif option == 4:
        refresh_shopping_cart = bullionstar_client.refresh_shopping_cart()
        # print(refresh_shopping_cart)
    elif option == 5:
        load_all_shopping_carts = bullionstar_client.load_all_shopping_carts()
        print(load_all_shopping_carts)
    elif option == 6:
        bullionstar_client.display_shopping_cart()
    elif option == -1:
        break


