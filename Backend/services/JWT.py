from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from config import SECRET_KEY, ALGORITHM


def create_access_token(data):
    try:
        payload = data.copy()

        expiry = datetime.utcnow() + timedelta(hours=24)
        payload.update ({
            "iat": datetime.utcnow(),
            "exp": expiry,
            "token_type": "access_token"
        })

        to_encode = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return to_encode
    except Exception as e:
        return {"error": f"Failed to create access token {str(e)} "}



def create_refresh_token(data):
    try:
        payload = data.copy()

        expiry = datetime.utcnow() + timedelta(days=7)
        payload.update ({
            "iat": datetime.utcnow(),
            "exp": expiry,
            "token_type": "refresh_token"
        })

        to_encode = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return to_encode
    except Exception as e:
        return {"error": f"Failed to create refresh token {str(e)}"}

def decode_token(token):
    try: 
        to_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return to_decode
    except ExpiredSignatureError:
        return {"error": "Token expired"}
    except JWTError:
        return {"error": "Invalid token"}
    except Exception as e:
        return {"error": str(e)}


 