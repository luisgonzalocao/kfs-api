Kiu Flight Service

kfs-api/                    # Root directory of the project
│── kfs/                    # Main module
│   │── __init__.py         # Marks `kfs` as a package
│   │── main.py             # FastAPI main file
│   │
│   ├── clients/            # External API clients module
│   │   │── __init__.py
│   │   ├── flight_api.py   # Flight API client
│   │
│   ├── tests/              # Tests module
│   │   │── __init__.py
│   │   ├── test_main.py    # Endpoint test
│   │   ├── test_flight_api.py  # API client test
│
│── requirements.txt        # Project dependencies
│── .gitignore              # Git ignored files
│── Dockerfile              # Dockerfile for containerization
│── docker-compose.yml      # Docker Compose setup
│── README.md               # Project documentation
│── .github/workflows/ci.yml # CI/CD configuration
