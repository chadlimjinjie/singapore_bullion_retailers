import bullionstar, stargrams, silverbullion

async def login(email: str, password: str, retailer: str):

    match retailer:
        case "bullionstar":
            result = await bullionstar.login(email, password)
        case "silverbullion":
            result = await silverbullion.login(email, password)
        case "stargrams":
            result = await stargrams.login(email, password)

    return result



