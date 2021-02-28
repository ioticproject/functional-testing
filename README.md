#### Build integration_tests image

    docker build -t testing:latest .

### Run tests
    docker-compose up --remove-orphans && docker-compose down

    docker run --rm --env-file=.env --network=backend testing pytest

    # For attaching to the test container, you can run the previous 
    # command with the -ti flag:
    docker run -ti --rm --env-file=.env --network=backend testing pytest bash

