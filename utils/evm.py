import aiohttp

async def get_evm_balance(address):
    url = f"https://api.etherscan.io/api?module=account&action=balance&address={address}&tag=latest&apikey=YourApiKeyToken"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data.get("status") == "1":
                eth = int(data["result"]) / 1e18
                return round(eth, 4)
            return 0.0