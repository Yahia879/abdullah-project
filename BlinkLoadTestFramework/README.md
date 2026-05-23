# Blink System Load Testing Framework

A comprehensive performance testing framework built with Locust for the Blink System platform. This framework simulates real user behavior across multiple applications and services in the Blink ecosystem.

## 🏗️ Architecture Overview

The framework is designed to test multiple applications within the Blink System:

- **OrgApp**: Organization management and logistics
- **Admission**: User admission and verification
- **Shop**: Badge and merchandise management
- **EventApp**: Real-time event interactions
- **EventAppSync**: GraphQL-based data synchronization

## 📁 Project Structure

```
BlinkSystemLoadTest/
├── apis/                          # API modules for each application
│   ├── base_api.py               # Shared utilities and data generators
│   ├── orgapp/                   # Organization app APIs
│   ├── admission/                # Admission system APIs
│   ├── shop/                     # Shop system APIs
│   └── eventapp/                 # Event app APIs
├── resources/                     # Test data files
│   ├── full_users_data.xlsx      # User data for testing
│   ├── session_ids.csv           # Session IDs for testing
│   ├── attendees.json            # Attendee data
│   └── users.csv                 # Additional user data
├── outputs/                       # Test results and logs
├── locustfile.py                 # Main Locust configuration
└── README.md                     # This file
```

## 🛠️ Tools and Libraries

### Core Dependencies
- **Locust**: Main load testing framework
- **Python 3.7+**: Runtime environment
- **pandas**: Data manipulation for test data
- **requests**: HTTP client library (via Locust)

### Key Features
- **Multi-Application Testing**: Tests 5 different applications simultaneously
- **Realistic Data Generation**: Uses real user data from Excel/CSV files
- **Error Logging**: Comprehensive error tracking and reporting
- **Custom Headers**: Application-specific authentication and headers
- **Task Weighting**: Realistic task distribution based on usage patterns

## 🚀 Getting Started

### Prerequisites
```bash
pip install locust pandas openpyxl
```

### Running the Tests

#### Basic Run
```bash
locust -f locustfile.py
```

#### With Custom Parameters
```bash
locust -f locustfile.py --host=https://your-api-endpoint.com --users 100 --spawn-rate 10
```

#### Headless Mode (for CI/CD)
```bash
locust -f locustfile.py --headless --users 50 --spawn-rate 5 --run-time 300s
```

## 👥 User Classes

### 1. OrgAppUser
### 2. AdmissionUser
### 3. ShopUser
### 4. EventAppUser
### 5. EventAppSyncUser


## 📊 Outputs and Results

### 1. Real-time Metrics
- **Response Times**: Average, median, 95th percentile
- **Request Rates**: Requests per second
- **Error Rates**: Failed requests percentage
- **User Count**: Active users over time

### 2. Error Logging (`error_offset.json`)
The framework automatically logs all errors to `error_offset.json`:

```json
{
  "timestamp": 1703123456.789,
  "datetime": "2023-12-21 10:30:56",
  "request_type": "POST",
  "name": "EventApp-UpdateProfile",
  "response_time_ms": 1250,
  "status_code": 500,
  "response_text": "Internal server error...",
  "request_body": {
    "user_id": "12345",
    "profile_data": {...}
  },
  "exception": "Connection timeout",
  "stack_trace": "..."
}
```

### 3. Locust Web Interface
Access the web interface at `http://localhost:8089` to:
- Monitor real-time metrics
- Start/stop tests
- View detailed statistics
- Download CSV reports

### 4. CSV Reports
Locust generates detailed CSV reports including:
- Request statistics
- Response time distributions
- Error summaries
- User behavior patterns

## 🔧 Configuration

### Environment Variables
```bash
export LOCUST_HOST=https://your-api-endpoint.com
export LOCUST_USERS=100
export LOCUST_SPAWN_RATE=10
```

### Custom Headers
Each user class uses application-specific headers defined in `apis/base_api.py`:
- Authentication tokens
- Content-Type specifications
- User-Agent strings
- Origin headers

### Data Sources
The framework uses real data from:
- `resources/full_users_data.xlsx`: User profiles and SSO IDs
- `resources/session_ids.csv`: Session identifiers
- `resources/attendees.json`: Attendee information


## 🐛 Troubleshooting

### Common Issues
1. **Authentication Errors**: Check token validity in `base_api.py`
2. **Data Loading Issues**: Verify Excel/CSV files in `resources/`
3. **Network Timeouts**: Adjust timeout settings in Locust
4. **Memory Issues**: Reduce user count or spawn rate


## 🔒 Security Considerations

- **Token Management**: Authentication tokens are embedded in headers
- **Data Privacy**: Test data should not contain sensitive information
- **Rate Limiting**: Respect API rate limits during testing
- **Environment Isolation**: Use separate environments for testing

## 📝 Contributing

1. Follow the existing API module structure
2. Add appropriate error handling
3. Include realistic task weights
4. Update documentation for new features
5. Test with various load scenarios

## 📄 License

This framework is designed for internal Blink System testing and should not be used for unauthorized load testing of external systems.

---

**Note**: This framework is specifically designed for the Blink platform and includes custom authentication, data generation, and error handling mechanisms tailored to the system's architecture. 