class Account:
    '''
    
    '''

    def __init__(self, accountId: int, type: str, email: str, 
                 name: str, nationalityCode: str, phoneNumber: str, 
                 phoneCountry: str, address1: str, address2: str,
                 postCode: str, state: str, city: str,
                 countryCode: str, twoFactorSMSAvailable: bool, twoFactorAuthenticationEnabled: bool) -> None:
        # Account details https://services.bullionstar.com/account/details/get
        self.accountId: int = accountId
        self.type: str = type
        self.email: str = email
        self.name: str = name
        self.nationalityCode: str = nationalityCode
        self.phoneNumber: str = phoneNumber
        self.phoneCountry: str = phoneCountry
        self.address1: str = address1
        self.address2: str = address2
        self.postCode: str = postCode
        self.state: str = state
        self.city: str = city
        self.countryCode: str = countryCode
        self.twoFactorSMSAvailable: bool = twoFactorSMSAvailable
        self.twoFactorAuthenticationEnabled: bool = twoFactorAuthenticationEnabled


