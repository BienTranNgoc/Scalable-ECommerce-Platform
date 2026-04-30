HTTP_STATUS_CODES = {
    "informational": {
        "CODE_STATUS_CONTINUE": 100,
        "CODE_STATUS_SWITCHING_PROTOCOLS": 101,
        "CODE_STATUS_PROCESSING": 102,
    },
    "success": {
        "CODE_STATUS_SUCCESS": 200,
        "CODE_STATUS_CREATED": 201,
        "CODE_STATUS_ACCEPTED": 202,
        "CODE_STATUS_NON_AUTHORITATIVE_INFORMATION": 203,
        "CODE_STATUS_NO_CONTENT": 204,
        "CODE_STATUS_RESET_CONTENT": 205,
        "CODE_STATUS_PARTIAL_CONTENT": 206,
    },
    "redirection": {
        "CODE_STATUS_MULTIPLE_CHOICES": 300,
        "CODE_STATUS_MOVED_PERMANENTLY": 301,
        "CODE_STATUS_FOUND": 302,
        "CODE_STATUS_SEE_OTHER": 303,
        "CODE_STATUS_NOT_MODIFIED": 304,
        "CODE_STATUS_TEMPORARY_REDIRECT": 307,
        "CODE_STATUS_PERMANENT_REDIRECT": 308,
    },
    "client_error": {
        "CODE_STATUS_BAD_REQUEST": 400,
        "CODE_STATUS_UNAUTHORIZED": 401,
        "CODE_STATUS_FORBIDDEN": 403,
        "CODE_STATUS_NOT_FOUND": 404,
        "CODE_STATUS_METHOD_NOT_ALLOWED": 405,
        "CODE_STATUS_NOT_ACCEPTABLE": 406,
        "CODE_STATUS_REQUEST_TIMEOUT": 408,
        "CODE_STATUS_CONFLICT": 409,
        "CODE_STATUS_GONE": 410,
        "CODE_STATUS_PAYLOAD_TOO_LARGE": 413,
        "CODE_STATUS_URI_TOO_LONG": 414,
        "CODE_STATUS_UNSUPPORTED_MEDIA_TYPE": 415,
        "CODE_STATUS_TOO_MANY_REQUESTS": 429,
    },
    "server_error": {
        "CODE_STATUS_INTERNAL_SERVER_ERROR": 500,
        "CODE_STATUS_NOT_IMPLEMENTED": 501,
        "CODE_STATUS_BAD_GATEWAY": 502,
        "CODE_STATUS_SERVICE_UNAVAILABLE": 503,
        "CODE_STATUS_GATEWAY_TIMEOUT": 504,
        "CODE_STATUS_HTTP_VERSION_NOT_SUPPORTED": 505,
        "CODE_STATUS_INSUFFICIENT_STORAGE": 507,
    }
}

CODE_STATUS_API = {
    '200': 1200,
    '201': 1201,
    '202': 1202,
    '400': 1400,
    '401': 1401,
    '402': 1402,
    '403': 1403,
    '404': 1404,
    '405': 1405,
    '406': 1406,
    '407': 1407,
    '440': 1440,  # Mã thông báo license hết hạn.
    '444': 1444,  # Mã Thông báo license được gia hạn yêu cầu app renew license mới.
    '445': 1445,  # Mã Thông báo mất quyền truy cập công ty
    '446': 1446,  # Mã Thông báo khi không tìm thấy input user ở api_user_access_control
    "447": 1447,  # Mã Thông báo kht mất quyền truy cập camera hoặc place
    "448": 1448,  # Mã Thông báo để app hiển thị snackbar
    "449": 1449,  # Mã Thông báo để app hiển thị backdrop
    "450": 1450,  # Mã Thông báo de app hien thi loi o nhap trong
    '500': 1500,
    '700': 1700,  # Mã Thông báo duplicate hình ảnh nhận diện
    '200_for_isc': 200,  # Phia anh manh yeu cau chinh cho MBS, API api_gift_codes_notification
    '500_for_cads': 5100
}
