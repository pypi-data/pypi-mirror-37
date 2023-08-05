Introduction
============

Basic catalog implementation for guillotina using the default postgresql
server.


Status
------

This is just a proof of concept right now.

What is does right now:

- provides indexes for basic types(not all, dates not supported)
- works with the POST @search endpoint


POST /db/container/@search {
  "tag": "foobar"
}
