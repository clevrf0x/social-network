# Social Networking Application API

## Problem Statement

This project involves creating an API for a social networking application using Django Rest Framework (DRF). The application is designed to be scalable, secure, and efficient, catering to various user functionalities.

## Table of Contents

- [Installation](#installation)
- [Documentation](#documentation)
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
   # The values in .env.example are sufficient for testing. 
   # However, for production, make sure to update the keys accordingly.
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

## Documentation

Navigate to the `docs` folder in the code repository, where you'll find a Postman collection. You can import this collection into Postman for testing the API.


## Security

- For enhanced security, the `postgres` database is not exposed to localhost. It is only accessible within Docker's internal network, meaning external access is restricted, and it can only be accessed through the Django server.
- All critical components of the application, including secret keys, passwords, allowed hosts, and debug mode, are managed through the `.env` file.
- Request rate limiting is implemented based on IP, with a default limit of 50 requests per minute for login endpoints, configurable via the `.env` file.
- The application is protected by CORS, allowing access only from whitelisted domains.

## Architecture (TODO)

### Horizontal Scaling (TODO)


## Usage

1. Install the dependencies as outlined in the [Installation](#installation) section.
2. Set up and run the project.
3. Use the included Postman collection to easily test all API endpoints.

## Notes

If you encounter any issues running this API service, feel free to reach out to me for assistance with troubleshooting.
