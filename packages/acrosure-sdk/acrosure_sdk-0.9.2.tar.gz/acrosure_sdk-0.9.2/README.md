# Acrosure Python SDK

![Acrosure](./static/Acrosure-color.png)

Python version 2 and 3 SDK for connecting with Acrosure Insurance Gateway

## Installation

Install via pip:

`pip install acrosure_sdk`

## Requirements

* Python 2.7.1+
* `requests` library

## Getting Started

Import AcrosureClient into your project.

```python
from acrosure_sdk import AcrosureClient

```

Instantiate with an API key from [Acrosure Dashboard](https://dashboard.acrosure.com).


```python
acrosure_client = AcrosureClient(token = '<your_api_key>')
```

## Basic Usage

AcrosureClient provides several objects such as `application`, `product`, etc. and associated APIs.

Any data will be inside an response object with `data` key, along with meta data, such as:

```json
{
  "data": { ... },
  "status": "ok",
  ...
}
```

### Application

#### Get

Get application with specified id.

```python
application = acrosure_client.application.get('<application_id>')
```

#### Create

Create an application.

```python
created_application = acrosure_client.application.create(
  productId = '<product_id>', # required
  basic_data = {},
  package_options = {},
  additional_data = {},
  package_code = '<package_code>',
  attachments = []
)
```

#### Update

Update an application.

```python
updatedApplication = acrosure_client.application.update(
  application_id = '<application_id>', # required
  basic_data = {},
  package_options = {},
  additional_data = {},
  package_code = '<package_code>',
  attachments = []
)
```

#### Get packages

Get current application available packages.

```python
packages = acrosure_client.application.get_packages(
  '<application_id>'
)
```

#### Select package

Select package for current application.

```python
updated_application = acrosure_client.application.select_package(
  application_id = '<application_id>',
  package_code = '<package_code>'
)
```

#### Get package

Get selected package of current application.

```python
current_package = acrosure_client.application.get_package(
  '<application_id>'
)
```

#### Get 2C2P hash

Get 2C2P hash.

```python
returned_hash = acrosure_client.application.get_2c2p_hash(
  application_id = '<application_id>',
  args = '<arguments>'
)
```

#### Submit

Submit current application.

```python
submitted_application = acrosure_client.application.submit(
  '<application_id>'
)
```

#### Confirm

Confirm current application.

_This function needs secret API key._

```python
confirmed_application = acrosure_client.application.confirm(
  '<application_id>'
)
```

#### List

List your applications (with or without query).

```python
applications = acrosure_client.application.list(query)
```

### Product

#### Get

Get product with specified id.

```python
product = acrosure_client.product.get('<product_id>')
```

#### List

List your products (with or without query).

```t
products = acrosure_client.product.list(query)
```

### Policy

#### Get

Get policy with specified id.

```python
policy = acrosure_client.policy.get('<policy_id>')
```

#### List

List your policies (with or without query).

```python
policies = acrosure_client.policy.list(query)
```

### Data

#### Get

Get values for a handler (with or without dependencies, please refer to Acrosure API Document).

```python
// Without dependencies
values = acrosure_client.data.get(
  handler = '<some_handler>'
)

// With dependencies
values = acrosure_client.data.get(
  handler = '<some_handler>',
  dependencies = ['<dependency_1>', '<dependency_2>']
)
```

### Team

#### Get info

Get current team information.

```python
team_info = acrosure_client.team.get_info()
```

### Other functionality

#### Verify webhook signature

Verify webhook signature by specify signature and raw data string

```python
is_signature_valid = acrosure_client.verify_webhook(
  signature = '<signature>',
  data = '<raw_data>'
)
```

## Advanced Usage

Please refer to [this document](https://github.com/Acrosure/acrosure-python-sdk/wiki/Acrosure-Python-SDK) for AcrosureClient usage.

And refer to [Acrosure API Document](https://docs.acrosure.com/docs/api-overall.html) for more details on Acrosure API.

## Associated Acrosure API endpoints

### Application

```
/applications/get
/applications/list
/applications/create
/applications/update
/applications/get-packages
/applications/get-package
/applications/select-package
/applications/submit
/applications/confirm
/applications/get-hash
```

### Product

```
/products/get
/products/list
```

### Policy

```
/policies/get
/policies/list
```

### Data

```
/data/get
```

### Team

```
/teams/get-info
```
