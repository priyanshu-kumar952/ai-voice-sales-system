import time

from fastapi import HTTPException, Request

from app.core.redis import redis_client


BUCKET_CAPACITY = 60
REFILL_RATE = 1.0  # tokens per second


TOKEN_BUCKET_SCRIPT = """
local key = KEYS[1]

local capacity = tonumber(ARGV[1])
local refill_rate = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

local data = redis.call("HMGET", key, "tokens", "timestamp")

local tokens = tonumber(data[1])
local timestamp = tonumber(data[2])

if tokens == nil then
    tokens = capacity
    timestamp = now
end

local elapsed = math.max(0, now - timestamp)
tokens = math.min(capacity, tokens + (elapsed * refill_rate))

local allowed = 0

if tokens >= 1 then
    tokens = tokens - 1
    allowed = 1
end

redis.call("HSET", key, "tokens", tokens, "timestamp", now)
redis.call("EXPIRE", key, 120)

return {allowed, tokens}
"""


rate_limit_script = redis_client.register_script(TOKEN_BUCKET_SCRIPT)


async def rate_limit(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"

    result = rate_limit_script(
        keys=[key],
        args=[
            BUCKET_CAPACITY,
            REFILL_RATE,
            time.time(),
        ],
    )

    allowed = int(result[0])

    if not allowed:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
        )