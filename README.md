# bouygues_pysms


Package to use the Bouygues Telecom SMS unofficial API (5 SMS /day limitation)

Uses calls from [this page](https://www.secure.bbox.bouyguestelecom.fr/services/SMSIHD/sendSMS.phtml), and based on [this JS script](https://github.com/y3nd/bouygues-sms)

* 5 SMS /day
* Quota reset at midnight
* 160 chars limit (message is truncated after the limit)
* Error(s) management
* Only ≈125 lines

## Usage
### Installation
```shell
pip install bouygues_pysms
```
### Auth and Get quota left
**Login and retrieve some info from the API (left quota and sending number) before using the quota**
```python
from bouygues_pysms import BouyguesClient

b = BouyguesClient('insert_lastname', 'insert_username', 'insert_passwd')
b.login()
```
### Send 'Hello World!' 
**Left quota is checked at sms sending, no need to double check it (_if the 'send to' number is not specified, the SMS is sent to the sending number_)**
```python
from bouygues_pysms import BouyguesClient

b = BouyguesClient('insert_lastname', 'insert_username', 'insert_passwd')
b.send('Hello World')
```
### Send to multiple numbers (up to 5)
**If more than 5 numbers is submitted, the module takes the 5 first. 
If the 160 chars limit is reached, the message is cut.**
```python 
from bouygues_pysms import BouyguesClient

b = BouyguesClient('insert_lastname', 'insert_username', 'insert_passwd')
b.send('Hello World'* 15, ['0600000001', '0600000002', '0600000003', '0600000004', '0600000005'])
```
### Error codes
| Code                  | Meaning                                                                    |
|:---------------------:|:--------------------------------------------------------------------------:|
| LOGIN_UNKNOWN         | Login page has changed or Bouygues services are down                       |
| LOGIN_WRONG           | Credentials are wrong                                                      |
| QUOTA_EXCEEDED        | Quota is exceeded and SMS can't be sent                                    |
| ERROR_GETQUOTA        | Error getting quota, page has changed or Bouygues services are down        |
| ERROR_GETSENDERNUMBER | Error getting sender number, page has changed or Bouygues services are down|
| CODE_ERROR_1003       | Technical problem encountered at SMS page, error from Bouygues service     |

### Notes
* **I'm NOT affiliated with Bouygues Telecom or one of its branches**
* This module may not work if Bouygues change the service, then **please report it by creating an issue**
* Emojis chars are replaced by a "?" by the Bouygues server ...
