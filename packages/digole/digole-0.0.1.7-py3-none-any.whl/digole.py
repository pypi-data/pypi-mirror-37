#!/usr/bin/env python3

import smbus as smbus

class lcd(object):
	def __init__(self, address):
		self.address = address # Will call the setter

	@property
	def address(self):
		print('called getter')
		print('address is {}'.format(self._address))
		return self._address

	@address.setter
	def address(self, value):
		print('called setter')
		print('setting the address to {}'.format(value))
		self._address = value

	@address.deleter
	def address(self):
		print('called deleter')
		print('Deleting...')
		del self._address


	def convert(self, text = 'test'):
		print(text)
		return [ord(i) for i in text]

