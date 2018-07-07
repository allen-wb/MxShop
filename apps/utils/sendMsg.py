import requests, json


class SendMsg(object):

	def __init__(self, api_key):
		self.api_key = api_key
		self.send_url = ''

	def seng_msg(self, code, mobile):
		params = {
			'apiKey': self.api_key,
			'mobile': mobile,
			'text': '模板验证码{code}'.format(code)
		}

		response = requests.post(self.send_url, data=params)
		# 解析response
		res_dict = json.loads(response.text)
		print(res_dict)
		return True
