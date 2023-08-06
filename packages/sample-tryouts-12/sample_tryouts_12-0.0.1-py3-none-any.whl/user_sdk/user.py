import enum
from dataclasses import dataclass, asdict
from enum import Enum
from http import HTTPStatus
from uuid import UUID
from typing import Optional
from datetime import datetime

import requests

from user_sdk.error import UserAuthenticationError, NoSuchUser, ProfileCreationError, ProfileUpdateError, UserCreationFailed, NoSuchProfile

from user_sdk.exceptions import IllegalArgumentException


class CredentialType(Enum):
    EMAIL = 'EMAIL'
    MOBILE = 'MOBILE'
    OAUTH = 'OAUTH'

    def __str__(self):
        return self.value


class Gender(Enum):
    MALE = 'MALE'
    FEMALE = 'FEMALE'

    def __str__(self):
        return self.value


@dataclass
class Location:
    lat: float
    lng: float


@dataclass
class Address:
    location_name: str
    location: Location
    street_address: Optional[str] = None


@dataclass
class UserProfile:
    name: str
    gender: Gender
    home_address: Address
    work_address: Address
    dob: Optional[datetime] = None
    email_id: Optional[str] = None
    push_notification_id: Optional[str] = None


@dataclass
class Credential:
    id: UUID
    identity: str
    verified: bool


@dataclass
class User:
    id: UUID
    identities: [Credential]


@dataclass
class Session:
    id: str
    user: User


class UserService:
    def __init__(self, auth_url, profile_url):
        self._auth_url, self._profile_url = auth_url, profile_url

    def login_with_email(self, email: str, password: str) -> Session:
        return self._login(cred_type=CredentialType.EMAIL, identity=email, password=password)

    def login_with_mobile(self, phone_number: str, otp: str) -> Session:
        return self._login(cred_type=CredentialType.MOBILE, identity=phone_number, otp=otp)

    def login_with_oauth(self, id_token: str) -> Session:
        return self._login(cred_type=CredentialType.OAUTH, identity=id_token)

    def _login(self, cred_type, identity, password=None, otp=None) -> Session:
        body = {'identity': identity, 'credential_type': str(cred_type)}
        if cred_type == CredentialType.EMAIL:
            body['password'] = password
        elif cred_type == CredentialType.MOBILE:
            body['otp'] = otp

        response = requests.post(f'{self._auth_url}/api/v1/sign_in', json=body)
        if response.status_code == HTTPStatus.CREATED:
            return self._dict_to_session(response.json()['data'])
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise UserAuthenticationError

    def get_user_from_session(self, session_id: str) -> Session:
        response = requests.get(f'{self._auth_url}/sessions/{session_id}')
        if response.status_code == HTTPStatus.OK:
            return self._dict_to_session(response.json()['data'])
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NoSuchUser



    def create_profile(self, user_id: UUID, profile: UserProfile) -> UserProfile:
        profileDict = asdict(profile)
        profileDict["gender"] = str(profileDict['gender'])
        response = requests.post(f'{self._profile_url}/api/v1/user_profiles', json={
            'user_id': str(user_id),
            'profile': profileDict,
        })

        if response.status_code == HTTPStatus.CREATED:
            return self._dict_to_user_profile(response.json().get('data'))
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise ProfileCreationError

    def update_profile(self, user_id: str, profile: dict) -> UserProfile:
        response = requests.patch(url=f'{self._profile_url}/api/v1/user_profiles/{user_id}', json=profile)

        if response.status_code == HTTPStatus.OK:
            return self._dict_to_user_profile(response.json().get('data'))
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise ProfileUpdateError
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NoSuchProfile

    def get_user_profile(self, id: str) -> UserProfile:
        response = requests.get(f'{self._profile_url}/api/v1/user_profiles/%s' % str(id))
        if response.status_code == HTTPStatus.OK:
            return self._dict_to_user_profile(response.json().get('data'))
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise NoSuchProfile

    def create_user(
            self,
            credential_type: str,
            identity: str,
            requires_verification: bool = True,
            password: str = None,
    ):
        try:
            credential_type = CredentialType[credential_type]
        except KeyError:
            raise IllegalArgumentException(f'Invalid credential_type {credential_type})')

        body = {
            'credential_type': credential_type.name,
            'identity': identity,
            'requires_verification': requires_verification
        }

        if password:
            body['password'] = password

        response = requests.post(f'{self._auth_url}/api/v1/users', json=body)

        if response.status_code == HTTPStatus.CREATED:
            return self._dict_to_user(response.json().get('data'))
        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise UserCreationFailed

    def get_by_email(self, email: str):
        response = requests.get(f'{self._auth_url}/api/v1/users/by_identity/%s' % email)
        if response.status_code == 200:
            return self._dict_to_user(response.json().get('data'))
        # Todo: handle failure cases

    def get_by_mobile_number(self, mobile_number: str):
        response = requests.get(f'{self._auth_url}/api/v1/users/by_identity/%s' % mobile_number)
        if response.status_code == 200:
            return self._dict_to_user(response.json().get('data'))
        # Todo: handle failure cases

    def _dict_to_session(self, param):
        user = self._dict_to_user(param.get('user'))
        return Session(param.get('session_id'), user=user)

    def _dict_to_user(self, param) -> User:
        def dict_to_cred(cred_dict):
            return Credential(id=cred_dict['id'], identity=cred_dict['identity'], verified=cred_dict['verified'])

        return User(
            id=param['id'],
            identities=[dict_to_cred(cred) for cred in param['credentials']],
        )

    def _dict_to_user_profile(self, param) -> UserProfile:
        def dict_to_address(address_dict):
            return Address(location=Location(address_dict['location']['lat'],address_dict['location']['lng']),
                           location_name=address_dict['location_name'],
                           street_address=address_dict.get('street_address'))

        return UserProfile(name=param['name'], gender=Gender(param['gender']),
                           home_address=dict_to_address(param['home_address']),
                           work_address=dict_to_address(param['work_address']),
                           dob= param.get('dob'), email_id=param.get('email'),
                           push_notification_id=param.get('gcmId'))
