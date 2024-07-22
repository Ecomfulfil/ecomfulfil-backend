from datetime import timedelta

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=365),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "SIGNING_KEY": "224602163826f289290e9267f1e4c5c18178c7fb73ace7201278d83d3244e53a",
    "UPDATE_LAST_LOGIN": True,
    "USER_ID_FIELD": "account_number",
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}
