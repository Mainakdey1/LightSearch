from fastapi import FastAPI, Request, HTTPException
import redis
import time
from jose import jwt, JWTError
from fastapi.security import HTTPBearer
 
app = FastAPI()

security = HTTPBearer()
SECRET_KEY = 'secretasf'
ALGORITHM = 'HS256'

redis_client = redis.Redis(host = 'localhost', port=6379, db=0, decode_responses=True)

RATE_LIMITS = {'/': 5, '/health' : 20}
WINDOW_SIZE = 60

def get_user_from_jwt(request: Request):
    auth = request.headers.get('Authorization')
    if not auth or not auth.startswith('Bearer'):
        return None
    token = auth.split(' ')[1]
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub')
    except JWTError:
        return None
    

def rate_limiter(request: Request):
    client_ip = request.client.host
    path = request.url.path

    user_id = get_user_from_jwt(request)

    if user_id:
        key = f'rate_limit:user:{user_id}:{path}'
    else:
        key = f'rate_limit:ip:{client_ip}:{path}'
    limit = RATE_LIMITS.get(path, 10)
    current = redis_client.get(key)

    if current is None:
        redis_client.set(key, 1, ex=WINDOW_SIZE)
        return
    if int(current) >= limit:
        raise HTTPException(status_code=429,
                            detail="Too many requests. Please try again later.")
    redis_client.incr(key)
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    rate_limiter(request)
    response = await call_next(request)
    return response

@app.get('/')
def root():
    return {'message': 'Hello, you are within the rate limit'}
@app.get('/health')
def health():
    return {'status': 'ok'}
    
