import bullion.silverbullion, bullion.stargrams
from .BullionStar import BullionStar

async def login(email: str, password: str, retailer: str):

    match retailer:
        case "bullionstar":
            result = BullionStar().login(email, password)
        case "silverbullion":
            result = await bullion.silverbullion.login(email, password)
        case "stargrams":
            result = await bullion.stargrams.StarGrams().login(email, password)

    return result



