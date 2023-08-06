# NAVER SENS CLIENT


* support only send sms yet

## Install
<pre>
pip install naver-sens-client
</pre>

## Usage
<pre>
sens_client = SensClient(service_id, secret_key, access_key_id)
</pre>
and then
<pre>
response = sens_client.send_sms(to_mobile_number, content, from_mobile_number)
</pre>

or

<pre>
sens_client.set_from_number(from_mobile_number)
response = sens_client.send_sms(to_mobile_number, content)
</pre>

then confirm response.
<pre>
print(response.status_code)
print(response.content.decode('utf-8'))
</pre>

## More detail
[Naver Sens API DOCUMENT/KR-KO](https://sens.ncloud.com/assets/html/docs/index.html?url=https://api-sens.ncloud.com/docs/openapi/ko)