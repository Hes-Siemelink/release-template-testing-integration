
# Digital.ai Release Tester Plugin

Test your templates with this plugin. You can run templates and replace integration tasks with mock tasks. 
This way you will have fast and predicatable results when testing your templates.

---
## How to build and run

### Prerequisites

You need to have the following installed in order to develop Python-based container tasks for Release using this project:

* Python 3
* Git
* Docker

### Start Release

We will run Release within a local Docker environment. In the development setup, the Release server will manage containerized tasks in Docker.

Start the Release environment with the following command

```commandline
cd dev-environment
docker compose up -d --build
```

### Configure your `hosts` file

The Release server needs to be able to find the container images of the integration you are creating. In order to do so the development setup has its own registry running inside Docker. Add the address of the registry to your local machine's `hosts` file.

**Unix / macOS**

Add the following entry to `/etc/hosts` (sudo privileges is required to edit):

    127.0.0.1 container-registry

**Windows**

Add the following entry to `C:\Windows\System32\drivers\etc\hosts` (Run as administrator permission is required to edit):

    127.0.0.1 container-registry


### Build & publish the plugin

Run the build script

**Unix / macOS**

```commandline
sh build.sh --upload
```

**Windows**

```commandline
build.bat --upload
```

The above command builds the zip, creates the container image, and then pushes the image to the configured registry and installs the plugin in the running Release server..


### 6. Clean up

Stop the development environment with the following command:

    docker compose down

---

# TODO

* Support tasks in reference releases with no variable in output
* Support Create Release task in templates that are mocked
* Support multiple mock types
* Support Jython script tasks as mock types (currently only container)