from bullion.bullionstar import BullionStar
import bullion.silverbullion, bullion.stargrams

async def login(email: str, password: str, retailer: str):

    match retailer:
        case "bullionstar":
            result = await BullionStar().login(email, password)
        case "silverbullion":
            result = await bullion.silverbullion.login(email, password)
        case "stargrams":
            result = await bullion.stargrams.StarGrams().login(email, password)

    return result



