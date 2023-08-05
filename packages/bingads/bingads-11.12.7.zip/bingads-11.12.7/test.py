import os
from suds.client import Client
url = 'https://clientcenter.api.sandbox.bingads.microsoft.com/Api/Billing/v12/CustomerBillingService.svc?singleWsdl'
client = Client(url)
print client