import os

import bcrypt

from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv

from jose import JWTError, jwt


# =====================================================
# LOAD ENVIRONMENT VARIABLES
# =====================================================

load_dotenv()


# =====================================================
# JWT CONFIGURATION
# =====================================================

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY"
)

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


# =====================================================
# VALIDATE SECRET KEY
# =====================================================

if not SECRET_KEY:

    raise ValueError(
        "JWT_SECRET_KEY is not configured in the .env file"
    )


# =====================================================
# PASSWORD HASHING
# =====================================================

def hash_password(
    password: str
) -> str:

    password_bytes = password.encode(
        "utf-8"
    )

    hashed = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed.decode(
        "utf-8"
    )


# =====================================================
# PASSWORD VERIFICATION
# =====================================================

def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return bcrypt.checkpw(
        plain_password.encode(
            "utf-8"
        ),
        hashed_password.encode(
            "utf-8"
        )
    )


# =====================================================
# CREATE JWT ACCESS TOKEN
# =====================================================

def create_access_token(
    username: str
) -> str:

    expire = (
        datetime.now(
            timezone.utc
        )
        + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


# =====================================================
# VERIFY JWT TOKEN
# =====================================================

def verify_token(
    token: str
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[
                ALGORITHM
            ]
        )

        username = payload.get(
            "sub"
        )

        if username is None:

            return None

        return username

    except JWTError:

        return None
