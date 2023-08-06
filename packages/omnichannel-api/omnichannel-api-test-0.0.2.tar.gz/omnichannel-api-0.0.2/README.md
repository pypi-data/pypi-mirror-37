# omnichannel-api
Messente's API which allows sending messages via various channels with fallback options.

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install
The latest released version is available via PyPI
```
pip install omnichannel-api
```


For the latest (unreleased) version you may want to install from Github

```sh
pip install git+https://github.com/messente/messente-omnichannel-python.git
```

Then import the package:
```python
import omnichannel 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import omnichannel
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import omnichannel
from omnichannel.rest import ApiException
from pprint import pprint

from omnichannel import OmnimessageApi, Viber, SMS, Omnimessage, Configuration, ApiClient, WhatsApp, WhatsAppText
from omnichannel.rest import ApiException

# API information from https://dashboard.messente.com/api-settings
configuration = Configuration()
configuration.username = "<MESSENTE_API_USERNAME>"
configuration.password = "<MESSENTE_API_PASSWORD>"

# create an instance of the API class
api_instance = OmnimessageApi(ApiClient(configuration))

whatsapp = WhatsApp(
    sender="<sender name (optional)>",
    text=WhatsAppText(
        body="hello whatsapp"
    )
)

viber = Viber(
    sender="<sender name (optional)>",
    text="hello python",
)

sms = SMS(
    sender="<sender name (optional)>",
    text="hello python",
)

# The order of items in "messages" specifies the sending order: WhatsApp will be attempted
# first, then Viber, and SMS as the final fallback
omnimessage = Omnimessage(
    messages=(whatsapp, viber, sms),
    to="<recipient_phone_number>",
)  # Omnimessage | Omnimessage object that is to be sent

try:
    # Sends an Omnimessage
    response = api_instance.send_omnimessage(omnimessage)
    print(
        "Successfully sent Omnimessage with id: %s that consists of the following messages:" % response.omnimessage_id
    )
    for message in response.messages:
        pprint(message)
except ApiException as e:
    print("Exception when calling OmnimessageApi->create_omnimessage: %s\n" % e)

```

## Documentation for API Endpoints

All URIs are relative to *https://api.messente.com/v1*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*DeliveryReportApi* | [**retrieve_delivery_report**](docs/DeliveryReportApi.md#retrieve_delivery_report) | **GET** /omnimessage/{omnimessage_id}/status | Retrieves the delivery report for the Omnimessage
*OmnimessageApi* | [**cancel_scheduled_message**](docs/OmnimessageApi.md#cancel_scheduled_message) | **DELETE** /omnimessage/{omnimessage_id} | Cancels a scheduled Omnimessage
*OmnimessageApi* | [**send_omnimessage**](docs/OmnimessageApi.md#send_omnimessage) | **POST** /omnimessage | Sends an Omnimessage


## Documentation For Models

 - [Channel](docs/Channel.md)
 - [DeliveryReportResponse](docs/DeliveryReportResponse.md)
 - [DeliveryResult](docs/DeliveryResult.md)
 - [Err](docs/Err.md)
 - [ErrorItem](docs/ErrorItem.md)
 - [ErrorResponse](docs/ErrorResponse.md)
 - [Message](docs/Message.md)
 - [MessageResult](docs/MessageResult.md)
 - [OmniMessageCreateSuccessResponse](docs/OmniMessageCreateSuccessResponse.md)
 - [Omnimessage](docs/Omnimessage.md)
 - [ResponseErrorCode](docs/ResponseErrorCode.md)
 - [ResponseErrorTitle](docs/ResponseErrorTitle.md)
 - [SMS](docs/SMS.md)
 - [Status](docs/Status.md)
 - [Viber](docs/Viber.md)
 - [WhatsApp](docs/WhatsApp.md)
 - [WhatsAppAudio](docs/WhatsAppAudio.md)
 - [WhatsAppDocument](docs/WhatsAppDocument.md)
 - [WhatsAppImage](docs/WhatsAppImage.md)
 - [WhatsAppText](docs/WhatsAppText.md)


## Documentation For Authorization


## basicAuth

- **Type**: HTTP basic authentication


## Author

messente@messente.com


