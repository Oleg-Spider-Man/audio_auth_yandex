from datetime import datetime, timedelta, timezone
from jose import jwt
from starlette.responses import JSONResponse
from my_app.config import SECRET_KEY

current_time = datetime.now(timezone.utc)
async def cr_token(openid: str):
    token = jwt.encode({
        "sub": openid,
        "exp": current_time + timedelta(minutes=60)
    }, SECRET_KEY, algorithm="HS256")
    return token
    # return JSONResponse({
    #     "access_token": token,
    #     "token_type": "bearer",
    #     "expires_in": 3600
    # })
