# Blink Computing Client

The [Blink Computing](https://blinkcomputing.co) client allows you to start and stop clusters
in the Blink Computing service programmatically. Once a clusters is running, the client
can create connection objects for various frameworks (Impyla, Ibis).

Install the client from PyPI with:

```sh
pip install blinkcomputing
```

Connect to cluster 'cluster1'. This will start the cluster if it isn't already running.
```python
cl = blinkcomputing.Connect(account='A1', user_name='user1', password='pass', cluster_name='cluster1')
```

Get a dbapi connection:
```python
dbapi_conn = cl.GetDbapiConnection()
```

Get an Ibis connection:
```python
ibis_conn = cl.GetIbisConnection()
```

Clean up when you're done by 'closing' the cluster. This will shut it down if it wasn't already running when you initially called Connect():
```python
cl.Close()
```
