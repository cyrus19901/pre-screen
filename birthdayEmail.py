import redis
import datetime
import time
import asyncio
# from './lib' import sendBirthdayEmail

class User(object):

	def __init__(self,id=None,birthday=None):
		self.redisClient = redis.Redis(host='127.0.0.1',port=6379)
		self.id = id or self.redisClient.incr('age-app:user-ids');
		self.birthday = birthday 


	# gets the highest value of ID in the existing cache to iterate over it
	async def getHighestId(self,key):
		try:
			value = await self.redisClient.get(key)
			return value
		except redis.RedisError as err:
			raise Exception 
		print(value)
	#finds the user's cached value
	def find(self,id):
		try: 
			cached_data = self.redisClient.get(id)
		except redis.RedisError as e:
			print(e)

		if cached_data is not None:
			return cached_data


	async def celebrateBirthday(self):
		key = 'sent-'+self.id
		if (await hasEmailSent(key) == False):
			await sendBirthdayEmail(key);
			await self.setSentStatus(key)
			await self.save()

	#Setting the status of the email sent to True, it will expire after a year -1 
	async def setSentStatus(self,key):
		expiryTime = 60*60*24*364
		await self.redisClient.setex(key,expiryTime,True)
		return

	#check if the birthday email has been sent out already to the person 
	async def hasEmailSent(self,key):
		try:
			result = await self.redisClient.get(key)
		except redis.RedisError:
			raise err
		if result:
			return True
		else:
			return False


		#check if its the birthday of the key
	def isBirthday(self,birthday):
		if (birthday == str(datetime.datetime.now().date())):
			return True
		else:
			return False
	#saves the value to the cache
	async def save(self):
		try:
			result = await self.redisClient.hset('users',self.id,'birthday',self.birthday)
		except redis.RedisError:
			raise err
		if (result == 0):
			raise Exception("the value was not written")

	def sendEmail(self,highestId):
		for userId in range[0,highestId]:
			user = self.find(userId);
			if (self.isBirthday(user.birthday)):
				self.celebrateBirthday()

if __name__ == '__main__':
    r = User()
    highestId = r.getHighestId('age-app:user-ids')
    time.sleep(24*60*60)
