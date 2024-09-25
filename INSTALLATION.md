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

> If for some reason `docker.service` is not launching just restart your system and try again.
