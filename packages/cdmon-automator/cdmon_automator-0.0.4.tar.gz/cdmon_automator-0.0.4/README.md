# Python library for CRUD operations on cdmon.com

This project will let you manage programmatically your domains in cdmon.com

## How does it work?

It runs Chrome in headless mode and does what you'd do manually. There is no
dark magic nor obscure hacks.

## What do I need?

Any Python 3.x (+3.2 recommended) with PIP and Chrome (headless)

## How can I use it?

A very basic usage example:

```python
from cdmon import CDMON

cdmon = CDMON()
cdmon.login()

cdmon.work_on("foo.com")
cdmon.create_record("TXT", {
    "redirect_type": "custom",
    "subdomain": "bar",
    "value": "123456789"
})

cdmon.work_on("mydomain.com")
cdmon.change_record("A", "www", "127.0.0.1")
cdmon.change_record("A", "mailcow", "1.2.3.4")
cdmon.change_record("TXT", "@", "v=spf1 ...")

cdmon.work_on("xyz.com")
cdmon.delete_record("TXT", "bar")

cdmon.terminate()
```

Keep in mind the library uses environment variables to get the login data.
You'll need to provide those, creating a `.env` file or by any other means.

```
USERNAME=
PASSWORD=
TIMEOUT=10
DEBUG=True
NETDEBUG=True
```

* `USERNAME` - The username / email you use to login in cdmon.com
* `PASSWORD` - The password
* `TIMEOUT` - Make Selenium timeout after that amount of time (in seconds). Default `10`.
* `DEBUG` - If set to `True` it will show Chrome's UI. Default `False`.
* `NETDEBUG` - If set to `True` it will show `urllib` debug to stdout. Default `False`.

## Usage details

### work_on(domain_name)

You must call this method before doing any other work, in order to let the
library know on which domain you want to do the work on.

### create_record(record_type, values)

`record_type` - The type of the record you're trying to create. It can be

* `TXT`
* `SPF`
* `A`
* `AAAA`
* `CNAME`
* `MX`
* `SRV`
* `NS`

`values` - A hash containing specific data for the type of record you're
trying to create. Not all records need/use the same (amount of) variables. Use
the following list to make sure to use the correct data.

#### TXT / SPF

`redirect_type` - The type of redirect. It can be

* `@` - The entire domain
* `*` - Undefined subdomains
* `custom` - A custom subdomain

`subdomain` - The custom subdomain. This argument makes sense only when
`redirect_type` is set to `custom`.

`value` - The value of the record.

Examples:

* Create a TXT record for the domain itself, with the value `foo bar xyz`

    ```python
    cdmon.create_record("TXT", {
        "redirect_type": "@",
        "value": "foo bar xyz"
    })
    ```

* Create a TXT record for `test.mydomain.com`, with the value `hi`

    ```python
    cdmon.create_record("TXT", {
        "redirect_type": "custom",
        "subdomain": "test",
        "value": "hi"
    })
    ```

#### A / AAAA / CNAME / NS

`redirect_type` - The type of redirect. It can be

* `@` - The entire domain
* `*` - Undefined subdomains
* `custom` - A custom subdomain

`subdomain` - The custom subdomain. This argument makes sense only when
`redirect_type` is set to `custom`.

`destination` - The IP you want to assign to the record. Note that the library won't stop you from trying to assign invalid values.

Examples:

* Create an A record for the domain itself, pointing to `127.0.0.1`

    ```python
    cdmon.create_record("A", {
        "redirect_type": "@",
        "destination": "127.0.0.1"
    })
    ```

* Create an AAAA record for the domain `test.mydomain.com`, pointing to `127.0.0.1`

    ```python
    cdmon.create_record("AAAA", {
        "redirect_type": "custom",
        "subdomain": "test",
        "destination": "127.0.0.1"
    })
    ```

* Create a CNAME record for the domain itself, pointing to `www.mydomain.com`

    ```python
    cdmon.create_record("CNAME", {
        "redirect_type": "@",
        "destination": "www.mydomain.com"
    })
    ```

* Create an NS record for the domain `test.mydomain.com`, pointing to `mydomain.com`

    ```python
    cdmon.create_record("NS", {
        "redirect_type": "custom",
        "subdomain": "test",
        "destination": "mydomain.com"
    })
    ```

#### SRV

`redirect_type` - The type of redirect. It can be

* `@` - The entire domain
* `*` - Undefined subdomains
* `custom` - A custom subdomain

`subdomain` - The custom subdomain. This argument makes sense only when
`redirect_type` is set to `custom`.

`destination` - The destination you want to assign to the record. Note that the library won't stop you from trying to assign invalid values.

`priority` - The priority of the record.

`weight` - The weight of the record.

`port` - The port of the record.

Examples:

* Create a SRV record for the domain itself, pointing to `foobar.com 5 800 22`

    ```python
    cdmon.create_record("SRV", {
        "redirect_type": "@",
        "destination": "foobar.com"
        "priority": "5",
        "weight": "800",
        "port": "22"
    })
    ```

* Create an SRV record for the domain `mail.mydomain.com`, pointing to `smtp.foo.bar 10 200 465`

    ```python
    cdmon.create_record("SRV", {
        "redirect_type": "custom",
        "subdomain": "mail",
        "destination": "foobar.com"
        "priority": "10",
        "weight": "200",
        "port": "465"
    })

#### MX

`subdomain` - The subdomain.

`destination` - The destination you want to assign to the record. Note that the library won't stop you from trying to assign invalid values.

`priority` - The priority of the record.

Example:

* Create an MX record for the domain `mail.mydomain.com`, pointing to `foobar.com 10`

    ```python
    cdmon.create_record("MX", {
        "redirect_type": "custom",
        "subdomain": "mail",
        "destination": "foobar.com"
        "priority": "10"
    })

### change_record(self, record_type, record_name, values)

This method will let you update the fields of a record. `values` has the same
rules as the `values` from the `create_record` method.

Note that you can't update the subdomain of the record, only the rest of the
fields. This is how cdmon.com works.

### delete_record(record_type, record_name)

This method will let you delete a record. Note that the search is based on
the type and the name (subdomain), which means that it's error prone in
situation when multiple records of the same type and on the same subdomain
exist, for example, multiple `TXT` records on the `@` domain.

### terminate()

Will close/quit Chrome.