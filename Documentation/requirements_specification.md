# Requirements Specification

## Application Purpose

The application is designed to manage **Magic: The Gathering** cards. It allows users to maintain a digital archive of their physical cards and perform various searches based on attributes such as card colors or mana costs. Cards are retrieved through the **Scryfall.com API**. The application supports multiple users, each of whom must register to access the system.

## Users

The application has only one user role: **normal user**. An **admin role** could be added later if needed.

## User Interface

At the start, the application displays a **login view**, where users can either log in or navigate to a user registration view. Once logged in, the user is directed to the **main view**, where they can add new cards to the database and search or list existing cards.

## Core Functionality

### Before Logging In

- Users can create an account ("done")
  - The username must be unique and at least **3 characters** long.
  - The password must be at least **12 characters** long.
- Users can log in ("done")
  - If the username does not exist or the password is incorrect, the system notifies the user.

### After Logging In

- The user sees the main interface. ("done")
- Users can add new cards to the database one at a time based on the name of the card.
  - Each user only sees their own cards.
- Users can search for cards using different kinds of filters, such as:
  - all cards
  - black cards
  - cards from a specific set
  - cards that cost three red mana
  - etc.
- Users can delete cards from the database.
- Users can log out. ("done")

## Future Development Ideas

The basic version of the application could be expanded with the following features:

- Clicking a card to view a larger image.
- Adding more advanced filtering options.
- Storing and managing prebuilt decks.
- Show card resale prices
- Show total count of each individual card
