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
> If Make or Docker are not installed, follow the instructions below based on your operating system.

### Installing Make and Docker

#### For Debian-based systems (Ubuntu, etc.)

1. **Update your package index:**
   ```bash
   sudo apt update
   ```

2. **Install Make:**
   ```bash
   sudo apt install make -y
   ```

3. **Install Docker:**
   ```bash
    # Remove packages if installed before
    for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done

    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian \
      $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update

    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

4. **Enable and start Docker:**
   ```bash
   sudo systemctl enable --now docker
   ```

5. **Install Docker Compose:**
   Docker Compose is now included in Docker itself. To check if it's available, run:
   ```bash
   docker compose version
   ```

#### For RedHat-based systems (RHEL, Fedora, CentOS)

1. **Update your package index:**
   ```bash
   sudo dnf update
   ```

2. **Install Make:**
   ```bash
   sudo dnf install make -y
   ```

3. **Install Docker:**
   ```bash
   # Remove packages if installed before
   sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-selinux \
                  docker-engine-selinux \
                  docker-engine

   # Add repository
   sudo dnf -y install dnf-plugins-core
   sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

   # Install docker and plugins
   sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

4. **Enable and start Docker:**
   ```bash
   sudo systemctl enable --now docker
   ```

5. **Install Docker Compose:**
   Docker Compose is now included in Docker itself. To check if it's available, run:
   ```bash
   docker compose version
   ```

#### For Arch-based systems (Arch, Manjaro)

1. **Update your package index:**
   ```bash
   sudo pacman -Syu
   ```

2. **Install Make:**
   ```bash
   sudo pacman -S make
   ```

3. **Install Docker:**
   ```bash
   sudo pacman -S docker
   ```

4. **Enable and start Docker:**
   ```bash
   sudo systemctl enable --now docker
   sudo systemctl start docker
   ```

5. **Install Docker Compose:**
   Docker Compose is now part of Docker, to verify its availability:
   ```bash
   docker compose version
   ```

### Notes for macOS and Windows Users
If you're not using a Linux distribution, please find the appropriate installation instructions for [macOS](https://docs.docker.com/desktop/install/mac-install/) or [Windows](https://docs.docker.com/desktop/install/windows-install/) on Docker's official site. Additionally, you can install Make using Homebrew on macOS or via Windows Subsystem for Linux (WSL) on Windows.

If for some reason `docker.service` is not launching just restart your system and try again.

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
