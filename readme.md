# KFS API

KFS API is a service designed to search for available flights based on a specified date, origin, and destination. It handles the retrieval of flight events, computes the available journeys (direct or with one connection), and returns them in an easily consumable format. This service is ideal for travel booking systems and can be consumed through its REST API.

---

# 📋 Table of Contents

1. Features
2. Requirements
3. Installation
4. Testing
5. Documentation
6. Access to deployed API.
7. Support



---

# 🚀 Features

- Search for available flights by date, origin, and destination.
- Direct flights (same-day travel).
- Flights with one connection (connections within 24 hours and with a maximum connection time of 4 hours).
- API with Swagger UI for easy interaction and testing.
- Fetch flight events from an external API and filter according to constraints.

---

# ⚙️ Requirements
- Docker (for running the application in a containerized environment).
- Git (for clone).

---

# 📦 Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/luisgonzalocao/kfs-api.git
    cd kfs-api
    ```

2. Copy the example environment file:s
    ```bash
    cp .env.example .env
    ```

3. Build with Docker:
    ```
    docker build -t kfs-api .
    ```

4. Start API Server:
    ```
    docker run --env-file .env -p 8000:8000 kfs-api
    ```

---

# ✅ Testing

1. Run tests:
    ```bash
    docker run --rm --env-file .env -it kfs-api pytest
    ```

#  📝 Documentation

The API's Swagger UI provides an interactive interface.

You can access it directly in local at: http://localhost:8000/docs/


# 🚀 API Deployed
- api url:  https://kfs-api-a119fbfb4496.herokuapp.com/
- api docs: https://kfs-api-a119fbfb4496.herokuapp.com/docs/


#  📧 Support
For any issues or questions, feel free to reach out to Luis Gonzalo Cao.        
email: luisgonzalocao@gmail.com           
linkedin: https://linkedin.com/in/luis-gonzalo-cao

---