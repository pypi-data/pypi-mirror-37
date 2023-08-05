import unittest
import core.automanlib as pyAutomanlib
from time import sleep
from core.pyautomanexceptions import ArgumentError, UnsupportedServerError, AdapterError
from core.grpc_gen_classes.automanlib_rpc_pb2 import TaskResponse, ServerStatusResponse
from automan import Automan, EstimateOutcome

"""
NOT IMPLEMENTED:
Test cases are not complete. Not working.
"""

class TestAutomanClass(unittest.TestCase):
	def setUp(self):
		self.longMessage = True
		self.good_adapter = {"access_id" : "TEST_ACCESS_ID",
							"access_key" : "TEST_ACCESS_KEY",
							"ADDITIONAL_ARG_1" : "ARG1",
							"ADDITIONAL_ARG_2" : "ARG2",
							"type" : "MTurk"
							}

		self.bad_type_adapter =  {"access_id" : "TEST_ACCESS_ID",
							"access_key" : "TEST_ACCESS_KEY",
							"ADDITIONAL_ARG_1" : "ARG1",
							"ADDITIONAL_ARG_2" : "ARG2",
							"type" : "not_mturk"
							}

		self.missing_id_adapter =  {"access_key" : "TEST_ACCESS_KEY",
							"ADDITIONAL_ARG_1" : "ARG1",
							"ADDITIONAL_ARG_2" : "ARG2",
							"type" : "MTurk"
							}
		self.missing_key_adapter =  {"access_id" : "TEST_ACCESS_ID",
							"ADDITIONAL_ARG_1" : "ARG1",
							"ADDITIONAL_ARG_2" : "ARG2",
							"type" : "MTurk"
							}

		self.missing_type_adapter =  {"access_id" : "TEST_ACCESS_ID",
							"access_key" : "TEST_ACCESS_KEY",
							"ADDITIONAL_ARG_1" : "ARG1",
							"ADDITIONAL_ARG_2" : "ARG2",
							}

	def test_constructor_args_type_check(self):
		# server_addr: test wrong type, test non-local address
		print("Testing server_addr: incorrect type, non-local address..")
		self.assertRaises(ArgumentError, Automan, adapter=self.good_adapter, server_addr=1200, port=50051, suppress_output='all', 
										loglevel='fatal', logging='none', stdout=None, stderr=None, testmode=True)
		self.assertRaises(UnsupportedServerError, Automan,adapter=self.good_adapter, server_addr='http://www.google.com', port=50051, suppress_output='all', 
										loglevel='fatal', logging='none', stdout=None, stderr=None, testmode=True)
		# port: test wrong type
		print("Testing port: incorrect type")
		self.assertRaises(ArgumentError,  Automan, adapter=self.good_adapter, server_addr='localhost', port='50051', suppress_output='all', 
										loglevel='fatal', logging='none', stdout=None, stderr=None, testmode=True)
		
		#suppress_output: test wrong type, test bad value
		print("Testing suppress_output: incorrect type, bad value..")
		self.assertRaises(ArgumentError, Automan, adapter=self.good_adapter, server_addr='localhost', port=50051, suppress_output=1200, 
										loglevel='fatal', logging='none', stdout=None, stderr=None, testmode=True)
		self.assertRaises(ArgumentError, Automan, adapter=self.good_adapter, server_addr='http://www.google.com', port=50051, suppress_output='bad_value', 
										loglevel='fatal', logging='none', stdout=None, stderr=None, testmode=True)

		# loglevel: test wrong type, test bad value
		print("Testing loglevel: incorrect type, bad value..")
		self.assertRaises(ArgumentError, Automan, adapter=self.good_adapter, server_addr='localhost', port=50051, suppress_output='all', 
										loglevel=1200, logging='none', stdout=None, stderr=None, testmode=True)
		self.assertRaises(ArgumentError, Automan, adapter=self.good_adapter, server_addr='localhost', port=50051, suppress_output='all', 
										loglevel='bad_value', logging='none', stdout=None, stderr=None, testmode=True)
		
		# logging: test wrong type, test bad value
		print("Testing logging: incorrect type, bad value..")
		self.assertRaises(ArgumentError, Automan, adapter=self.good_adapter, server_addr='localhost', port=50051, suppress_output='all', 
										loglevel='fatal', logging=1200, stdout=None, stderr=None, testmode=True)
		
		self.assertRaises(ArgumentError, Automan, adapter=self.good_adapter, server_addr='localhost', port=50051, suppress_output='all', 
										loglevel='fatal', logging='bad_value', stdout=None, stderr=None, testmode=True)

		# adapter: test wrong type
		print("Testing adapter: incorrect type..")
		self.assertRaises(ArgumentError,  Automan, adapter=["access_id", "access_key", "type"], server_addr='localhost', port=50051, suppress_output='all', 
										loglevel='fatal', logging='none', stdout=None, stderr=None, testmode=True)
		

		# test no args
		print("Testing no args supplied..")
		self.assertRaises(TypeError, Automan, testmode=True)

	def test_default_args(self):
		self.assertIsInstance(Automan(self.good_adapter, testmode=True), 
							Automan,
							" default args fail with good adapter")

	def test_bad_adapter(self):
		self.assertRaises(AdapterError,  Automan, {'adapter':self.missing_key_adapter, 'server_addr':'localhost', 'port':50051, 'suppress_output':'all', 
										'loglevel':'fatal', 'logging':'none', 'stdout':None, 'stderr':None, 'testmode':True})
		self.assertRaises(AdapterError,  Automan, {'adapter':self.missing_id_adapter, 'server_addr':'localhost', 'port':50051, 'suppress_output':'all', 
										'loglevel':'fatal', 'logging':'none', 'stdout':None, 'stderr':None, 'testmode':True})
		self.assertRaises(AdapterError,  Automan, {'adapter':self.missing_key_adapter, 'server_addr':'localhost', 'port':50051, 'suppress_output':'all', 
										'loglevel':'fatal', 'logging':'none', 'stdout':None, 'stderr':None, 'testmode':True})
		self.assertRaises(AdapterError,  Automan, {'adapter':self.missing_type_adapter, 'server_addr':'localhost', 'port':50051, 'suppress_output':'all', 
										'loglevel':'fatal', 'logging':'none', 'stdout':None, 'stderr':None, 'testmode':True})
		self.assertRaises(AdapterError,  Automan, {'adapter':self.bad_type_adapter, 'server_addr':'localhost', 'port':50051, 'suppress_output':'all', 
										'loglevel':'fatal', 'logging':'none', 'stdout':None, 'stderr':None, 'testmode':True})


class TestAutomanServerStartShutdown(unittest.TestCase):
	def setUp(self):
		self.started = False
		self.finished = False
		self.good_adapter =  {"access_id" : "TEST_ACCESS_ID",
							"access_key" : "TEST_ACCESS_KEY",
							"ADDITIONAL_ARG_1" : "ARG1",
							"ADDITIONAL_ARG_2" : "ARG2",
							"type" : "mturk"
							}
		self.automan_obj = Automan(self.good_adapter, server_addr = 'localhost', port = 50051, suppress_output = 'all', 
										loglevel = 'fatal', logging='none', stdout =None, stderr = None, testmode=True)
							
	def tearDown(self):
		if self.started and not self.finished:
			print("Server was started but could not be shutdown. You may need to manually kill the server java process. Attempting to force shutdown..")
			self.automan_obj._force_svr_shutdown()


	def test_start_shutdown_methods(self):
		# attempt to start server, and then shut down server
		print("Attempting to start server..")
		try:
			self.automan_obj._start()
			self.started = True
			print("started server successfully..")
		except:
			self.fail("could not start server")
		print("Attempting to shutdown server..")
		if self.started:
			try:
				self.automan_obj.shutdown()
				tries = 0
				while self.automan_obj.srvr_popen_obj.poll() is not None and tries<20:
					sleep(1)
					tries = tries + 1
				if tries >= 20:
					self.fail("could not shutdown server")
				else:
					print("server shutdown successfully")
			except:
				self.fail("could not shutdown server")
		else:
			self.fail("could not test shutdown, because server could not be started")

class TestEstimate(unittest.TestCase):
	def setUp(self):
		self.good_adapter =  {"access_id" : "TEST_ACCESS_ID",
							"access_key" : "TEST_ACCESS_KEY",
							"ADDITIONAL_ARG_1" : "ARG1",
							"ADDITIONAL_ARG_2" : "ARG2",
							"type" : "mturk"
							}
		self.automan_obj = Automan(self.good_adapter, server_addr = 'localhost', port = 50051, suppress_output = 'all', 
										loglevel = 'fatal', logging='none', stdout =None, stderr = None, testmode=False)
							
	def tearDown(self):
		self.automan_obj._force_svr_shutdown()

	def test_args_check(self):
		# check text field not blank (it is a required arg), correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="", budget = 1.00)
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text=None, budget = 1.00)
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text=123, budget = 1.00)

		#check budget non-negative ,correct type, not blank (it is a required arg)
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = -1.00)
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = '1.00')

		#check title ,correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, title=123)

		#check img_url ,correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, img_url=123)
		#check img_alt_txt ,correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, img_alt_txt=123)

		#check sample_size ,correct type, strictly postive (except default of -1)
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, sample_size='30')
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, sample_size=0)

		#check confidence ,correct type, between range 50-100
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, confidence='49')
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, confidence=49)
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, confidence=101)

		# check wage, correct type, strictly postive
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, wage='1.00')
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, wage=0)

		# check min_value and max_value, correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, min_value='1')
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, max_value='12')

		# check question_timeout_multiplier and initial_worker_timeout_in_s, correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, question_timeout_multiplier='1')
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, initial_worker_timeout_in_s='12')

		# check dont_reject, correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, dont_reject='False')
		# check pay_all_on_failure, correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, pay_all_on_failure='False')
		# check dry_run, correct type
		self.assertRaises(ArgumentError, self.automan_obj.estimate, text="test text", budget = 1.00, dry_run='False')

	# NEED TO ADD TESTMODE TO SERVER
	'''
	def test_default_args(self):
		self.assertIsInstance(self.automan_obj.estimate(text="test text", budget = 1.00, question_timeout_multiplier=2, initial_worker_timeout_in_s=60)
							EstimateOutcome,
							" estimation test: default args fail")

	def test_estimate(self):
		# submit a question and wait for it to return
		print("")
		qt = 2
		wt = 60
		estim = self.automan_obj.estimate(text="test text", budget = 1.00, question_timeout_multiplier=qt, initial_worker_timeout_in_s=wt)
		estim.done(timeout=3*qt*wt)
	'''

class TestEstimateOutcomeClass(unittest.TestCase):
	pass

