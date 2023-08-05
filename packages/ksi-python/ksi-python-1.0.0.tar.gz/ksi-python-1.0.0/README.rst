KSI Python SDK
==============

This is a thin wrapper on top of KSI C SDK. Experimental, non-supported code.

Synopsis
--------

Example of synchronous singing and verification.

.. code-block:: python

    import ksi
    import hashlib

    # Instantiate service parameters from the environment
    KSI = ksi.KSI(**ksi.ksi_env())

    # Sign a text string
    sig = KSI.sign_hash(hashlib.sha256(b"Tere!"))
    # Print some signature properties
    print(sig.get_signing_time(), sig.get_signer_id())

    # Now verify this text string, first obtaining a data hasher
    h = sig.get_hasher()
    h.update(b"Tere!")
    print(KSI.verify_hash(sig, h))

    # Obtain a binary blob which can be stored for long term
    serialized_signature = sig.get_binary()

    # Some time have passed, fetch the signature and verify again
    sig2 = KSI.new_signature_object(serialized_signature)
    print(KSI.verify_hash(sig2, h))

Note that asynchronous signing can provide a significant speedup when multiple signatures are requested.
Example of asynchronous singing with gevent.

.. code-block:: python

    import ksi
    import hashlib
    from gevent.pool import Pool

    # Instantiate service parameters from the environment
    KSI = ksi.KSI(**ksi.ksi_env())

    # Multiple strings to be signed
    string_list = ["This", "is", "a", "list", "of", "strings"]

    # Define a signer function.
    def sign_hash(h):
      sig = KSI.sign_hash(h)
      # Verification and/or storing could be done here
      print(KSI.verify_hash(sig, h))

    # Create a gevent pool. Note that for optimal efficiency
    # pool size should not be smaller than
    # ``KSI.get_async_config()['max_pending_count']``
    pool = Pool(100)

    # Sign all strings asynchronously
    for string in string_list:
      pool.spawn(sign_hash, hashlib.sha256(string.encode()))
    pool.join()

Client-side aggregation (signing in blocks) is also possible if the KSI Gateway allows it. This means
that multiple hashes can be individually signed by a single request to the Gateway server. In addition, if
block signing is allowed, the asynchronous signing service will by default dynamically sign in blocks depending
on if the signing requests demand becomes too large to efficiently sign them one-by-one.
Example of signing a block of hashes synchronously (asynchronous block signing is supported as well).

.. code-block:: python

    import ksi
    import hashlib

    # Instantiate service parameters from the environment
    KSI = ksi.KSI(**ksi.ksi_env())

    # Multiple strings to be signed
    string_list = ["This", "is", "a", "list", "of", "strings"]

    # Hashes of strings
    hash_list = [hashlib.sha256(string.encode()) for string in string_list]

    # Sign hashes in a block
    sigs = KSI.sign_hash_list(hash_list)

    # Verify hashes
    for i in range(len(sigs)):
        print(KSI.verify_hash(sigs[i], hash_list[i]))


Install
-------

#. Requirements: Python 2.7+ or Python 3.1+. Jython, IronPython are not supported.

#. Install fresh libksi aka KSI C SDK; see https://github.com/guardtime/libksi/

#. Install python-devel package

#. Run::

    > pip install ksi-python

or

    > easy_install ksi-python



Tests
-----
Specify KSI Gateway access parameters and run
::

    > python setup.py test

To test if KSI Python SDK signs asynchronously with gevent, make sure gevent is installed.

Documentation
-------------

http://guardtime.github.io/ksi-python/

Type::

    > pydoc ksi

to read the documentation after installation. Generating html or pdf documentation:
make sure that dependencies like sphinx (``pip install sphinx``) are installed, extension
is built (``python setup.py build``) and run::

   > cd docs
   > make html
   or
   > make latexpdf



License
-------
Apache 2.0. Please contact Guardtime for supported options.
