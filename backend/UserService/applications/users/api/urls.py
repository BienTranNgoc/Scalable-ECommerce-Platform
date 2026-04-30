from django.urls import path
from apps.users.views import UserLogView, UserStatusView


prefix = 'user/log'

user_patterns = [
    path(f'user/deactivate/',
         UserStatusView.as_view({'post': 'deactivate_user'}),
         name='deactivate_user'),
    path(f'{prefix}/list/',
         UserLogView.as_view({'post': 'api_user_log_data'}),
         name='api_user_log_data'),
    path(f'{prefix}/filter/list/',
         UserLogView.as_view({'get': 'api_user_log_list_filter'}),
         name='api_user_log_list_filter'),
#     path(f'{prefix}/filter/metadata/',
#          UserLogView.as_view({'post': 'api_user_log_data_filter_metadata'}),
#          name='api_user_log_data_filter_metadata'),
#     path(f'{prefix}/report/',
#          UserLogView.as_view({'post': 'api_user_log_report'}),
#          name='api_user_log_report'),
]
