import logging
import re
import sys
import phonenumbers
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from apps.apis.utils import mobile_validate, password_validate
from apps.commons.rncryptor import decrypt_data_rn, encrypt_data_rn

logger = logging.getLogger(__name__)


class SignUpPhoneValidator:
    @staticmethod
    def validate_phone_number_register(phone_number, country_code, password, is_decrypt=False, key='', iterators=100):
        ctx = []
        logger.info(
            f'Validate phone number: {phone_number}, country_code: {country_code}, password: {password}')
        code_status = settings.CODE_STATUS_API.get('200', 0)
        message = ''
        ctx, code_status, message = HandlePhoneNumberValidator.validate_country_code(
            country_code, ctx, code_status, message)
        ctx, code_status, message = HandlePhoneNumberValidator.validate_phone_number(
            phone_number, country_code, ctx, code_status, message)
        ctx, code_status, message, password = HandlePasswordValidator.validate_password(
            password, ctx, message, code_status, is_decrypt=is_decrypt, key=key, iterators=iterators)
        return ctx, code_status, message, password


class SignUpEmailValidator:
    @staticmethod
    def validate_email(email, ctx, code_status, message):
        # Tách regex thành 2 phần để dễ đọc
        local_part = r'[a-zA-Z0-9._%+-]{1,64}'  # phần trước @
        host_part = r'[a-zA-Z0-9.-]{1,190}\.[a-zA-Z]{2,}'  # phần sau @

        email_regex = f'^(?=.{{6,254}}$)(?P<local>{local_part})@(?P<host>{host_part})$'

        logger.info(f'Validate email: {email}')

        if not isinstance(email, str):
            code_status = settings.CODE_STATUS_API.get('400', 0)
            message = 'The email is required'
            ctx.append({
                'field': 'email',
                'message': message
            })
            logger.error(message)
        else:
            match = re.match(email_regex, email)
            if not match:
                code_status = settings.CODE_STATUS_API.get('400', 0)
                message = 'Invalid email format'
                ctx.append({
                    'field': 'email',
                    'message': message
                })
                logger.error(message)
            else:
                local_part = match.group('local')
                host_part = match.group('host')

                if '..' in local_part or local_part.startswith('.') or local_part.endswith('.'):
                    code_status = settings.CODE_STATUS_API.get('400', 0)
                    message = 'Invalid email format'
                    ctx.append({
                        'field': 'email',
                        'message': message
                    })
                    logger.error(message)

                if host_part.startswith('-') or host_part.endswith('-'):
                    code_status = settings.CODE_STATUS_API.get('400', 0)
                    message = 'Invalid email format'
                    ctx.append({
                        'field': 'email',
                        'message': message
                    })
                    logger.error(message)

        return ctx, code_status, message

    @staticmethod
    def validate_email_register(email, password, is_decrypt=False, key='', iterators=100):
        ctx = []
        logger.info(
            f'Validate email: {email}, password: {password}')
        code_status = settings.CODE_STATUS_API.get('200', 0)
        message = ''
        ctx, code_status, message = SignUpEmailValidator.validate_email(
            email, ctx, code_status, message)
        ctx, code_status, message, password = HandlePasswordValidator.validate_password(
            password, ctx, message, code_status, is_decrypt=is_decrypt, key=key, iterators=iterators)
        return ctx, code_status, message, password


class HandlePhoneNumberValidator:
    @staticmethod
    def validate_phone_number(phone_number, country_code, ctx, code_status, message):
        logger.info('Check phone number')
        if not phone_number:
            code_status = settings.CODE_STATUS_API.get('400', 0)
            message = 'The phone_number is required'
            ctx.append({
                'field': 'phone_number',
                'message': message
            })
            logger.error(message)
        else:
            is_format, mes, phone = mobile_validate(phone_number, country_code)
            if not ctx and not is_format:
                code_status = settings.CODE_STATUS_API.get('400', 0)
                message = mes
                ctx.append({
                    'field': 'phone_number',
                    'message': mes
                })
                logger.error('Phone number has incorrect format')
        return ctx, code_status, message

    @staticmethod
    def validate_country_code(country_code, ctx, code_status, message):
        logger.info('Check phone number')
        if not country_code:
            code_status = settings.CODE_STATUS_API.get('400', 0)
            message = 'The country_code is required'
            ctx.append({
                'field': 'country_code',
                'message': message
            })
            logger.error(message)
        elif not str(country_code).isdigit():
            code_status = settings.CODE_STATUS_API.get('400', 0)
            message = 'The country_code must be a number.'
            ctx.append({
                'field': 'country_code',
                'message': message
            })
            logger.error(message)
        elif not phonenumbers.COUNTRY_CODE_TO_REGION_CODE.get(int(country_code)):
            code_status = settings.CODE_STATUS_API.get('400', 0)
            message = 'The country_code has incorrect format'
            ctx.append({
                'field': 'country_code',
                'message': message
            })
            logger.error(message)
        return ctx, code_status, message


class HandlePasswordValidator:
    @staticmethod
    def validate_password(password, ctx, message, code_status, is_decrypt=False, key='', iterators=100):
        if not password:
            code_status = settings.CODE_STATUS_API.get('400', 0)
            message = 'The password is required'
            ctx.append({'field': 'password', 'message': message})
            logger.error(message)
            return ctx, code_status, message, password

        if is_decrypt:
            try:
                logger.info('Decrypt password.')
                password = decrypt_data_rn(password, key, iterators)
            except Exception as e:
                code_status = settings.CODE_STATUS_API.get('400', 0)
                message = 'The password format is wrong. Please try again.'
                ctx.append({'field': 'password', 'message': message})
                logger.error('Password has incorrect format with error {} - on line {}'.format(
                    e, sys.exc_info()[-1].tb_lineno))
                return ctx, code_status, message, password

        if not password_validate(password):
            code_status = settings.CODE_STATUS_API.get('400', 0)
            message = 'Password must be 6-30 characters and not contain emojis or all identical characters. Please try again!'
            ctx.append({'field': 'password', 'message': message})
            logger.error(message)

        return ctx, code_status, message, password
