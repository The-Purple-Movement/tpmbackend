import pytest
from unittest.mock import patch
import time
import os

PREFIX = "/api/v1/bs"

def test_rate_limiting_login(client, db):
    # Enable rate limiting just for this test
    with patch.dict(os.environ, {"TESTING": "False"}):
        # 1. First five requests should pass the rate limiter
        for i in range(5):
            response = client.post(
                f"{PREFIX}/login",
                json={"email": f"ratelimit{i}@nonexistent.com", "password": "any"}
            )
            assert response.status_code == 401 

        # 2. Sixth request should be BLOCKED (429)
        response = client.post(
            f"{PREFIX}/login",
            json={"email": "ratelimit5@nonexistent.com", "password": "any"}
        )
        assert response.status_code == 429
        assert response.json()["detail"] == "Too many requests. Please try again later."

        # 3. Simulate 61 seconds passing using a mock
        # This proves our "Window Expiration" logic works
        future_time = time.time() + 61
        with patch("time.time", return_value=future_time):
            response = client.post(
                f"{PREFIX}/login",
                json={"email": "ratelimit3@nonexistent.com", "password": "any"}
            )
            # Should pass the rate limiter again!
            assert response.status_code == 401
