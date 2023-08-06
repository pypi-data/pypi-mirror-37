from typing import Union, List, Optional, Dict
import requests


class Obj:
    pass


class SMSSsendBody(Obj):
    type: str  # defualt 'sms' 일반 | 'lms' 긴 메세지
    contentType: str  # 'AD' 광고용 | default 'COMM' 일반
    countryCode: str  # default korean 82
    fromNumber: str  # registed your mobile number on SENS
    to: [str]  # 보낼 번호들
    subject: str  # lsm 에서만 사용가능
    content: str  # 내용

    def __init__(self, fromNumber: str):
        self.fromNumber = fromNumber
        self.type = 'sms'
        self.contentType = 'COMM'
        self.countryCode = '82'

    @property
    def __dict__(self):
        dict = super(SMSSsendBody, self).__dict__
        if 'fromNumber' in dict:
            dict.update({'from': self.fromNumber})
            del dict['fromNumber']
        return dict


class SensClient:
    _host: str = 'https://api-sens.ncloud.com'
    _sms_uri: str = '/v1/sms/services/%s/messages'

    def __init__(self, service_id: str, secret_key: str, access_key_id: str):
        self._service_id = service_id
        self._secret_key = secret_key
        self._access_key_id = access_key_id

    def send_sms_by_body(self, body: Union[SMSSsendBody, Dict]):
        if not isinstance(body, Dict):
            body = body.__dict__

        session = requests.Session()
        url = self._get_url(self._sms_uri, self._service_id)
        return session.post(url, json=body, headers=self._make_headers())

    def send_sms(self, mobile_numbers: Union[str, List[str]], content: str, from_number: str = Optional[str]):
        if not isinstance(mobile_numbers, List):
            mobile_numbers = [mobile_numbers]
        if not from_number:
            from_number = self._from_number

        body = SMSSsendBody(from_number)
        body.to = mobile_numbers
        body.content = content

        session = requests.Session()
        url = self._get_url(self._sms_uri, self._service_id)
        return session.post(url, json=body.__dict__, headers=self._make_headers())

    def set_from_number(self, from_number: str) -> None:
        self._from_number = from_number

    def set_service_id(self, service_id) -> None:
        self._service_id = service_id

    def _get_url(self, uri: str, servid_id: str) -> str:
        return self._host + uri % servid_id

    def _make_headers(self) -> Dict:
        return {
            'X-NCP-auth-key': self._access_key_id,
            'X-NCP-service-secret': self._secret_key,
            'content-type': 'application/json'
        }
