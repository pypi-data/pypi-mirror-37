#####################################################################
# Copyright (C) 2015-18 Guardtime, Inc
# This file is part of the Guardtime client SDK.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES, CONDITIONS, OR OTHER LICENSES OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
# "Guardtime" and "KSI" are trademarks or registered trademarks of
# Guardtime, Inc., and no license to trademarks is granted; Guardtime
# reserves and retains all trademark rights.

import os
import hashlib
from datetime import datetime
import math
import time
import sys
import re
import uuid

import _ksi


class KsiSignature(object):
    """ KSI Signature object.

    Exists only in instantiated, integrity-checked form. Created by the KSI class only.
    Do not initialize directly.

    Args:
        ksi (class KSI): KSI class. Necessary to avoid early garbage collection.
        sig: serialized signature.
    """

    def __init__(self, ksi, sig):
        self.__ksi_ref = ksi
        self.__binary = sig

    def get_binary(self):
        """ Returns a serialized signature, ready to be passed to C language binding or
            stored into a file or db field.
        """
        return self.__binary

    def set_binary(self, sig):
        """ Sets a new serialized signature.
            Called after successfully extending the prior signature. Internal use.
        """
        self.__binary = sig

    def get_hash_algorithm(self):
        """ Returns the hash algorithm name used for hashing data during signing.

        It is important to use exactly the same hash algorithm for hashing data during
        signing and during signature verification.

        Note:
            Returns algorithm names like ``SHA2-256``. Some older libraries, like Python's
            hashlib and OpenSSL use names like ``SHA256``. Use some processing to get
            legacy compatible name, for example:

                sig.get_hash_algorithm().replace("SHA2-", "sha")

        Returns:
            str: hash algorithm name

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        return _ksi.ksi_get_hash_algorithm(self.__ksi_ref._ctx, self.__binary)

    def get_data_hash(self):
        """ Returns the hash algorithm and hash value of signed data

        See the note about `get_hash_algorithm()`

        Returns:
            (str, str/buffer): A tuple of hash algorithm name and a binary data hash.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        return _ksi.ksi_get_data_hash(self.__ksi_ref._ctx, self.__binary)

    def get_hasher(self):
        """ Returns a data hasher object from hashlib.

        Used hash algorithm matches the one which was used during the signature creation.

        Returns:
            Object: a new hashing object from `hashlib`

        Raises:
            ksi.Error: or its subclass on KSI errors
            ValueError: hashlib does not support used hash algorithm
        """
        algname = _ksi.ksi_get_hash_algorithm(self.__ksi_ref._ctx, self.__binary).lower()
        algname = algname.replace("sha2-", "sha")
        algname = algname.replace("-", "")
        return hashlib.new(algname)

    def get_signing_time_utc(self):
        """ Extract cryptographically protected signing time from a signature.

        Returns:
            Object: ``datetime.datetime`` object, using UTC timezone.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        signing_time = _ksi.ksi_get_signing_time(self.__ksi_ref._ctx, self.__binary)
        return datetime.utcfromtimestamp(signing_time)

    def get_signing_time(self):
        """ Extract cryptographically protected signing time from a signature.

        Returns:
            Object: ``datetime.datetime`` object, in local timezone.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        signing_time = _ksi.ksi_get_signing_time(self.__ksi_ref._ctx, self.__binary)
        return datetime.fromtimestamp(signing_time)

    def get_signer_id(self):
        """ Extract cryptographically protected data signer's identity.

        This identifier contains hierarchical namespace of KSI aggregators, gateway and end user.
        May look like ``GT :: GT :: Company :: user.name``.

        Returns:
            str: a signer's id prefixed with full aggregator hierarchy.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        return _ksi.ksi_get_signer_id(self.__ksi_ref._ctx, self.__binary)

    def is_extended(self):
        """ Checks if signature is extened and contains a publication record.

        Returns:
            Bool: True if extended, False if not.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        return _ksi.ksi_is_extended(self.__ksi_ref._ctx, self.__binary)

    def get_publication_data(self):
        """ Returns publication data used for extending this signature.

        Returned data can be used to validate the signature in strongest possible form,
        using an independent publication. Publications references refer to the choice of mediums;
        publication code can be compared with one printed in chosen medium.

        Returns:
            None if publication record is not available. A dictionary on success, see example below::

            {
                'refs': [
                    u'ref1',
                    u'Financial Times, ISSN: 0307-1766, 2015-06-17',
                    u'https://twitter.com/Guardtime/status/611103980870070272'
                ],
                'publication': 'AAAAAA-CVPYKY-AANVCV-Q7IJFM-ZJ5YBK-BNXRKG-IWIFER-5XXL73-4NXXLS-D6CROT-QUMAHA-JDWBQI',
                'publishing_time_t': 1434326400L,
                'publishing_time': datetime.datetime(2015, 6, 15, 0, 0)
            }

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        r = _ksi.ksi_get_publication_data(self.__ksi_ref._ctx, self.__binary)
        if r and r['publishing_time_t']:
            r['publishing_time'] = datetime.utcfromtimestamp(r['publishing_time_t'])
        return r

class KsiAsync(object):
    """ Async service class. Handles the KSI asynchronous signing service.

    Created by the KSI class only. Do not initialize or call methods directly.

    Note that this class is optimized to be used with gevent. Requests called without
    spawned greenlets (e.g. by gevent.spawn or gevent.Pool.spawn) will be blocking.
    """
    def __init__(self, ctx, surl, suser, skey):
        self.requests = {}
        self.responses = {}
        self.queue = []
        self.block_levels = {}
        self.pending_count = 0
        self.max_retry_count = 4
        self.block_signing_wait_ms_time = 400
        self.ctx = ctx
        url = "ksi+http://" + suser + ":" + skey + "@" + re.sub("http[s]*://", "", surl)
        max_req_count, max_level = _ksi.ksi_get_aggr_config(ctx)
        self.max_block_size = min(2**max_level, 65536)
        self.max_req_count = max(min(max_req_count/10, 250), 4)
        self.max_pending_count = self.max_req_count * 2
        self.dynamic_block_signing = True if self.max_block_size > 1 else False
        self.service = _ksi.ksi_new_async_service(ctx, url, suser, skey, self.max_req_count, self.max_pending_count + 1)

    def new_request(self, hash_name, hash_digest):
        """ Creates request and sends to the service.

        Args:
            string: name of the hashing function which created this hash.
            Object: hash created using a hasher from Python ``hashlib``

        Returns:
            uuid: id of the request so its progress can be tracked

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        request_id = str(uuid.uuid4())
        self.requests.update({request_id: {'name': hash_name, 'hash': hash_digest, 'err': [False, None], 'block_id': None,
                                           't': int(round(time.time() * 1000)), 'request_count': 0, 'lvl': 0,
                                           'spawned': self.__is_gevent_spawned()}})
        self.queue.append(request_id)
        self.__send_request(request_id)
        return request_id

    def new_block_request(self, hash_names, hash_digests, leaf_ids = None):
        """ Creates block signing request and sends to the service.

        Args:
            [string]: list of hashing function names
            [Object]: list of hashes created by ``hashlib``
            [uuid]: list of hash uuids if block signing request is dynamically
                    initialized by KsiAsync

        Returns:
            uuid: id of the request so its progress can be tracked

        Raises:
            ksi.AsyncServiceError: requested block size exceeds limit
            ksi.Error: or its subclass on KSI errors
        """
        if self.max_block_size == 1:
            raise AsyncServiceError("Block signing is not permitted")
        elif len(hash_names) > self.max_block_size:
            raise AsyncServiceError("Hash count for block signing exceeds limit")
        request_id = "b_" + str(uuid.uuid4())

        leaf_ids = leaf_ids and leaf_ids or {}
        for leaf_id in leaf_ids:
            self.requests[leaf_id]['block_id'] = request_id
            self.requests[leaf_id]['request_count'] = 0
            self.requests[leaf_id]['err'] = [False, None]
            self.queue.remove(leaf_id)

        block_builder, block_handles, hash_digest, level = _ksi.ksi_build_block(self.ctx, hash_names, hash_digests)
        self.requests.update({request_id: {'name': 'default', 'hash': hash_digest, 'err': [False, None], 'request_count': 0,
                                         'block_id': request_id, 'leaf_ids': leaf_ids, 'handles': block_handles, 'lvl': level,
                                         'block_builder': block_builder, 'spawned': self.__is_gevent_spawned()}})
        self.queue.append(request_id)
        self.block_levels.update({request_id: level})
        if not leaf_ids:
            self.__send_request(request_id)
            return request_id

    def run_service(self, request_id):
        """ Runs the async signing service

        ``_ksi.ksi_run_async_service`` returns:
            dict/bool:
                {uuid: signature} in case the async response handle returned a
                signature response
            int:
                is the number of responses yet to be received
            list/bool:
                [response_id, error_string] if the async response handle returned an error

        Args:
            uuid: in order to track current request

        Raises:
            ksi.Error: or its subclass on KSI errors
            ksi.AsyncServiceError: if too many retry requests have been sent with current uuid
            ksi.HashError: if problems with the request hash
        """
        if not self.requests[request_id]['err'][0]:
            sig, pending_count, error = _ksi.ksi_run_async_service(self.service, self.block_levels)
            self.__update_from_response(sig, pending_count, error, request_id)
        elif self.requests[request_id]['err'][0]:
            if self.requests[request_id]['request_count'] > self.max_retry_count:
                if self.__is_block_leaf(request_id) and self.requests[request_id]['block_id'] in self.requests:
                    block_id = self.requests[request_id]['block_id']
                    del self.requests[block_id]
                    self.queue.remove(block_id)
                error_string = "Request max retry count reached."

                if self.requests[request_id]['err'][1]:
                    error_string += " Last Error: " + self.requests[request_id]['err'][1]
                del self.requests[request_id]
                if request_id in self.queue:
                    self.queue.remove(request_id)
                raise AsyncServiceError(error_string)
            else:
                self.__send_request(request_id)
                self.__sleep(request_id)

    def get_response(self, request_id):
        """ Returns the serialized signature

        Removes request and response data from instance and returns the received signature.

        Args:
            uuid: id of request
        Returns:
            sig: signature of the hash with given uuid
        """
        if request_id in self.queue:
            self.queue.remove(request_id)
        del self.requests[request_id]
        return self.responses.pop(request_id)

    def get_config(self):
        """ Returns async service configuration

        Note:
            Mutable entries (see ``KsiAsync.set_config``):
                'max_req_count', 'max_pending_count', 'dynamic_block_signing'
            Immutable entries:
                'server_max_req_count':
                    maximum number of requests the aggregator is willing to respond to per round
                'max_block_size':
                    capped at 2^16, max block size gives the maximum number of hashes one block
                    can contain
                'block_signing':
                    if block signing is available for the current ksi context. If not,
                    'dynamic_block_signing' cannot be set to True and ``KSI.sign_hash_list``
                    raises ``KSI.AsyncServiceError``
        Returns:
            dict: {"server_max_req_count": int, "max_req_count": int,
                   "max_pending_count": int, "max_block_size": int,
                   "dynamic_block_signing": bool, "block_signing": bool}
        """
        max_req_count, max_level = _ksi.ksi_get_aggr_config(self.ctx)
        self.max_block_size = min(2**max_level, 65536)
        config = {
            "server_max_req_count": max_req_count, "max_block_size": self.max_block_size,
            "max_req_count": self.max_req_count, "max_pending_count": self.max_pending_count,
            "dynamic_block_signing": self.dynamic_block_signing, "block_signing": self.max_block_size > 1
            }
        return config

    def set_config(self, max_req_count = None, max_pending_count = None, dynamic_block_signing = None):
        """ Saves new async service configuration

        Args:
            int: maximum request count per round, should not be larger than the server maximum
                 request count per round, as timeouts and HTTP errors will occur
            int: maximum number of requests to be cached at one time, must not be smaller than
                 last configured value
            bool: sign with blocks explicitly or in case demand exceeds max_pending_count, not permitted
                  to use if ``config['block_signing'] == False``
        Raises:
            ValueError: when parameters are incorrect
        """
        max_req_count = max_req_count if type(max_req_count) is int else self.max_req_count
        max_pending_count = max_pending_count if type(max_pending_count) is int else self.max_pending_count
        if max_req_count < 1 or max_pending_count < self.max_pending_count:
            raise ValueError("Invalid config parameters")
        if self.max_block_size == 1 and dynamic_block_signing:
            raise ValueError("Block signing is not permitted")
        dbs = dynamic_block_signing if dynamic_block_signing is not None else self.dynamic_block_signing
        self.max_req_count = max_req_count
        self.max_pending_count = max_pending_count
        self.dynamic_block_signing = dbs
        _ksi.ksi_set_async_config(self.service, self.max_req_count, self.max_pending_count + 1)

    def get_state(self):
        """ Returns async service state

        `state` dictionary key/value pairs:
            "pending requests":
                (int) number of requests which have been sent for
                signing. Cannot be larger than
                ``KsiAsync.max_pending_count``
            "responses ready":
                (int) number of signatures which have been received
                but not returned by ``KSI.sign_hash``
            "waiting in queue":
                (int) number of signatures which have not yet been sent
                for signing as ``KsiAsync.max_pending_count`` has been
                reached (if a request stays in queue for more than 1
                minute, then ``AsyncServiceError`` is raised)
            "requests in cache":
                (int) number of active ``KSI.sign_hash`` and ``KSI.sign_hash_list`` instances

        Returns:
            dict (state)
        """
        state = {'pending requests': self.pending_count, 'responses ready': len(self.responses),
                 'waiting in queue': len(self.queue), 'requests in cache': len(self.requests)}
        return state

    def is_pending(self, request_id):
        """ Checks if request hash has been signed

        Args:
            uuid: id of request
        Returns:
            bool: True if requested hash has been signed
        """
        return request_id not in self.responses

    def __send_request(self, request_id):
        """ Gives the request to C api to be sent to the aggregator

        Args:
            uuid: id of the request
        Raises:
            ksi.Error: or its subclass on KSI errors
            ksi.HashError: if problems with the request hash
            ksi.AsyncServiceError: if request cache is full (note this should not happen unless
                                   KsiAsync is improperly used) or request timeout
        """
        _id = self.__run_queue_handler(request_id)
        if _id:
            request = self.requests[_id]
            res = _ksi.ksi_new_async_sign_request(self.service, self.ctx, _id, request['name'], request['hash'], request['lvl'])
            request['request_count'] += 1
            for leaf_id in request.get('leaf_ids', {}):
                self.requests[leaf_id]['request_count'] += 1

            if res:
                self.pending_count += 1
                request['err'][0] = False
                for leaf_id in self.requests[_id].get('leaf_ids', {}):
                    self.requests[leaf_id]['err'][0] = False
                self.queue.remove(_id)
                self.__sleep(request_id)
            else:
                request['err'] = [True, res]
                for leaf_id in request.get('leaf_ids', {}):
                    self.requests[leaf_id]['err'][0] = True

    def __maybe_put_queue_in_blocks(self):
        """ If required, forms blocks from requests in the queue for faster signing

        If the oldest single-hash sign requests in ``KsiAsync.queue`` has been waiting at least
        ``KsiAsync.block_signing_wait_ms_time`` and dynamic block signing is enabled, then takes
        all single-hash sign requests in ``KsiAsync.queue`` and aggregates them into trees to
        accelerate signing.
        """
        if not self.dynamic_block_signing:
            return
        exceeded_wait_time = False
        cur_ms_time = int(round(time.time() * 1000))

        for request_id in self.queue:
            if not self.__is_part_of_block(request_id):
                exceeded_wait_time = cur_ms_time - self.requests[request_id]['t'] >= self.block_signing_wait_ms_time
                break

        if exceeded_wait_time:
            waiting_leaf_ids = [request_id for request_id in self.queue if not self.__is_part_of_block(request_id)]
            block_num = int(math.ceil(len(waiting_leaf_ids)/float(self.max_block_size)))
            for i in range(block_num):
                block_leaf_ids = waiting_leaf_ids[i*self.max_block_size:(i+1)*self.max_block_size]
                block_leaf_hash_names = [self.requests[leaf_req]['name'] for leaf_req in block_leaf_ids]
                block_leaf_hash_digests = [self.requests[leaf_req]['hash'] for leaf_req in block_leaf_ids]
                self.new_block_request(block_leaf_hash_names, block_leaf_hash_digests, block_leaf_ids)

    def __run_queue_handler(self, request_id):
        """ Handles pending requests and forms blocks if configured accordingly

        Raises:
            ksi.AsyncServiceError: if request timeout
        """

        begin_time = int(time.time())
        request = self.requests[request_id]
        while self.pending_count >= self.max_pending_count and request['spawned']:
            self.__maybe_put_queue_in_blocks()

            if int(time.time()) - begin_time > 60 and not self.__is_block_leaf(request_id):
                self.queue.remove(request_id)
                del self.requests[request_id]
                raise AsyncServiceError("Request timeout")
            self.__sleep(request_id)
            if self.__is_sent_as_block(request_id):
                return None
        block_id = request['block_id'] if request['request_count'] <= self.max_retry_count else None
        return block_id or (request_id in self.queue and request_id) or None

    def __update_from_response(self, sig, pending_count, err, request_id):
        """ Processes the response from running the async service

        Args:
            dict/bool: {uuid: signature} in case the async response handle returned a
                       signature response
            int:       is the number of responses yet to be received
            list/bool: [response_id, error_string] if the async response handle returned an error
            uuid: id of the current request
        """
        self.pending_count = pending_count
        if sig:
            sig_id, signature = sig.popitem()
            if self.__is_block_id(sig_id):
                signatures = _ksi.ksi_get_block_signatures(self.ctx, signature, self.requests[sig_id]['handles'])
                leaf_ids = self.requests[sig_id]['leaf_ids']
                del self.block_levels[sig_id]
                if leaf_ids:
                    for i in range(len(leaf_ids)):
                        self.__update_from_response({leaf_ids[i]: signatures[i]}, pending_count, None, leaf_ids[i])
                    del self.requests[sig_id]
                else:
                    self.responses.update({sig_id: signatures})
            else:
                self.responses.update({sig_id: signature})
            if request_id != sig_id:
                self.__sleep(request_id)
        elif err:
            _id, error_string = err
            request = self.requests[_id]
            request['err'] = [True, error_string]
            self.queue.append(_id)
            for leaf_id in self.requests[_id].get('leaf_ids', {}):
                self.requests[leaf_id]['err'] = [True, error_string]

            if _id != request_id:
                self.__sleep(request_id)
        elif self.pending_count == 0:
            self.requests[request_id]['err'][0] = True
            self.queue.append(request_id)
            block_request = self.requests.get(self.requests[request_id]['block_id'], {})
            block_request['err'] = [True, "Request lost."]
            for leaf_id in block_request.get('leaf_ids', {}):
                self.requests[leaf_id]['err'] = [True, "Request lost."]

    def __is_gevent_spawned(self):
        """ Checks if gevent is used and the current greenlet is in gevent's event loop """
        if 'gevent' in sys.modules:
            return sys.modules['gevent'].getcurrent().parent

    def __is_block_id(self, request_id):
        """ Checks if given request id type is a block id type """
        if request_id:
            return request_id[:2] == "b_"

    def __is_sent_as_block(self, request_id):
        """ Checks if given request id is part of a block and if the block has been sent """
        block_id = self.requests[request_id]['block_id']
        return block_id and block_id not in self.queue

    def __is_block_leaf(self, request_id):
        """ Checks if given request id is a leaf in a block """
        block_id = self.requests[request_id]['block_id']
        return self.__is_block_id(block_id) and not self.__is_block_id(request_id)

    def __is_part_of_block(self, request_id):
        """ Checks if given request id is a leaf or a root node in a block """
        return self.__is_block_id(self.requests[request_id]['block_id'])

    def __sleep(self, request_id, t = 0.25):
        """ Sleeps current greenlet if it has been spawned by gevent

        Note if gevent is not used (or if it is used, but the signing is called synchronously),
        ``KsiAsync.__sleep`` becomes blocking.
        """
        (sys.modules['gevent'] if self.requests[request_id]['spawned'] else time).sleep(t)


class KSI(object):
    """KSI service provider class. Holds context and service parameters.

    Args:
        signing_service (dict):   Signing/aggregation service access parameters. A dictionary
                                  with following keys: {'url': .., 'user': ..., 'pass': ...}
        extending_service (dict): Extending service access parameters. A dictionary
                                  with following keys: {'url': .., 'user': ..., 'pass': ...}
        publications_file (str, optional):  Publications file download URL. Default one works
                                  with Guardtime commercial KSI service.
        publications_cnstr (dict, optional):  Publications file verification constraints: signing
                                  certificate (must be issued under a root in global system
                                  truststore) fields are validated against provided rules, e.g.::

                                        {"email" : "publications@guardtime.com"}

                                  Default one works with Guardtime commercial KSI service.

    Properties:
        verification: constants specifying verification policies. see ``set_verification_policy()``
    """
    def __init__(self, signing_service, extending_service,
                 publications_file='http://verify.guardtime.com/ksi-publications.bin',
                 publications_cnstr={"email" : "publications@guardtime.com"},
                ):

        self._ctx = _ksi.ksi_init(signing_service['url'], signing_service['user'], signing_service['pass'],
                                   extending_service['url'], extending_service['user'], extending_service['pass'],
                                   publications_file, publications_cnstr)

        self.verification = _ksi
        self.__policy = _ksi.POLICY_GENERAL_EXT
        self.async_service = KsiAsync(self._ctx, signing_service['url'], signing_service['user'], signing_service['pass'])

    def sign_hash(self, data_hash):
        """ Signs a data hash.

        Note:
            In case of gevent use (function run by spawned greenlet):
                Signing is an asynchronous operation.
            Otherwise:
                Signing blocks for 1..2 seconds.

            When using gevent, the state of the async service can be monitored by calling
            ``KSI.get_async_state()``. Spawning greenlets does not automatically guarantee
            that that the async state is updated as greenlets may not run instantaneously.
            It is recommended to also monitor how many greenlets are being spawned or even
            use gevent.pool in accordance with the async service configuration (see
            ``KSI.get_async_config()``) for increased memory safety.

        Args:
            Object: hash created using a hasher from Python ``hashlib``.

        Returns:
            KsiSignature: see ``KsiSignature`` class in this module.

        Raises:
            ksi.Error: or its subclass on KSI errors
            ksi.AsyncServiceError: when the request has waited over a minute to be sent
                                   out or when the maximum retry count has been reached
                                   due to previous errors. Related to too many
                                   asynchronous requests or incorrect async service
                                   config
        """
        request_id = self.async_service.new_request(data_hash.name, data_hash.digest())
        while True:
            if self.async_service.is_pending(request_id):
                self.async_service.run_service(request_id)
            else:
                return KsiSignature(self, self.async_service.get_response(request_id))

    def sign_hash_list(self, data_hashes):
        """ Signs a list of hashes in one block.

        Note:
            In case of gevent use (function run by spawned greenlet):
                Signing is an asynchronous operation.
            Otherwise:
                Signing blocks for 1..2 seconds.

        Args:
            list: hashes created using a hasher from Python ``hashlib``.

        Returns:
            [KsiSignature]: list of ``KsiSignature`` instances

        Raises:
            ksi.Error: or its subclass on KSI errors
            ksi.AsyncServiceError: when this function is called, but block signing
                                   is not allowed
        """
        data_hash_names = [data_hash.name for data_hash in data_hashes]
        data_hash_digests = [data_hash.digest() for data_hash in data_hashes]
        request_id = self.async_service.new_block_request(data_hash_names, data_hash_digests)
        while True:
            if self.async_service.is_pending(request_id):
                self.async_service.run_service(request_id)
            else:
                sig_binaries = self.async_service.get_response(request_id)
                return [KsiSignature(self, binary) for binary in sig_binaries]

    def sign_blob(self, blob):
        """ Signs a data blob.

        Note:
            In case of gevent use (function run by spawned greenlet):
                Signing is an asynchronous operation.
            Otherwise:
                Signing blocks for 1..2 seconds.

        Args:
            str/buffer: data to be signed.

        Returns:
            KsiSignature: see ``KsiSignature`` class in this module.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        h = hashlib.sha256(blob)
        return self.sign_hash(h)

    def new_signature_object(self, blob):
        """ Instantiates a KsiSignature object from earlier serialized binary representation.

        Args:
            str/buffer: binary representation of signature data.

        Returns:
            KsiSignature: A newly instantiated ``KsiSignature`` object.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        _ksi.ksi_verify_sig(self._ctx, blob)
        return KsiSignature(self, blob)

    def extend(self, sig):
        """ Extend the signature to the latest available publication.

        Modifies the signature in-place. Extender sever must be specified earlier.
        Possible, if there is at least 1 publication created after signing, i.e.
        quite safe to try if 35 days have passed from signing.

        Extending a signature is very useful before long-term archiving. This makes
        distant-future verification possible without access to extender service.

        Args:
            KsiSignature:

        Returns:
            `True` if extending was successful, `False` if no suitable publication was found.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        success, ext = _ksi.ksi_extend(self._ctx, sig.get_binary())
        if success:
            sig.set_binary(ext)
        return success

    def verify(self, sig):
        """ Verify signature consistency. No document content check.

        No return value.

        Raises:
            ksi.Error: or its subclass on KSI errors
        """
        return _ksi.ksi_verify_sig(self._ctx, sig.get_binary())

    def set_verification_policy(self, new_policy):
        """ Specify a verification policy for future verifications.

            Note that it is hard to fail with the default one.
            Change only if necessary. Suffix ``_EXT`` instructs verification
            to transparently extend the signature if possible.

        Args:
            policy_id: A property from the KSI object::

               KSI.verification.POLICY_GENERAL
               KSI.verification.POLICY_GENERAL_EXT
               KSI.verification.POLICY_KEY_BASED
               KSI.verification.POLICY_CALENDAR_BASED
               KSI.verification.POLICY_PUBLICATIONS_FILE_BASED
               KSI.verification.POLICY_PUBLICATIONS_FILE_BASED_EXT

        """
        self.__policy = new_policy

    def get_verification_policy(self):
        """ Retrieves the current verification policy.

        Returns:
            int: Identifier. see ``set_verification_policy()`` for a list of values.
        """
        return self.__policy

    def verify_hash(self, sig, data_hash):
        """ Verify a signature and a provided data hash of signed data.

        Args:
            KsiSignature: Signature object.
            data_hash: A hasher from ``hashlib``, after processing its input data.

        Returns:
            (result (boolean), code (str), reason (str)): A 3-tuple with following data:
                True if signature is OK; False if there is conslusive evidence that signature
                is invalid and further action can not change the situation.
                Code: error code as string.
                See https://github.com/guardtime/libksi/blob/v3.16.2482/src/ksi/policy.h#L70.
                Reason: Human readable message.

        Raises:
            ValueError: Final decision is not possible given current input data. Changing something,
                e.g. verification policy, might help to find a conclusive answer.

            ksi.Error: or its subclass on KSI errors
        """
        return _ksi.ksi_verify_hash_with_policy(self._ctx, sig.get_binary(),
                                                data_hash.name, data_hash.digest(), self.__policy)

    def verify_blob(self, sig, blob):
        """ Verify a data blob and its signature.

        Args:
            KsiSignature: Signature object.
            blob: A string or buffer containing binary data bytes.

        Returns:
            (result (boolean), code (str), reason (str)): A 3-tuple with following data:
                True if signature is OK; False if there is conslusive evidence that signature
                is invalid and further action can not change the situation.
                Code: error code as string.
                See https://github.com/guardtime/libksi/blob/v3.16.2482/src/ksi/policy.h#L70.
                Reason: Human readable message.

        Raises:
            ValueError: Final decision is not possible given current input data. Changing something,
                e.g. verification policy, might help to find a conclusive answer.

            ksi.Error: or its subclass on KSI errors
        """
        hasher = sig.get_hasher()
        hasher.update(blob)
        return _ksi.ksi_verify_hash_with_policy(self._ctx, sig.get_binary(),
                                                hasher.name, hasher.digest(), self.__policy)

    def get_async_config(self):
        """ Get the current async configuration.

        The maximum aggregator request count (from ``KSI.get_async_config``) is the
        maximum number of requests the server is willing to respond to per round. Setting a
        ``max_req_count`` significantly larger than that will most probably cause failures and
        the async service to unnecessarily resend often failing requests in cache.

        See ``set_async_config()``

        Returns:
            dict: {"max_req_count": (int), "max_pending_count": (int), "max_aggregator_req_count": (int)}
        """
        return self.async_service.get_config()

    def set_async_config(self, config):
        """ Set the async configuration.

        Note ``max_pending_count`` cannot be assigned a smaller value than previously set.
        Setting it significantly higher will cause request timeouts (meaning a high rate of
        request resending) and possibly ``AsyncServiceError`` instances.

        Note that if ``max_pending_count`` is reached then new requests will be cached in a queue
        until the number of pending requests becomes smaller. The user is responsible for memory
        safety of the queued requests, possibly using gevent.pool with a max size of
        ``max_pending_count`` + queue max size (depending on the amount of memory the program
        should have access to).

        Note:
            The asynchronous service maximum request count is initially capped at 250 responses
            per round (one round lasts for 1 second) and maximum pending count at 500. Even if the
            maximum pending count is allowed to be set higher, network errors may occur, as the
            host may not be able to send/receive all requests on time, depending on the host's
            NIC, CPU, etc.

        Args:
            dict: {'max_req_count': (int), 'max_pending_count': (int)}

        Raises:
            ValueError: when input contains invalid values or if 'max_pending_count' is smaller
                        than previously set
            TypeError:  when input contains invalid keys
        """
        self.async_service.set_config(**config)

    def get_async_state(self):
        """ Get the async state.

            See ``KsiAsync.get_state()``
        """
        return self.async_service.get_state()


def ksi_env():
    """ Helper for initializing a KSI class with KSI service parameters from the environment.

    System environment parameters should look like:
        Required:
            KSI_AGGREGATOR='url=http://url user=name pass=xyz'
            KSI_EXTENDER='url=http://url user=name pass=xyz'
        Required if using Guardtime commerical KSI service:
            KSI_PUBFILE='http://verify.guardtime.com/ksi-publications.bin'
            KSI_PUBFILE_CNSTR='{"email" : "publications@guardtime.com"}'

    Example:
        ``KSI = ksi.KSI(**ksi.ksi_env())``

    Raises:
        ksi.FormatError: when an environment variable misses required component.
    """

    def __parse_value(value):
        struct = {}
        for thing in value.split():
            key, val = thing.split('=')
            struct[key] = val
        if 'url' not in struct:
            raise FormatError('KSI service parameter misses required component "url"')
        if 'user' not in struct:
            raise FormatError('KSI service parameter misses required field "user"')
        if 'pass' not in struct:
            raise FormatError('KSI service parameter misses required field "pass"')

        return struct

    ret = {}
    if 'KSI_AGGREGATOR' in os.environ:
        ret['signing_service'] = __parse_value(os.environ['KSI_AGGREGATOR'])
    else:
        raise FormatError('Environment parameter "KSI_AGGREGATOR" is not set')
    if 'KSI_EXTENDER' in os.environ:
        ret['extending_service'] = __parse_value(os.environ['KSI_EXTENDER'])
    else:
        raise FormatError('Environment parameter "KSI_EXTENDER" is not set')
    if 'KSI_PUBFILE' in os.environ:
        ret['publications_file'] = os.environ['KSI_PUBFILE']
    if 'KSI_PUBFILE_CNSTR' in os.environ:
        ret['publications_cnstr'] = os.environ['KSI_PUBFILE_CNSTR']

    return ret


# Note: following exceptions are expected to be here by _ksi.c. Throws RuntimeError if not found
class Error(Exception):
    """ Unspecfied KSI error """
    pass

class ConfigurationError(Error):
    """ Necessary parameters are not configured """
    pass

class FormatError(Error):
    """ Invalid argument, format, or parameter. Untrusted or unavailable hash algorithm. """
    pass

class InvalidSignatureError(Error):
    """
         * Invalid KSI signature.
         * Invalid PKI signature.
         * The PKI signature is not trusted by the API.
         * The objects used are in an invalid state.
    """
    pass

class HashError(Error):
    """
         * Unknown hash algorithm.
         * Untrusted hash algorithm.
    """
    pass

class AsyncServiceError(Error):
    """
        * Request max retry count reached.
        * HTTP error (possibly caused by requesting significantly more responses than the
          aggregator can handle, see ``KSI.set_async_config()``).
        * Network error (possibly caused by sening too many requests and receiving timeout
          errors, see ``KSI.set_async_config()``).
        * Async service request cache full.
        * Async connection was closed.
        * Async service has not finished.
        * Request timeout (possibly caused by too many pending requests or initializing a
          synchronous sign requests on top of a full request queue).
        * If ``KSI.sign_hash_list`` is called, but block signing is not allowed.
    """
    pass

class NetworkError(Error):
    """
         * A network error occurred.
         * A network connection timeout occurred.
         * A network send timeout occurred.
         * A network receive timeout occurred.
         * A HTTP error occurred.
    """
    pass

class PublicationError(Error):
    """  Problems with publication based verification.

         * The extender returned a wrong calendar chain.
         * No suitable publication to extend to.
         * The publication in the signature was not found in the publications file.
         * Invalid publication.
         * The publications file is not signed.
    """
    pass

class CryptoError(Error):
    """
         * Cryptographic operation could not be performed. Likely causes are
           unsupported cryptographic algorithms, invalid keys and lack of
           resources.
    """
    pass

class ServiceAuthError(Error):
    """
         * The request could not be authenticated (missing or unknown login
           identifier, MAC check failure, etc).
    """
    pass

class ServiceError(Error):
    """ Various KSI service related errors.

        * The request is still pending.
        * The request ID in response does not match with request ID in request.
        * Pattern for errors with client request.
        * The request contained invalid payload (unknown payload type, missing
          mandatory elements, unknown critical elements, etc).
        * The server encountered an unspecified internal error.
        * The server encountered unspecified critical errors connecting to
          upstream servers.
        * No response from upstream aggregators.
        * The extender returned an error.
        * The request indicated client-side aggregation tree larger than allowed
          for the client (retrying would not succeed either).
        * The request combined with other requests from the same client in the same
          round would create an aggregation sub-tree larger than allowed for the client
          (retrying in a later round could succeed).
        * Too many requests from the client in the same round (retrying in a later
          round could succeed)
        * Input hash value in the client request is longer than the server allows.
        * Received PDU v2 response to PDU v1 request. Configure the SDK to use PDU
          v2 format for the given aggregator.
        * Received PDU v1 response to PDU v2 request. Configure the SDK to use PDU
          v1 format for the given aggregator.
    """
    pass

class ServiceExtenderBlockchainError(ServiceError):
    """ The Extender server does not have required period of Calendar Blockchain.

        * The request asked for a hash chain going backwards in time
        * Pattern for local errors in the server.
        * The server misses the internal database needed to service the request
          (most likely it has not been initialized yet).
        * The server's internal database is in an inconsistent state.
        * The request asked for hash values older than the oldest round in the
          server's database.
        * The request asked for hash values newer than the newest round in the
          server's database.
    """
