import aiohttp

async def login(email, password):
    
    body_login = {
        "username": email,
        "password": password
    }

    async with aiohttp.ClientSession() as session:

        async with session.post('https://www.stargrams.app/api/login', data=body_login) as resp:
            # print(resp.status)
            data = await resp.text()
            print(data)

        token = input("Enter 2FA: ")

        body_2fa = {
            "token": token
        }

        async with session.post('https://www.stargrams.app/api/user/2fa/phone', data=body_2fa) as resp:
            # print(resp.status)
            data = await resp.text()
            print(data)
    
    return


