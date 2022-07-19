import aiohttp


# Get a random image from Unsplash using the API key
# Returns the link to download the image
async def get_random_image(client_key, query, orientation):
    params = {'query': query, 'orientation': orientation, 'client_id': client_key}
    session = aiohttp.ClientSession()

    async with session.get('https://api.unsplash.com/photos/random', params=params) as resp:
        # Check if the response code is OK
        if resp.status != 200:
            print(f'Error encountered while requesting picture. Response code {resp.status}')
            return None

        # Read the JSON response and obtain the source image
        resp_json = await resp.json()

        # Close the session after the image download link is obtained
        await session.close()

        return resp_json['urls']['regular']
