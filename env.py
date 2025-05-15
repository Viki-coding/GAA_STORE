import os

os.environ.setdefault('MY_ENVIRONMENT_VARIABLE', 'variable_value')
os.environ["SECRET_KEY"] = (
	"w!3x@4&$z^7+8k9l0m1n2o3p4q5r6s7t8u9v0w1x2y3z4a5b6c7d8e9f0g1h2"
)
os.environ["DEBUG"] = "True"  # Set to "False" in production
