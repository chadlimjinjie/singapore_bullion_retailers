from .BullionStar import BullionStar
from .StarGrams import StarGrams
from .SilverBullion import SilverBullion

async def login(email: str, password: str, retailer: str):

    match retailer:
        case "bullionstar":
            result = BullionStar.login(email, password)
        case "silverbullion":
            result = await SilverBullion.login(email, password)
        case "stargrams":
            result = await StarGrams.login(email, password)

    return result



