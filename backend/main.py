from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware

from backend.services.chat_service import chat

from backend.models.schemas import (
    ChatRequest,
    RegisterRequest,
    LoginRequest
)

from backend.auth.database import (
    create_users_table,
    create_user,
    get_user
)

from backend.auth.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    verify_token
)


app = FastAPI(
    title="Industrial Maintenance Knowledge Chatbot",
    description="Multilingual RAG chatbot for industrial maintenance",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


create_users_table()


@app.get("/")
def root():

    return {
        "system": "Industrial Maintenance Knowledge Chatbot",
        "status": "online",
        "model": "openai/gpt-oss-120b",
        "rag": "enabled",
        "authentication": "enabled",
        "languages": [
            "English",
            "Kiswahili",
            "French"
        ]
    }


@app.post("/register")
def register(
    request: RegisterRequest
):

    existing_user = get_user(
        request.username
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )


    password_hash = hash_password(
        request.password
    )


    try:

        create_user(
            username=request.username,
            email=request.email,
            password_hash=password_hash
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )


    return {
        "message": "Registration successful",
        "username": request.username
    }


@app.post("/login")
def login(
    request: LoginRequest
):

    user = get_user(
        request.username
    )


    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    user_id = user[0]

    username = user[1]

    password_hash = user[3]


    if not verify_password(
        request.password,
        password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )


    token = create_access_token(
        username
    )


    return {
        "message": "Login successful",
        "user_id": user_id,
        "username": username,
        "access_token": token,
        "token_type": "bearer"
    }


@app.post("/chat")
def chat_endpoint(
    request: ChatRequest,
    authorization: str = Header(None)
):

    if not authorization:

        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )


    if not authorization.startswith(
        "Bearer "
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid authorization format"
        )


    token = authorization.replace(
        "Bearer ",
        "",
        1
    ).strip()


    username = verify_token(
        token
    )


    if not username:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )


    try:

        history = [
            {
                "role": message.role,
                "content": message.content
            }

            for message in request.history
        ]


        result = chat(
            question=request.question,
            top_k=request.top_k,
            history=history
        )


        return result


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )