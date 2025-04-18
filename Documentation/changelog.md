# Changelog

## Week 3

- User can see the "login" and "create user" views
- Added local SQLite database access
- Added UserRepository class for handling User database actions
- Added MagicService class for handling application logic
- Added tasks for quick CLI start and testing
- 'Create user' -button creates a new user into the database
- UserRepository tested for "create new user" and "find all users"

## Week 4

- User can login and logout
- Error message is shown if login credentials are not correct
- Error message is shown if username already exists when creating a new account
- Successfull account creation directs user to "login" view
- Successfull login directs user to "card management" view
- User can see the "card management" view
- Logout directs user to "login" view
- UserRepository tested for "find by username"
- MagicService tested for "login" and "create user"

## Week 5

- Separate database environment for testing created
- Hide password characters in UI
- Add notification of successfull user creation
- Move helper functions/files to 'utils' directory
- Add CardRepository for fetching cards from api.scryfall.com and storing them in Sqlite
- Initial version of "Magic card view" for fetching and showing Magic cards
- Fetching cards from api.scryfall.com works, currently only prints the name in terminal
- CardRepository tested for "fetch_card_by_name_and_set"

