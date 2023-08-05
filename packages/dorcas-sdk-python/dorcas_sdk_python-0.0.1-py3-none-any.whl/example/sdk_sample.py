import dorcas_sdk_python
from dorcas_sdk_python.helpers import login_via_password, create_account

client_id = 'jAGOn0aygL'
client_secret = '7CDouHd526pbPubv4fFLRnw5uWjKeaIh0ymsjJ39'
sdk = dorcas_sdk_python.Sdk(client_id, client_secret, environment='local')


def get_plans():
    plans = sdk('resource', 'Plan')
    response = plans.send('get')
    print(response)
    print(response.response.status_code)


def try_login():
    token = login_via_password(sdk, 'emailid@gmail.com', 'password')
    print(token)


def try_register():
    user = create_account(sdk, email='emailid@gmail.com', password='my-password', firstname='Emmanuel', lastname='O',
                          phone='09031234567')
    print(user)
