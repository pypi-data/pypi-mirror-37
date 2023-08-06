from decouple import config

MONGOHOST = config('MONGOHOST', default='localhost')
# The mongodb port 
MONGOPORT = config('MONGOPORT', default=27107)
LIBRARYTYPE = config('LIBRARYTYPE', default='funtime.FunStore') # The name of the library
# ACCESS_TOKEN_SECRET = config('ACCESS_TOKEN_SECRET')
# CONSUMER_KEY = config('CONSUMER_KEY')
# CONSUMER_SECRET = config('CONSUMER_SECRET')

