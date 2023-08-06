# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['django_test_curl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-test-curl',
    'version': '0.1.0',
    'description': 'Write Django test requests using curl syntax',
    'long_description': 'Django test curl\n================\n\n[![Build Status](https://travis-ci.org/crccheck/django-test-curl.svg?branch=master)](https://travis-ci.org/crccheck/django-test-curl)\n\nWith _Django test curl_, you can take your test cases and immediately try them\nagainst an actual server via the magic of copy-paste!\n\nDjango\'s [testing tools] come with a great [test client] you can use to\nsimulate requests against views. Against deployed Django projects, if you want\nto do simple requests, you would probably use [curl]. If you want to use the\nsame syntax for both, this is the package for you.\n\n### Good places to use this\n\nThis was developed to TDD recreating an existing API in Django. If you have a\nlibrary of [curl] requests that you need to replicate, this is perfect for\nthat. If you need a portable format to turn test cases into QA automation, this\nis great for that too.\n\n### Bad places to use this\n\nIf the `.curl(...)` syntax requires lots of string formatting, you should stick\nto the traditional [test client]. If the test case isn\'t copy-pastable, it\'s\nnot a good fit. This also means if you use randomness to generate your\nrequests, you\'ll lose that extra test coverage.\n\n\nInstallation\n------------\n\n```sh\n$ pip install django-test-curl\n```\n\n\nUsage\n-----\n\n```python\nfrom django_test_curl import CurlClient\n\nclass SimpleTest(TestCase):\n    """https://docs.djangoproject.com/en/stable/topics/testing/tools/#example"""\n    def setUp(self):\n        self.client = CurlClient()\n\n    def test_details(self):\n        response = self.client.curl("""\n          curl http://localhost:8000/customer/details/\n        """)\n\n        self.assertEqual(response.status_code, 200)\n\n        self.assertEqual(len(response.context[\'customers\']), 5)\n```\n\nIf you\'re using a custom `Client`, you can use the mixin version:\n\n```\nfrom django.test import Client\nfrom django_test_curl import CurlClientMixin\n\nclass MyClient(CurlClientMixin, Client):\n    ...\n```\n\nWe support a subset of curl\'s functionality. For a full list and examples, see\nthe [tests](./django_test_curl/test_django_test_curl.py).\n\n* Headers\n* GET/POST/PUT/DELETE/etc\n* HTTP basic auth\n\n\n[curl]: https://curl.haxx.se/\n[test client]: https://docs.djangoproject.com/en/stable/topics/testing/tools/#the-test-client\n[testing tools]: https://docs.djangoproject.com/en/stable/topics/testing/tools/\n',
    'author': 'crccheck',
    'author_email': 'oss@crccheck.com',
    'url': 'https://github.com/crccheck/django-test-curl',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
