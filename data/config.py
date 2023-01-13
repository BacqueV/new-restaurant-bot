from environs import Env

# using environs framework
env = Env()
env.read_env()

# environment variables
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = env.list("ADMINS")  # admins list

CHANNELS = ['-1001827005661', '-1001398879340']  # required channels

GEOPY_USER_AGENT = env.str('GEOPY_USER_AGENT')
PROVIDER_TOKEN = env.str('PROVIDER_TOKEN')
