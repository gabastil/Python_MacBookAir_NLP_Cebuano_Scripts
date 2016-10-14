
def wrap_test(func):
	def inner_func(name):
		return "This is the result of the func: {}".format(func(name))
	return inner_func

@wrap_test
def get_test(name):
	return "this is a test {}".format(name)

print get_test("TESTES")