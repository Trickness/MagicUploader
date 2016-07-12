# coding=utf8

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
from qiniu import BucketManager
from qiniu.http import ResponseInfo


access_key = ''
secret_key = ''

q = Auth(access_key,secret_key)

print (q)

bucket = BucketManager(q)

print (bucket)
print (bucket.auth)

bucket_name = 'resources'

ret = bucket.list(bucket_name)

print (ret[2].status_code)

for item in ret[0]['items']:
    assert isinstance(item, dict)
    print (item)
print (ret[2].text_body[0])
