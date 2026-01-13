# Digital Library REST API

## Docker Execution

### Docker Compose

```bash
# Put the services up
docker-compose up -d

# See logs
docker-compose logs -f

# Put the services down
docker-compose down
```

Docker was chosen for the facility it brings to deploy an application, as it allows only one command to be executed and runs on every platform.

### Endpoints

- API: http://localhost:8000
- PostgreSQL: localhost:5432

### DB credentials

- Database: library
- User: library_user
- Password: library_pass
