from typing import Any
import httpx
from flask import  jsonify
from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from mcp.server import Server
import requests
import uvicorn
import json
import time

# Initialize FastMCP server for Flight tools (SSE)
mcp = FastMCP("Flight-MCP")

@mcp.tool()
async def search_flights(source: str, destination: str, date: str) -> str:
    """Search for flights in 
    Args:
        source: Departure airport code (e.g. LAX)
        destination: Arrival airport code (e.g. JFK)
        date: Date of travel in YYYY-MM-DD format
    """
    headers = {
        "Content-Type": "application/json",
    }
    print(f"Searching flights from {source} to {destination} on {date}")


    bearer_token = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MzI4MzI4LCJqdGkiOiI5OGQxMmQ3NjlkMTM0MmYwYjUwODJiMTNmMWU4ZGU2NCIsInVzZXJfaWQiOiJyb2hpdEB5b3BtYWlsLmNvbSJ9.C_hQgbFdrU5_Td31J0b3AAs7FnBsK70qRGR5Zq4fkF4rmbGh0wNH3QB27GXzx97aT-GbwTczihmQ-il0hJoFKNSYlIDczEJ__FvovthhoCCvxtELGKM8tp65J3rB7A8pej2ZxhEc237EzVhGU3v02jUZArP7iNkDj7SLHa68vOJ-n2VU5RE07rwJ4svJrv7KqdY909eVHu6w5KllGCKKdRUXohyW08Ol1b1-c6l11S4wElOqQn8F1rG8UPgTTFnHTfrIxqrfsq7wJgQpbYTuhSgVIETo5hURmcLMQ9lgyZdDk2NBzc8b-G2cL85HhEis6vum3xagJBubH0pMeeBIA5x3gqZSIUsvlAgSRYRhSItgW5eqYR7qNCkSCHRJ_r2_mB3rqTRzzyVEeWinAbF9PrbXOs_v7hZ8j5rDsPLjjUIIC67hzLUc3CRgEdU9E7i_y8Gtcxmlp3ydMmO6sE3V70jT6vRGU9Mej0V-4ycwP_3POZGt5fPwXzLvOLTS529BNHu8K4JmYwX-7CwFxu97fFmcypeBIEhj-lrgGG8VyzBjOgkJX21ht31sEQ75T1Uje5tfI4nwQ9hEC5CKvno4NzF42Nk1U-06NT7o26i7sqxZ033lx7I2IucqfBEmBYIyxzyEDN5OcCRo-5dMldIkla6c3zi0Q0odSitMcUf4dVI"

    # if not all([src, dest, date, time]):
    #     return jsonify({"error": "Missing required fields: src, dest, date, time"}), 400

    payload = {"source_new_ui":1,"isPersonalDetailsEdit": False,"acknowledge":1,"title":"","instruction":"","action":"add","personal_booking":0,"travel_type":"ow","event_id":None,"travel":[{"mode":"Flight","date":"26 Apr, 2025","from":"Las Vegas, US (LAS)","to":"Los Angeles, US (LAX)","from_city_id":"214","to_city_id":"104","origin_country":{"country_name":"United States"},"dest_country":{"country_name":"United States"},"trip_type":"Domestic","trip_type_window":"Domestic","time":"4"}],"customDimension":0,"trip_type":2,"self_data":{"employee_id":"1424","gender":"Male","salutation":"Mr","first_name":"Rohit","last_name":"sharma","phone":"6058765417","country_code":"US","contact_country_code":"+1","dob":"1995-09-05","passport_expiry":"2026-12-06"},"no_of_rooms_count":1,"no_of_adults_count":1,"no_of_child_count":0,"no_of_infant_count":0,"multioccupancy_rooms":0,"trip_creation_utc":"2025-04-10 11:39:48","timezone":"Asia/Calcutta","pre_fetch_request_id":"0ed931a0-fa24-4164-aa02-72c74aa8159f","pre_fetch":0}

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "python-requests",
        "Cookie": "_ga=GA1.1.792384896.1743685186; Path=/; AMP_MKTG_968605772d=JTdCJTdE; PHPSESSID=f9ril79ikegalk9gtni4koqmav; is_include_me_checked=true; sessionid=hs2i25iww2r3utdo501t7fzjhdlgxdid; ftr_blst_1h=1744280912844; forterToken=c0fa44a08bee411cb82309690d455b42_1744280911391__UDF43-m4_17ck; mp_3f350e9124c15ea7a76648ef3f4c4b9d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A196057fb7f41721f-0ae2b6f37ee5ce-13462c6e-4b9600-196057fb7f51721f%22%2C%22%24device_id%22%3A%20%22196057fb7f41721f-0ae2b6f37ee5ce-13462c6e-4b9600-196057fb7f51721f%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpr%22%3A%20%5B%5D%2C%22__mpap%22%3A%20%5B%5D%7D; _hp2_ses_props.2414103148=%7B%22ts%22%3A1744284401154%2C%22d%22%3A%22ilqaapp.iltech.in%22%2C%22h%22%3A%22%2Fcreate-new-trip%22%7D; __ilreactappexp=1744370838; il_app_refresh_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDM3MDgzOCwianRpIjoiZDU3YzBjM2U2ZGNhNDg2Njk3MzRkNTNmYjA4NTI1ZmIiLCJ1c2VyX2lkIjoicm9oaXRAeW9wbWFpbC5jb20ifQ.ydFaOBWJAi8HJgvsAYt00F6tjpTqb0RdIg4P-Q_GHx76v8HjO5RDzdgab1noAzdwNOAmdtCqha12BL7DwkFEn5lMu8aXEkKHeeuvYSE-gzAE4QLJJHj214j1wZftTAaNu73xJWqmmjK6zeoBs_7IhIT4oj6DfhmHdjYfhwP_ksMK1Z600zQW7A6LAKZ65LBLk_iVAcggFkixFjWpXy-4f-58iblDElM6qJ22D06sI-k9np7AVWnHv27AEWyXe-bcO04TqeZCeecalgs1EHdGyCk12i4CGrdrHV8NOWTIFSZ5cYJsfBZzKeYP_byznk3_4r1QabiC30Ck7DKMwL_fTYiBjwA8vVkby5zH83nZEuCS9po_TS_7bGyG3R6H2pzfMTfTBheghgMxPA5qxgUyP9WPk3gkgLoYjbH2mRAl804A0aal0XNqAODEowrD_E8KW1hdQ-QGGmx2dsZq5PmsDQ_R359i7y7SjVJXwkP19VM4aCX33zavRuAu5OrfrSy-JkVDmBZQpvLBotEdSxD6I4vExTCi2D2V3S-3gAHV7h2Y1jhc7_gcMCV1sW8fnGsYySRE9vmOaMU89YBZQMXWriUo116-v0EDo9AMCDjNp6UoBKWlVM29P9CoK07LxlOY56wb4ohw1XiJsVISAlxjbCKOnsNuNlheeqgDTTukJ18; AMP_968605772d=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjJhNGQ1NTE1NC00MTMyLTQ3YTMtYTFhMi0xMzM5NDQzNjQzNWMlMjIlMkMlMjJ1c2VySWQlMjIlM0EyMjE1JTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc0NDI4NDM5NjMxNCUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NDQyODQ0NjAxMjYlMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTI5OCUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBMSU3RA==; twk_uuid_58b968cf78d62074c097b1f8=%7B%22uuid%22%3A%221.PUsg8IvLf3ucVkk0fvU2ypWkY82zeRJM95rF4bbEuGapC2M6l8DkoTrskhIvNhGZmsAIQfUnYp3LIietEWsYKnYQ5vFD6fYN17ZtFFsetFdI112bD%22%2C%22version%22%3A3%2C%22domain%22%3A%22iltech.in%22%2C%22ts%22%3A1744285108944%7D; __ilappaccess=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MzI4MzI4LCJqdGkiOiI5OGQxMmQ3NjlkMTM0MmYwYjUwODJiMTNmMWU4ZGU2NCIsInVzZXJfaWQiOiJyb2hpdEB5b3BtYWlsLmNvbSJ9.C_hQgbFdrU5_Td31J0b3AAs7FnBsK70qRGR5Zq4fkF4rmbGh0wNH3QB27GXzx97aT-GbwTczihmQ-il0hJoFKNSYlIDczEJ__FvovthhoCCvxtELGKM8tp65J3rB7A8pej2ZxhEc237EzVhGU3v02jUZArP7iNkDj7SLHa68vOJ-n2VU5RE07rwJ4svJrv7KqdY909eVHu6w5KllGCKKdRUXohyW08Ol1b1-c6l11S4wElOqQn8F1rG8UPgTTFnHTfrIxqrfsq7wJgQpbYTuhSgVIETo5hURmcLMQ9lgyZdDk2NBzc8b-G2cL85HhEis6vum3xagJBubH0pMeeBIA5x3gqZSIUsvlAgSRYRhSItgW5eqYR7qNCkSCHRJ_r2_mB3rqTRzzyVEeWinAbF9PrbXOs_v7hZ8j5rDsPLjjUIIC67hzLUc3CRgEdU9E7i_y8Gtcxmlp3ydMmO6sE3V70jT6vRGU9Mej0V-4ycwP_3POZGt5fPwXzLvOLTS529BNHu8K4JmYwX-7CwFxu97fFmcypeBIEhj-lrgGG8VyzBjOgkJX21ht31sEQ75T1Uje5tfI4nwQ9hEC5CKvno4NzF42Nk1U-06NT7o26i7sqxZ033lx7I2IucqfBEmBYIyxzyEDN5OcCRo-5dMldIkla6c3zi0Q0odSitMcUf4dVI; __ilappaccessexp=1744328328; __ilapprefresh=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NDM3MTUyOCwianRpIjoiNTEyZDU0M2U0YTM1NGE4ZjkwMGI4MmNiYmRjY2ZhNjYiLCJ1c2VyX2lkIjoicm9oaXRAeW9wbWFpbC5jb20ifQ.fWDvviwiDE3UKhgF4he-Ahu5mxv92Kco7cMAtNFe3Qb032VnYJX229qnecqZwdKqvXQ-UB70wM600rCN45tLyad2D6zGpekYABMUnQLPhrgLN44q-uUh-NYH4dZYepQV9854Wnzg8Z2m04SdySWE4dCQpywke24s8g2E2hGqCdTkFBIJvazL7bNp9u-6awt3tZ_YHLRYF8-QcAAcRUY7ARJtgFUS96rAgptX9FW0vtgbxhWbPQlpHdC8255QQKSiidd8cp-DTT6NJ1mf7azdianImn9DH7tAzJ-C7rjCXkcvNAmUxWVtlPq64h7OVzVi_xqzEd_LyLS6B6M7ug-h07r-rxJJQ55pm2I7QIDM46IMFxbGd5iKlCYPsoDW5yx8vx5C19aaY8x9ddU73ZyXP7z1mNBy8-guEaNija-fVnY61ZyXTyV0Wnh4IC09lGIrsSpeqZe-A7-I2m18NC1PyjUgujNqC7hV7JufD47iHqOey6Ohx5YuTAyYtnlwpIxaPjGCPidldZXso6rxfzS4zrhb94RIXBw289si90BG4TAKzDfomIPBsHshmuLi5-AOqRnDD6N3jr-UmYDTaOGb1yMoY8y_Bxu2Z6kyjAYiJelBXDsrJkE1Kmo3Dp0xzfRZoMLSccyJxzU9-FYlrQ5-glPX2mm9CQHAPSGgjtWtZCs; __ilapprefreshexp=1744371528; __iluser=7460d3e67baa12e17627b3249c35eef3; __iltoken=1b53c508d6872e95752e1c2febfbc3ce; __ilop=ZXlKdmNDSTZJbU55WldGMFpTMXVaWGN0ZEhKcGNDSXNJbkp2YkdVaU9pSnpkR0ZtWmlKOQ==; _hp2_id.2414103148=%7B%22userId%22%3A%225445956803295933%22%2C%22pageviewId%22%3A%227172597539381124%22%2C%22sessionId%22%3A%225982035446915271%22%2C%22identity%22%3Anull%2C%22trackerVersion%22%3A%224.0%22%7D; _ga_WS3055H5DH=GS1.1.1744284396.15.1.1744285138.9.0.0; AMP_bbf126af3d=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjI1YzlhY2QxYS01ZDEzLTRmNTEtYjg4YS1iZTY3NmY1ZWRlNWYlMjIlMkMlMjJ1c2VySWQlMjIlM0EyMjE1JTJDJTIyc2Vzc2lvbklkJTIyJTNBMTc0NDI4NDQwMjA4NiUyQyUyMm9wdE91dCUyMiUzQWZhbHNlJTJDJTIybGFzdEV2ZW50VGltZSUyMiUzQTE3NDQyODUxMzk4MDglMkMlMjJsYXN0RXZlbnRJZCUyMiUzQTE2NiU3RA==; TawkConnectionTime=0; twk_uuid_5ed7d6a64a7c62581799da2d=%7B%22uuid%22%3A%221.PUsijGmveBsvex2VMLImPMyAcN9sbGAxy0Fao3elBActygGLTMuRj1BwmMS2H3TTbfEmSEUFcdwKsDAvSffw48wbcEgamtfLKFhiLWDf4MZDltrnV%22%2C%22version%22%3A3%2C%22domain%22%3A%22iltech.in%22%2C%22ts%22%3A1744285140118%7D"
    }

    try:
        print("Hitting first API")
        response = requests.post(
            'https://ilqaapp.iltech.in/create-trip',
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            try:
                trip_response = response.json()
                trip_id = trip_response.get("trip-id")

                if not trip_id:
                    return jsonify({"error": "Trip ID not found in response"}), 500

                # 👇 Second API call with trip_id
                print("Hitting second API")
                package_url = f"https://itilite-stream-qa-1.iltech.in/api/v1/package/trip?trip_id={trip_id}"
                package_headers = {
                    "Content-Type": "application/json",
                    "Authorization": bearer_token,
                }

                package_resp =  requests.get(package_url, headers=package_headers)
                print("Completed second API")
                if package_resp.status_code == 200:
                    try:
                        search_package = package_resp.json()

                        # 👇 Second API call with trip_id
                        flight_search_id = search_package["leg_info"][0]["leg_request_id"]

                        if not flight_search_id:
                            return jsonify({
                                "create_trip_response": trip_response,
                                "package_response": package_resp.json(),
                                "search_package_response": "Flight ID not found in response"
                            })

                        print(flight_search_id)
                        package_url = (
                            f"https://itilite-stream-qa-1.iltech.in/api/v1/search/flight/request/{flight_search_id}/"
                            "recommendation_completed"
                            "?sort_by_recommended_only=-1"
                            "&page_no=1"
                            "&page_size=20"
                            "&default_current_filter=true"
                            "&version=2"
                            "&multi_city=false"
                        )
                        print(package_url)

                        package_headers = {
                            "Content-Type": "application/json",
                            "Authorization": bearer_token,
                        }
                        
                        print("Hitting third API")
                        max_retries = 20
                        retry_delay = 2  # seconds

                        search_package_resp = None
                        for attempt in range(max_retries):
                            try:
                                search_package_resp =  requests.get(package_url, headers=package_headers, timeout=30)
                                if search_package_resp.status_code == 200:
                                    break  # Success: status code is 200
                            except requests.exceptions.RequestException as err:
                                pass  # You can log the error here if needed

                            if attempt < max_retries - 1:
                                time.sleep(retry_delay)
                            else:
                                return jsonify({"error": "Request failed after multiple attempts."}), 500
                        # print("Completed third API", search_package_resp.status_code)
                        # print(f"Package response: {package_resp.json()}")
                        # print(f"Search package response: {search_package_resp.json()}")

                        if search_package_resp.status_code == 200:
                            result =  {
                                "create_trip_response": trip_response,
                                "package_response": package_resp.json(),
                                "search_package_response": search_package_resp.json()
                            }, 200
                        else:
                            result =  {
                                "search_package_response": f"Failed to fetch search package: {search_package_resp.status_code}",
                                "text": search_package_resp.text
                            }, search_package_resp.status_code

                        return result
                    except json.JSONDecodeError:
                        return jsonify({"error": "Response was not valid JSON", "text": response.text}), 502
            except json.JSONDecodeError:
                return jsonify({"error": "Response was not valid JSON", "text": response.text}), 502
        else:
            return jsonify({
                "error": f"Request failed with status {response.status_code}",
                "text": response.text
            }), response.status_code

    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create a Starlette application that can server the provied mcp server with SSE."""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,  # noqa: SLF001
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )


if __name__ == "__main__":
    mcp_server = mcp._mcp_server  # noqa: WPS437

    import argparse
    
    parser = argparse.ArgumentParser(description='Run MCP SSE-based server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8081, help='Port to listen on')
    args = parser.parse_args()

    # Bind SSE request handling to MCP server
    starlette_app = create_starlette_app(mcp_server, debug=True)

    uvicorn.run(starlette_app, host=args.host, port=args.port)
