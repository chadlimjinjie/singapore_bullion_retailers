import os
import getpass

from bullion import BullionStar

# email, password = {
#     'email': 1,
#     'password': 2
# }.values()
# print(email, password)

def display_menu():
    print('1. Add to Shopping Cart')
    print('2. Update Shopping Cart')
    print('3. Remove from Shopping Cart')
    print('4. Refresh Shopping Cart')
    print('5. Load All Shopping Carts')
    print('6. Display Shopping Cart')
    print('7. Initialize Order')
    print('8. Display Option Menu')
    print('9. Display Option Menu')


email = os.getenv('BULLIONSTAR_EMAIL')
password = os.getenv('BULLIONSTAR_PASSWORD')
# password = getpass.getpass('Enter your password: ')
# print(email, password)
bullionstar_client = BullionStar(currency='SGD', locationId=1, development=False)
bullionstar_client.login(email, password)
display_menu()
while True:
    option = input('Enter option: ')
    print()
    if option == '1':
        productId = int(input('Enter productId: '))
        quantity = int(input('Enter quantity: '))
        add_to_shopping_cart = bullionstar_client.add_to_shopping_cart(productId, quantity)
    elif option == '2':
        productId = int(input('Enter productId: '))
        quantity = int(input('Enter quantity: '))
        update_shopping_cart = bullionstar_client.update_shopping_cart(productId, quantity)
    elif option == '3':
        productId = int(input('Enter productId: '))
        bullionstar_client.remove_from_shopping_cart(productId)
    elif option == '4':
        refresh_shopping_cart = bullionstar_client.refresh_shopping_cart()
        # print(refresh_shopping_cart)
    elif option == '5':
        load_all_shopping_carts = bullionstar_client.load_all_shopping_carts()
        print(load_all_shopping_carts)
    elif option == '6':
        bullionstar_client.display_shopping_cart()
    elif option == '7':
        bullionstar_client.initialize_order(3, 37)
        # print(bullionstar_client.initialize_order('SGD', 3, 37))
    elif option == '8':
        bullionstar_client.confirm_order()
        # print(bullionstar_client.initialize_order('SGD', 3, 37))
    elif option == '9':
        display_menu()
        # bullionstar_client.affiliate()
    elif option == '-1':
        break


