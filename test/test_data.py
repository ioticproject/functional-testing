# import pytest
# from utils import SharedValues
# from utils import template_get, template_post
# from config import (
#     payload_client_account,
#     GET_DATA_URL,
#     ADD_DATA_URL,
#     GET_SENSOR_DATA_URL,
#     rq_per_s, time_per_rq, time_per_rq_c,
#     transfer_rate,
#     connect_time, processing_time, waiting_time,
#     failed_rq,
#     reqs
# )


# @pytest.fixture(autouse=True)
# def run_before_tests():
#     rq_per_s.clear()
#     time_per_rq.clear()
#     time_per_rq_c.clear()
#     transfer_rate.clear()
#     connect_time.clear()
#     processing_time.clear()
#     waiting_time.clear()
#     failed_rq.clear()
#     reqs.clear()


# def test_get_data():
#     json_path = str('test/helper_jsons/admin_credentials.json')
#     template_post(GET_DATA_URL,
#                   'get_data',
#                   json_path=json_path)

#     assert True


# def test_add_data():
#     json_path = str('test/helper_jsons/new_data.json')
#     template_post(ADD_DATA_URL,
#                   'add_data',
#                   json_path=json_path)

#     assert True


# def test_get_sensor_data():
#     template_get(GET_SENSOR_DATA_URL.replace("{ID}", "2"),
#                  'get_sensor_data',
#                  SharedValues.access_token)

#     assert True
