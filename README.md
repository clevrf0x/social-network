# Social Networking Application API

## Problem Statement

This project involves creating an API for a social networking application using Django Rest Framework (DRF). The application is designed to be scalable, secure, and efficient, catering to various user functionalities.

## Table of Contents

- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Design Choices](#design-choices)
- [Features](#features)
- [Architecture](#architecture)
- [Security](#security)
- [Usage](#usage)
- [Additional Notes](#notes)

## Installation

### Prerequisites

- Make
- Docker
- Docker Compose (available as part of Docker)

> I am going to assume you have `make`, `docker`, and the `docker compose` plugin installed.  
> If Make or Docker are not installed, follow the instructions [here](INSTALLATION.md) based on your operating system.

### Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/clevrf0x/social-network
   cd social-network
   ```

2. **Set Up Environment Variables:**

   ```bash
   # The values in .env.example are sufficient for testing. However, for production, make sure to update the keys accordingly.
   cp .env.example .env
   ```

3. **Run migrations:**

   ```bash
   make migrate
   ```

4. **Run the application:**

   ```bash
   make run
   ```

## API Documentation

Navigate to the `docs` folder in the code repository, where you'll find a Postman collection. You can import this collection into Postman for testing the API.


## Design Choices

- **Database:** PostgreSQL is used for its advanced features and full-text search capabilities.
- **Caching:** Django’s built-in cache framework is employed to optimize response times.
- **Token-based Authentication:** JWT tokens are used for secure authentication and role-based access control (RBAC).
- **Rate Limiting:** Implemented to enhance security on sensitive endpoints.
- **Atomic Operations:** Ensured for friend request management to handle race conditions.

## Features

- **User Authentication:** Email-based signup and login with token refresh capabilities.
- **User Search:** Efficient searching through full-text search capabilities.
- **Friend Management:** Robust friend request handling with blocking features.
- **Activity Logging:** User activities are logged for notification purposes.
- **Security Measures:** Sensitive data is encrypted, and common vulnerabilities are mitigated.

## Security

- For enhanced security, the `postgres` database is not exposed to localhost. It is only accessible within Docker's internal network, meaning external access is restricted, and it can only be accessed through the Django server.
- All critical components of the application, including secret keys, passwords, allowed hosts, and debug mode, are managed through the `.env` file.
- Request rate limiting is implemented based on IP, with a default limit of 50 requests per minute, configurable via the `.env` file.
- The application is protected by CORS, allowing access only from whitelisted domains.

## Architecture (TODO)

### Horizontal Scaling (TODO)


## Usage

- Install the dependencies as outlined in the [Installation](#installation) section.
- Set up and run the project.
- Use the included Postman collection to easily test all API endpoints.

## Notes

If you encounter any issues running this API service, feel free to reach out to me for assistance with troubleshooting.
