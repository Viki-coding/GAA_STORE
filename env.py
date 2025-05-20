import os

os.environ.setdefault('MY_ENVIRONMENT_VARIABLE', 'variable_value')
os.environ["SECRET_KEY"] = (
	"w!3x@4&$z^7+8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6c7d8e9f0g1h2"
)
os.environ["DEBUG"] = "True"  # Set to "False" in production

os.environ['STRIPE_PUBLIC_KEY'] = 'pk_test_51R8kSeFJh9ihQ61QcMHGVNaBwhJmyPDEyoxGYAyWi5fOzyQ28SjZ6sIdDLlwn1VN2nmCxQyKUTHXaL1BjVqupoZA00CxlM9k3H'
os.environ['STRIPE_SECRET_KEY'] = 'sk_test_51R8kSeFJh9ihQ61QGHpGuZW9dmuEc39dpZMSc7qzxT1hPlGSihlLHxI7ktnKJGwsp8Gtw3te6Cdu5sNzlc1nimGx00VskxdOb5'
os.environ['STRIPE_WH_SECRET'] = 'your_test_webhook_secret'
os.environ['DEBUG'] = 'True'  # Set to 'False' in production