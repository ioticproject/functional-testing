#### Build integration_tests image

    docker build -t testing:latest .

### Run tests
    docker-compose up && docker-compose down

    docker run --rm --env-file=.env --network=backend testing pytest
