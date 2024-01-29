# Backend Work Plan

## Overview
The backend will support a three-screen web application with multiple API calls and user inputs that culminate in sending an email. It will be built using FastAPI.

## Tech Stack
- **Framework**: FastAPI

## Development Setup
- Install Python 3.10+.
- Set up a virtual environment.
- Install dependencies with poerty: `poetry install`.
- Run the development server: `poetry run uvicorn main:app --reload`.

## API Endpoints

### Screen 1 Endpoints
- **POST /info**:
  - Description: Receive user input about the recipient.
  - Payload: { "recipient_info": "string" }
  - Response: 
  ```json
  [
    { "question": "string", "answer": "string", "placeholder": "string" },
    { "question": "string", "answer": "string", "placeholder": "string" },
    ...
  ]
  ```

### Screen 2 Endpoints
- **POST /refine**:
    - Description: Receive refined and in context user input about the recipient.
    - Payload: 
    ```json
    [ 
      { "question": "string", "answer": "string"},
      { "question": "string", "answer": "string"},
      ...
    ]
    ```
    - Response: 
    ```json
    { "email_title": "string", 
    "email_content": "string",
    "email_image": "base64_image_data"}
    ```

### Screen 3 Endpoints
- **POST /send**:
    - Description: Send the email to the recipient.
    - Payload: 
    ```json
    {
    "recipient_email": "string", 
    "email_title": "string", 
    "email_content": "string",
    "email_image": "base64_image_data"}
    ```
    - Response: 
    ```json
    { "message": "string" }
    ```
