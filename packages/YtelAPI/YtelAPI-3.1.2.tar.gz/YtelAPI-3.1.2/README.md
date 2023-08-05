# Getting started

Ytel API version 3

## How to Build


You must have Python ```2 >=2.7.9``` or Python ```3 >=3.4``` installed on your system to install and run this SDK. This SDK package depends on other Python packages like nose, jsonpickle etc. 
These dependencies are defined in the ```requirements.txt``` file that comes with the SDK.
To resolve these dependencies, you can use the PIP Dependency manager. Install it by following steps at [https://pip.pypa.io/en/stable/installing/](https://pip.pypa.io/en/stable/installing/).

Python and PIP executables should be defined in your PATH. Open command prompt and type ```pip --version```.
This should display the version of the PIP Dependency Manager installed if your installation was successful and the paths are properly defined.

* Using command line, navigate to the directory containing the generated files (including ```requirements.txt```) for the SDK.
* Run the command ```pip install -r requirements.txt```. This should install all the required dependencies.

![Building SDK - Step 1](https://apidocs.io/illustration/python?step=installDependencies&workspaceFolder=Ytel%20API%20V3-Python)


## How to Use

The following section explains how to use the Ytelapiv3 SDK package in a new project.

### 1. Open Project in an IDE

Open up a Python IDE like PyCharm. The basic workflow presented here is also applicable if you prefer using a different editor or IDE.

![Open project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=pyCharm)

Click on ```Open``` in PyCharm to browse to your generated SDK directory and then click ```OK```.

![Open project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=openProject0&workspaceFolder=Ytel%20API%20V3-Python)     

The project files will be displayed in the side bar as follows:

![Open project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=openProject1&workspaceFolder=Ytel%20API%20V3-Python&projectName=ytelapi)     

### 2. Add a new Test Project

Create a new directory by right clicking on the solution name as shown below:

![Add a new project in PyCharm - Step 1](https://apidocs.io/illustration/python?step=createDirectory&workspaceFolder=Ytel%20API%20V3-Python&projectName=ytelapi)

Name the directory as "test"

![Add a new project in PyCharm - Step 2](https://apidocs.io/illustration/python?step=nameDirectory)
   
Add a python file to this project with the name "testsdk"

![Add a new project in PyCharm - Step 3](https://apidocs.io/illustration/python?step=createFile&workspaceFolder=Ytel%20API%20V3-Python&projectName=ytelapi)

Name it "testsdk"

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=nameFile)

In your python file you will be required to import the generated python library using the following code lines

```Python
from ytelapi.ytel_api_client import YtelAPIClient
```

![Add a new project in PyCharm - Step 4](https://apidocs.io/illustration/python?step=projectFiles&workspaceFolder=Ytel%20API%20V3-Python&libraryName=ytelapi.ytel_api_client&projectName=ytelapi&className=YtelAPIClient)

After this you can write code to instantiate an API client object, get a controller object and  make API calls. Sample code is given in the subsequent sections.

### 3. Run the Test Project

To run the file within your test project, right click on your Python file inside your Test project and click on ```Run```

![Run Test Project - Step 1](https://apidocs.io/illustration/python?step=runProject&workspaceFolder=Ytel%20API%20V3-Python&libraryName=ytelapi.ytel_api_client&projectName=ytelapi&className=YtelAPIClient)


## How to Test

You can test the generated SDK and the server with automatically generated test
cases. unittest is used as the testing framework and nose is used as the test
runner. You can run the tests as follows:

  1. From terminal/cmd navigate to the root directory of the SDK.
  2. Invoke ```pip install -r test-requirements.txt```
  3. Invoke ```nosetests```

## Initialization

### Authentication
In order to setup authentication and initialization of the API client, you need the following information.

| Parameter | Description |
|-----------|-------------|
| basic_auth_user_name | The username to use with basic authentication |
| basic_auth_password | The password to use with basic authentication |



API client can be initialized as following.

```python
# Configuration parameters and credentials
basic_auth_user_name = 'basic_auth_user_name' # The username to use with basic authentication
basic_auth_password = 'basic_auth_password' # The password to use with basic authentication

client = YtelAPIClient(basic_auth_user_name, basic_auth_password)
```



# Class Reference

## <a name="list_of_controllers"></a>List of Controllers

* [ShortCodeController](#short_code_controller)
* [AreaMailController](#area_mail_controller)
* [PostCardController](#post_card_controller)
* [LetterController](#letter_controller)
* [CallController](#call_controller)
* [PhoneNumberController](#phone_number_controller)
* [SMSController](#sms_controller)
* [SharedShortCodeController](#shared_short_code_controller)
* [ConferenceController](#conference_controller)
* [CarrierController](#carrier_controller)
* [EmailController](#email_controller)
* [AccountController](#account_controller)
* [SubAccountController](#sub_account_controller)
* [AddressController](#address_controller)
* [RecordingController](#recording_controller)
* [TranscriptionController](#transcription_controller)
* [UsageController](#usage_controller)

## <a name="short_code_controller"></a>![Class: ](https://apidocs.io/img/class.png ".ShortCodeController") ShortCodeController

### Get controller instance

An instance of the ``` ShortCodeController ``` class can be accessed from the API Client.

```python
 short_code_controller = client.short_code
```

### <a name="create_list_shortcodes"></a>![Method: ](https://apidocs.io/img/method.png ".ShortCodeController.create_list_shortcodes") create_list_shortcodes

> Retrieve a list of Short Code assignment associated with your Ytel account.

```python
def create_list_shortcodes(self,
                               shortcode=None,
                               page=None,
                               pagesize=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Optional ```  | Only list Short Code Assignment sent from this Short Code |
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |



#### Example Usage

```python
shortcode = 'Shortcode'
page = 'page'
pagesize = 'pagesize'

result = short_code_controller.create_list_shortcodes(shortcode, page, pagesize)

```


### <a name="create_view_sms"></a>![Method: ](https://apidocs.io/img/method.png ".ShortCodeController.create_view_sms") create_view_sms

> Retrieve a single Short Code object by its shortcode assignment.

```python
def create_view_sms(self,
                        shortcode)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Required ```  | List of valid Dedicated Short Code to your Ytel account |



#### Example Usage

```python
shortcode = 'Shortcode'

result = short_code_controller.create_view_sms(shortcode)

```


### <a name="create_view_sms_1"></a>![Method: ](https://apidocs.io/img/method.png ".ShortCodeController.create_view_sms_1") create_view_sms_1

> View a single Sms Short Code message.

```python
def create_view_sms_1(self,
                          message_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| messageSid |  ``` Required ```  | The unique identifier for the sms resource |



#### Example Usage

```python
message_sid = 'MessageSid'

result = short_code_controller.create_view_sms_1(message_sid)

```


### <a name="create_list_sms"></a>![Method: ](https://apidocs.io/img/method.png ".ShortCodeController.create_list_sms") create_list_sms

> Retrieve a list of Short Code messages.

```python
def create_list_sms(self,
                        shortcode=None,
                        to=None,
                        date_sent=None,
                        page=None,
                        page_size=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Optional ```  | Only list messages sent from this Short Code |
| to |  ``` Optional ```  | Only list messages sent to this number |
| dateSent |  ``` Optional ```  | Only list messages sent with the specified date |
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pageSize |  ``` Optional ```  | The count of objects to return per page. |



#### Example Usage

```python
shortcode = 'Shortcode'
to = 'To'
date_sent = 'DateSent'
page = 60
page_size = 60

result = short_code_controller.create_list_sms(shortcode, to, date_sent, page, page_size)

```


### <a name="create_send_sms"></a>![Method: ](https://apidocs.io/img/method.png ".ShortCodeController.create_send_sms") create_send_sms

> Send Dedicated Shortcode

```python
def create_send_sms(self,
                        shortcode,
                        to,
                        body,
                        method=None,
                        messagestatuscallback=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Required ```  | Your dedicated shortcode |
| to |  ``` Required ```  | The number to send your SMS to |
| body |  ``` Required ```  | The body of your message |
| method |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once the Short Code message is sent.GET or POST |
| messagestatuscallback |  ``` Optional ```  | URL that can be requested to receive notification when Short Code message was sent. |



#### Example Usage

```python
shortcode = 60
to = 60.4520415703077
body = 'body'
method = 'method'
messagestatuscallback = 'messagestatuscallback'

result = short_code_controller.create_send_sms(shortcode, to, body, method, messagestatuscallback)

```


### <a name="create_list_inbound_sms"></a>![Method: ](https://apidocs.io/img/method.png ".ShortCodeController.create_list_inbound_sms") create_list_inbound_sms

> Retrive a list of inbound Sms Short Code messages associated with your Ytel account.

```python
def create_list_inbound_sms(self,
                                page=None,
                                pagesize=None,
                                mfrom=None,
                                shortcode=None,
                                datecreated=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | Number of individual resources listed in the response per page |
| mfrom |  ``` Optional ```  | Only list SMS messages sent from this number |
| shortcode |  ``` Optional ```  | Only list SMS messages sent to Shortcode |
| datecreated |  ``` Optional ```  | Only list SMS messages sent in the specified date MAKE REQUEST |



#### Example Usage

```python
page = 60
pagesize = 60
mfrom = 'From'
shortcode = 'Shortcode'
datecreated = 'Datecreated'

result = short_code_controller.create_list_inbound_sms(page, pagesize, mfrom, shortcode, datecreated)

```


### <a name="update_shortcode"></a>![Method: ](https://apidocs.io/img/method.png ".ShortCodeController.update_shortcode") update_shortcode

> Update a dedicated shortcode.

```python
def update_shortcode(self,
                         shortcode,
                         friendly_name=None,
                         callback_method=None,
                         callback_url=None,
                         fallback_method=None,
                         fallback_url=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Required ```  | List of valid dedicated shortcode to your Ytel account. |
| friendlyName |  ``` Optional ```  | User generated name of the dedicated shortcode. |
| callbackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required StatusCallBackUrl once call connects. |
| callbackUrl |  ``` Optional ```  | URL that can be requested to receive notification when call has ended. A set of default parameters will be sent here once the call is finished. |
| fallbackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required FallbackUrl once call connects. |
| fallbackUrl |  ``` Optional ```  | URL used if any errors occur during execution of InboundXML or at initial request of the required Url provided with the POST. |



#### Example Usage

```python
shortcode = 'Shortcode'
friendly_name = 'FriendlyName'
callback_method = 'CallbackMethod'
callback_url = 'CallbackUrl'
fallback_method = 'FallbackMethod'
fallback_url = 'FallbackUrl'

result = short_code_controller.update_shortcode(shortcode, friendly_name, callback_method, callback_url, fallback_method, fallback_url)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="area_mail_controller"></a>![Class: ](https://apidocs.io/img/class.png ".AreaMailController") AreaMailController

### Get controller instance

An instance of the ``` AreaMailController ``` class can be accessed from the API Client.

```python
 area_mail_controller = client.area_mail
```

### <a name="create_delete_area_mail"></a>![Method: ](https://apidocs.io/img/method.png ".AreaMailController.create_delete_area_mail") create_delete_area_mail

> Remove an AreaMail object by its AreaMailId.

```python
def create_delete_area_mail(self,
                                areamailid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| areamailid |  ``` Required ```  | The unique identifier for an AreaMail object. |



#### Example Usage

```python
areamailid = 'areamailid'

result = area_mail_controller.create_delete_area_mail(areamailid)

```


### <a name="create_view_area_mail"></a>![Method: ](https://apidocs.io/img/method.png ".AreaMailController.create_view_area_mail") create_view_area_mail

> Retrieve an AreaMail object by its AreaMailId.

```python
def create_view_area_mail(self,
                              areamailid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| areamailid |  ``` Required ```  | The unique identifier for an AreaMail object. |



#### Example Usage

```python
areamailid = 'areamailid'

result = area_mail_controller.create_view_area_mail(areamailid)

```


### <a name="create_list_area_mails"></a>![Method: ](https://apidocs.io/img/method.png ".AreaMailController.create_list_area_mails") create_list_area_mails

> Retrieve a list of AreaMail objects.

```python
def create_list_area_mails(self,
                               page=None,
                               pagesize=None,
                               areamailsid=None,
                               date_created=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |
| areamailsid |  ``` Optional ```  | The unique identifier for an AreaMail object. |
| dateCreated |  ``` Optional ```  | The date the AreaMail was created. |



#### Example Usage

```python
page = 60
pagesize = 60
areamailsid = 'areamailsid'
date_created = 'dateCreated'

result = area_mail_controller.create_list_area_mails(page, pagesize, areamailsid, date_created)

```


### <a name="create_area_mail"></a>![Method: ](https://apidocs.io/img/method.png ".AreaMailController.create_area_mail") create_area_mail

> Create a new AreaMail object.

```python
def create_area_mail(self,
                         routes,
                         attachbyid,
                         front,
                         back,
                         description=None,
                         targettype=None,
                         htmldata=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| routes |  ``` Required ```  | List of routes that AreaMail should be delivered to.  A single route can be either a zipcode or a carrier route.List of routes that AreaMail should be delivered to.  A single route can be either a zipcode or a carrier route. A carrier route is in the form of 92610-C043 where the carrier route is composed of 5 numbers for zipcode, 1 letter for carrier route type, and 3 numbers for carrier route code. Delivery can be sent to mutliple routes by separating them with a commas. Valid Values: 92656, 92610-C043 |
| attachbyid |  ``` Required ```  | Set an existing areamail by attaching its AreamailId. |
| front |  ``` Required ```  | The front of the AreaMail item to be created. This can be a URL, local file, or an HTML string. Supported file types are PDF, PNG, and JPEG. Back required |
| back |  ``` Required ```  | The back of the AreaMail item to be created. This can be a URL, local file, or an HTML string. Supported file types are PDF, PNG, and JPEG. |
| description |  ``` Optional ```  | A string value to use as a description for this AreaMail item. |
| targettype |  ``` Optional ```  | The delivery location type. |
| htmldata |  ``` Optional ```  | A string value that contains HTML markup. |



#### Example Usage

```python
routes = 'routes'
attachbyid = 'attachbyid'
front = 'front'
back = 'back'
description = 'description'
targettype = 'targettype'
htmldata = 'htmldata'

result = area_mail_controller.create_area_mail(routes, attachbyid, front, back, description, targettype, htmldata)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="post_card_controller"></a>![Class: ](https://apidocs.io/img/class.png ".PostCardController") PostCardController

### Get controller instance

An instance of the ``` PostCardController ``` class can be accessed from the API Client.

```python
 post_card_controller = client.post_card
```

### <a name="create_delete_postcard"></a>![Method: ](https://apidocs.io/img/method.png ".PostCardController.create_delete_postcard") create_delete_postcard

> Remove a postcard object.

```python
def create_delete_postcard(self,
                               postcardid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| postcardid |  ``` Required ```  | The unique identifier of a postcard object. |



#### Example Usage

```python
postcardid = 'postcardid'

result = post_card_controller.create_delete_postcard(postcardid)

```


### <a name="create_view_postcard"></a>![Method: ](https://apidocs.io/img/method.png ".PostCardController.create_view_postcard") create_view_postcard

> Retrieve a postcard object by its PostcardId.

```python
def create_view_postcard(self,
                             postcardid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| postcardid |  ``` Required ```  | The unique identifier for a postcard object. |



#### Example Usage

```python
postcardid = 'postcardid'

result = post_card_controller.create_view_postcard(postcardid)

```


### <a name="create_postcard"></a>![Method: ](https://apidocs.io/img/method.png ".PostCardController.create_postcard") create_postcard

> Create, print, and mail a postcard to an address. The postcard front must be supplied as a PDF, image, or an HTML string. The back can be a PDF, image, HTML string, or it can be automatically generated by supplying a custom message.

```python
def create_postcard(self,
                        to,
                        mfrom,
                        attachbyid,
                        front,
                        back,
                        message,
                        setting,
                        description=None,
                        htmldata=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| to |  ``` Required ```  | The AddressId or an object structured when creating an address by addresses/Create. |
| mfrom |  ``` Required ```  | The AddressId or an object structured when creating an address by addresses/Create. |
| attachbyid |  ``` Required ```  | Set an existing postcard by attaching its PostcardId. |
| front |  ``` Required ```  | A 4.25"x6.25" or 6.25"x11.25" image to use as the front of the postcard.  This can be a URL, local file, or an HTML string. Supported file types are PDF, PNG, and JPEG. |
| back |  ``` Required ```  | A 4.25"x6.25" or 6.25"x11.25" image to use as the back of the postcard, supplied as a URL, local file, or HTML string.  This allows you to customize your back design, but we will still insert the recipient address for you. |
| message |  ``` Required ```  | The message for the back of the postcard with a maximum of 350 characters. |
| setting |  ``` Required ```  | Code for the dimensions of the media to be printed. |
| description |  ``` Optional ```  | A description for the postcard. |
| htmldata |  ``` Optional ```  | A string value that contains HTML markup. |



#### Example Usage

```python
to = 'to'
mfrom = 'from'
attachbyid = 'attachbyid'
front = 'front'
back = 'back'
message = 'message'
setting = 'setting'
description = 'description'
htmldata = 'htmldata'

result = post_card_controller.create_postcard(to, mfrom, attachbyid, front, back, message, setting, description, htmldata)

```


### <a name="create_list_postcards"></a>![Method: ](https://apidocs.io/img/method.png ".PostCardController.create_list_postcards") create_list_postcards

> Retrieve a list of postcard objects. The postcards objects are sorted by creation date, with the most recently created postcards appearing first.

```python
def create_list_postcards(self,
                              page=None,
                              pagesize=None,
                              postcardid=None,
                              date_created=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |
| postcardid |  ``` Optional ```  | The unique identifier for a postcard object. |
| dateCreated |  ``` Optional ```  | The date the postcard was created. |



#### Example Usage

```python
page = 223
pagesize = 223
postcardid = 'postcardid'
date_created = 'dateCreated'

result = post_card_controller.create_list_postcards(page, pagesize, postcardid, date_created)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="letter_controller"></a>![Class: ](https://apidocs.io/img/class.png ".LetterController") LetterController

### Get controller instance

An instance of the ``` LetterController ``` class can be accessed from the API Client.

```python
 letter_controller = client.letter
```

### <a name="create_delete_letter"></a>![Method: ](https://apidocs.io/img/method.png ".LetterController.create_delete_letter") create_delete_letter

> Remove a letter object by its LetterId.

```python
def create_delete_letter(self,
                             lettersid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| lettersid |  ``` Required ```  | The unique identifier for a letter object. |



#### Example Usage

```python
lettersid = 'lettersid'

result = letter_controller.create_delete_letter(lettersid)

```


### <a name="create_view_letter"></a>![Method: ](https://apidocs.io/img/method.png ".LetterController.create_view_letter") create_view_letter

> Retrieve a letter object by its LetterSid.

```python
def create_view_letter(self,
                           lettersid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| lettersid |  ``` Required ```  | The unique identifier for a letter object. |



#### Example Usage

```python
lettersid = 'lettersid'

result = letter_controller.create_view_letter(lettersid)

```


### <a name="create_letter"></a>![Method: ](https://apidocs.io/img/method.png ".LetterController.create_letter") create_letter

> Create, print, and mail a letter to an address. The letter file must be supplied as a PDF or an HTML string.

```python
def create_letter(self,
                      to,
                      mfrom,
                      attachbyid,
                      file,
                      color,
                      description=None,
                      extraservice=None,
                      doublesided=None,
                      template=None,
                      htmldata=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| to |  ``` Required ```  | The AddressId or an object structured when creating an address by addresses/Create. |
| mfrom |  ``` Required ```  | The AddressId or an object structured when creating an address by addresses/Create. |
| attachbyid |  ``` Required ```  | Set an existing letter by attaching its LetterId. |
| file |  ``` Required ```  | File can be a 8.5"x11" PDF uploaded file or URL that links to a file. |
| color |  ``` Required ```  | Specify if letter should be printed in color. |
| description |  ``` Optional ```  | A description for the letter. |
| extraservice |  ``` Optional ```  | Add an extra service to your letter. Options are "certified" or "registered". Certified provides tracking and delivery confirmation for domestic destinations and is an additional $5.00. Registered provides tracking and confirmation for international addresses and is an additional $16.50. |
| doublesided |  ``` Optional ```  | Specify if letter should be printed on both sides. |
| template |  ``` Optional ```  | Boolean that defaults to true. When set to false, this specifies that your letter does not follow the m360 address template. In this case, a blank address page will be inserted at the beginning of your file and you will be charged for the extra page. |
| htmldata |  ``` Optional ```  | A string value that contains HTML markup. |



#### Example Usage

```python
to = 'to'
mfrom = 'from'
attachbyid = 'attachbyid'
file = 'file'
color = 'color'
description = 'description'
extraservice = 'extraservice'
doublesided = 'doublesided'
template = 'template'
htmldata = 'htmldata'

result = letter_controller.create_letter(to, mfrom, attachbyid, file, color, description, extraservice, doublesided, template, htmldata)

```


### <a name="create_list_letters"></a>![Method: ](https://apidocs.io/img/method.png ".LetterController.create_list_letters") create_list_letters

> Retrieve a list of letter objects. The letter objects are sorted by creation date, with the most recently created letters appearing first.

```python
def create_list_letters(self,
                            page=None,
                            pagesize=None,
                            lettersid=None,
                            date_created=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |
| lettersid |  ``` Optional ```  | The unique identifier for a letter object. |
| dateCreated |  ``` Optional ```  | The date the letter was created. |



#### Example Usage

```python
page = 223
pagesize = 223
lettersid = 'lettersid'
date_created = 'dateCreated'

result = letter_controller.create_list_letters(page, pagesize, lettersid, date_created)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="call_controller"></a>![Class: ](https://apidocs.io/img/class.png ".CallController") CallController

### Get controller instance

An instance of the ``` CallController ``` class can be accessed from the API Client.

```python
 call_controller = client.call
```

### <a name="create_view_call_1"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_view_call_1") create_view_call_1

> Retrieve a single voice call’s information by its CallSid.

```python
def create_view_call_1(self,
                           call_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| callSid |  ``` Required ```  | The unique identifier for the voice call. |



#### Example Usage

```python
call_sid = 'callSid'

result = call_controller.create_view_call_1(call_sid)

```


### <a name="create_view_call"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_view_call") create_view_call

> Retrieve a single voice call’s information by its CallSid.

```python
def create_view_call(self,
                         callsid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| callsid |  ``` Required ```  | The unique identifier for the voice call. |



#### Example Usage

```python
callsid = 'callsid'

result = call_controller.create_view_call(callsid)

```


### <a name="create_play_dtmf"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_play_dtmf") create_play_dtmf

> Play Dtmf and send the Digit

```python
def create_play_dtmf(self,
                         call_sid,
                         play_dtmf,
                         play_dtmf_direction=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| callSid |  ``` Required ```  | The unique identifier of each call resource |
| playDtmf |  ``` Required ```  | DTMF digits to play to the call. 0-9, #, *, W, or w |
| playDtmfDirection |  ``` Optional ```  | The leg of the call DTMF digits should be sent to |



#### Example Usage

```python
call_sid = 'CallSid'
play_dtmf = 'PlayDtmf'
play_dtmf_direction = PlayDtmfDirectionEnum.IN

result = call_controller.create_play_dtmf(call_sid, play_dtmf, play_dtmf_direction)

```


### <a name="create_make_call"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_make_call") create_make_call

> You can experiment with initiating a call through Ytel and view the request response generated when doing so and get the response in json

```python
def create_make_call(self,
                         mfrom,
                         to,
                         url,
                         method=None,
                         status_call_back_url=None,
                         status_call_back_method=None,
                         fall_back_url=None,
                         fall_back_method=None,
                         heart_beat_url=None,
                         heart_beat_method=None,
                         timeout=None,
                         play_dtmf=None,
                         hide_caller_id=None,
                         record=None,
                         record_call_back_url=None,
                         record_call_back_method=None,
                         transcribe=None,
                         transcribe_call_back_url=None,
                         if_machine=None,
                         if_machine_url=None,
                         if_machine_method=None,
                         feedback=None,
                         survey_id=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| mfrom |  ``` Required ```  | A valid Ytel Voice enabled number (E.164 format) that will be initiating the phone call. |
| to |  ``` Required ```  | To number |
| url |  ``` Required ```  | URL requested once the call connects |
| method |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once call connects. |
| statusCallBackUrl |  ``` Optional ```  | URL that can be requested to receive notification when call has ended. A set of default parameters will be sent here once the call is finished. |
| statusCallBackMethod |  ``` Optional ```  | Specifies the HTTP methodlinkclass used to request StatusCallbackUrl. |
| fallBackUrl |  ``` Optional ```  | URL requested if the initial Url parameter fails or encounters an error |
| fallBackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required FallbackUrl once call connects. |
| heartBeatUrl |  ``` Optional ```  | URL that can be requested every 60 seconds during the call to notify of elapsed tim |
| heartBeatMethod |  ``` Optional ```  | Specifies the HTTP method used to request HeartbeatUrl. |
| timeout |  ``` Optional ```  | Time (in seconds) Ytel should wait while the call is ringing before canceling the call |
| playDtmf |  ``` Optional ```  | DTMF Digits to play to the call once it connects. 0-9, #, or * |
| hideCallerId |  ``` Optional ```  | Specifies if the caller id will be hidden |
| record |  ``` Optional ```  | Specifies if the call should be recorded |
| recordCallBackUrl |  ``` Optional ```  | Recording parameters will be sent here upon completion |
| recordCallBackMethod |  ``` Optional ```  | Method used to request the RecordCallback URL. |
| transcribe |  ``` Optional ```  | Specifies if the call recording should be transcribed |
| transcribeCallBackUrl |  ``` Optional ```  | Transcription parameters will be sent here upon completion |
| ifMachine |  ``` Optional ```  | How Ytel should handle the receiving numbers voicemail machine |
| ifMachineUrl |  ``` Optional ```  | URL requested when IfMachine=continue |
| ifMachineMethod |  ``` Optional ```  | Method used to request the IfMachineUrl. |
| feedback |  ``` Optional ```  | Specify if survey should be enable or not |
| surveyId |  ``` Optional ```  | The unique identifier for the survey. |



#### Example Usage

```python
mfrom = 'From'
to = 'To'
url = 'Url'
method = 'Method'
status_call_back_url = 'StatusCallBackUrl'
status_call_back_method = 'StatusCallBackMethod'
fall_back_url = 'FallBackUrl'
fall_back_method = 'FallBackMethod'
heart_beat_url = 'HeartBeatUrl'
heart_beat_method = 'HeartBeatMethod'
timeout = 223
play_dtmf = 'PlayDtmf'
hide_caller_id = True
record = True
record_call_back_url = 'RecordCallBackUrl'
record_call_back_method = 'RecordCallBackMethod'
transcribe = True
transcribe_call_back_url = 'TranscribeCallBackUrl'
if_machine = IfMachineEnum.CONTINUE
if_machine_url = 'IfMachineUrl'
if_machine_method = 'IfMachineMethod'
feedback = True
survey_id = 'SurveyId'

result = call_controller.create_make_call(mfrom, to, url, method, status_call_back_url, status_call_back_method, fall_back_url, fall_back_method, heart_beat_url, heart_beat_method, timeout, play_dtmf, hide_caller_id, record, record_call_back_url, record_call_back_method, transcribe, transcribe_call_back_url, if_machine, if_machine_url, if_machine_method, feedback, survey_id)

```


### <a name="create_play_audio"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_play_audio") create_play_audio

> Play Audio from a url

```python
def create_play_audio(self,
                          call_sid,
                          audio_url,
                          say_text,
                          length=None,
                          direction=None,
                          mix=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| callSid |  ``` Required ```  | The unique identifier of each call resource |
| audioUrl |  ``` Required ```  | URL to sound that should be played. You also can add more than one audio file using semicolons e.g. http://example.com/audio1.mp3;http://example.com/audio2.wav |
| sayText |  ``` Required ```  | Valid alphanumeric string that should be played to the In-progress call. |
| length |  ``` Optional ```  | Time limit in seconds for audio play back |
| direction |  ``` Optional ```  | The leg of the call audio will be played to |
| mix |  ``` Optional ```  | If false, all other audio will be muted |



#### Example Usage

```python
call_sid = 'CallSid'
audio_url = 'AudioUrl'
say_text = 'SayText'
length = 223
direction = DirectionEnum.IN
mix = True

result = call_controller.create_play_audio(call_sid, audio_url, say_text, length, direction, mix)

```


### <a name="create_record_call"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_record_call") create_record_call

> Start or stop recording of an in-progress voice call.

```python
def create_record_call(self,
                           call_sid,
                           record,
                           direction=None,
                           time_limit=None,
                           call_back_url=None,
                           fileformat=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| callSid |  ``` Required ```  | The unique identifier of each call resource |
| record |  ``` Required ```  | Set true to initiate recording or false to terminate recording |
| direction |  ``` Optional ```  | The leg of the call to record |
| timeLimit |  ``` Optional ```  | Time in seconds the recording duration should not exceed |
| callBackUrl |  ``` Optional ```  | URL consulted after the recording completes |
| fileformat |  ``` Optional ```  | Format of the recording file. Can be .mp3 or .wav |



#### Example Usage

```python
call_sid = 'CallSid'
record = True
direction = Direction4Enum.IN
time_limit = 223
call_back_url = 'CallBackUrl'
fileformat = FileformatEnum.MP3

result = call_controller.create_record_call(call_sid, record, direction, time_limit, call_back_url, fileformat)

```


### <a name="create_voice_effect"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_voice_effect") create_voice_effect

> Add audio voice effects to the an in-progress voice call.

```python
def create_voice_effect(self,
                            call_sid,
                            audio_direction=None,
                            pitch_semi_tones=None,
                            pitch_octaves=None,
                            pitch=None,
                            rate=None,
                            tempo=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| callSid |  ``` Required ```  | The unique identifier for the in-progress voice call. |
| audioDirection |  ``` Optional ```  | The direction the audio effect should be placed on. If IN, the effects will occur on the incoming audio stream. If OUT, the effects will occur on the outgoing audio stream. |
| pitchSemiTones |  ``` Optional ```  | Set the pitch in semitone (half-step) intervals. Value between -14 and 14 |
| pitchOctaves |  ``` Optional ```  | Set the pitch in octave intervals.. Value between -1 and 1 |
| pitch |  ``` Optional ```  | Set the pitch (lowness/highness) of the audio. The higher the value, the higher the pitch. Value greater than 0 |
| rate |  ``` Optional ```  | Set the rate for audio. The lower the value, the lower the rate. value greater than 0 |
| tempo |  ``` Optional ```  | Set the tempo (speed) of the audio. A higher value denotes a faster tempo. Value greater than 0 |



#### Example Usage

```python
call_sid = 'CallSid'
audio_direction = AudioDirectionEnum.IN
pitch_semi_tones = 223.956759678645
pitch_octaves = 223.956759678645
pitch = 223.956759678645
rate = 223.956759678645
tempo = 223.956759678645

result = call_controller.create_voice_effect(call_sid, audio_direction, pitch_semi_tones, pitch_octaves, pitch, rate, tempo)

```


### <a name="create_interrupt_call"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_interrupt_call") create_interrupt_call

> Interrupt the Call by Call Sid

```python
def create_interrupt_call(self,
                              call_sid,
                              url=None,
                              method=None,
                              status=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| callSid |  ``` Required ```  | The unique identifier for voice call that is in progress. |
| url |  ``` Optional ```  | URL the in-progress call will be redirected to |
| method |  ``` Optional ```  | The method used to request the above Url parameter |
| status |  ``` Optional ```  | Status to set the in-progress call to |



#### Example Usage

```python
call_sid = 'CallSid'
url = 'Url'
method = 'Method'
status = StatusEnum.CANCELED

result = call_controller.create_interrupt_call(call_sid, url, method, status)

```


### <a name="create_list_calls"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_list_calls") create_list_calls

> A list of calls associated with your Ytel account

```python
def create_list_calls(self,
                          page=None,
                          page_size=None,
                          to=None,
                          mfrom=None,
                          date_created=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pageSize |  ``` Optional ```  | Number of individual resources listed in the response per page |
| to |  ``` Optional ```  | Filter calls that were sent to this 10-digit number (E.164 format). |
| mfrom |  ``` Optional ```  | Filter calls that were sent from this 10-digit number (E.164 format). |
| dateCreated |  ``` Optional ```  | Return calls that are from a specified date. |



#### Example Usage

```python
page = 223
page_size = 223
to = 'To'
mfrom = 'From'
date_created = 'DateCreated'

result = call_controller.create_list_calls(page, page_size, to, mfrom, date_created)

```


### <a name="create_send_rvm"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_send_rvm") create_send_rvm

> Initiate an outbound Ringless Voicemail through Ytel.

```python
def create_send_rvm(self,
                        mfrom,
                        rvm_caller_id,
                        to,
                        voice_mail_url,
                        method=None,
                        status_call_back_url=None,
                        stats_call_back_method=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| mfrom |  ``` Required ```  | A valid Ytel Voice enabled number (E.164 format) that will be initiating the phone call. |
| rVMCallerId |  ``` Required ```  | A required secondary Caller ID for RVM to work. |
| to |  ``` Required ```  | A valid number (E.164 format) that will receive the phone call. |
| voiceMailURL |  ``` Required ```  | The URL requested once the RVM connects. A set of default parameters will be sent here. |
| method |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once call connects. |
| statusCallBackUrl |  ``` Optional ```  | URL that can be requested to receive notification when call has ended. A set of default parameters will be sent here once the call is finished. |
| statsCallBackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required StatusCallBackUrl once call connects. |



#### Example Usage

```python
mfrom = 'From'
rvm_caller_id = 'RVMCallerId'
to = 'To'
voice_mail_url = 'VoiceMailURL'
method = 'Method'
status_call_back_url = 'StatusCallBackUrl'
stats_call_back_method = 'StatsCallBackMethod'

result = call_controller.create_send_rvm(mfrom, rvm_caller_id, to, voice_mail_url, method, status_call_back_url, stats_call_back_method)

```


### <a name="create_group_call"></a>![Method: ](https://apidocs.io/img/method.png ".CallController.create_group_call") create_group_call

> Group Call

```python
def create_group_call(self,
                          mfrom,
                          to,
                          url,
                          group_confirm_key,
                          group_confirm_file,
                          method=None,
                          status_call_back_url=None,
                          status_call_back_method=None,
                          fall_back_url=None,
                          fall_back_method=None,
                          heart_beat_url=None,
                          heart_beat_method=None,
                          timeout=None,
                          play_dtmf=None,
                          hide_caller_id=None,
                          record=None,
                          record_call_back_url=None,
                          record_call_back_method=None,
                          transcribe=None,
                          transcribe_call_back_url=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| mfrom |  ``` Required ```  | This number to display on Caller ID as calling |
| to |  ``` Required ```  | Please enter multiple E164 number. You can add max 10 numbers. Add numbers separated with comma. e.g : 1111111111,2222222222 |
| url |  ``` Required ```  | URL requested once the call connects |
| groupConfirmKey |  ``` Required ```  | Define the DTMF that the called party should send to bridge the call. Allowed Values : 0-9, #, * |
| groupConfirmFile |  ``` Required ```  | Specify the audio file you want to play when the called party picks up the call |
| method |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once call connects. |
| statusCallBackUrl |  ``` Optional ```  | URL that can be requested to receive notification when call has ended. A set of default parameters will be sent here once the call is finished. |
| statusCallBackMethod |  ``` Optional ```  | Specifies the HTTP methodlinkclass used to request StatusCallbackUrl. |
| fallBackUrl |  ``` Optional ```  | URL requested if the initial Url parameter fails or encounters an error |
| fallBackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required FallbackUrl once call connects. |
| heartBeatUrl |  ``` Optional ```  | URL that can be requested every 60 seconds during the call to notify of elapsed time and pass other general information. |
| heartBeatMethod |  ``` Optional ```  | Specifies the HTTP method used to request HeartbeatUrl. |
| timeout |  ``` Optional ```  | Time (in seconds) we should wait while the call is ringing before canceling the call |
| playDtmf |  ``` Optional ```  | DTMF Digits to play to the call once it connects. 0-9, #, or * |
| hideCallerId |  ``` Optional ```  | Specifies if the caller id will be hidden |
| record |  ``` Optional ```  | Specifies if the call should be recorded |
| recordCallBackUrl |  ``` Optional ```  | Recording parameters will be sent here upon completion |
| recordCallBackMethod |  ``` Optional ```  | Method used to request the RecordCallback URL. |
| transcribe |  ``` Optional ```  | Specifies if the call recording should be transcribed |
| transcribeCallBackUrl |  ``` Optional ```  | Transcription parameters will be sent here upon completion |



#### Example Usage

```python
mfrom = 'From'
to = 'To'
url = 'Url'
group_confirm_key = 'GroupConfirmKey'
group_confirm_file = GroupConfirmFileEnum.MP3
method = 'Method'
status_call_back_url = 'StatusCallBackUrl'
status_call_back_method = 'StatusCallBackMethod'
fall_back_url = 'FallBackUrl'
fall_back_method = 'FallBackMethod'
heart_beat_url = 'HeartBeatUrl'
heart_beat_method = 'HeartBeatMethod'
timeout = 132
play_dtmf = 'PlayDtmf'
hide_caller_id = 'HideCallerId'
record = True
record_call_back_url = 'RecordCallBackUrl'
record_call_back_method = 'RecordCallBackMethod'
transcribe = True
transcribe_call_back_url = 'TranscribeCallBackUrl'

result = call_controller.create_group_call(mfrom, to, url, group_confirm_key, group_confirm_file, method, status_call_back_url, status_call_back_method, fall_back_url, fall_back_method, heart_beat_url, heart_beat_method, timeout, play_dtmf, hide_caller_id, record, record_call_back_url, record_call_back_method, transcribe, transcribe_call_back_url)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="phone_number_controller"></a>![Class: ](https://apidocs.io/img/class.png ".PhoneNumberController") PhoneNumberController

### Get controller instance

An instance of the ``` PhoneNumberController ``` class can be accessed from the API Client.

```python
 phone_number_controller = client.phone_number
```

### <a name="create_get_did_score"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_get_did_score") create_get_did_score

> Get DID Score Number

```python
def create_get_did_score(self,
                             phonenumber)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phonenumber |  ``` Required ```  | Specifies the multiple phone numbers for check updated spamscore . |



#### Example Usage

```python
phonenumber = 'Phonenumber'

result = phone_number_controller.create_get_did_score(phonenumber)

```


### <a name="create_move_number"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_move_number") create_move_number

> Transfer phone number that has been purchased for from one account to another account.

```python
def create_move_number(self,
                           phonenumber,
                           fromaccountsid,
                           toaccountsid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phonenumber |  ``` Required ```  | A valid 10-digit Ytel number (E.164 format). |
| fromaccountsid |  ``` Required ```  | A specific Accountsid from where Number is getting transfer. |
| toaccountsid |  ``` Required ```  | A specific Accountsid to which Number is getting transfer. |



#### Example Usage

```python
phonenumber = 'phonenumber'
fromaccountsid = 'fromaccountsid'
toaccountsid = 'toaccountsid'

result = phone_number_controller.create_move_number(phonenumber, fromaccountsid, toaccountsid)

```


### <a name="create_purchase_number"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_purchase_number") create_purchase_number

> Purchase a phone number to be used with your Ytel account

```python
def create_purchase_number(self,
                               phone_number)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phoneNumber |  ``` Required ```  | A valid 10-digit Ytel number (E.164 format). |



#### Example Usage

```python
phone_number = 'PhoneNumber'

result = phone_number_controller.create_purchase_number(phone_number)

```


### <a name="create_release_number"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_release_number") create_release_number

> Remove a purchased Ytel number from your account.

```python
def create_release_number(self,
                              response_type,
                              phone_number)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| responseType |  ``` Required ```  | Response type format xml or json |
| phoneNumber |  ``` Required ```  | A valid 10-digit Ytel number (E.164 format). |



#### Example Usage

```python
response_type = 'ResponseType'
phone_number = 'PhoneNumber'

result = phone_number_controller.create_release_number(response_type, phone_number)

```


### <a name="create_view_details"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_view_details") create_view_details

> Retrieve the details for a phone number by its number.

```python
def create_view_details(self,
                            phone_number)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phoneNumber |  ``` Required ```  | A valid Ytel 10-digit phone number (E.164 format). |



#### Example Usage

```python
phone_number = 'PhoneNumber'

result = phone_number_controller.create_view_details(phone_number)

```


### <a name="create_bulk_release"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_bulk_release") create_bulk_release

> Remove a purchased Ytel number from your account.

```python
def create_bulk_release(self,
                            phone_number)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phoneNumber |  ``` Required ```  | A valid Ytel comma separated numbers (E.164 format). |



#### Example Usage

```python
phone_number = 'PhoneNumber'

result = phone_number_controller.create_bulk_release(phone_number)

```


### <a name="create_available_numbers"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_available_numbers") create_available_numbers

> Retrieve a list of available phone numbers that can be purchased and used for your Ytel account.

```python
def create_available_numbers(self,
                                 numbertype,
                                 areacode,
                                 pagesize=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| numbertype |  ``` Required ```  | Number type either SMS,Voice or all |
| areacode |  ``` Required ```  | Specifies the area code for the returned list of available numbers. Only available for North American numbers. |
| pagesize |  ``` Optional ```  | The count of objects to return. |



#### Example Usage

```python
numbertype = NumbertypeEnum.ALL
areacode = 'areacode'
pagesize = 132

result = phone_number_controller.create_available_numbers(numbertype, areacode, pagesize)

```


### <a name="update_number"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.update_number") update_number

> Update properties for a Ytel number that has been purchased for your account. Refer to the parameters list for the list of properties that can be updated.

```python
def update_number(self,
                      phone_number,
                      voice_url,
                      friendly_name=None,
                      voice_method=None,
                      voice_fallback_url=None,
                      voice_fallback_method=None,
                      hangup_callback=None,
                      hangup_callback_method=None,
                      heartbeat_url=None,
                      heartbeat_method=None,
                      sms_url=None,
                      sms_method=None,
                      sms_fallback_url=None,
                      sms_fallback_method=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phoneNumber |  ``` Required ```  | A valid Ytel number (E.164 format). |
| voiceUrl |  ``` Required ```  | URL requested once the call connects |
| friendlyName |  ``` Optional ```  | Phone number friendly name description |
| voiceMethod |  ``` Optional ```  | Post or Get |
| voiceFallbackUrl |  ``` Optional ```  | URL requested if the voice URL is not available |
| voiceFallbackMethod |  ``` Optional ```  | Post or Get |
| hangupCallback |  ``` Optional ```  | callback url after a hangup occurs |
| hangupCallbackMethod |  ``` Optional ```  | Post or Get |
| heartbeatUrl |  ``` Optional ```  | URL requested once the call connects |
| heartbeatMethod |  ``` Optional ```  | URL that can be requested every 60 seconds during the call to notify of elapsed time |
| smsUrl |  ``` Optional ```  | URL requested when an SMS is received |
| smsMethod |  ``` Optional ```  | Post or Get |
| smsFallbackUrl |  ``` Optional ```  | URL used if any errors occur during execution of InboundXML from an SMS or at initial request of the SmsUrl. |
| smsFallbackMethod |  ``` Optional ```  | The HTTP method Ytel will use when URL requested if the SmsUrl is not available. |



#### Example Usage

```python
phone_number = 'PhoneNumber'
voice_url = 'VoiceUrl'
friendly_name = 'FriendlyName'
voice_method = 'VoiceMethod'
voice_fallback_url = 'VoiceFallbackUrl'
voice_fallback_method = 'VoiceFallbackMethod'
hangup_callback = 'HangupCallback'
hangup_callback_method = 'HangupCallbackMethod'
heartbeat_url = 'HeartbeatUrl'
heartbeat_method = 'HeartbeatMethod'
sms_url = 'SmsUrl'
sms_method = 'SmsMethod'
sms_fallback_url = 'SmsFallbackUrl'
sms_fallback_method = 'SmsFallbackMethod'

result = phone_number_controller.update_number(phone_number, voice_url, friendly_name, voice_method, voice_fallback_url, voice_fallback_method, hangup_callback, hangup_callback_method, heartbeat_url, heartbeat_method, sms_url, sms_method, sms_fallback_url, sms_fallback_method)

```


### <a name="create_list_numbers"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_list_numbers") create_list_numbers

> Retrieve a list of purchased phones numbers associated with your Ytel account.

```python
def create_list_numbers(self,
                            page=None,
                            page_size=None,
                            number_type=None,
                            friendly_name=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | Which page of the overall response will be returned. Page indexing starts at 1. |
| pageSize |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| numberType |  ``` Optional ```  | The capability supported by the number.Number type either SMS,Voice or all |
| friendlyName |  ``` Optional ```  | A human-readable label added to the number object. |



#### Example Usage

```python
page = 132
page_size = 132
number_type = NumberType14Enum.ALL
friendly_name = 'FriendlyName'

result = phone_number_controller.create_list_numbers(page, page_size, number_type, friendly_name)

```


### <a name="create_bulk_update_numbers"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_bulk_update_numbers") create_bulk_update_numbers

> Update properties for a Ytel numbers that has been purchased for your account. Refer to the parameters list for the list of properties that can be updated.

```python
def create_bulk_update_numbers(self,
                                   phone_number,
                                   voice_url,
                                   friendly_name=None,
                                   voice_method=None,
                                   voice_fallback_url=None,
                                   voice_fallback_method=None,
                                   hangup_callback=None,
                                   hangup_callback_method=None,
                                   heartbeat_url=None,
                                   heartbeat_method=None,
                                   sms_url=None,
                                   sms_method=None,
                                   sms_fallback_url=None,
                                   sms_fallback_method=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phoneNumber |  ``` Required ```  | A valid comma(,) separated Ytel numbers. (E.164 format). |
| voiceUrl |  ``` Required ```  | The URL returning InboundXML incoming calls should execute when connected. |
| friendlyName |  ``` Optional ```  | A human-readable value for labeling the number. |
| voiceMethod |  ``` Optional ```  | Specifies the HTTP method used to request the VoiceUrl once incoming call connects. |
| voiceFallbackUrl |  ``` Optional ```  | URL used if any errors occur during execution of InboundXML on a call or at initial request of the voice url |
| voiceFallbackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the VoiceFallbackUrl once incoming call connects. |
| hangupCallback |  ``` Optional ```  | URL that can be requested to receive notification when and how incoming call has ended. |
| hangupCallbackMethod |  ``` Optional ```  | The HTTP method Ytel will use when requesting the HangupCallback URL. |
| heartbeatUrl |  ``` Optional ```  | URL that can be used to monitor the phone number. |
| heartbeatMethod |  ``` Optional ```  | The HTTP method Ytel will use when requesting the HeartbeatUrl. |
| smsUrl |  ``` Optional ```  | URL requested when an SMS is received. |
| smsMethod |  ``` Optional ```  | The HTTP method Ytel will use when requesting the SmsUrl. |
| smsFallbackUrl |  ``` Optional ```  | URL used if any errors occur during execution of InboundXML from an SMS or at initial request of the SmsUrl. |
| smsFallbackMethod |  ``` Optional ```  | The HTTP method Ytel will use when URL requested if the SmsUrl is not available. |



#### Example Usage

```python
phone_number = 'PhoneNumber'
voice_url = 'VoiceUrl'
friendly_name = 'FriendlyName'
voice_method = 'VoiceMethod'
voice_fallback_url = 'VoiceFallbackUrl'
voice_fallback_method = 'VoiceFallbackMethod'
hangup_callback = 'HangupCallback'
hangup_callback_method = 'HangupCallbackMethod'
heartbeat_url = 'HeartbeatUrl'
heartbeat_method = 'HeartbeatMethod'
sms_url = 'SmsUrl'
sms_method = 'SmsMethod'
sms_fallback_url = 'SmsFallbackUrl'
sms_fallback_method = 'SmsFallbackMethod'

result = phone_number_controller.create_bulk_update_numbers(phone_number, voice_url, friendly_name, voice_method, voice_fallback_url, voice_fallback_method, hangup_callback, hangup_callback_method, heartbeat_url, heartbeat_method, sms_url, sms_method, sms_fallback_url, sms_fallback_method)

```


### <a name="create_bulk_buy_numbers"></a>![Method: ](https://apidocs.io/img/method.png ".PhoneNumberController.create_bulk_buy_numbers") create_bulk_buy_numbers

> Purchase a selected number of DID's from specific area codes to be used with your Ytel account.

```python
def create_bulk_buy_numbers(self,
                                number_type,
                                area_code,
                                quantity,
                                leftover=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| numberType |  ``` Required ```  | The capability the number supports. |
| areaCode |  ``` Required ```  | Specifies the area code for the returned list of available numbers. Only available for North American numbers. |
| quantity |  ``` Required ```  | A positive integer that tells how many number you want to buy at a time. |
| leftover |  ``` Optional ```  | If desired quantity is unavailable purchase what is available . |



#### Example Usage

```python
number_type = NumberType15Enum.ALL
area_code = 'AreaCode'
quantity = 'Quantity'
leftover = 'Leftover'

result = phone_number_controller.create_bulk_buy_numbers(number_type, area_code, quantity, leftover)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="sms_controller"></a>![Class: ](https://apidocs.io/img/class.png ".SMSController") SMSController

### Get controller instance

An instance of the ``` SMSController ``` class can be accessed from the API Client.

```python
 sms_controller = client.sms
```

### <a name="create_view_sms_1"></a>![Method: ](https://apidocs.io/img/method.png ".SMSController.create_view_sms_1") create_view_sms_1

> Retrieve a single SMS message object with details by its SmsSid.

```python
def create_view_sms_1(self,
                          message_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| messageSid |  ``` Required ```  | The unique identifier for a sms message. |



#### Example Usage

```python
message_sid = 'MessageSid'

result = sms_controller.create_view_sms_1(message_sid)

```


### <a name="create_view_sms"></a>![Method: ](https://apidocs.io/img/method.png ".SMSController.create_view_sms") create_view_sms

> Retrieve a single SMS message object by its SmsSid.

```python
def create_view_sms(self,
                        message_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| messageSid |  ``` Required ```  | The unique identifier for a sms message. |



#### Example Usage

```python
message_sid = 'MessageSid'

result = sms_controller.create_view_sms(message_sid)

```


### <a name="create_send_sms"></a>![Method: ](https://apidocs.io/img/method.png ".SMSController.create_send_sms") create_send_sms

> Send an SMS from a Ytel number

```python
def create_send_sms(self,
                        mfrom,
                        to,
                        body,
                        method=None,
                        message_status_callback=None,
                        smartsms=None,
                        delivery_status=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| mfrom |  ``` Required ```  | The 10-digit SMS-enabled Ytel number (E.164 format) in which the message is sent. |
| to |  ``` Required ```  | The 10-digit phone number (E.164 format) that will receive the message. |
| body |  ``` Required ```  | The body message that is to be sent in the text. |
| method |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once SMS sent. |
| messageStatusCallback |  ``` Optional ```  | URL that can be requested to receive notification when SMS has Sent. A set of default parameters will be sent here once the SMS is finished. |
| smartsms |  ``` Optional ```  | Check's 'to' number can receive sms or not using Carrier API, if wireless = true then text sms is sent, else wireless = false then call is recieved to end user with audible message. |
| deliveryStatus |  ``` Optional ```  | Delivery reports are a method to tell your system if the message has arrived on the destination phone. |



#### Example Usage

```python
mfrom = 'From'
to = 'To'
body = 'Body'
method = 'Method'
message_status_callback = 'MessageStatusCallback'
smartsms = True
delivery_status = True

result = sms_controller.create_send_sms(mfrom, to, body, method, message_status_callback, smartsms, delivery_status)

```


### <a name="create_list_sms"></a>![Method: ](https://apidocs.io/img/method.png ".SMSController.create_list_sms") create_list_sms

> Retrieve a list of Outbound SMS message objects.

```python
def create_list_sms(self,
                        page=None,
                        page_size=None,
                        mfrom=None,
                        to=None,
                        date_sent=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pageSize |  ``` Optional ```  | Number of individual resources listed in the response per page |
| mfrom |  ``` Optional ```  | Filter SMS message objects from this valid 10-digit phone number (E.164 format). |
| to |  ``` Optional ```  | Filter SMS message objects to this valid 10-digit phone number (E.164 format). |
| dateSent |  ``` Optional ```  | Only list SMS messages sent in the specified date range |



#### Example Usage

```python
page = 174
page_size = 174
mfrom = 'From'
to = 'To'
date_sent = 'DateSent'

result = sms_controller.create_list_sms(page, page_size, mfrom, to, date_sent)

```


### <a name="create_list_inbound_sms"></a>![Method: ](https://apidocs.io/img/method.png ".SMSController.create_list_inbound_sms") create_list_inbound_sms

> Retrieve a list of Inbound SMS message objects.

```python
def create_list_inbound_sms(self,
                                page=None,
                                page_size=None,
                                mfrom=None,
                                to=None,
                                date_sent=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pageSize |  ``` Optional ```  | The count of objects to return per page. |
| mfrom |  ``` Optional ```  | Filter SMS message objects from this valid 10-digit phone number (E.164 format). |
| to |  ``` Optional ```  | Filter SMS message objects to this valid 10-digit phone number (E.164 format). |
| dateSent |  ``` Optional ```  | Filter sms message objects by this date. |



#### Example Usage

```python
page = 174
page_size = 174
mfrom = 'From'
to = 'To'
date_sent = 'DateSent'

result = sms_controller.create_list_inbound_sms(page, page_size, mfrom, to, date_sent)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="shared_short_code_controller"></a>![Class: ](https://apidocs.io/img/class.png ".SharedShortCodeController") SharedShortCodeController

### Get controller instance

An instance of the ``` SharedShortCodeController ``` class can be accessed from the API Client.

```python
 shared_short_code_controller = client.shared_short_code
```

### <a name="create_view_shortcode"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_view_shortcode") create_view_shortcode

> The response returned here contains all resource properties associated with the given Shortcode.

```python
def create_view_shortcode(self,
                              shortcode)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Required ```  | List of valid Shortcode to your Ytel account |



#### Example Usage

```python
shortcode = 'Shortcode'

result = shared_short_code_controller.create_view_shortcode(shortcode)

```


### <a name="create_view_keyword"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_view_keyword") create_view_keyword

> View a set of properties for a single keyword.

```python
def create_view_keyword(self,
                            keywordid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| keywordid |  ``` Required ```  | The unique identifier of each keyword |



#### Example Usage

```python
keywordid = 'Keywordid'

result = shared_short_code_controller.create_view_keyword(keywordid)

```


### <a name="create_view_template"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_view_template") create_view_template

> View a Shared ShortCode Template

```python
def create_view_template(self,
                             template_id)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| templateId |  ``` Required ```  | The unique identifier for a template object |



#### Example Usage

```python
template_id = uuid.uuid4()

result = shared_short_code_controller.create_view_template(template_id)

```


### <a name="create_list_inbound_sms"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_list_inbound_sms") create_list_inbound_sms

> List All Inbound ShortCode

```python
def create_list_inbound_sms(self,
                                datecreated=None,
                                page=None,
                                pagesize=None,
                                mfrom=None,
                                shortcode=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| datecreated |  ``` Optional ```  | Only list messages sent with the specified date |
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | Number of individual resources listed in the response per page |
| mfrom |  ``` Optional ```  | From Number to Inbound ShortCode |
| shortcode |  ``` Optional ```  | Only list messages sent to this Short Code |



#### Example Usage

```python
datecreated = 'Datecreated'
page = 174
pagesize = 174
mfrom = 'from'
shortcode = 'Shortcode'

result = shared_short_code_controller.create_list_inbound_sms(datecreated, page, pagesize, mfrom, shortcode)

```


### <a name="create_send_sms"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_send_sms") create_send_sms

> Send an SMS from a Ytel ShortCode

```python
def create_send_sms(self,
                        shortcode,
                        to,
                        templateid,
                        data,
                        method=None,
                        message_status_callback=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Required ```  | The Short Code number that is the sender of this message |
| to |  ``` Required ```  | A valid 10-digit number that should receive the message |
| templateid |  ``` Required ```  | The unique identifier for the template used for the message |
| data |  ``` Required ```  | format of your data, example: {companyname}:test,{otpcode}:1234 |
| method |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once the Short Code message is sent. |
| messageStatusCallback |  ``` Optional ```  | URL that can be requested to receive notification when Short Code message was sent. |



#### Example Usage

```python
shortcode = 'shortcode'
to = 'to'
templateid = uuid.uuid4()
data = 'data'
method = 'Method'
message_status_callback = 'MessageStatusCallback'

result = shared_short_code_controller.create_send_sms(shortcode, to, templateid, data, method, message_status_callback)

```


### <a name="create_list_templates"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_list_templates") create_list_templates

> List Shortcode Templates by Type

```python
def create_list_templates(self,
                              mtype=None,
                              page=None,
                              pagesize=None,
                              shortcode=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| mtype |  ``` Optional ```  | The type (category) of template Valid values: marketing, authorization |
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |
| shortcode |  ``` Optional ```  | Only list templates of type |



#### Example Usage

```python
mtype = 'type'
page = 174
pagesize = 174
shortcode = 'Shortcode'

result = shared_short_code_controller.create_list_templates(mtype, page, pagesize, shortcode)

```


### <a name="create_list_keywords"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_list_keywords") create_list_keywords

> Retrieve a list of keywords associated with your Ytel account.

```python
def create_list_keywords(self,
                             page=None,
                             pagesize=None,
                             keyword=None,
                             shortcode=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | Number of individual resources listed in the response per page |
| keyword |  ``` Optional ```  | Only list keywords of keyword |
| shortcode |  ``` Optional ```  | Only list keywords of shortcode |



#### Example Usage

```python
page = 174
pagesize = 174
keyword = 'Keyword'
shortcode = 174

result = shared_short_code_controller.create_list_keywords(page, pagesize, keyword, shortcode)

```


### <a name="create_list_shortcodes"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.create_list_shortcodes") create_list_shortcodes

> Retrieve a list of shortcode assignment associated with your Ytel account.

```python
def create_list_shortcodes(self,
                               shortcode=None,
                               page=None,
                               pagesize=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Optional ```  | Only list keywords of shortcode |
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | Number of individual resources listed in the response per page |



#### Example Usage

```python
shortcode = 'Shortcode'
page = 174
pagesize = 174

result = shared_short_code_controller.create_list_shortcodes(shortcode, page, pagesize)

```


### <a name="update_shortcode"></a>![Method: ](https://apidocs.io/img/method.png ".SharedShortCodeController.update_shortcode") update_shortcode

> Update Assignment

```python
def update_shortcode(self,
                         shortcode,
                         friendly_name=None,
                         callback_url=None,
                         callback_method=None,
                         fallback_url=None,
                         fallback_url_method=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| shortcode |  ``` Required ```  | List of valid shortcode to your Ytel account |
| friendlyName |  ``` Optional ```  | User generated name of the shortcode |
| callbackUrl |  ``` Optional ```  | URL that can be requested to receive notification when call has ended. A set of default parameters will be sent here once the call is finished. |
| callbackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required StatusCallBackUrl once call connects. |
| fallbackUrl |  ``` Optional ```  | URL used if any errors occur during execution of InboundXML or at initial request of the required Url provided with the POST. |
| fallbackUrlMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required FallbackUrl once call connects. |



#### Example Usage

```python
shortcode = 'Shortcode'
friendly_name = 'FriendlyName'
callback_url = 'CallbackUrl'
callback_method = 'CallbackMethod'
fallback_url = 'FallbackUrl'
fallback_url_method = 'FallbackUrlMethod'

result = shared_short_code_controller.update_shortcode(shortcode, friendly_name, callback_url, callback_method, fallback_url, fallback_url_method)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="conference_controller"></a>![Class: ](https://apidocs.io/img/class.png ".ConferenceController") ConferenceController

### Get controller instance

An instance of the ``` ConferenceController ``` class can be accessed from the API Client.

```python
 conference_controller = client.conference
```

### <a name="create_play_audio"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_play_audio") create_play_audio

> Play an audio file during a conference.

```python
def create_play_audio(self,
                          conference_sid,
                          participant_sid,
                          audio_url)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| conferenceSid |  ``` Required ```  | The unique identifier for a conference object. |
| participantSid |  ``` Required ```  | The unique identifier for a participant object. |
| audioUrl |  ``` Required ```  | The URL for the audio file that is to be played during the conference. Multiple audio files can be chained by using a semicolon. |



#### Example Usage

```python
conference_sid = 'ConferenceSid'
participant_sid = 'ParticipantSid'
audio_url = AudioUrlEnum.MP3

result = conference_controller.create_play_audio(conference_sid, participant_sid, audio_url)

```


### <a name="create_hangup_participant"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_hangup_participant") create_hangup_participant

> Remove a participant from a conference.

```python
def create_hangup_participant(self,
                                  participant_sid,
                                  conference_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| participantSid |  ``` Required ```  | The unique identifier for a participant object. |
| conferenceSid |  ``` Required ```  | The unique identifier for a conference object. |



#### Example Usage

```python
participant_sid = 'ParticipantSid'
conference_sid = 'ConferenceSid'

result = conference_controller.create_hangup_participant(participant_sid, conference_sid)

```


### <a name="create_view_conference"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_view_conference") create_view_conference

> Retrieve information about a conference by its ConferenceSid.

```python
def create_view_conference(self,
                               conference_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| conferenceSid |  ``` Required ```  | The unique identifier of each conference resource |



#### Example Usage

```python
conference_sid = 'ConferenceSid'

result = conference_controller.create_view_conference(conference_sid)

```


### <a name="create_view_participant"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_view_participant") create_view_participant

> Retrieve information about a participant by its ParticipantSid.

```python
def create_view_participant(self,
                                conference_sid,
                                participant_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| conferenceSid |  ``` Required ```  | The unique identifier for a conference object. |
| participantSid |  ``` Required ```  | The unique identifier for a participant object. |



#### Example Usage

```python
conference_sid = 'ConferenceSid'
participant_sid = 'ParticipantSid'

result = conference_controller.create_view_participant(conference_sid, participant_sid)

```


### <a name="create_silence_participant"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_silence_participant") create_silence_participant

> Deaf Mute Participant

```python
def create_silence_participant(self,
                                   conference_sid,
                                   participant_sid,
                                   muted=None,
                                   deaf=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| conferenceSid |  ``` Required ```  | ID of the active conference |
| participantSid |  ``` Required ```  | ID of an active participant |
| muted |  ``` Optional ```  | Mute a participant |
| deaf |  ``` Optional ```  | Make it so a participant cant hear |



#### Example Usage

```python
conference_sid = 'conferenceSid'
participant_sid = 'ParticipantSid'
muted = True
deaf = True

result = conference_controller.create_silence_participant(conference_sid, participant_sid, muted, deaf)

```


### <a name="add_participant"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.add_participant") add_participant

> Add Participant in conference 

```python
def add_participant(self,
                        conference_sid,
                        participant_number,
                        muted=None,
                        deaf=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| conferenceSid |  ``` Required ```  | The unique identifier for a conference object. |
| participantNumber |  ``` Required ```  | The phone number of the participant to be added. |
| muted |  ``` Optional ```  | Specifies if participant should be muted. |
| deaf |  ``` Optional ```  | Specifies if the participant should hear audio in the conference. |



#### Example Usage

```python
conference_sid = 'ConferenceSid'
participant_number = 'ParticipantNumber'
muted = True
deaf = True

result = conference_controller.add_participant(conference_sid, participant_number, muted, deaf)

```


### <a name="create_conference"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_conference") create_conference

> Here you can experiment with initiating a conference call through Ytel and view the request response generated when doing so.

```python
def create_conference(self,
                          url,
                          mfrom,
                          to,
                          method=None,
                          status_call_back_url=None,
                          status_call_back_method=None,
                          fallback_url=None,
                          fallback_method=None,
                          record=None,
                          record_call_back_url=None,
                          record_call_back_method=None,
                          schedule_time=None,
                          timeout=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| url |  ``` Required ```  | URL requested once the conference connects |
| mfrom |  ``` Required ```  | A valid 10-digit number (E.164 format) that will be initiating the conference call. |
| to |  ``` Required ```  | A valid 10-digit number (E.164 format) that is to receive the conference call. |
| method |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once call connects. |
| statusCallBackUrl |  ``` Optional ```  | URL that can be requested to receive notification when call has ended. A set of default parameters will be sent here once the conference is finished. |
| statusCallBackMethod |  ``` Optional ```  | Specifies the HTTP methodlinkclass used to request StatusCallbackUrl. |
| fallbackUrl |  ``` Optional ```  | URL requested if the initial Url parameter fails or encounters an error |
| fallbackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required FallbackUrl once call connects. |
| record |  ``` Optional ```  | Specifies if the conference should be recorded. |
| recordCallBackUrl |  ``` Optional ```  | Recording parameters will be sent here upon completion. |
| recordCallBackMethod |  ``` Optional ```  | Specifies the HTTP method used to request the required URL once conference connects. |
| scheduleTime |  ``` Optional ```  | Schedule conference in future. Schedule time must be greater than current time |
| timeout |  ``` Optional ```  | The number of seconds the call stays on the line while waiting for an answer. The max time limit is 999 and the default limit is 60 seconds but lower times can be set. |



#### Example Usage

```python
url = 'Url'
mfrom = 'From'
to = 'To'
method = 'Method'
status_call_back_url = 'StatusCallBackUrl'
status_call_back_method = 'StatusCallBackMethod'
fallback_url = 'FallbackUrl'
fallback_method = 'FallbackMethod'
record = False
record_call_back_url = 'RecordCallBackUrl'
record_call_back_method = 'RecordCallBackMethod'
schedule_time = 'ScheduleTime'
timeout = 82

result = conference_controller.create_conference(url, mfrom, to, method, status_call_back_url, status_call_back_method, fallback_url, fallback_method, record, record_call_back_url, record_call_back_method, schedule_time, timeout)

```


### <a name="create_list_participants"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_list_participants") create_list_participants

> Retrieve a list of participants for an in-progress conference.

```python
def create_list_participants(self,
                                 conference_sid,
                                 page=None,
                                 pagesize=None,
                                 muted=None,
                                 deaf=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| conferenceSid |  ``` Required ```  | The unique identifier for a conference. |
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |
| muted |  ``` Optional ```  | Specifies if participant should be muted. |
| deaf |  ``` Optional ```  | Specifies if the participant should hear audio in the conference. |



#### Example Usage

```python
conference_sid = 'ConferenceSid'
page = 82
pagesize = 82
muted = False
deaf = False

result = conference_controller.create_list_participants(conference_sid, page, pagesize, muted, deaf)

```


### <a name="create_list_conferences"></a>![Method: ](https://apidocs.io/img/method.png ".ConferenceController.create_list_conferences") create_list_conferences

> Retrieve a list of conference objects.

```python
def create_list_conferences(self,
                                page=None,
                                pagesize=None,
                                friendly_name=None,
                                date_created=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | Number of individual resources listed in the response per page |
| friendlyName |  ``` Optional ```  | Only return conferences with the specified FriendlyName |
| dateCreated |  ``` Optional ```  | Conference created date |



#### Example Usage

```python
page = 82
pagesize = 82
friendly_name = 'FriendlyName'
date_created = 'DateCreated'

result = conference_controller.create_list_conferences(page, pagesize, friendly_name, date_created)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="carrier_controller"></a>![Class: ](https://apidocs.io/img/class.png ".CarrierController") CarrierController

### Get controller instance

An instance of the ``` CarrierController ``` class can be accessed from the API Client.

```python
 carrier_controller = client.carrier
```

### <a name="create_lookup_carrier"></a>![Method: ](https://apidocs.io/img/method.png ".CarrierController.create_lookup_carrier") create_lookup_carrier

> Get the Carrier Lookup

```python
def create_lookup_carrier(self,
                              phone_number)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| phoneNumber |  ``` Required ```  | A valid 10-digit number (E.164 format). |



#### Example Usage

```python
phone_number = 'PhoneNumber'

result = carrier_controller.create_lookup_carrier(phone_number)

```


### <a name="create_carrier_results"></a>![Method: ](https://apidocs.io/img/method.png ".CarrierController.create_carrier_results") create_carrier_results

> Retrieve a list of carrier lookup objects.

```python
def create_carrier_results(self,
                               page=None,
                               page_size=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pageSize |  ``` Optional ```  | The count of objects to return per page. |



#### Example Usage

```python
page = 82
page_size = 82

result = carrier_controller.create_carrier_results(page, page_size)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="email_controller"></a>![Class: ](https://apidocs.io/img/class.png ".EmailController") EmailController

### Get controller instance

An instance of the ``` EmailController ``` class can be accessed from the API Client.

```python
 email_controller = client.email
```

### <a name="create_remove_invalid_email"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_remove_invalid_email") create_remove_invalid_email

> Remove an email from the invalid email list.

```python
def create_remove_invalid_email(self,
                                    email)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| email |  ``` Required ```  | A valid email address that is to be remove from the invalid email list. |



#### Example Usage

```python
email = 'Email'

result = email_controller.create_remove_invalid_email(email)

```


### <a name="create_blocked_emails"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_blocked_emails") create_blocked_emails

> Retrieve a list of emails that have been blocked.

```python
def create_blocked_emails(self,
                              offset=None,
                              limit=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| offset |  ``` Optional ```  | The starting point of the list of blocked emails that should be returned. |
| limit |  ``` Optional ```  | The count of results that should be returned. |



#### Example Usage

```python
offset = 'Offset'
limit = 'Limit'

result = email_controller.create_blocked_emails(offset, limit)

```


### <a name="create_spam_emails"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_spam_emails") create_spam_emails

> Retrieve a list of emails that are on the spam list.

```python
def create_spam_emails(self,
                           offset=None,
                           limit=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| offset |  ``` Optional ```  | The starting point of the list of spam emails that should be returned. |
| limit |  ``` Optional ```  | The count of results that should be returned. |



#### Example Usage

```python
offset = 'Offset'
limit = 'Limit'

result = email_controller.create_spam_emails(offset, limit)

```


### <a name="create_bounced_emails"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_bounced_emails") create_bounced_emails

> Retrieve a list of emails that have bounced.

```python
def create_bounced_emails(self,
                              offset=None,
                              limit=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| offset |  ``` Optional ```  | The starting point of the list of bounced emails that should be returned. |
| limit |  ``` Optional ```  | The count of results that should be returned. |



#### Example Usage

```python
offset = 'Offset'
limit = 'Limit'

result = email_controller.create_bounced_emails(offset, limit)

```


### <a name="create_remove_bounced_email"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_remove_bounced_email") create_remove_bounced_email

> Remove an email address from the bounced list.

```python
def create_remove_bounced_email(self,
                                    email)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| email |  ``` Required ```  | The email address to be remove from the bounced email list. |



#### Example Usage

```python
email = 'Email'

result = email_controller.create_remove_bounced_email(email)

```


### <a name="create_invalid_emails"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_invalid_emails") create_invalid_emails

> Retrieve a list of invalid email addresses.

```python
def create_invalid_emails(self,
                              offset=None,
                              limit=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| offset |  ``` Optional ```  | The starting point of the list of invalid emails that should be returned. |
| limit |  ``` Optional ```  | The count of results that should be returned. |



#### Example Usage

```python
offset = 'Offset'
limit = 'Limit'

result = email_controller.create_invalid_emails(offset, limit)

```


### <a name="create_list_unsubscribed_emails"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_list_unsubscribed_emails") create_list_unsubscribed_emails

> Retrieve a list of email addresses from the unsubscribe list.

```python
def create_list_unsubscribed_emails(self,
                                        offset=None,
                                        limit=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| offset |  ``` Optional ```  | The starting point of the list of unsubscribed emails that should be returned. |
| limit |  ``` Optional ```  | The count of results that should be returned. |



#### Example Usage

```python
offset = 'Offset'
limit = 'Limit'

result = email_controller.create_list_unsubscribed_emails(offset, limit)

```


### <a name="create_remove_unsubscribed_email"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_remove_unsubscribed_email") create_remove_unsubscribed_email

> Remove an email address from the list of unsubscribed emails.

```python
def create_remove_unsubscribed_email(self,
                                         email)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| email |  ``` Required ```  | A valid email address that is to be remove from the unsubscribe list. |



#### Example Usage

```python
email = 'email'

result = email_controller.create_remove_unsubscribed_email(email)

```


### <a name="add_email_unsubscribe"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.add_email_unsubscribe") add_email_unsubscribe

> Add an email to the unsubscribe list

```python
def add_email_unsubscribe(self,
                              email)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| email |  ``` Required ```  | A valid email address that is to be added to the unsubscribe list |



#### Example Usage

```python
email = 'email'

result = email_controller.add_email_unsubscribe(email)

```


### <a name="create_remove_blocked_address"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_remove_blocked_address") create_remove_blocked_address

> Remove an email from blocked emails list.

```python
def create_remove_blocked_address(self,
                                      email)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| email |  ``` Required ```  | The email address to be remove from the blocked list. |



#### Example Usage

```python
email = 'Email'

result = email_controller.create_remove_blocked_address(email)

```


### <a name="create_remove_spam_address"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_remove_spam_address") create_remove_spam_address

> Remove an email from the spam email list.

```python
def create_remove_spam_address(self,
                                   email)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| email |  ``` Required ```  | A valid email address that is to be remove from the spam list. |



#### Example Usage

```python
email = 'Email'

result = email_controller.create_remove_spam_address(email)

```


### <a name="create_send_email"></a>![Method: ](https://apidocs.io/img/method.png ".EmailController.create_send_email") create_send_email

> Create and submit an email message to one or more email addresses.

```python
def create_send_email(self,
                          to,
                          mtype,
                          subject,
                          message,
                          mfrom=None,
                          cc=None,
                          bcc=None,
                          attachment=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| to |  ``` Required ```  | A valid address that will receive the email. Multiple addresses can be separated by using commas. |
| mtype |  ``` Required ```  | Specifies the type of email to be sent |
| subject |  ``` Required ```  | The subject of the mail. Must be a valid string. |
| message |  ``` Required ```  | The email message that is to be sent in the text. |
| mfrom |  ``` Optional ```  | A valid address that will send the email. |
| cc |  ``` Optional ```  | Carbon copy. A valid address that will receive the email. Multiple addresses can be separated by using commas. |
| bcc |  ``` Optional ```  | Blind carbon copy. A valid address that will receive the email. Multiple addresses can be separated by using commas. |
| attachment |  ``` Optional ```  | A file that is attached to the email. Must be less than 7 MB in size. |



#### Example Usage

```python
to = 'To'
mtype = TypeEnum.TEXT
subject = 'Subject'
message = 'Message'
mfrom = 'From'
cc = 'Cc'
bcc = 'Bcc'
attachment = 'Attachment'

result = email_controller.create_send_email(to, mtype, subject, message, mfrom, cc, bcc, attachment)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="account_controller"></a>![Class: ](https://apidocs.io/img/class.png ".AccountController") AccountController

### Get controller instance

An instance of the ``` AccountController ``` class can be accessed from the API Client.

```python
 account_controller = client.account
```

### <a name="create_view_account"></a>![Method: ](https://apidocs.io/img/method.png ".AccountController.create_view_account") create_view_account

> Retrieve information regarding your Ytel account by a specific date. The response object will contain data such as account status, balance, and account usage totals.

```python
def create_view_account(self,
                            date)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| date |  ``` Required ```  | Filter account information based on date. |



#### Example Usage

```python
date = 'Date'

result = account_controller.create_view_account(date)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="sub_account_controller"></a>![Class: ](https://apidocs.io/img/class.png ".SubAccountController") SubAccountController

### Get controller instance

An instance of the ``` SubAccountController ``` class can be accessed from the API Client.

```python
 sub_account_controller = client.sub_account
```

### <a name="create_toggle_subaccount_status"></a>![Method: ](https://apidocs.io/img/method.png ".SubAccountController.create_toggle_subaccount_status") create_toggle_subaccount_status

> Suspend or unsuspend

```python
def create_toggle_subaccount_status(self,
                                        sub_account_sid,
                                        m_activate)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subAccountSID |  ``` Required ```  | The SubaccountSid to be activated or suspended |
| mActivate |  ``` Required ```  | 0 to suspend or 1 to activate |



#### Example Usage

```python
sub_account_sid = 'SubAccountSID'
m_activate = MActivateEnum.ENUM_1

result = sub_account_controller.create_toggle_subaccount_status(sub_account_sid, m_activate)

```


### <a name="create_delete_subaccount"></a>![Method: ](https://apidocs.io/img/method.png ".SubAccountController.create_delete_subaccount") create_delete_subaccount

> Delete sub account or merge numbers into parent

```python
def create_delete_subaccount(self,
                                 sub_account_sid,
                                 merge_number)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| subAccountSID |  ``` Required ```  | The SubaccountSid to be deleted |
| mergeNumber |  ``` Required ```  | 0 to delete or 1 to merge numbers to parent account. |



#### Example Usage

```python
sub_account_sid = 'SubAccountSID'
merge_number = MergeNumberEnum.ENUM_0

result = sub_account_controller.create_delete_subaccount(sub_account_sid, merge_number)

```


### <a name="create_subaccount"></a>![Method: ](https://apidocs.io/img/method.png ".SubAccountController.create_subaccount") create_subaccount

> Create a sub user account under the parent account

```python
def create_subaccount(self,
                          first_name,
                          last_name,
                          email,
                          friendly_name,
                          password)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| firstName |  ``` Required ```  | Sub account user first name |
| lastName |  ``` Required ```  | sub account user last name |
| email |  ``` Required ```  | Sub account email address |
| friendlyName |  ``` Required ```  | Descriptive name of the sub account |
| password |  ``` Required ```  | The password of the sub account.  Please make sure to make as password that is at least 8 characters long, contain a symbol, uppercase and a number. |



#### Example Usage

```python
first_name = 'FirstName'
last_name = 'LastName'
email = 'Email'
friendly_name = 'FriendlyName'
password = 'Password'

result = sub_account_controller.create_subaccount(first_name, last_name, email, friendly_name, password)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="address_controller"></a>![Class: ](https://apidocs.io/img/class.png ".AddressController") AddressController

### Get controller instance

An instance of the ``` AddressController ``` class can be accessed from the API Client.

```python
 address_controller = client.address
```

### <a name="create_delete_address"></a>![Method: ](https://apidocs.io/img/method.png ".AddressController.create_delete_address") create_delete_address

> To delete Address to your address book

```python
def create_delete_address(self,
                              addressid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| addressid |  ``` Required ```  | The identifier of the address to be deleted. |



#### Example Usage

```python
addressid = 'addressid'

result = address_controller.create_delete_address(addressid)

```


### <a name="create_verify_address"></a>![Method: ](https://apidocs.io/img/method.png ".AddressController.create_verify_address") create_verify_address

> Validates an address given.

```python
def create_verify_address(self,
                              addressid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| addressid |  ``` Required ```  | The identifier of the address to be verified. |



#### Example Usage

```python
addressid = 'addressid'

result = address_controller.create_verify_address(addressid)

```


### <a name="create_view_address"></a>![Method: ](https://apidocs.io/img/method.png ".AddressController.create_view_address") create_view_address

> View Address Specific address Book by providing the address id

```python
def create_view_address(self,
                            addressid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| addressid |  ``` Required ```  | The identifier of the address to be retrieved. |



#### Example Usage

```python
addressid = 'addressid'

result = address_controller.create_view_address(addressid)

```


### <a name="create_list_addresses"></a>![Method: ](https://apidocs.io/img/method.png ".AddressController.create_list_addresses") create_list_addresses

> List All Address 

```python
def create_list_addresses(self,
                              page=None,
                              pagesize=None,
                              addressid=None,
                              date_created=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | How many results to return, default is 10, max is 100, must be an integer |
| addressid |  ``` Optional ```  | addresses Sid |
| dateCreated |  ``` Optional ```  | date created address. |



#### Example Usage

```python
page = 82
pagesize = 82
addressid = 'addressid'
date_created = 'dateCreated'

result = address_controller.create_list_addresses(page, pagesize, addressid, date_created)

```


### <a name="create_address"></a>![Method: ](https://apidocs.io/img/method.png ".AddressController.create_address") create_address

> To add an address to your address book, you create a new address object. You can retrieve and delete individual addresses as well as get a list of addresses. Addresses are identified by a unique random ID.

```python
def create_address(self,
                       name,
                       address,
                       country,
                       state,
                       city,
                       zip,
                       description=None,
                       email=None,
                       phone=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| name |  ``` Required ```  | Name of user |
| address |  ``` Required ```  | Address of user. |
| country |  ``` Required ```  | Must be a 2 letter country short-name code (ISO 3166) |
| state |  ``` Required ```  | Must be a 2 letter State eg. CA for US. For Some Countries it can be greater than 2 letters. |
| city |  ``` Required ```  | City Name. |
| zip |  ``` Required ```  | Zip code of city. |
| description |  ``` Optional ```  | Description of addresses. |
| email |  ``` Optional ```  | Email Id of user. |
| phone |  ``` Optional ```  | Phone number of user. |



#### Example Usage

```python
name = 'Name'
address = 'Address'
country = 'Country'
state = 'State'
city = 'City'
zip = 'Zip'
description = 'Description'
email = 'email'
phone = 'Phone'

result = address_controller.create_address(name, address, country, state, city, zip, description, email, phone)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="recording_controller"></a>![Class: ](https://apidocs.io/img/class.png ".RecordingController") RecordingController

### Get controller instance

An instance of the ``` RecordingController ``` class can be accessed from the API Client.

```python
 recording_controller = client.recording
```

### <a name="create_delete_recording"></a>![Method: ](https://apidocs.io/img/method.png ".RecordingController.create_delete_recording") create_delete_recording

> Remove a recording from your Ytel account.

```python
def create_delete_recording(self,
                                recordingsid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| recordingsid |  ``` Required ```  | The unique identifier for a recording. |



#### Example Usage

```python
recordingsid = 'recordingsid'

result = recording_controller.create_delete_recording(recordingsid)

```


### <a name="create_view_recording"></a>![Method: ](https://apidocs.io/img/method.png ".RecordingController.create_view_recording") create_view_recording

> Retrieve the recording of a call by its RecordingSid. This resource will return information regarding the call such as start time, end time, duration, and so forth.

```python
def create_view_recording(self,
                              recordingsid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| recordingsid |  ``` Required ```  | The unique identifier for the recording. |



#### Example Usage

```python
recordingsid = 'recordingsid'

result = recording_controller.create_view_recording(recordingsid)

```


### <a name="create_list_recordings"></a>![Method: ](https://apidocs.io/img/method.png ".RecordingController.create_list_recordings") create_list_recordings

> Retrieve a list of recording objects.

```python
def create_list_recordings(self,
                               page=None,
                               pagesize=None,
                               datecreated=None,
                               callsid=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |
| datecreated |  ``` Optional ```  | Filter results by creation date |
| callsid |  ``` Optional ```  | The unique identifier for a call. |



#### Example Usage

```python
page = 82
pagesize = 82
datecreated = 'Datecreated'
callsid = 'callsid'

result = recording_controller.create_list_recordings(page, pagesize, datecreated, callsid)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="transcription_controller"></a>![Class: ](https://apidocs.io/img/class.png ".TranscriptionController") TranscriptionController

### Get controller instance

An instance of the ``` TranscriptionController ``` class can be accessed from the API Client.

```python
 transcription_controller = client.transcription
```

### <a name="create_transcribe_audio_url"></a>![Method: ](https://apidocs.io/img/method.png ".TranscriptionController.create_transcribe_audio_url") create_transcribe_audio_url

> Transcribe an audio recording from a file.

```python
def create_transcribe_audio_url(self,
                                    audiourl)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| audiourl |  ``` Required ```  | URL pointing to the location of the audio file that is to be transcribed. |



#### Example Usage

```python
audiourl = 'audiourl'

result = transcription_controller.create_transcribe_audio_url(audiourl)

```


### <a name="create_transcribe_recording"></a>![Method: ](https://apidocs.io/img/method.png ".TranscriptionController.create_transcribe_recording") create_transcribe_recording

> Transcribe a recording by its RecordingSid.

```python
def create_transcribe_recording(self,
                                    recording_sid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| recordingSid |  ``` Required ```  | The unique identifier for a recording object. |



#### Example Usage

```python
recording_sid = 'recordingSid'

result = transcription_controller.create_transcribe_recording(recording_sid)

```


### <a name="create_view_transcription"></a>![Method: ](https://apidocs.io/img/method.png ".TranscriptionController.create_view_transcription") create_view_transcription

> Retrieve information about a transaction by its TranscriptionSid.

```python
def create_view_transcription(self,
                                  transcriptionsid)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| transcriptionsid |  ``` Required ```  | The unique identifier for a transcription object. |



#### Example Usage

```python
transcriptionsid = 'transcriptionsid'

result = transcription_controller.create_view_transcription(transcriptionsid)

```


### <a name="create_list_transcriptions"></a>![Method: ](https://apidocs.io/img/method.png ".TranscriptionController.create_list_transcriptions") create_list_transcriptions

> Retrieve a list of transcription objects for your Ytel account.

```python
def create_list_transcriptions(self,
                                   page=None,
                                   pagesize=None,
                                   status=None,
                                   date_transcribed=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| page |  ``` Optional ```  | The page count to retrieve from the total results in the collection. Page indexing starts at 1. |
| pagesize |  ``` Optional ```  | The count of objects to return per page. |
| status |  ``` Optional ```  | The state of the transcription. |
| dateTranscribed |  ``` Optional ```  | The date the transcription took place. |



#### Example Usage

```python
page = 82
pagesize = 82
status = Status12Enum.INPROGRESS
date_transcribed = 'dateTranscribed'

result = transcription_controller.create_list_transcriptions(page, pagesize, status, date_transcribed)

```


[Back to List of Controllers](#list_of_controllers)

## <a name="usage_controller"></a>![Class: ](https://apidocs.io/img/class.png ".UsageController") UsageController

### Get controller instance

An instance of the ``` UsageController ``` class can be accessed from the API Client.

```python
 usage_controller = client.usage
```

### <a name="create_list_usage"></a>![Method: ](https://apidocs.io/img/method.png ".UsageController.create_list_usage") create_list_usage

> Retrieve usage metrics regarding your Ytel account. The results includes inbound/outbound voice calls and inbound/outbound SMS messages as well as carrier lookup requests.

```python
def create_list_usage(self,
                          product_code=None,
                          start_date=None,
                          end_date=None,
                          include_sub_accounts=None)
```

#### Parameters

| Parameter | Tags | Description |
|-----------|------|-------------|
| productCode |  ``` Optional ```  | Filter usage results by product type. |
| startDate |  ``` Optional ```  | Filter usage objects by start date. |
| endDate |  ``` Optional ```  | Filter usage objects by end date. |
| includeSubAccounts |  ``` Optional ```  | Will include all subaccount usage data |



#### Example Usage

```python
product_code = ProductCodeEnum.ENUM_0
start_date = 'startDate'
end_date = 'endDate'
include_sub_accounts = 'IncludeSubAccounts'

result = usage_controller.create_list_usage(product_code, start_date, end_date, include_sub_accounts)

```


[Back to List of Controllers](#list_of_controllers)



