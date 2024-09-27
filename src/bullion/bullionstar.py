import hashlib
import requests

'''
https://services.bullionstar.com/auth/v1/initialize
email: example@example.com
machineId: EMV93wOBXXOUg04IOsKY
ignoreWarning: false
device: D

{
  "status": 0,
  "title": "",
  "message": "",
  "authToken": "eyJraWQiOiIxLjAuMCIsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJidWxsaW9uc3RhciIsImV4cCI6MTcyNzE1ODc5OCwiaWF0IjoxNzI3MTU4NDk4LCJzdWIiOiJMUTFhZkxZfik1XSttRD0rWUxwci1rTF8rN3RDRmFLUlgpWVRHdFRuTnQpWGs5K1lUZD92JXF5Kmh9JX5RdE4zXXE2Zj90OUprcHowNV59ZmJ9bTB3VUoxdS1WUk5xWX1zeGk9e1widG9rZW5cIjpcIkdDSE1DQkpLSElUQ1NRRlNTSE1SQ0NUQk1CTkpCT0pGXCIsXCJlbWFpbFwiOlwiXCIsXCJhY2NvdW50SWRcIjotMSxcInNhbHRcIjpcIkF2dnVuTFhOTVZKWmhjRXQ3bkIvdmhNaUFLaE1hYzlhZlVXSTM4eFFPVTZ5cllRYldSYjEwVUswZ1J1clc5U2JKNEkvRjZsbGNwRDg1SUk4UE9VK0NFTzhCc29zQlExeVwiLFwibWFjaGluZUlkXCI6XCJcIixcImV4cGlyZVRpbWVcIjoxNzI3MTY1Njk4NzE2fSJ9.Ditv4EFQI5i0CT0UdkxO6juaWpXQTztazV4FA7YSUOIr5Rk40CD9G9EW4ABWAyW-Rh_McCmSRZ-lfILj7f6PkOiW5e--m7jBKdsXM2bXaqqyj--W-AHHjXmcBpw92XdOQ4smv2ocd3EF7x_YsYlCcYZwD3QP3JC47PONVSrfLLjcEzA1esPYe_ce5KfKbQ5FHEq4op28N9CXQTIK7xNEUJjE4ro3F9UguC3SRy3RRdzwpktJb84NiAIKVp6jgr2d0P8bQJ1dT6HrKnM8a_xB0QtZXIH8fjWPW_WT_QcSLxvL7TxqjOU_7Xd_NxFQ9ScX4JdETqUafm_B9i6lV-QjKQ",
  "salt": "AvvunLXNMVJZhcEt7nB/vhMiAKhMac9afUWI38xQOU6yrYQbWRb10UK0gRurW9SbJ4I/F6llcpD85II8POU+CEO8BsosBQ1y",
  "error": false,
  "warning": false,
  "success": true,
  "authenticationRequired": false,
  "accessDenied": false
}




https://services.bullionstar.com/auth/v1/authenticate
authToken: eyJraWQiOiIxLjAuMCIsImFsZyI6IlJTMjU2In0.eyJpc3MiOiJidWxsaW9uc3RhciIsImV4cCI6MTcyNzE1ODc5OCwiaWF0IjoxNzI3MTU4NDk4LCJzdWIiOiJMUTFhZkxZfik1XSttRD0rWUxwci1rTF8rN3RDRmFLUlgpWVRHdFRuTnQpWGs5K1lUZD92JXF5Kmh9JX5RdE4zXXE2Zj90OUprcHowNV59ZmJ9bTB3VUoxdS1WUk5xWX1zeGk9e1widG9rZW5cIjpcIkdDSE1DQkpLSElUQ1NRRlNTSE1SQ0NUQk1CTkpCT0pGXCIsXCJlbWFpbFwiOlwiXCIsXCJhY2NvdW50SWRcIjotMSxcInNhbHRcIjpcIkF2dnVuTFhOTVZKWmhjRXQ3bkIvdmhNaUFLaE1hYzlhZlVXSTM4eFFPVTZ5cllRYldSYjEwVUswZ1J1clc5U2JKNEkvRjZsbGNwRDg1SUk4UE9VK0NFTzhCc29zQlExeVwiLFwibWFjaGluZUlkXCI6XCJcIixcImV4cGlyZVRpbWVcIjoxNzI3MTY1Njk4NzE2fSJ9.Ditv4EFQI5i0CT0UdkxO6juaWpXQTztazV4FA7YSUOIr5Rk40CD9G9EW4ABWAyW-Rh_McCmSRZ-lfILj7f6PkOiW5e--m7jBKdsXM2bXaqqyj--W-AHHjXmcBpw92XdOQ4smv2ocd3EF7x_YsYlCcYZwD3QP3JC47PONVSrfLLjcEzA1esPYe_ce5KfKbQ5FHEq4op28N9CXQTIK7xNEUJjE4ro3F9UguC3SRy3RRdzwpktJb84NiAIKVp6jgr2d0P8bQJ1dT6HrKnM8a_xB0QtZXIH8fjWPW_WT_QcSLxvL7TxqjOU_7Xd_NxFQ9ScX4JdETqUafm_B9i6lV-QjKQ
encryptedPassword: 88790e6f3bf8fd50ac5d95a3c1571c09
valuation: buy
locationId: 1
ignoreWarning: false
device: D


{
  "status": 1,
  "title": "Incorrect email or password",
  "message": "The email address or password you entered was incorrect.",
  "accessToken": null,
  "authenticateIp": false,
  "pendingDueDiligence": false,
  "twoFactorToken": null,
  "twoFactorMachineToken": null,
  "twoFactorGoogleAuthenticatorToken": null,
  "locked": false,
  "loggedIn": false,
  "accountInfo": null,
  "error": true,
  "success": false,
  "warning": false,
  "authenticationRequired": false,
  "accessDenied": false
}

https://services.bullionstar.com/product/filter/desktop?locationId=1&page=1&name=root&currency=SGD&apg=-1


'''

class BullionStar:
    def __init__(self, apiKey: str = "") -> None:
        self.session = requests.Session()
        self.apiKey: str = apiKey
        self.accessToken: str = ""
        pass

    

    # Authentication API
    def login(self, email: str, password: str):
        data = self.initialize(email)
        data = self.authenticate(data["authToken"], self.encryptPassword(data["salt"], self.hashPassword(password)))
        return data


    def initialize(self, email: str):
        body_initialize = {
            "email": email,
            "machineId": "EMV93wOBXXOUg04IOsKY",
            "ignoreWarning": "false",
            "device": "D"
        }

        resp = self.session.post('https://services.bullionstar.com/auth/v1/initialize', data=body_initialize)
        data = resp.json()
        
        print(resp.status_code, data)
        
        return data


    def hashPassword(self, password: str):
        hashedPassword = hashlib.md5(str.encode(password)).hexdigest()
        return hashedPassword


    def encryptPassword(self, salt: str, hashedPassword: str):
        encryptedPassword = hashlib.md5(str.encode(salt + hashedPassword)).hexdigest()
        return encryptedPassword


    def authenticate(self, authToken: str, encryptedPassword: str):
        body_authenticate = {
            "authToken": authToken,
            "encryptedPassword": encryptedPassword,
            "valuation": "buy",
            "locationId": "1",
            "ignoreWarning": "false",
            "device": "D"
        }
        resp = self.session.post('https://services.bullionstar.com/auth/v1/authenticate', data=body_authenticate) 
        data = resp.json()
        print(resp.status_code, data)
        return data


    async def authenticate_2fa(self, twoFactorToken: str, code: str):
        body_authenticate_2fa = {
            "twoFactorToken": twoFactorToken,
            "code": code,
            # "valuation": "buy",
            # "locationId": "1",
            # "ignoreWarning": "false",
            # "device": "D"
        }
        resp = self.session.post('https://services.bullionstar.com/auth/v1/authenticateTwoFactor', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)
        return data


    async def authenticateTwoFactorResendCode(self, twoFactorToken: str):
        body_authenticate_2fa = {
            "twoFactorToken": twoFactorToken,
            # "valuation": "buy",
            # "locationId": "1",
            # "ignoreWarning": "false",
            # "device": "D"
        }
        resp = self.session.post('https://services.bullionstar.com/auth/v1/authenticateTwoFactorResendCode', data=body_authenticate_2fa)
        data = resp.json()
        print(resp.status_code, data)

        return data


    async def invalidate(self):
        body_invalidate = {
            "accessToken": self.accessToken,
            # "valuation": "buy",
            # "locationId": "1",
            # "ignoreWarning": "false",
            # "device": "D"
        }
        
        
        resp = self.session.post('https://services.bullionstar.com/auth/v1/invalidate', data=body_invalidate)
        data = resp.json()
        print(resp.status_code, data)
        self.accessToken = ""
        return data

