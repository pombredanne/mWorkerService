# -*- coding: utf-8 -*- 
# Copyright (c) 2014 Baidu.com, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
# an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
"""
Samples for sms client.
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import logging
import os
import sys
import time

file_path = os.path.normpath(os.path.dirname(__file__))
sys.path.append(file_path + '/../../')

import sms_sample_conf
from baidubce.services.sms import sms_client as sms
from baidubce import exception as ex


logging.basicConfig(level=logging.DEBUG, filename='./sms_sample.log', filemode='w')
LOG = logging.getLogger(__name__)
CONF = sms_sample_conf

if __name__ == '__main__':
    sms_client = sms.SmsClient(CONF.config)
    try:
        # query user quota
        LOG.debug('\n\n\nSample 1: Query quota\n\n\n')
        response = sms_client.query_quota()
        print response.max_send_per_day, response.max_receive_per_phone_number_day, \
                response.sent_today
        
        # create template
        LOG.debug('\n\n\nSample 2: Create template \n\n\n')
        response = sms_client.create_template('python-sdk-test', '${PYTHON} SDK ${CODE}')
        template_id = response.template_id
        print template_id
        
        # query template list
        LOG.debug('\n\n\nSample 3: Query template list\n\n\n')
        response = sms_client.get_template_list()
        valid_template_id = None
        valid_template_content = None
        for temp in response.template_list:
            print temp.template_id, temp.name, temp.content, \
                    temp.status, temp.create_time, temp.update_time
            if temp.status == u'VALID':
                valid_template_id = temp.template_id
                valid_template_content = temp.content
                
        #query template        
        LOG.debug('\n\n\nSample 4: Query template\n\n\n')
        response = sms_client.get_template_detail(template_id)
        print response.template_id, response.name, response.content, \
                response.status, response.create_time, response.update_time
                
                
        #delete template
        LOG.debug('\n\n\nSample 5: Delete template\n\n\n')
        sms_client.delete_template(template_id)
        print 'delete ok'
        
        #send message
        LOG.debug('\n\n\nSample 6: Send Message \n\n\n')
        response = sms_client.send_message(valid_template_id, ['13800138000', '13800138001'], \
                                           {'number': "10"})
        
        message_id = response.message_id
        print response.message_id
        
        #query message
        LOG.debug('\n\n\nSample 7: query Message \n\n\n')
        response = sms_client.query_message_detail(message_id)
        
        print response.message_id, response.receiver, response.content, response.send_time
        
        # stat receiver
        LOG.debug('\n\n\nSample 8: query receiver quota\n\n\n')
        response= sms_client.stat_receiver('13800138000')        
        print response.max_receive_per_phone_number_day, response.received_today
        
    except ex.BceHttpClientError as e:
        if isinstance(e.last_error, ex.BceServerError):
            LOG.error('send request failed. Response %s, code: %s, msg: %s'
                      % (e.last_error.status_code, e.last_error.code, e.last_error.message))
        else:
            LOG.error('send request failed. Unknown exception: %s' % e)
