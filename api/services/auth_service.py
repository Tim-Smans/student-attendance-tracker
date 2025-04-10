from fastapi import Header, HTTPException, Depends
from ..config import API_KEY


def verify_api_key(x_api_key: str = Header(...)):
    """
    Verify that the provided API key matches the expected API key.

    Args:
        x_api_key (str): The API key provided in the request header.

    Raises:
        HTTPException: If the provided API key does not match the expected API key,
                       a 403 Forbidden exception is raised with an "Invalid API Key" message.
    """

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")