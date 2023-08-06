from guillotina import configure

app_settings = {
}


def includeme(root):
    configure.scan('guillotina_pgcatalog.api')
    configure.scan('guillotina_pgcatalog.utility')
