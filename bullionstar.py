import aiohttp
import hashlib


async def login(email, password):
    data = await initialize_bullionstar(email)
    data = await authenticate_bullionstar(data["authToken"], encryptPassword(data["salt"], hashPassword(password)))
    return data


async def initialize_bullionstar(email):
    body_initialize = {
        "email": email,
        "machineId": "EMV93wOBXXOUg04IOsKY",
        "ignoreWarning": "false",
        "device": "D"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://services.bullionstar.com/auth/v1/initialize', data=body_initialize) as resp:
            print(resp.status)
            data = await resp.json()
            print(data)

    return data


def hashPassword(password: str):
    hashedPassword = hashlib.md5(str.encode(password)).hexdigest()
    return hashedPassword


def encryptPassword(salt: str, hashedPassword: str):
    encryptedPassword = hashlib.md5(str.encode(salt + hashedPassword)).hexdigest()
    return encryptedPassword


async def authenticate_bullionstar(authToken: str, encryptedPassword: str):
    body_authenticate = {
        "authToken": authToken,
        "encryptedPassword": encryptedPassword,
        "valuation": "buy",
        "locationId": "1",
        "ignoreWarning": "false",
        "device": "D"
    }
    async with aiohttp.ClientSession() as session:

        async with session.post('https://services.bullionstar.com/auth/v1/authenticate', data=body_authenticate) as resp:
            print(resp.status)
            data = await resp.json()
            print(data)
    return data

