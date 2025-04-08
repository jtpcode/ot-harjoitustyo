# Architecture Description

## Structure

The application has the following code package structure:

![Package Structure](./pics/architecture_package.png)

The **ui** package contains the code responsible for the user interface, **services** handles the application logic, and **repositories** is responsible for data persistence. The **entities** package contains classes that represent the data objects used by the application.

## Application Logic

The following class/package diagram describes the application logic and relationship between the MagicService class and the rest of the application:

**NOTE: in the future diagram will include classes/packages responsible for connecting to Scryfall API**

![Package Structure and Classes](./pics/architecture_package_classes.png)