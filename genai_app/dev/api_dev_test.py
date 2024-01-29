import requests
# Test the api for the genai_app
# @app.post("/info", response_model=List[QuestionAnswer])
# async def post_info(recipient_info: RecipientInfo):
#     ...

response = requests.post(
    "http://localhost:8000/info",
    json={"recipient_info": "John Doe"},
)
print(response.json())


# %%
