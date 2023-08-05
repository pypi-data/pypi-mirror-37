import io

from bddrest import Story


def test_markdown():

    def get_field_info(resource, verb, name):
        return dict(
            f1=dict(required=True, not_none=True),
        ).get(name)

    story = Story.loads(provided_story)
    outfile = io.StringIO()
    story.document(outfile, fieldinfo=get_field_info)
    outputstring = outfile.getvalue()
    assert expected_markdown == outputstring


provided_story = '''
    base_call:
      as_: visitor
      title: Quickstart!
      description: Awesome API!
      url: /books/:id
      url_parameters:
        id: '1'
      query:
        a: 1
        b: '2'
      verb: PUT
      form:
        f1: abc
        f2: 123
      headers:
        - 'Content-Type: application/json;charset=utf-8'
      response:
        headers:
        - 'Content-Type: application/json;charset=utf-8'
        json:
          foo: bar
        status: 200 OK
    calls:
    - response:
        headers:
        - 'Content-Type: text/plain;charset=utf-8'
        status: 404 Not Found
      title: Trying invalid book id
      description: trying an invalid book id.
      url_parameters:
        id: None
      query:
        a: 2
        b: 4
      headers:
      - 'A: B'
      form:
        f1: cba
'''

expected_markdown = '''\
## Quickstart!

### PUT /books/:id

Awesome API!

### Url Parameters

Name | Example
--- | ---
id | 1

### Query Strings

Name | Example
--- | ---
a | 1
b | 2

### Form

Name | Required | Not Nullable | Example
--- | --- | --- | ---
f1 | True | True | abc
f2 | ? | ? | 123

### Request Headers

* Content-Type: application/json;charset=utf-8

### Response: 200 OK

#### Body

Content-Type: application/json

```json
{"foo": "bar"}
```

---

## WHEN: Trying invalid book id

trying an invalid book id.

### Url Parameters

Name | Example
--- | ---
id | None

### Query Strings

Name | Example
--- | ---
a | 2
b | 4

### Form

Name | Required | Not Nullable | Example
--- | --- | --- | ---
f1 | True | True | cba

### Request Headers

* A: B

### Response: 404 Not Found

'''

