# Requirements Specification

## Application Purpose

The application is designed to manage **Magic: The Gathering** cards. It allows users to maintain a digital archive of their physical cards. Cards are retrieved through the **Scryfall.com API**. The application supports multiple users, each of whom must register to access the system.

## Users

The application has only one user role: **normal user**.

## User Interface

At the start, the application displays a **login view**, where users can either log in or navigate to a **registration view**. Once logged in, the user is directed to the **card view**, where they can add new cards or remove cards from their collection.

## Core Functionality

### Before Logging In

- User can create an account &check;
  - The username must be unique and at least **3 characters** long. &check;
  - The password must be at least **12 characters** long. &check;
- User can log in &check;
  - If the username does not exist or the password is incorrect, the system notifies the user. &check;

### After Logging In

- The user sees the card view. &check;
- Users can add new cards to their collection one at a time based on the name and set of the card. &check;
  - Each user only sees their own cards. &check;
- Users can remove cards from their collection.&check;
- Users can log out. &check;

## Future Development Ideas

The application could be expanded with the following features and lots more:

- Different kinds of search options
- Clicking a card to view a larger image.
- Remove cards using UI, ie. clicking specific card
- Show card resale prices
- Show total count of each individual card in collection
- Storing and managing prebuilt decks.
