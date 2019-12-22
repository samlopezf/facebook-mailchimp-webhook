#!/usr/bin/python2
from flask import Flask, request

from facebookads.adobjects.lead import Lead
from facebookads.adobjects.leadgenform import LeadgenForm
from facebookads.api import FacebookAdsApi
import mailchimp
import time
import os
import json

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_ACCESS_TOKEN')
FACEBOOK_FORM_ID = os.environ.get('FACEBOOK_FORM_ID')
MAILCHIMP_API_KEY = os.environ.get('MAILCHIMP_API_KEY')
MAILCHIMP_LIST_ID = os.environ.get('MAILCHIMP_LIST_ID')
# Run script every x seconds
SCRIPT_RUNTIME_PERIOD = 86400

def processLead(lead_data):

    subscriber_info = {}

    for fields in lead_data['field_data']:
        subscriber_info[fields['name']] = fields['values'][0]
    print(subscriber_info)
    #mailchimp_api = mailchimp.Mailchimp(MAILCHIMP_API_KEY)
    #mailchimp_api.lists.subscribe(MAILCHIMP_LIST_ID, subscriber_info)

def getLeads(timestamp):
    FacebookAdsApi.init(FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, FACEBOOK_ACCESS_TOKEN)
    form = LeadgenForm(FACEBOOK_FORM_ID)
    leads_data = form.get_leads(params={'filtering':[{'field':'time_created','operator':'GREATER_THAN','value':timestamp}]}

    return leads_data

while 1:
    timestamp = time.time()-SCRIPT_RUNTIME_PERIOD
    leads_data = getLeads(timestamp)
    for lead_data in leads_data:
        processLead(lead_data)
    time.sleep(SCRIPT_RUNTIME_PERIOD)