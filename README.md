# User endpoints

The user profile endpoints require you to be logged in. They use the
`access_token` HTTP-only cookie set when you log in.

## Receive and send the authentication cookie

Log in by sending your username and password as form data to `POST /auth/token`:

```bash
curl -i -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=YOUR_USERNAME" \
  --data-urlencode "password=YOUR_PASSWORD" \
  -c cookies.txt
```

The response includes a `Set-Cookie` header for `access_token`. The `-c
cookies.txt` option saves it; pass `-b cookies.txt` on later requests so curl
sends it:

```bash
curl http://localhost:8000/users/me -b cookies.txt
```

The cookie is `HttpOnly`, so browser JavaScript cannot read it with
`document.cookie`. Browsers store and send it automatically. For a frontend
running on a different origin, include credentials in fetch requests:

```javascript
const response = await fetch("http://localhost:8000/users/me", {
  credentials: "include",
});
```

Use `credentials: "include"` for the login request too. The API must allow
credentials and the frontend origin must be listed in `CORS_ORIGINS`.

The cookie is marked `Secure` by default, which requires HTTPS. For local
development over HTTP, set `COOKIE_SECURE=false` in the API environment.

## Get your profile

`GET /users/me` returns the profile associated with the authenticated cookie:

```http
GET /users/me
Cookie: access_token=...
```

Example response:

```json
{
  "id": 1,
  "username": "jdoe",
  "first_name": "Jane",
  "last_name": "Doe",
  "date_of_birth": "1990-01-15",
  "phone_number": "555-0100",
  "email": "jane@example.com",
  "address": "123 Main Street"
}
```

## Update your profile

`PATCH /users/me` updates only the fields included in the JSON body. The
authenticated user's ID comes from the cookie; you do not send a user ID.

```http
PATCH /users/me
Content-Type: application/json
Cookie: access_token=...

{
  "first_name": "Janet",
  "address": "45 Oak Avenue"
}
```

The endpoint returns the updated profile. Editable fields are `username`,
`first_name`, `last_name`, `date_of_birth`, `phone_number`, `email`, and
`address`.