import requests,json

# Get access token from a bot
ACCESS_TOKEN = "NDE5ZWNkYTEtYTcxMi00NWRjLWIxNDktZTNlNzZiNzdiMjEwOTViNGJkM2MtMGFj_PF84_1eb65fdf-9643-417f-9974-ad72cae0e10f"
# Get the roomID from https://developer.webex.com/docs/api/v1/rooms/list-rooms
roomID = "Y2lzY29zcGFyazovL3VzL1JPT00vN2I3NTRiNjItNzE3Yi0zMmYzLWJiNmUtNDVjNjlkNGRkYjdk"

m = {
    "roomId": roomID,
    "text": "Este es un test desde webinar de Devnet"
}

r = requests.post(
    "https://webexapis.com/v1/messages",
    data=json.dumps(m),
    headers={
        "Authorization": "Bearer {}".format(ACCESS_TOKEN),
        "Content-Type": "application/json",
    },
)
print(r.text)


