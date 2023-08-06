CheKnife
========

Python utilities compilation.

-  Free software: MIT license

Install
=======

-  TODO

Features
========

hashing
-------

.. code:: python

    from CheKnife.hashing import textmd5sum, filemd5sum
    textmd5sum('Hello')
    '8b1a9953c4611296a827abf8c47804d7'

    filemd5sum('README.md')
    '00ddcc5ef19040b9d7921008afcfa5bb'

PKI
---

Generate CA
~~~~~~~~~~~

.. code:: python

    from CheKnife.pki import DistinguishedName, CA
    dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'RootCA')
    ca = CA(dn, working_dir='./test_ca/')
    ca.gen_ca()

Generate IntermediaryCA
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from CheKnife.pki import DistinguishedName, CA, IntermediaryCA
    dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'RootCA')
    ca = CA(dn, working_dir='./test_ca/')
    # ca.gen_ca()   # If not generated yet
    intermediary_dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'IntermediateCA')
    intermediary_ca = IntermediaryCA(intermediary_dn, ca, working_dir='./test_ca/')
    intermediary_ca.gen_ca()

Generate Server Certificate signed with intermediary CA
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Creating RootCA and IntermediaryCA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from CheKnife.pki import DistinguishedName, CA, IntermediaryCA, ServerCertificate
    dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'RootCA')
    ca = CA(dn, working_dir='./test_ca/')
    ca.gen_ca()   # If not generated yet
    intermediary_dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'IntermediateCA')
    intermediary_ca = IntermediaryCA(intermediary_dn, ca, working_dir='./test_ca/')
    intermediary_ca.gen_ca()
    server_dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'example.com', subject_alt_names=['www.example.com', 'web.example.com'])
    server_cert = ServerCertificate(server_dn, intermediary_ca, working_dir='./test_ca/')
    server_cert.gen_cert()
    print(server_cert.check_crt())

Generate CSR + Key
^^^^^^^^^^^^^^^^^^

.. code:: python

    from CheKnife.pki import DistinguishedName, ServerCertificate
    server_dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'example2.com', subject_alt_names=['www.example2.com', 'web.example2.com'])
    server_cert = ServerCertificate(server_dn, working_dir='./test_ca/')
    server_cert.gen_key()
    server_cert.gen_csr()
    print(server_cert.get_csr())

Sign CSR
^^^^^^^^

.. code:: python

    from CheKnife.pki import DistinguishedNameFactory, ServerCertificate, CAFactory
    csr = """-----BEGIN CERTIFICATE REQUEST-----
    MIIE0jCCAroCAQAwgYwxCzAJBgNVBAYTAkVTMQ8wDQYDVQQIDAZNYWRyaWQxDzAN
    BgNVBAcMBk1hZHJpZDEPMA0GA1UECgwGRW1waXJlMRQwEgYDVQQDDAtleGFtcGxl
    LmNvbTE0MDIGA1UdEQwrRE5TLjE9d3d3LmV4YW1wbGUuY29tLEROUy4yPXdlYi5l
    eGFtcGxlLmNvbTCCAiIwDQYJKoZIhvcNAQEBBQADggIPADCCAgoCggIBALEmezTA
    N70sM4Rr4MXjqy1tNZlzq5CEuMhWNKM8euPfsY4WY7Fz1iAlV87F9ZcpJPlqKQcJ
    u/B6RQWD4o4+ZWeOOz+92qeokP+A4Us2nMglru22e+bwLDSah0mNrn7dZoVNqYRg
    vEy9BFLyN1t2wkNiWh6C+YkV8/gsSKAQbI/UKxa6qq2eap7rkWeNsjw+IOzdzXCP
    uJEy8bT86NeL5HVJ7GiBBWqjaGURhauYXV2M3RdOpnmH7jCtEjpeCJUKedOWqC07
    GNqls73cUAzRkwzEcbQxY2IlgLxNfYLP/VG9e7zujBx/5pCj7cudziaa3dy+XJPw
    JIAIskcwWvjSlevzX78X7dJKVcFCVSTQs99ViySGsQBgazvXHkDFad5qWaj9yYaW
    yt8J+KFP/e+zqj254A+VAh+xFf9XSVr4F6xdcb3ffuEAF91W3ahP0MRlh2J5YtUS
    hReCwZRxR9o2aSy1GzwKudIugQ3Qfj5Y0+dqRbgjEwVWMDy8nFyLUMHYnMMuSRpt
    cPYXLxxnyqc2J3f2ujkeytGU+CK21XSrXJS2fA0NaTNFpDGjQAfl7aRTMmPZYq1h
    k3ccZDL3M0nf33EXgYmDnwO6/LApqzce+XMGbr3iX20C9mEdCMpiH+11jyrM3Gay
    /mV8pFE/6WjoWfUoE+v+sluLlvjcrNSjHwfnAgMBAAGgADANBgkqhkiG9w0BAQsF
    AAOCAgEAYWAZBrcMI1EYtAafW6xkYUa9SZHrFdvzc9H3vfAhipzA+QGf0/u4XRSo
    hTWJraGVFVvFzGA2EUKjIzBkAgDj6HdL9YTj17zw5sClJS8CLoOZwKjtIn823N7a
    EutpDMjBhBc5i71MJPhFEYTTPzNwb569u8B9NNlO7MJyQkIJM0QSkvWeXvPMvyr1
    qlrms3pJVLRG1rOcEH0K03DonI0RpAtFSc8sZApxTmLr5Ww1NPSfU6FSq868jiZD
    pGndafJPRVp2ASeFABgIuVvCR9oE+XX/MJGEHeLMr3qHUmugdykc6XrHyf7FGmlQ
    Hzqk3z/rkxOewqwz5HQNzidxas+nTE1YuVxh9EQLTB+qYAzYcUl4yMqYn7NJp+C2
    ydhtGjdvfieZPxMetOPPa4ZRHOHKMDAMwNLWGDN/lysjs7DQ8xMPKT027P54TqUI
    ROfr/J770Y2MouQnt/U3u2e7JZbR6j8buUK8M0aO54ZaIdzd/Bpudpxxiqa4hRvK
    HKRLULmtIXZ0r2d6LIOdJPwE3yXUHI8rI1/MuqfRTabB3nEbK7irH75pX3QbFMpx
    6Cw6L0kgqc5Zc/aOm+SbPZgGYSQ6AKPWZoADo543QMs2JM+MlWLOErp+0nviw/OT
    2ffBPftfqZYVsIhn0o5vGAumwQ3OPnfQieGAK8fpTC7O9vtD1XI=
    -----END CERTIFICATE REQUEST-----
    """

    # server_dn = DistinguishedNameFactory()
    ca = CAFactory().from_file('./test_ca/CA/certs/IntermediateCA.crt')
    server_cert = ServerCertificate(csr=csr, ca=ca, working_dir='./test_ca/')
    server_cert.sign_csr()
    server_cert.check_crt()

Using existing RootCA and IntermediaryCA
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from CheKnife.pki import DistinguishedName, ServerCertificate, IntermediaryCAFactory
    intermediary_ca = IntermediaryCAFactory().from_file('./test_ca/CA/certs/IntermediateCA.crt')  # optional argument ca_path='./test_ca/CA/certs/RootCA.crt

    server_dn = DistinguishedName('ES', 'Madrid', 'Madrid', 'Empire', 'example3.com', subject_alt_names=['www.example3.com', 'web.example3.com'])
    server_cert = ServerCertificate(server_dn, intermediary_ca, working_dir='./test_ca/')
    server_cert.gen_cert()
    print(server_cert.check_crt())

Check Keys, CSR and certificates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from CheKnife.pki import OpenSSL
    openssl = OpenSSL()
    openssl.check_crt('/pat/to/certificate.crt')
    openssl.check_key('/pat/to/certificate.key')
    openssl.check_csr('/pat/to/certificate.csr')

Distinguished Name from crt
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from CheKnife.pki import DistinguishedNameFactory
    factory = DistinguishedNameFactory()

    crt_path = './test_ca/CA/certs/IntermediateCA.crt'
    dn = factory.from_crt(crt_path)

Intermediary CA from path
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from CheKnife.pki import IntermediaryCAFactory
    intermediary_ca_factory = IntermediaryCAFactory()
    intermediary_ca = intermediary_ca_factory.from_file('./test_ca/CA/certs/IntermediateCA.crt')  # optional argument ca_path='./test_ca/CA/certs/RootCA.crt

Check Connection
~~~~~~~~~~~~~~~~

.. code:: python

    from CheKnife.pki import OpenSSL
    openssl = OpenSSL()
    out, err = openssl.check_connect('www.google.com', 443)

Distinguished Name Cheatsheet
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------+--------------------------+
| Short   | Long                     |
+=========+==========================+
| DN      | Distinguished Name       |
+---------+--------------------------+
| CN      | CommonName               |
+---------+--------------------------+
| L       | LocalityName             |
+---------+--------------------------+
| ST      | StateOrProvinceName      |
+---------+--------------------------+
| O       | OrganizationName         |
+---------+--------------------------+
| OU      | OrganizationalUnitName   |
+---------+--------------------------+
| C       | CountryName              |
+---------+--------------------------+

| DN Example:
| C=PT, ST=Lisboa, L=Lisboa, O=Foo Org, OU=Bar Sector,
  CN=foo.org/emailAddress=admin@foo.org

Tests
=====

.. code:: bash

    nosetests --with-coverage --cover-inclusive --cover-package=CheKnife --cover-html

Upload to PyPi
==============

.. code:: bash

    python setup.py sdist upload -r pypi
