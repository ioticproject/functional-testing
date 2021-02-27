import logging
import os
import sys


# Check all the required environment variables
if not (HOST := os.getenv('HOST')):
    sys.exit('The host name must be provided '
             'through the "HOST" environment variable!')

if not (EXPOSED_PORT := os.getenv('EXPOSED_PORT')):
    sys.exit('The port must be provided '
             'through the "EXPOSED_PORT" environment variable!')

if not (ADMIN_PASSWORD := os.getenv('ADMIN_PASSWORD')):
    sys.exit('The admin password must be provided '
             'through the "ADMIN_PASSWORD" environment variable!')

if not (ADMIN_USERNAME := os.getenv('ADMIN_USERNAME')):
    sys.exit('The admin username must be provided '
             'through the "ADMIN_USERNAME" environment variable!')
    
CLIENT_PASSWORD = os.getenv('CLIENT_PASSWORD')
CLIENT_USERNAME = os.getenv('CLIENT_USERNAME')

HEALTH = os.getenv('HEALTH')

AUTH = os.getenv('AUTH')
USER_LOGIN = os.getenv('USER_LOGIN')
GET_USERS = os.getenv('GET_USERS')
ADD_USER = os.getenv('ADD_USER')
DELETE_USER = os.getenv('DELETE_USER')
UPDATE_USER = os.getenv('UPDATE_USER')

GET_DEVICES = os.getenv('GET_DEVICES')
ADD_DEVICE = os.getenv('ADD_DEVICE')
DELETE_DEVICE = os.getenv('DELETE_DEVICE')
UPDATE_DEVICE = os.getenv('UPDATE_DEVICE')
GET_USER_DEVICES = os.getenv('GET_USER_DEVICES')

GET_SENSORS = os.getenv('GET_SENSORS')
ADD_SENSORS = os.getenv('ADD_SENSORS')
DELETE_SENSORS = os.getenv('DELETE_SENSORS')
UPDATE_SENSORS = os.getenv('UPDATE_SENSORS')
GET_DEVICE_SENSORS = os.getenv('GET_DEVICE_SENSORS')
GET_USER_SENSORS = os.getenv('GET_USER_SENSORS')

GET_DATA = os.getenv('GET_DATA')
ADD_DATA = os.getenv('ADD_DATA')
DELETE_DATA = os.getenv('DELETE_DATA')
GET_SENSOR_DATA = os.getenv('GET_SENSOR_DATA')
GET_FILTERED_SENSOR_DATA = os.getenv('GET_FILTERED_SENSOR_DATA')

# verbose settings
VERBOSE = int(os.getenv('VERBOSE'))

# default Flask port, on this port all microservices will be exposed internally.
EXPOSED_PORT = int(os.getenv('EXPOSED_PORT'))

HEALTH_URL = f"http://{HOST}:{EXPOSED_PORT}/{HEALTH}"

AUTH_URL = f"http://{HOST}:{EXPOSED_PORT}/{AUTH}"
USER_LOGIN_URL = f"http://{HOST}:{EXPOSED_PORT}/{USER_LOGIN}"
GET_USERS_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_USERS}"
ADD_USER_URL = f"http://{HOST}:{EXPOSED_PORT}/{ADD_USER}"
DELETE_USER_URL = f"http://{HOST}:{EXPOSED_PORT}/{DELETE_USER}"
UPDATE_USER_URL = f"http://{HOST}:{EXPOSED_PORT}/{UPDATE_USER}"

GET_DEVICES_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_DEVICES}"
ADD_DEVICE_URL = f"http://{HOST}:{EXPOSED_PORT}/{ADD_DEVICE}"
DELETE_DEVICE_URL = f"http://{HOST}:{EXPOSED_PORT}/{DELETE_DEVICE}"
UPDATE_DEVICE_URL = f"http://{HOST}:{EXPOSED_PORT}/{UPDATE_DEVICE}"
GET_USER_DEVICES_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_USER_DEVICES}"

GET_SENSORS_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_SENSORS}"
ADD_SENSORS_URL = f"http://{HOST}:{EXPOSED_PORT}/{ADD_SENSORS}"
DELETE_SENSORS_URL = f"http://{HOST}:{EXPOSED_PORT}/{DELETE_SENSORS}"
UPDATE_SENSORS_URL = f"http://{HOST}:{EXPOSED_PORT}/{UPDATE_SENSORS}"
GET_DEVICE_SENSORS_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_DEVICE_SENSORS}"
GET_USER_SENSORS_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_USER_SENSORS}"

GET_DATA_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_DATA}"
ADD_DATA_URL = f"http://{HOST}:{EXPOSED_PORT}/{ADD_DATA}"
DELETE_DATA_URL = f"http://{HOST}:{EXPOSED_PORT}/{DELETE_DATA}"
GET_SENSOR_DATA_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_SENSOR_DATA}"
GET_FILTERED_SENSOR_DATA_URL = f"http://{HOST}:{EXPOSED_PORT}/{GET_FILTERED_SENSOR_DATA}"


payload_admin_account = str({'username': ADMIN_USERNAME, 'password': ADMIN_PASSWORD}).replace("\'", "\"")
payload_client_account = str({'username': CLIENT_USERNAME, 'password': CLIENT_PASSWORD}).replace("\'", "\"")


C = 5
N = 50
rq_range = [5, 10, 25, 50, 100, 250, 500, 1000, 1500]
concurency_range = [5, 10, 15, 20, 25, 50, 50, 50, 50]
rq_per_s = []
time_per_rq = []
time_per_rq_c = []
transfer_rate = []
connect_time = []
processing_time = []
waiting_time = []
failed_rq = []
reqs = []

# Configure Logging
# LoggingConfig.disable_default_loggers()
# LoggingConfig.configure_app_logger()
LOGGER = logging.getLogger(__name__)
