import os
import ssl

FSS_MANAGEMENT_PROTOCOL = os.getenv('FSS_MANAGEMENT_PROTOCOL', default='https')
FSS_MANAGEMENT_HOST = os.getenv('FSS_MANAGEMENT_HOST', default='fss-mngt.fcam.vn')
FSS_MANAGEMENT_GIS = os.getenv('FSS_MANAGEMENT_GIS', default='a8a55ef4e4924c2dbf2f80be8cff14de')

KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', default='42.119.146.47:29092,42.119.146.48:29092,42.119.146.49:29092')
KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', default='cads-facereg')
KAFKA_GROUP_ID_ATTENDANCE = os.getenv('KAFKA_GROUP_ID_ATTENDANCE', default='b2b-face-attendance')
KAFKA_GROUP_ID_CHECK_FACE_SERVICE_HEALTH = os.getenv('KAFKA_GROUP_ID_CHECK_FACE_SERVICE_HEALTH', default='b2b-face-service-health')
KAFKA_USERNAME = os.getenv('KAFKA_USERNAME', default='admin-fss')
KAFKA_PASSWORD = os.getenv('KAFKA_PASSWORD', default='admin-fss')
KAFKA_RESULT_STREAM_TOPIC = os.getenv('KAFKA_RESULT_STREAM_TOPIC', default='queuing.b2b-face.recognise')
KAFKA_FACE_HEALTH_TOPIC = os.getenv('KAFKA_FACE_HEALTH_TOPIC', default='queuing.b2b-face.stream.health')
KAFKA_EVALUATION_RESULT_TOPIC = os.getenv('KAFKA_EVALUATION_RESULT_TOPIC', default='result-evaluate-ai-model')
KAFKA_EVALUATION_GROUP_ID = os.getenv('KAFKA_EVALUATION_GROUP_ID', default='cads-evaluation-ai')
AI_FACE_RESULT_META_INDEX_FORMAT = os.getenv('AI_FACE_RESULT_META_INDEX_FORMAT', default='ai-face-recognise-result-meta-{}')
AI_FACE_RESULT_ATTENDANCE_INDEX_FORMAT = os.getenv('AI_FACE_RESULT_ATTENDANCE_INDEX_FORMAT', default='ai-face-recognise-result-attendance-{}')
WEBHOOK_NOTIFICATION_INDEX_FORMAT = os.getenv('WEBHOOK_NOTIFICATION_INDEX_FORMAT', default='webhook-notifications-{}')
KAFKA_EXPORT_TOPIC = os.getenv('KAFKA_EXPORT_TOPIC', default='queuing.b2b-face.record.export')
KAFKA_ALARM_AI_TOPIC = os.getenv('KAFKA_ALARM_AI_TOPIC', default='queuing.b2b-ai-alarm')
KAFKA_FACE_ATTENDANCE_TOPIC = os.getenv('KAFKA_FACE_ATTENDANCE_TOPIC', default='queuing.b2b-face.recognise.attendance')
KAFKA_ALARM_AI_THREAD = int(os.getenv('KAFKA_ALARM_AI_THREAD', default=3))
KAFKA_ATTENDANCE_THREAD = int(os.getenv('KAFKA_ATTENDANCE_THREAD', default=3))
VIP_NOTIFICATION_THREAD = int(os.getenv('VIP_NOTIFICATION_THREAD', default=3))

CAD_SERVICE_PROTOCOL = os.getenv('CAD_SERVICE_PROTOCOL', default='https')
CAD_SERVICE_URL = os.getenv('CAD_SERVICE_URL', default='staging-aicam.cads.live')
CADS_DEFAULT_TIMEOUT = int(os.getenv('CADS_DEFAULT_TIMEOUT', default=15))
CAD_API_GIS = os.getenv('CAD_API_GIS', 'cad')
CAD_CLIENT_ID = os.getenv('CAD_CLIENT_ID', default='0PrNWuy0Y5WgXFj9cv6IP3B4WeqGBOfz')
CAD_CLIENT_SECRET = os.getenv('CAD_CLIENT_SECRET', default='IiDNnEHq2fnJwKjW9UznAN8a3fAkRZtq')
# CAD_FACE_PROFILE_MOCK_API = bool(int(os.getenv('CAD_FACE_PROFILE_MOCK_API', default='0')))
CAD_FACE_PROFILE_MOCK_API = False

# MQTT Bi-direction
MQTT_SECRET = os.getenv("MQTT_SECRET", "rm6DH@#wc9FJyCcM9bEw")
MQTT_SESSION_EXP = int(os.getenv("MQTT_SESSION_EXP", '86400'))
MQTT_ENCODE_ALGORITHM = os.getenv("MQTT_ENCODE_ALGORITHM", default="HS256")
MQTT_BROKER_PROTOCOL = os.getenv("MQTT_BROKER_PROTOCOL", default="mqtts")
MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", default="beta-broker-mqtt.fcam.vn")
MQTT_BROKER_PORT = os.getenv("MQTT_BROKER_PORT", default=8883)
MQTT_BROKER_USERNAME = os.getenv("MQTT_BROKER_USERNAME", default="SYSManagement")
MQTT_BROKER_PASSWORD = os.getenv("MQTT_BROKER_PASSWORD", default="SYSManagement")
MQTT_BROKER_OVER_WS_PROTOCOL = os.getenv("MQTT_BROKER_OVER_WS_PROTOCOL", default="wss")
MQTT_BROKER_OVER_WS_PORT = int(os.getenv("MQTT_BROKER_OVER_WS_PORT", default='8084'))
MQTT_BROKER_OVER_WS_PATH = os.getenv("MQTT_BROKER_OVER_WS_PATH", default="/mqtt")
IS_AUTHENTICATE_MQTT = os.getenv("CA_ROOT_CERT_FILE", default=True)
CA_ROOT_CERT_FILE = os.getenv("CA_ROOT_CERT_KEY", default=None)
CA_ROOT_CERT_KEY = os.getenv("CA_ROOT_CERT_KEY", default=True)
CA_ROOT_CERT_CLIENT = os.getenv("CA_ROOT_CERT_CLIENT", default=None)
CA_ROOT_CERT_REQS = os.getenv("CA_ROOT_CERT_REQS", default=ssl.CERT_NONE)
CA_ROOT_CERT_CIPHERS = os.getenv("CA_ROOT_CERT_CIPHERS", default=None)
CA_ROOT_TLS_VERSION = os.getenv("CA_ROOT_TLS_VERSION", default=ssl.PROTOCOL_TLSv1_2)

CUSTOMER_SERVICE_PROTOCOL = os.getenv('CUSTOMER_SERVICE_PROTOCOL', default='https')
CUSTOMER_SERVICE_URL = os.getenv('CUSTOMER_SERVICE_URL', default='beta-api-gateway.fcam.vn/customer-b2b')
CUSTOMER_API_GIS = os.getenv('CUSTOMER_API_GIS', default='c5e7a47f2d334dddbcc1ba50adf370f0')

OPENSEARCH_SERVICE_PROTOCOL = os.getenv('OPENSEARCH_SERVICE_PROTOCOL', default='http')
OPENSEARCH_SERVICE_URL = os.getenv('OPENSEARCH_SERVICE_URL', default='beta-es-moment.fcam.vn')
OPENSEARCH_SERVICE_HOST = os.getenv('OPENSEARCH_SERVICE_HOST', default='beta-es-moment.fcam.vn')
OPENSEARCH_SERVICE_PORT = int(os.getenv('OPENSEARCH_SERVICE_PORT', default=80))
OPEN_SEARCH_USERNAME = os.getenv('OPEN_SEARCH_USERNAME', default='backend')
OPEN_SEARCH_PASSWORD = os.getenv('OPEN_SEARCH_PASSWORD', default='Backend@123')

IAM_TOKEN_VALIDATION_URL = os.getenv('IAM_TOKEN_VALIDATION_URL')
IAM_DEVICES_VALIDATION_URL = os.getenv('IAM_DEVICES_VALIDATION_URL')
IAM_VALIDATION_GIS = os.getenv('IAM_VALIDATION_GIS')

PLAYBACK_SERVICE_PROTOCOL = os.getenv('PLAYBACK_SERVICE_PROTOCOL', default='http')
PLAYBACK_SERVICE_URL = os.getenv('PLAYBACK_SERVICE_URL', default='pbapi-hcm.fcam.vn')

CLOUD_SERVICE_PROTOCOL = os.getenv('CLOUD_SERVICE_PROTOCOL', default='https')
CLOUD_SERVICE_URL = os.getenv('CLOUD_SERVICE_URL', default='cloud-mngt.fcam.vn')
CLOUD_API_GIS = os.getenv('CLOUD_API_GIS', default='6cd0e748385a44f09d95f022eb851a0d')

MQTT_CLIENT_ID_PREFIX = os.getenv("MQTT_CLIENT_ID_PREFIX", default="ipc-{}")

CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_TASK_TIME_LIMIT = 15  # set the task time limit to 15 seconds
CELERY_TASK_RETRIES = 3  # set the maximum number of retries to 3
CELERY_TASK_RETRY_DELAY = 3  # wait 3 seconds between retries
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Ho_Chi_Minh'
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"

# ====== Type from Message Template (Notification) ======
ALARM_AI_FACE_DETECT_STRANGER = os.getenv("ALARM_AI_FACE_DETECT_STRANGER", default='AIFaceDetectStranger')
ALARM_AI_FACE_DETECT_FAMILIAR = os.getenv("ALARM_AI_FACE_DETECT_FAMILIAR", default='AIFaceDetectFamiliar')
ALARM_AI_FACE_DETECT_VIP = os.getenv("ALARM_AI_FACE_DETECT_VIP", default='AIFaceDetectVip')
ALARM_AI_FACE_DETECT_VISITOR = os.getenv("ALARM_AI_FACE_DETECT_VISITOR", default='AIFaceDetectVisitor')

ALLOWED_GIS = os.getenv('ALLOWED_GIS', '23a8c0c2da5b4fd4ac2e9e4f8ea67dbh')
WEBHOOK_NOTIFICATION_URL = os.getenv('WEBHOOK_NOTIFICATION_URL', default='https://webhook-automation.fcam.vn/webhook/notification')

EMAIL_HOST = os.getenv('EMAIL_HOST', default='smtp.office365.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', default=587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', default='cmr.ops@fpt.com')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', default='Fcam@@)@@049')

EVENT_TYPE_STREAM_HEALTH = os.getenv("EVENT_TYPE_STREAM_HEALTH", default='stream_health')

CMR_MANAGEMENT_PROTOCOL = os.getenv("CMR_MANAGEMENT_PROTOCOL", default="https")
CMR_MANAGEMENT_HOST = os.getenv("CMR_MANAGEMENT_HOST", default="beta-api-gateway.fcam.vn/cmrmngt-b2b")
CMR_MANAGEMENT_GIS = os.getenv("CMR_MANAGEMENT_GIS", default="d0241d2e185f4cd5a1d53d21c0ef8df2")

NVR_MANAGEMENT_PROTOCOL = os.getenv("NVR_MANAGEMENT_PROTOCOL", default="https")
NVR_MANAGEMENT_HOST = os.getenv("NVR_MANAGEMENT_HOST", default="beta-api-gateway.fcam.vn/nvrmngt-b2b")
NVR_MANAGEMENT_GIS = os.getenv("NVR_MANAGEMENT_GIS", default="b6b67071eb164df5a0636d3aa0c11e6a")