import schedule
import time
import subprocess
import random

def jobDaily(attempts):
	print('******** daily job(s) ********')
	seed = random.randint(1, 5)
	time.sleep(random.randint(0, 300 * seed))
	condition = 'i < attempts' if isinstance(attempts, int) else 'True'
	i = 0
	while eval(condition):
		try:
			subprocess.check_call(['python', '001selenium.py'], timeout=600)
			#subprocess.run(['python', '001selenium.py'], check=True, timeout=600)
			print('Successed')
			break
		except:
			i = i + 1
			print('Failed')
	print('********Waiting********')

if __name__ == '__main__':
	print('Scheduled tasks starts...')
	schedule.every(5).minutes.do(jobDaily, attempts=5)
	#schedule.every().day.at("00:55").do(jobDaily, attempts=5)
	
	while True:
		schedule.run_pending()
		time.sleep(60)