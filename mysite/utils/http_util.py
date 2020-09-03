def get_Authorization_token(req):
	http_auth_key = req.META["HTTP_AUTHORIZATION"]
	_, _, key = http_auth_key.partition(" ")
	return key