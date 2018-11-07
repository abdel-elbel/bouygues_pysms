# -*- coding: UTF-8 -*-

"""
This module provides a Python interface to Bouygues Mobile SMS API.

See:
    https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/sendSMS.phtml

.. moduleauthor:: abdel.elbel <abdel.elbel@gmail.com>
"""

import requests
import re

__version__ = '0.0.1'


class BouyguesClient(object):
    """
    The Bouygues Telecom Mobile client uses 3 URLs :
    # login : https://www.mon-compte.bouyguestelecom.fr/cas/login
    # step 1 : https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/sendSMS.phtml
    # step 2 : https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/confirmSendSMS.phtml
    # step 3 : https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/resultSendSMS.phtml
    """
        

    def __init__(self, lastname, user, passwd):
        """
        Create a new Bouygues Telecom Mobile client.
        """
        self._lastname = lastname
        self._user = user
        self._passwd = passwd

        print('Profile created')
        
    def login(self):
        """
        Loging in to the Bouygues Telecom site using the credentials through :
        1 - Authenticate + Get sessionId & lt
        2 - Login to base URL using sessionId & lt
        3 - Access to base URL and retrieve info
        """
    #==========================================================================
    #  PART 1 - Authenticate + Get sessionId & lt
    #==========================================================================

        lastname = self._lastname 
        username = self._user
        password = self._passwd
        code=''
         
        print("Authenticating..")
        sess = requests.Session()
        response = sess.get("https://www.mon-compte.bouyguestelecom.fr/cas/login") #SIGNIN_URL 
    
        jsessionid = re.search(b'JSESSIONID=(.*); Path=\/cas\/; HttpOnly'.decode('utf-8'),  response.headers["set-cookie"])
        lt = re.search('<input type=\"hidden\" name=\"lt\" value=\"([a-zA-Z0-9_-]*)\"', response.content.decode('utf-8'))
        
        if (jsessionid == None) | (lt == None):
            code = "LOGIN_UNKNOWN"
        else:
            jsessionid = jsessionid.groups()[0] 
            lt = lt.groups()[0]
            print("Got jsessionid " + jsessionid);
            print("Got lt value " + lt);
    
    #==========================================================================
    #  PART 2 - Login to base URL using sessionId & lt
    #==========================================================================
    
        postData = {
                  'lastname': lastname,  
                  'username': username,
                  'password': password,
                  'rememberMe': 'true',
                  '_rememberMe': 'on',
                  'lt': lt,
                  'execution': 'e1s1',
                  '_eventId': 'submit'
                  }
                  
        response = sess.post("https://www.mon-compte.bouyguestelecom.fr/cas/login;jsessionid=" + jsessionid + "?service=https%3A%2F%2Fwww.secure.bbox.bouyguestelecom.fr%2Fservices%2FSMSIHD%2FsendSMS.phtml", data = postData)  #BASE_URL='https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/sendSMS.phtml'        
        err = re.search('<p class=\"color-mid-grey\">Votre identifiant ou votre mot de passe est incorrect<\/p>', response.content.decode('utf-8'))
        
        if err != None :
            code = "LOGIN_WRONG"
            print(code)
        else :
            print("Authenticated successfully!")
            self._session = sess
            
    #==========================================================================
    #  PART 3 - Access to base URL and retrieve info
    #==========================================================================
            
        response = sess.get("https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/sendSMS.phtml")  
        
        #quota
        quota = re.search(b'Il vous reste <strong>(\d*) SMS gratuit\(s\)<\/strong>', response.content)

        if quota == None :
            code = "ERROR_GETQUOTA"
            print(code)
        else :
            quota = quota.groups()[0].decode("utf-8") 
            print(quota + "/5 message(s) left")
            
        if int(quota) == 0:
            code="QUOTA_EXCEEDED"
                
        self.quota = int(quota)
        
        #sender
        sender = re.search(b'<span class="txt11">Votre SMS apparaitra comme provenant du : (.*)</span>', response.content)
    
        if sender == None :
            code = "ERROR_GETSENDERNUMBER"
            print(code)
        else :
            sender = sender.groups()[0].decode("utf-8") 
            print(sender + " is the sender's number")
            sender = sender.replace(" ", "")
            
        self.sender = sender
                
        return code
  
    def send(self, msg, numbers=None):
        err = self.login()
        maxLength = 160
        sep = ';'
        
        if err :
            print('Message not sent due to error : %s' % err)
        else :
            quota=self.quota
            
            if numbers:
                if isinstance(numbers, list):
                    if len(numbers) > int(quota):
                        print('WARNING : too many numbers to send to. Only the %s first numbers will be used' % quota)
                        numbers = numbers[0:(quota-len(numbers))]
                        
                    numbers = sep.join(numbers)
            else:
                numbers = self.sender
            
            if len(msg) > maxLength : 
                print('WARNING : message have been cut to %s characters to respect the max length ' % maxLength)
                msg = str(msg)[0:maxLength]
            
            return self.sendSMS(msg, numbers)

            
    def sendSMS(self, msg, numbers):
        print(msg, numbers)
        sess = self._session
        code = ''
        
        
    #==========================================================================
    #  Step 1 : 'envoyer un sms', 'valider'
    #==========================================================================
        
        postdata = {
                    'fieldMsisdn': numbers,
                    'fieldMessage': msg,
                    'Verif.x': '72',
                    'Verif.y': '17'
                    }
        
        step1 = sess.post("https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/confirmSendSMS.phtml", postdata)  
        
        err = re.search('Suite \xc3\xa0 un probl\xc3\xa8me technique, nous ne sommes pas en mesure de r\xc3\xa9pondre \xc3\xa0 votre demande.', step1.content.decode("utf-8"))        
        if err != None :
            code = "CODE_ERROR_1003 : Technical problem encountered"
            print(code)   
        else:
            verify = re.search('<span class=\"titre\" style=\"float:left;\">Validation<\/span>', step1.content.decode("utf-8"))
            if verify != None :
                
    #==========================================================================
    #  Step 2 : 'validation', 'envoyer'
    #==========================================================================
    
                print("SMS_CONFIRMATION")
                
                postdata = {
                            'msisdn': numbers,
                            'msg': msg,
                            'Verif.x': '79',
                            'Verif.y': '17'
                            }
        
                step2 = sess.post("https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/SendSMS.phtml", postdata) 
                
    #==========================================================================
    #  PART 3 - Step 3 : 'result', 'envoyer'
    #==========================================================================
    
                step3 = sess.get("https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/resultSendSMS.phtml")  
                verify = re.search('Votre message a bien été envoyé au numéro', 
                                   step3.content.decode("utf-8"))
                if verify != None :
                    print("SMS_SENT")
                
        sess.close()
        return code