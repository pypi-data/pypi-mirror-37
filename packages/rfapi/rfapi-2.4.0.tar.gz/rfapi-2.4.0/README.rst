rfapi-python
============

Python 2/3 library for using the Recorded Future API

Recorded Future’s API enables you to build analytic applications and
perform analysis which is aware of events happening around the globe
24x7. You can perform queries and receive results from the Recorded
Future Temporal Analytics™ Engine across a vast set of events, entities,
and time points spanning from the far past into the future.

We provide our users with 2 API clients in this package; the Raw API Client
and the Connect API Client, see below.

Installing
__________

To install with pip run ``pip install rfapi``

An API token is required to use the Recorded Future APIs. You can request
a Recorded Future API token by contacting `support@recordedfuture.com` or
your account representative. The easiest way to setup your program is to
save your API token inside an environment variable ``RF_TOKEN``. It is
also possible to explicitly pass a token in the api client constructor. Different
licensing models apply to the Raw API and Connect API.

Public documentation for the Raw API has been discontinued. We do provide documentation on
our `Support Portal <https://support.recordedfuture.com/hc/en-us/categories/115000803507-Raw-API>`__

Examples for Connect API
________________________

The Connect API client provides a façade for our simplified Connect API.
See the `Connect API Explorer <https://api.recordedfuture.com/v2/>`__.

Creating a ConnectApiClient
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from rfapi import ConnectApiClient
    api = ConnectApiClient()

    # or explicitly
    api = ConnectApiClient(auth='my_token')

Examples for Raw API
____________________

The Raw API client provides access to our classical API to get references, entities, etc.
for further details and example usage. See the `Raw API Explorer <https://api.recordedfuture.com/explore.html>`__.

Creating a RawApiClient
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from rfapi import RawApiClient
    api = RawApiClient()

    # or explicitly
    api = RawApiClient(auth='my_token')


Entity
^^^^^^

If you know the id of an entity, here's how to retrieve the
information about it:

.. code:: python

    entity = api.get_entity("ME4QX") # Find the Recorded Future Entity
    print(entity.name) # prints Recorded Future

Entities
^^^^^^^^

Searching for entities is done using ``get_entities``. The first
mandatory argument corresponds to the ``entity`` section of API call.

.. code:: python

    # create a generator of entities
    entities = api.get_entities({
        "type": "Company"
    }, limit=20)
    for e in entities:
        print(e.name) # prints company names

References
^^^^^^^^^^

Searching for references is done using ``get_references``. The first
mandatory argument corresponds to the ``instance`` section of API call.

.. code:: python

    # create a generator of references
    references = api.get_references({
        "type": "CyberAttack"
    }, limit=20)
    for r in references:
        print(r.fragment) # prints event fragments


Events
^^^^^^^^^^

Searching for events is done using ``get_events``. The first
mandatory argument corresponds to the ``cluster`` section of API call.

.. code:: python

    # create a generator of events
    events = api.get_events({
        "type": "CyberAttack"
    }, limit=20)
    for e in events:
        print(e.id) # prints event id


Raw query
^^^^^^^^^

.. code:: python

    # Get QueryResponse object
    import json
    query_response = api.query({
        "references": {
            "type": "CyberAttack",
            "limit": 20
        }
    })

    print(json.dumps(query_response.result, indent=2))

Metadata
^^^^^^^^^

.. code:: python

    # Get dict with metadata info
    import json
    metadata = api.get_metadata()

    print(json.dumps(metadata, indent=2))

Status
^^^^^^^^^

.. code:: python

    # Get API user token usage
    import json
    status = api.get_status()
    # get json as dict
    print(json.dumps(status, indent=2))

