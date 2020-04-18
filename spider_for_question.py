# -*- coding: utf-8 -*

import requests

from settings import HEADERS

url = "https://www.zhihu.com/question/309298287"

rs = requests.get(url, headers=HEADERS)
#
# stream = StringIO.StringIO(rs.text)
# gziper = gzip.GzipFile(fileobj=stream)
#
# gziper.read()


