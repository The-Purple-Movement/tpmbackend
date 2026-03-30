import os
import time
from typing import Dict
from fastapi import Request, HTTPException, status


class RateLimiter:
    def __init__(self, requests_limit: int, window_seconds: int):
        self.requests_limit = requests_limit
        self.window_seconds = window_seconds
        # This will be our "In-Memory" storage
        # Format: { "ip_address": {"attempts": int, "reset_at": float} }
        self.store: Dict[str, dict] = {} #{str: {int, float}}

    # making objects into callable functions
    async def __call__(self, request: Request):
        # Bypass rate limiting during tests if necessary
        if os.getenv("TESTING") == "True":
            return

        # 1. Get the user's IP address
        user_ip = request.client.host
        now = time.time()
        
        # 2. If the user hasn't sent any requests yet, 
        # initialize their data
        if user_ip not in self.store:
            self.store[user_ip] = {
                "attempts": 1,
                "reset_at": now + self.window_seconds
            }
            return # Let them pass!

        # otherwise the user must have sent requests before, 
        # so get their data first
        user_data = self.store[user_ip]

        # 3. Check if the window has passed
        if now > user_data["reset_at"]:
            # Reset the attempts and window
            user_data["attempts"] = 1
            user_data["reset_at"] = now + self.window_seconds
            return

        #! 4. If window is active, 
        # check the attempts
        # and if its greater than or equal to the requests limit
        # then raise an exception
        if user_data["attempts"] >= self.requests_limit:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later."
            )

        # 5. Increment the attempts and let them pass
        user_data["attempts"] += 1



# Algorithm
# 1. Get the user's IP address
# 2. If the user hasn't sent any requests yet, 
# initialize their data
# 3. Check if the window has passed
# 4. If window is active, check the attempts
# and if its greater than or equal to the requests limit
# then raise an exception
# 5. Increment the attempts and let them pass