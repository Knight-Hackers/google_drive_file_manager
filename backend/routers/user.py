# user.py - user specific routes
from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import requests
import urllib.parse

router = APIRouter()

CLIENT_ID = "1036975395025-cr4f5c03p4o3v38a7m4tnsllja3njl0v.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8000/user/oauth2callback"
SCOPE = "https://www.googleapis.com/auth/drive.readonly email profile"

# Step 1: redirect user to Google login
@router.get("/login")
def login_with_google():
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    return RedirectResponse(url)

# Step 2: handle callback and exchange code for token
@router.get("/oauth2callback")
def oauth2callback(request: Request):
    code = request.query_params.get("code")
    if not code:
        return {"error": "No code returned from Google"}

    # Exchange code for access token
    token_endpoint = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    resp = requests.post(token_endpoint, data=data)
    tokens = resp.json()  # contains access_token and refresh_token

    # You now have the access token to call your endpoints
    frontend_redirect=f"http://localhost:5173/oauth-callback?access_token={tokens['access_token']}"
    return RedirectResponse(frontend_redirect) 

