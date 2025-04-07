# Changelog

## Viikko 3

- User can see the "login" and "create user" views
- Added local SQLite database access
- Added UserRepository class for handling User database actions
- Added MagicService class for handling application logic
- Added tasks for quick CLI start and testing
- 'Create user' -button creates a new user into the database
- UserRepository tested for "create new user" and "find all users"

## Viikko 4

- User can login and logout
- Error message is shown if login credentials are not correct
- Successfull account creation directs user to "card management" view
- Error message is shown if username already exists when creating a new account
- Successfull login directs user to "card management" view
- User can see the "card management" view
- Logout directs user to "login" view
