import asyncio
import httpx

async def ping_indexnow(urls: list[str]):
    payload = {
        "host": "snapreeldownload.com",
        "key": "49ee0a05f62d4645bd7fd30f5840e72e",
        "keyLocation": "https://snapreeldownload.com/49ee0a05f62d4645bd7fd30f5840e72e.txt",
        "urlList": urls
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.indexnow.org/indexnow",
            json=payload
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

async def main():
    urls_to_submit = [
        "https://snapreeldownload.com/",
        "https://snapreeldownload.com/youtube",
        "https://snapreeldownload.com/tiktok",
        "https://snapreeldownload.com/instagram",
        "https://snapreeldownload.com/facebook",
        "https://snapreeldownload.com/snapchat",
        "https://snapreeldownload.com/pinterest",
    ]
    await ping_indexnow(urls_to_submit)

if __name__ == "__main__":
    asyncio.run(main())
