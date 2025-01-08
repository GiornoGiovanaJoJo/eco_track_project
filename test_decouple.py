from decouple import config

print(config('TEST_VARIABLE', default='It works!'))