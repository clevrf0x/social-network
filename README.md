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
- Docker Compose (included with Docker)

> This guide assumes you have `make`, `docker`, and the `docker compose` plugin installed.  
> If you need to install Make or Docker, please follow the instructions [here](INSTALLATION.md) for your operating system.

### Steps

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/clevrf0x/social-network
   cd social-network
   ```

2. **Set Up Environment Variables:**

   ```bash
   # The values in .env.example are sufficient for testing. 
   # For production use, ensure you update the keys appropriately.
   cp .env.example .env
   ```

3. **Run Migrations:**

   ```bash
   make migrate
   ```

4. **Start the Application:**

   ```bash
   make run
   ```

## Documentation

Navigate to the `docs` folder in the code repository, where you will find a Postman collection. Import this collection into Postman to test the API. 

I've included a Postman script that automatically sets up the required tokens inside the collection variables after you log in successfully, minimizing manual steps needed to test the protected API endpoints.

To test the User Endpoints with Role-Based Access Control (RBAC) implemented, you'll need:

- A staff account for creating and updating user accounts.
- A super admin account for deleting users.

Since I have disabled the default Django admin endpoints, I created two Make commands for easier management: `make createsuperuser` for super admin accounts and `make createstaffuser` for staff accounts. If you need assistance, run `make help` to see the available commands and their usage.

The RBAC implementation allows:

- **Normal Users**: View all non-blocked user accounts and search through them.
- **Staff Users**: Access all user accounts and perform full or partial updates, as well as create new accounts.
- **Super Admins**: Have all the permissions above, plus the ability to delete user accounts.


## Security

- For enhanced security, the `postgres` database is not exposed to localhost. It is only accessible within Docker's internal network, meaning external access is restricted, and it can only be accessed through the Django server.
- All critical components of the application, including secret keys, passwords, allowed hosts, and debug mode, are managed through the `.env` file.
- Request rate limiting is implemented based on IP, with a default limit of 200 requests per hour for login endpoints, configurable via the `.env` file.


## Architecture 

Our current setup consists of a single Docker Compose multi-container environment that includes our application server, PostgreSQL database, and Redis instance, all operating within an isolated internal Docker network. This network is accessible only to our web server, which works well for the development environment. However, this configuration is not scalable for production deployments.

![Development Server Architecture](dev-server.jpg?raw=true "Development Server Architecture")

### Horizontal Scaling

To achieve horizontal scaling for our application, we need to decouple our services. For the database, we can utilize a managed service like AWS RDS or host our own PostgreSQL instance on a dedicated server that all our scaled application instances can access. 

Similarly, we should decouple the Redis instance to avoid cache misses; a centralized cache storage server will help maintain performance. 

Once we have these services decoupled, we can deploy multiple application instances behind a load balancer. Users will communicate with this load balancer, which will route traffic according to our requirements, such as round-robin or least-used server strategies. 

To monitor the health of our application instances, I’ve implemented an endpoint at `api/v1/healthcheck`. The response will resemble the following structure:

```json
{
    "status": "healthy",
    "timestamp": "2024-10-02T08:06:51.054470",
    "database": true,
    "memory_usage": {
        "total": "15.37 GB",
        "available": "7.94 GB",
        "percent": "48.3%",
        "limit": "15.37 GB"
    },
    "cpu_usage": "11.5%"
}
```

This endpoint allows us to assess the health of each application instance, helping us decide whether to route traffic to a particular instance. 

![Production Server Architecture](prd-server.jpg?raw=true "Production Server Architecture")


## Usage

1. Install the dependencies as described in the [Installation](#installation) section.
2. Set up and run the project.
3. Utilize the provided Postman collection to test all API endpoints effortlessly.
4. For administrative commands, use `make` or `make help`.


## Notes

If you encounter any issues running this API service, feel free to reach out to me for assistance with troubleshooting.
