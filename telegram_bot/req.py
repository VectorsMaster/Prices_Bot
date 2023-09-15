import requests
import links
import httpx


async def check_password(password: str):
    async with httpx.AsyncClient() as client:
        auth_response = await client.post(
            links.auth_endpoint, json={"username": "ProductAdmin", "password": password}
        )
        if auth_response.status_code == 200:
            return auth_response.json().get("token")
        else:
            return None


async def upload_file(file_path: str, token: str):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Token {token}"}
        get_response = await client.post(
            links.endpoint, headers=headers, json={"file_path": file_path}
        )
        print(f"Upload file: {get_response.status_code}")
        if get_response.status_code == 200:
            return True
        else:
            return False


async def get_products(vehicle_type: str, category: str, description: str):
    async with httpx.AsyncClient() as client:
        params = {
            "description": description,
        }
        if category is not None:
            params["category"] = category

        if vehicle_type is not None:
            params["vehicle_type"] = vehicle_type

        get_response = await client.get(links.search_endpoint, params=params)
        print(get_response.json())
        if get_response.status_code == 200:
            res = ""
            for product in get_response.json():
                res = res + f"{product['price']} {product['vehicle_type']} {product['name']} "
                res = res + "\n"
            print(res)
            return res
        else:
            return None
