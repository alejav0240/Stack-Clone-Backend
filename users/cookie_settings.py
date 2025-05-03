COOKIE_SETTINGS = {
    'httponly': True,
    'secure': True,
    'samesite': 'Lax',
    'domain': None  # Set this in production
}

ACCESS_TOKEN_MAX_AGE = 300  # 5 minutes
REFRESH_TOKEN_MAX_AGE = 86400  # 24 hours