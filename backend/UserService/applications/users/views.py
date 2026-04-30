import logging
import json
import pandas as pd
from opentelemetry import trace
from apps.apis.serializers import (
    UserProfileUpdateSerializer,
)
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import datetime, time
from rest_framework.decorators import action, throttle_classes
from rest_framework import viewsets, status
from apps.commons.keycloak import IAMHandler
from apps.uac.models import Customer, KeycloakTransaction
from apps.commons.decorators import validate_request, auth_keycloak_decorator, log_request_time
from apps.commons.responses import ResponseHandler
from opentelemetry import trace
from tracing.decorators import span_decorator
from apps.users.kyc_verify import kyc_verify
from apps.apis.authentication import IAMLicenseAuthorization, IAMAuthorization
from apps.users.services import UserLogService
from apps.uac.models import UserAccess
from apps.users.serializers import ReportUserLogSerializer, FilterUserLogDetailSerializer, \
    FilterUserLogMetadataSerializer
from apps.commons.management.commands.user_log_producer import KafkaProducerManager
from rest_framework.throttling import UserRateThrottle
from django.http import HttpResponse
from rest_framework.response import Response
import csv
import io
from django.core.cache import cache

tracer = trace.get_tracer(__name__)
logger = logging.getLogger(__name__)


class UserView(viewsets.ViewSet):
    authentication_classes = (IAMLicenseAuthorization,)

    @span_decorator(tracer)
    @log_request_time()
    @action(detail=False, methods=['post'])
    @auth_keycloak_decorator()
    def api_user_profile_details(self, request, **kwargs):
        try:
            resp_check_kyc = kyc_verify(request.user)
            kyc_message = 'We are verifying your identity document. A notification will be sent to you after having the identification status' if resp_check_kyc.get(
                'kyc_status', -1) == 2 else ''
            data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'sex': '' if not request.user.sex else request.user.sex,
                'dob': '' if not request.user.dob else request.user.dob,
                'email': request.user.email,
                'phone_number': str(request.user.phone_number),
                'native_language': '' if not request.user.native_language else request.user.native_language,
                'last_login': request.user.last_login,
                'status': request.user.status,
                'is_active': request.user.is_active,
                'kyc_data': {
                    'kyc_status': resp_check_kyc.get('kyc_status'),
                    'kyc_message': kyc_message
                }
            }
            customer_address = request.user.address_customer.all() if hasattr(request.user, 'address_customer') else []
            if customer_address:
                for address_customer in customer_address:
                    if not address_customer.is_default:
                        data.update({
                            'address': {
                                'city': {'id': address_customer.city.id, 'name': address_customer.city.name},
                                'district': {'id': address_customer.district.id,
                                             'name': address_customer.district.name},
                                'ward': {'id': address_customer.ward.id, 'name': address_customer.ward.name},
                                'street_no': address_customer.street_no,
                                'street_name': address_customer.street_name
                            }
                        })
            else:
                data.update({
                    'address': {
                        'city': {},
                        'district': {},
                        'ward': {},
                        'street_no': '',
                        'street_name': ''
                    }
                })
            return ResponseHandler.handle_response(
                result=True, code_status=settings.CODE_STATUS_API.get('200', 0), message=_('Success'),
                data=[data], status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f'Error: {e}')
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('500', 0),
                message=e
            )

    @log_request_time()
    @action(detail=False, methods=['post'])
    @auth_keycloak_decorator()
    @validate_request(serializer_class=UserProfileUpdateSerializer)
    def update_user(self, request, validated_data, **kwargs):
        try:
            access_token = kwargs.get('access_token', '')
            message = 'Updated the user successfully'
            first_name = validated_data.get('first_name', '')
            last_name = validated_data.get('last_name', '')
            email = validated_data.get('email', '')
            dob = validated_data.get('dob', '')
            sex = validated_data.get('sex', '')
            native_language = validated_data.get('native_language', '')
            address = validated_data.get('address', '')

            username = validated_data.get('username', '')
            # Get customer by username
            user: Customer | None = Customer.find_customer(
                username=username)
            if not user:
                raise Customer.DoesNotExist(f'User {username} not found')
            # Update customer first name
            data_json = {"firstName": first_name}
            user.update_customer(first_name=first_name)
            # Get keycloak transaction
            keycloak_transaction = KeycloakTransaction.find_keycloak_transaction(
                keycloak_id=user.id)
            if not keycloak_transaction:
                raise KeycloakTransaction.DoesNotExist(
                    'Not found keycload transaction')
            # Call to keycloak to update user
            is_update = IAMHandler(access_token).update_user(
                data_json, str(keycloak_transaction.id))
            logger.info(
                f'Result update user response from keycloak: {is_update}')
            if not is_update:
                message = 'Keycloak response error when updating user'
                logger.error(f'Error: {message}')
                return ResponseHandler.handle_response(
                    code_status=settings.CODE_STATUS_API.get('400', 0),
                    message=message
                )
            return ResponseHandler.handle_response(
                result=True, code_status=settings.CODE_STATUS_API.get(
                    '200', 0), message=message)
        except KeycloakTransaction.DoesNotExist:
            message = 'Not found keycload transaction'
            logger.error(f'Error: {message}')
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('404', 0),
                message=message
            )
        except Customer.DoesNotExist:
            message = f'User {username} not found'
            logger.error(f'Error: {message}')
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('404', 0),
                message=message
            )
        except Exception as e:
            logger.error(f'Error: {e}')
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('500', 0),
                message=e
            )


class UserStatusView(viewsets.ViewSet):
    authentication_classes = (IAMAuthorization,)

    @action(detail=False, methods=['post'])
    def deactivate_user(self, request, **kwargs):
        try:
            user = request.user
            user.is_active = False
            user.save()
            return ResponseHandler.handle_response(
                result=True,
                code_status=settings.CODE_STATUS_API.get('200', 0),
                message=_('The account has been locked.')
            )
        except Exception as e:
            logger.error(f'Error: {e}')
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('500', 0),
                message=str(e)
            )


class UserLogView(viewsets.ViewSet):
    authentication_classes = (IAMLicenseAuthorization,)

    @span_decorator(tracer)
    @throttle_classes([UserRateThrottle])
    @validate_request(serializer_class=FilterUserLogDetailSerializer)
    @action(detail=False, methods=['get'])
    def api_user_log_data(self, request, validated_data, **kwargs):
        is_export_csv = validated_data.get('is_export_csv', False)
        try:
            company_id = request.company_id

            # Get all filter parameters from validated_data
            username = validated_data.get('username', [])
            start_date = validated_data.get('start_date')
            end_date = validated_data.get('end_date')
            start_time_str = validated_data.get('start_time', '00:00')
            end_time_str = validated_data.get('end_time', '23:59')
            start_time = datetime.strptime(start_time_str, '%H:%M').time()
            end_time = datetime.strptime(end_time_str, '%H:%M').time()
            metadata = validated_data.get('metadata', '')
            action = validated_data.get('action', [])
            object_type = validated_data.get('object_type', [])
            status_val = validated_data.get('status', [])

            if not status_val:
                status_val = [True, False]

            # Pagination parameters
            page = validated_data.get('page', 1) if not is_export_csv else 1
            limit = validated_data.get('limit', 10) if not is_export_csv else 1000

            # Check user access
            user_access = UserAccess.get_access(request.user, company_id)
            if not (user_access and user_access.check_role_permission_uac()):
                return ResponseHandler.handle_response(
                    code_status=settings.CODE_STATUS_API.get('447', 0),
                    message=_('Access denied')
                )

            # Return empty results if no filters are provided
            if not (username and object_type and action and status_val):
                return ResponseHandler.handle_response(
                    result=True,
                    code_status=settings.CODE_STATUS_API.get('200', 0),
                    message=_('Success'),
                    data={
                        "results": [],
                        "pagination": {
                            "page": page,
                            "limit": limit,
                            "total": 0,
                            "total_pages": 0,
                            "has_next": False,
                            "has_previous": False,
                            "next_page": 1,
                            "previous_page": 1
                        }
                    },
                    status=status.HTTP_200_OK
                )

            # Convert dates to datetime objects
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if isinstance(end_date, str):
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            start_datetime = datetime.combine(start_date, time(0, 0))
            end_datetime = datetime.combine(end_date, time(23, 59, 59, 999999))

            # Use the first status value if available
            status_val = status_val[0] if status_val and len(status_val) == 1 else None

            # Filter logs with company_id in the query instead of the index name
            data, error = UserLogService.filter_logs(
                page=page,
                limit=limit,
                start_time=start_datetime,
                end_time=end_datetime,
                username=username,
                action=action,
                status=status_val,
                company_id=company_id,
                object_type=object_type,
                metadata=metadata,
            )

            if error:
                return ResponseHandler.handle_response(
                    code_status=settings.CODE_STATUS_API.get('400', 0),
                    message=error
                )

            # Filter by time range
            filtered_results = [
                result for result in data['results']
                if start_time <= datetime.fromisoformat(result['created_at']).time() <= end_time
            ]

            # Handle CSV export
            if is_export_csv:
                logger.info(f"Exporting {len(filtered_results)} rows to CSV")
                output = io.StringIO()
                writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

                writer.writerow(["Created at", "Username", "Action type", "Object type", "Status", "Metadata"])

                for row in filtered_results:
                    metadata = row.get('metadata', '')
                    if isinstance(metadata, dict):
                        metadata = ';'.join(str(v) for v in metadata.values())
                    elif isinstance(metadata, list):
                        processed_items = []
                        for item in metadata:
                            if isinstance(item, dict):
                                processed_items.append(';'.join(str(v) for v in item.values()))
                            else:
                                processed_items.append(str(item).strip())
                        metadata = ';'.join(processed_items)
                    elif isinstance(metadata, str):
                        metadata = metadata.strip()
                    else:
                        metadata = str(metadata)

                    writer.writerow([
                        str(row.get('created_at', '')).strip(),
                        str(row.get('username', '')).strip(),
                        str(row.get('action_type', '')).strip(),
                        str(row.get('object_type', '')).strip(),
                        str(row.get('status', '')).strip(),
                        metadata
                    ])

                csv_content = output.getvalue()
                filename = f"user_logs_{start_date.strftime('%Y%m%d')}_to_{end_date.strftime('%Y%m%d')}.csv"

                response = Response(csv_content, status=status.HTTP_200_OK)
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
                response['Content-Type'] = 'text/csv; charset=utf-8'
                return response

            # Update response with filtered results
            data['results'] = filtered_results

            return ResponseHandler.handle_response(
                result=True,
                code_status=settings.CODE_STATUS_API.get('200', 0),
                message=_('Success'),
                data=data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f'Error: {e}')
            if is_export_csv:
                df = pd.DataFrame([{'Error': str(e)}])
                response = HttpResponse(content_type='application/octet-stream')
                response['Content-Disposition'] = 'attachment; filename="user_logs_error.csv"'
                df.to_csv(path_or_buf=response, index=False)
                return response

            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('500', 0),
                message=str(e)
            )

    @span_decorator(tracer)
    @validate_request(serializer_class=ReportUserLogSerializer)
    @action(detail=False, methods=['post'])
    def api_user_log_report(self, request, validated_data, **kwargs):
        try:
            company_id = request.company_id
            type_object = validated_data.get('type_object')
            action = validated_data.get('action')
            object_id = validated_data.get('object_id')
            status = validated_data.get('status', True)

            # Prepare log data
            log_data = {
                'company_id': company_id,
                'type_object': type_object,
                'action': action,
                'object_id': object_id,
                'status': status,
                'time': int(datetime.now().timestamp() * 1000),
                'user_name': request.user.username or '',
            }

            # Send to Kafka topic
            KafkaProducerManager.produce_message(
                topic=settings.KAFKA_RESULT_USER_LOG_TOPIC,
                data=json.dumps(log_data).encode('utf-8')
            )

            return ResponseHandler.handle_response(
                result=True,
                code_status=settings.CODE_STATUS_API.get('200', 0),
                message=_('Success')
            )
        except Exception as e:
            logger.error(f'Error: {e}')
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('500', 0),
                message=str(e)
            )

    @span_decorator(tracer)
    @throttle_classes([UserRateThrottle])
    @action(detail=False, methods=['get'])
    def api_user_log_list_filter(self, request, **kwargs):
        try:
            user_access = UserAccess.get_access(request.user, request.company_id)
            if not (user_access and user_access.check_role_permission_uac()):
                return ResponseHandler.handle_response(
                    code_status=settings.CODE_STATUS_API.get('447', 0),
                    message=_('Access denied')
                )
            company_id = request.company_id
            filter_key = f'{settings.FILER_LIST_KEY}_{company_id}'
            data_resp = cache.get(filter_key) or {}
            if not data_resp:
                list_user_access = UserAccess.objects.filter(company_id=company_id).all()
                list_username = UserLogService.get_usernames_by_company_id(company_id)
                for user_access in list_user_access:
                    list_username.append(user_access.user_id)
                data_resp = {
                    'object_type': [{"value": value, "label": _(value)} for value in settings.LIST_OBJECT_TYPE],
                    'action_type': [{"value": value, "label": _(value)} for value in settings.LIST_ACTION_TYPE],
                    'list_username': list(set(list_username)),
                }
                cache.set(filter_key, data_resp, 2 * 60)
            return ResponseHandler.handle_response(
                result=True,
                code_status=settings.CODE_STATUS_API.get('200', 0),
                message=_('Success'),
                data=data_resp
            )
        except Exception as e:
            logger.error(f"Error in api_user_log_list_filter: {str(e)}")
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('500', 0),
                message=_('Internal server error')
            )

    @span_decorator(tracer)
    @validate_request(serializer_class=FilterUserLogMetadataSerializer)
    @action(detail=False, methods=['get'])
    def api_user_log_data_filter_metadata(self, request, validated_data, **kwargs):
        try:
            company_id = request.company_id
            metadata = validated_data.get('metadata')
            page = validated_data.get('page', 1)
            limit = validated_data.get('limit', 10)

            # Validate user access
            user_access = UserAccess.get_access(request.user, company_id)
            if not user_access:
                return ResponseHandler.handle_response(
                    code_status=settings.CODE_STATUS_API.get('447', 0),
                    message=_('Access denied')
                )

            # Use the new service method
            data, error = UserLogService.filter_by_metadata_value(
                company_id=company_id,
                metadata_value=metadata,
                page=page,
                limit=limit
            )

            if error:
                return ResponseHandler.handle_response(
                    code_status=settings.CODE_STATUS_API.get('400', 0),
                    message=error
                )

            return ResponseHandler.handle_response(
                result=True,
                code_status=settings.CODE_STATUS_API.get('200', 0),
                message=_('Success'),
                data=data,
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f'Error: {e}')
            return ResponseHandler.handle_response(
                code_status=settings.CODE_STATUS_API.get('500', 0),
                message=str(e)
            )
