#NAVER SENS CLIENT

##Install
<pre>
pip install 
</pre>

##Usage
<pre><code>
sens_client = SensClient(service_id, secret_key, access_key_id)

response = sens_client.send_sms(to_mobile_number, content, from_mobile_number)

print(response.status_code)
print(response.content.decode('utf-8'))
</code></pre>


##More detail
[Naver Sens API DOCUMENT/KR-KO](https://sens.ncloud.com/assets/html/docs/index.html?url=https://api-sens.ncloud.com/docs/openapi/ko)