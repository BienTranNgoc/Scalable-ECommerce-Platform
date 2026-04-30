import re

class ArnValidator:
    def __init__(self, arn: str):
        self.arn = arn
        self.pattern = r"^arn:(?P<partition>[a-z0-9-]+):(?P<service>[a-z0-9-*/]+):(?P<region>[a-z0-9-]*):(?P<app>[a-z0-9-*/]+)/(?P<model>[a-z0-9-*/]+)(/(?P<child_model>.+))?$"

    def is_valid_arn(self) -> bool:
        """Check if the ARN matches the custom pattern."""
        match = re.match(self.pattern, self.arn)
        return bool(match)

    def get_arn_parts(self) -> dict:
        """Extract parts of the ARN."""
        match = re.match(self.pattern, self.arn)
        if match:
            return match.groupdict()
        return {}

    def is_action_allowed(self, current_model: str, action: str, allowed_actions: list) -> bool:
        """
        Check if the action is allowed based on the ARN and the provided model path.

        :param current_model: The current model path in the format app/model/.../<current-model>.
        :param action: The action to check (e.g., 'view', 'create', etc.).
        :param allowed_actions: List of allowed actions (dynamically provided).
        :return: True if the action is allowed, False otherwise.
        """
        parts = self.get_arn_parts()
        if not parts:
            return False

        # Check if any higher level part contains '*', which grants full access
        if '*' in parts['app'] or '*' in parts['service'] or '*' in parts['partition']:
            return action in allowed_actions

        # Rebuild the path based on the ARN structure to compare with the current model path
        arn_path = f"{parts['app']}/{parts['model']}"
        if parts.get('child_model'):
            arn_path += f"/{parts['child_model']}"

        # Normalize wildcards to check against the current model path
        arn_path_pattern = arn_path.replace('*', '.*')

        # Match the current model path against the ARN pattern
        if re.fullmatch(arn_path_pattern, current_model):
            # If the path matches, check if the action is allowed
            return action in allowed_actions

        return False
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class KeycloakJWTAuthentication(JWTAuthentication):
     def get_user(self, validated_token):
        """
        Custom get_user to provide Lazy Creation (Sync User)
        """
        user_id = validated_token.get('sub')
        if not user_id:
            raise InvalidToken('Token contained no recognizable user identification')
            
        phone_number = validated_token.get('phone_number', '')  # Change to accurate claim name if needed
        email = validated_token.get('email', '')
        
        # Lazy creation: if user with sub doesn't exist, create an empty one
        # Here we use 'id'=sub. Assuming User.id is a UUIDField.
        user, created = User.objects.get_or_create(
            id=user_id,
            defaults={
                'phone_number': phone_number,
                'email': email,
                'username': user_id, 
            }
        )
        
        return user
