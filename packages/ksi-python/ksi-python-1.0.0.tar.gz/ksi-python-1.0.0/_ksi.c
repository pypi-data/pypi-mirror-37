/*
 * Copyright 2015-2018 Guardtime, Inc.
 *
 * This file is part of the Guardtime client SDK.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *     http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES, CONDITIONS, OR OTHER LICENSES OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 * "Guardtime" and "KSI" are trademarks or registered trademarks of
 * Guardtime, Inc., and no license to trademarks is granted; Guardtime
 * reserves and retains all trademark rights.
 */

#include <Python.h>
#include <ksi/ksi.h>
#include <ksi/net_async.h>
#include <ksi/net_uri.h>
#include <ksi/signature_builder.h>
#include <ksi/tree_builder.h>


#define Py_LIMITED_API

// backward compatibility for format string: blob as string or bytes
#if PY_MAJOR_VERSION >= 3
    #define _SoB_ "y#"
    #define string_from_object(py_obj) PyBytes_AsString(PyUnicode_AsUTF8String(py_obj))
#else
    #define _SoB_ "s#"
    #define string_from_object(py_obj) PyString_AsString(py_obj)
#endif

// Some verification policies.
#define POLICY_EXTEND   (1<<6)
#define POLICY_KEY_BASED 1
#define POLICY_CALENDAR_BASED 2
#define POLICY_PUBLICATIONS_FILE_BASED 3
#define POLICY_PUBLICATIONS_FILE_BASED_EXT (POLICY_PUBLICATIONS_FILE_BASED | POLICY_EXTEND)
#define POLICY_GENERAL 4
#define POLICY_GENERAL_EXT (POLICY_GENERAL | POLICY_EXTEND)

PyObject *import_exception(char* name) {
    PyObject *module, *result = NULL;

    module = PyImport_ImportModule("ksi");
    if (module) {
        result = PyDict_GetItemString(PyModule_GetDict(module), name);
    }
    if (!result) {
        result = PyExc_RuntimeError;
        // note that this error will be overwritten
        PyErr_SetString(PyExc_RuntimeError, "Can not find exception in module");
    }
    return result;
}

PyObject *get_exception_obj(int code) {
    switch (code) {
        case KSI_OUT_OF_MEMORY:
            return PyExc_MemoryError;

		case KSI_AGGREGATOR_NOT_CONFIGURED:
		case KSI_EXTENDER_NOT_CONFIGURED:
		case KSI_PUBLICATIONS_FILE_NOT_CONFIGURED:
		case KSI_PUBFILE_VERIFICATION_NOT_CONFIGURED:
		case KSI_INVALID_VERIFICATION_INPUT:
            return import_exception("ConfigurationError");

		case KSI_INVALID_ARGUMENT:
		case KSI_INVALID_FORMAT:
		case KSI_UNTRUSTED_HASH_ALGORITHM:
		case KSI_UNAVAILABLE_HASH_ALGORITHM:
            return import_exception("FormatError");

		case KSI_INVALID_SIGNATURE:
		case KSI_INVALID_PKI_SIGNATURE:
		case KSI_PKI_CERTIFICATE_NOT_TRUSTED:
		case KSI_INVALID_STATE:
            return import_exception("InvalidSignatureError");

		case KSI_IO_ERROR:
            return PyExc_IOError;

        case KSI_NETWORK_ERROR:
        case KSI_NETWORK_CONNECTION_TIMEOUT:
        case KSI_NETWORK_SEND_TIMEOUT:
        case KSI_NETWORK_RECIEVE_TIMEOUT:
        case KSI_HTTP_ERROR:
            return import_exception("NetworkError");

		case KSI_EXTEND_WRONG_CAL_CHAIN:

		case KSI_EXTEND_NO_SUITABLE_PUBLICATION:
		case KSI_VERIFICATION_FAILURE:
		case KSI_INVALID_PUBLICATION:
		case KSI_PUBLICATIONS_FILE_NOT_SIGNED_WITH_PKI:
            return import_exception("PublicationError");

		case KSI_CRYPTO_FAILURE:
            return import_exception("CryptoError");

		case KSI_SERVICE_AUTHENTICATION_FAILURE:
            return import_exception("ServiceAuthError");

		case KSI_REQUEST_PENDING:
		case KSI_HMAC_MISMATCH:
		case KSI_HMAC_ALGORITHM_MISMATCH:
		case KSI_UNSUPPORTED_PDU_VERSION:
		case KSI_SERVICE_INVALID_REQUEST:
		case KSI_SERVICE_INVALID_PAYLOAD:
		case KSI_SERVICE_INTERNAL_ERROR:
		case KSI_SERVICE_UPSTREAM_ERROR:
		case KSI_SERVICE_UPSTREAM_TIMEOUT:
		case KSI_SERVICE_AGGR_REQUEST_TOO_LARGE:
		case KSI_SERVICE_AGGR_REQUEST_OVER_QUOTA:
		case KSI_SERVICE_AGGR_INPUT_TOO_LONG:
		case KSI_SERVICE_AGGR_TOO_MANY_REQUESTS:
		case KSI_SERVICE_AGGR_PDU_V2_RESPONSE_TO_PDU_V1_REQUEST:
		case KSI_SERVICE_AGGR_PDU_V1_RESPONSE_TO_PDU_V2_REQUEST:

		case KSI_SERVICE_EXTENDER_PDU_V2_RESPONSE_TO_PDU_V1_REQUEST:
		case KSI_SERVICE_EXTENDER_PDU_V1_RESPONSE_TO_PDU_V2_REQUEST:
		case KSI_SERVICE_UNKNOWN_ERROR:
            return import_exception("ServiceError");

		case KSI_SERVICE_EXTENDER_INVALID_TIME_RANGE:
		case KSI_SERVICE_EXTENDER_DATABASE_MISSING:
		case KSI_SERVICE_EXTENDER_DATABASE_CORRUPT:
		case KSI_SERVICE_EXTENDER_REQUEST_TIME_TOO_OLD:
		case KSI_SERVICE_EXTENDER_REQUEST_TIME_TOO_NEW:
		case KSI_SERVICE_EXTENDER_REQUEST_TIME_IN_FUTURE:
            return import_exception("ServiceExtenderBlockchainError");

        case KSI_ASYNC_NOT_FINISHED:
        case KSI_ASYNC_CONNECTION_CLOSED:
        case KSI_ASYNC_REQUEST_CACHE_FULL:
            return import_exception("AsyncServiceError");

		case KSI_BUFFER_OVERFLOW:
		case KSI_TLV_PAYLOAD_TYPE_MISMATCH:

		case KSI_UNKNOWN_ERROR:
        default:
            return import_exception("Error");
    }
}

static void format_exception(KSI_CTX *ctx, int res, int line) {
    char buf[512];
    PyObject *s;

    if (KSI_ERR_getBaseErrorMessage(ctx, buf, sizeof(buf), NULL, NULL) == KSI_OK) {
        s = PyBytes_FromFormat("L%04d: %s <%s>", line, KSI_getErrorString(res), buf);
    } else {
        s = PyBytes_FromFormat("L%04d: %s", line, KSI_getErrorString(res));
    }
    PyErr_SetObject(get_exception_obj(res), s);
    Py_DECREF(s);
}

#define EH(plah) { int _res = (plah);  \
            if (_res != KSI_OK) { \
                format_exception(ctx, _res, __LINE__); \
                goto cleanup; \
            }};

//  no KSI_CTX available:
#define EHX(plah) { int _res = (plah);  \
            if (_res != KSI_OK) { \
                 PyErr_SetString(PyExc_Exception, KSI_getErrorString(_res)) ; \
                 goto cleanup; \
             }};

 void async_service_capsule_destroy(PyObject *capsule) {
     KSI_AsyncService *as = NULL;
     as = (KSI_AsyncService *) PyCapsule_GetPointer(capsule, "ASYNC_SERVICE");
     KSI_AsyncService_free(as);
 }

 void ctx_capsule_destroy(PyObject *capsule) {
     KSI_CTX *ctx = NULL;
     ctx = (KSI_CTX *) PyCapsule_GetPointer(capsule, "CTX");
     KSI_CTX_free(ctx);
 }

 void tree_builder_capsule_destroy(PyObject *capsule) {
     KSI_TreeBuilder *builder = NULL;
     builder = (KSI_TreeBuilder *) PyCapsule_GetPointer(capsule, "TREE_BUILDER");
     KSI_TreeBuilder_free(builder);
 }

 void tree_handles_capsule_destroy(PyObject *capsule) {
    KSI_LIST(KSI_TreeLeafHandle)  *handle_list = NULL;
    handle_list = (KSI_LIST(KSI_TreeLeafHandle)  *) PyCapsule_GetPointer(capsule, "TREE_HANDLES");
    KSI_TreeLeafHandleList_free(handle_list);
}

static PyObject *
ksi_init(PyObject *self, PyObject *args) {
    const char *surl, *suser, *skey;
    const char *xurl, *xuser, *xkey;
    const char *purl;
    PyObject *cnstr_obj = NULL;

    long len = 0;
    KSI_CertConstraint *pcnstr = NULL;
    Py_ssize_t pos = 0;
    PyObject *key_obj = NULL, *val_obj = NULL;
    int i = 0;
    KSI_CTX *ctx = NULL;

    if (!PyArg_ParseTuple(args, "sssssssO:ksi_init", &surl, &suser, &skey,
                          &xurl, &xuser, &xkey, &purl, &cnstr_obj)) {
        goto cleanup;
    }

    len = (PyDict_Size(cnstr_obj)) + 1;
    pcnstr = calloc(len, sizeof(KSI_CertConstraint));
    if (pcnstr == NULL) {
        goto cleanup;
    }

    while (PyDict_Next(cnstr_obj, &pos, &key_obj, &val_obj)) {
        if (key_obj != NULL && val_obj != NULL) {
            char *tmp_oid = string_from_object(key_obj);

            /* Check if it is an alias string representation of the OID */
            if (strncmp(tmp_oid, "email", 5) == 0) {
                tmp_oid = KSI_CERT_EMAIL;
            } else if (strncmp(tmp_oid, "country", 7) == 0) {
                tmp_oid = KSI_CERT_COUNTRY;
            } else if (strncmp(tmp_oid, "org", 3) == 0) {
                tmp_oid = KSI_CERT_ORGANIZATION;
            } else if (strncmp(tmp_oid, "common_name", 11) == 0) {
                tmp_oid = KSI_CERT_COMMON_NAME;
            }

            pcnstr[i].oid = tmp_oid;
            pcnstr[i].val = string_from_object(val_obj);
        }
        i++;
    }
    pcnstr[i].oid = NULL;
    pcnstr[i].val = NULL;

    EH( KSI_CTX_new(&ctx) );
    EH( KSI_CTX_setAggregator(ctx, surl, suser, skey) );
    EH( KSI_CTX_setExtender(ctx, xurl, xuser, xkey) );
    EH( KSI_CTX_setPublicationUrl(ctx, purl) );
    EH( KSI_CTX_setDefaultPubFileCertConstraints(ctx, pcnstr) );
    free(pcnstr);
    return PyCapsule_New((void*) ctx, "CTX", ctx_capsule_destroy);
cleanup:
    free(pcnstr);
    KSI_CTX_free(ctx);
    return NULL;
}

static PyObject *
ksi_get_aggr_config(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;

    KSI_Config *config = NULL;
    KSI_Integer *max_req_count = NULL;
    KSI_Integer *max_level = NULL;

    if (!PyArg_ParseTuple(args, "O:ksi_get_aggr_config", &ctx_capsule)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_receiveAggregatorConfig(ctx, &config) );
    EHX( KSI_Config_getMaxRequests(config, &max_req_count) );
    EHX( KSI_Config_getMaxLevel(config, &max_level) );
    py_result = Py_BuildValue("KK", KSI_Integer_getUInt64(max_req_count), KSI_Integer_getUInt64(max_level));
cleanup:
    KSI_Config_free(config);
    return py_result;
}

static PyObject *
ksi_set_async_config(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *async_capsule = NULL;
    long int max_req_int = 0;
    long int req_cache_size = 0;

    if (!PyArg_ParseTuple(args, "Oll:ksi_set_async_config", &async_capsule, &max_req_int, &req_cache_size)) {
        goto cleanup;
    }
    KSI_AsyncService *as = (KSI_AsyncService *) PyCapsule_GetPointer(async_capsule, "ASYNC_SERVICE");
    EHX( KSI_AsyncService_setOption(as, KSI_ASYNC_OPT_MAX_REQUEST_COUNT, (void*) max_req_int) );
    EHX( KSI_AsyncService_setOption(as, KSI_ASYNC_OPT_REQUEST_CACHE_SIZE, (void*) req_cache_size) );
    py_result = Py_True;
cleanup:
    return py_result;
}

static PyObject *
ksi_new_async_service(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    const char *surl, *suser, *skey;
    long int max_req_count;
    long int req_cache_size;

    KSI_AsyncService *as;

    if (!PyArg_ParseTuple(args, "Osssll:ksi_new_async_service", &ctx_capsule, &surl, &suser, &skey, &max_req_count, &req_cache_size)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_SigningAsyncService_new(ctx, &as) );
    EHX( KSI_AsyncService_setEndpoint(as, surl, suser, skey) );
    EHX( KSI_AsyncService_setOption(as, KSI_ASYNC_OPT_MAX_REQUEST_COUNT, (void*) max_req_count) );
    EHX( KSI_AsyncService_setOption(as, KSI_ASYNC_OPT_REQUEST_CACHE_SIZE, (void*) req_cache_size) );
    py_result = PyCapsule_New((void*) as, "ASYNC_SERVICE", async_service_capsule_destroy);
cleanup:
    return py_result;
}

static PyObject *
ksi_new_async_sign_request(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *async_capsule = NULL;
    PyObject *ctx_capsule = NULL;
    const char *requestId = NULL;
    const char *hashalgname = NULL;
    const unsigned char *hash_bytes = NULL;
    int hash_len = 0;
    int request_level = 0;

    KSI_AggregationReq *req = NULL;
    int hashalgid = 0;
    KSI_DataHash *hash = NULL;
    KSI_AsyncHandle *reqHandle = NULL;
    KSI_Integer *level = NULL;
    int res = KSI_UNKNOWN_ERROR;

    if (!PyArg_ParseTuple(args, "OOss"_SoB_"i:ksi_new_async_sign_request", &async_capsule, &ctx_capsule,
                          &requestId, &hashalgname, &hash_bytes, &hash_len, &request_level)) {
        goto cleanup;
    }
    KSI_AsyncService *as = (KSI_AsyncService *) PyCapsule_GetPointer(async_capsule, "ASYNC_SERVICE");
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_AggregationReq_new(ctx, &req) );

    hashalgid = KSI_getHashAlgorithmByName(hashalgname);
    if (hashalgid == -1) {
        PyErr_SetString(import_exception("HashError"), "Unknown hash algorithm.");
        goto cleanup;
    } else if (!KSI_isHashAlgorithmTrusted(hashalgid)) {
        PyErr_SetString(import_exception("HashError"), KSI_getErrorString(KSI_UNTRUSTED_HASH_ALGORITHM));
        goto cleanup;
    }
    EH( KSI_DataHash_fromDigest(ctx, hashalgid, hash_bytes, hash_len, &hash) );
    EHX( KSI_AggregationReq_setRequestHash(req, hash) );
    hash = NULL;

    if (request_level > 0) {
        EH( KSI_Integer_new(ctx, (KSI_uint64_t) request_level, &level) );
        EHX( KSI_AggregationReq_setRequestLevel(req, level) );
    }
    EH( KSI_AsyncAggregationHandle_new(ctx, req, &reqHandle) );
    req = NULL;

    EHX( KSI_AsyncHandle_setRequestCtx(reqHandle, (void*) requestId, NULL) );
    res = KSI_AsyncService_addRequest(as, reqHandle);
    switch (res) {
        case KSI_OK:
            Py_INCREF(Py_True);
            py_result = Py_True;
            break;
        case KSI_ASYNC_REQUEST_CACHE_FULL:
            PyErr_SetString(import_exception("AsyncServiceError"), KSI_getErrorString(res));
            break;
        default:
            Py_INCREF(Py_False);
            py_result = Py_False;
            goto cleanup;
        }
cleanup:
    reqHandle = NULL;
    KSI_Integer_free(level);
    KSI_AsyncHandle_free(reqHandle);
    KSI_DataHash_free(hash);
    KSI_AggregationReq_free(req);
    return py_result;
}

static PyObject *
ksi_run_async_service(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *async_capsule = NULL;
    PyObject *block_levels = NULL;

    size_t pending = 0;
    KSI_AsyncService *as = NULL;
    KSI_Signature *sig = NULL;
    KSI_SignatureBuilder *builder = NULL;
    KSI_AsyncHandle *respHandle = NULL;

    if (!PyArg_ParseTuple(args, "OO:ksi_run_async_service", &async_capsule, &block_levels)) {
        goto cleanup;
    }
    as = (KSI_AsyncService *) PyCapsule_GetPointer(async_capsule, "ASYNC_SERVICE");
    EHX( KSI_AsyncService_run(as, &respHandle, &pending) );
    if (respHandle != NULL) {
        char *requestId = "";
        int state = KSI_ASYNC_STATE_UNDEFINED;
        EHX( KSI_AsyncHandle_getState(respHandle, &state) );
        switch (state) {
            case KSI_ASYNC_STATE_RESPONSE_RECEIVED: {
                    KSI_AggregationResp *resp = NULL;
                    unsigned char *serialized = NULL;
                    size_t serialized_len = 0;
                    int level = 0;
                    EHX( KSI_AsyncHandle_getRequestCtx(respHandle, (const void**)&requestId) );
                    if (strstr(requestId, "b_") != NULL) {
                        PyObject * id = Py_BuildValue("s", requestId);
                        PyObject * py_long = PyDict_GetItem(block_levels, id);
                        level = (int) PyLong_AsLong(py_long);
                    }
                    EHX( KSI_AsyncHandle_getAggregationResp(respHandle, &resp) );
                    EHX( KSI_SignatureBuilder_openFromAggregationResp(resp, &builder) );
                    EHX( KSI_SignatureBuilder_close(builder, level, &sig) );
                    EHX( KSI_Signature_serialize(sig, &serialized, &serialized_len) );
                    py_result = Py_BuildValue("{s:"_SoB_"}iO", requestId, serialized, (int) serialized_len, (int) pending, Py_False);
                    KSI_free(serialized);
                }
                break;
            case KSI_ASYNC_STATE_ERROR: {
                    int err = KSI_UNKNOWN_ERROR;
                    long extErr = 0L;

                    EHX( KSI_AsyncHandle_getError(respHandle, &err) );
                    EHX( KSI_AsyncHandle_getExtError(respHandle, &extErr) );
                    EHX( KSI_AsyncHandle_getRequestCtx(respHandle, (const void**)&requestId) );
                    char error_message[256];
                    snprintf(error_message, 256, "Request for '%s' failed with error: [0x%x:%ld] %s  ", requestId, err, extErr, KSI_getErrorString(err));
                    py_result = Py_BuildValue("Oi[s,s]", Py_False, (int) pending, requestId, KSI_getErrorString(err));
                }
                break;
            default:
                break;
        }
    } else {
        py_result = Py_BuildValue("OiO", Py_False, (int) pending, Py_False);
    }
cleanup:
    KSI_AsyncHandle_free(respHandle);
    KSI_Signature_free(sig);
    KSI_SignatureBuilder_free(builder);
    return py_result;
}

static PyObject *
ksi_build_block(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    PyObject *hash_names;
    PyObject *hashes;

    KSI_LIST(KSI_TreeLeafHandle) *handle_list = NULL;
    KSI_TreeBuilder *builder = NULL;
    PyObject *hash_name_object;
    PyObject *hash_object;
    KSI_DataHash *hash = NULL;
    KSI_TreeLeafHandle *handle = NULL;

    if (!PyArg_ParseTuple(args, "OO!O!:ksi_build_block", &ctx_capsule, &PyList_Type, &hash_names, &PyList_Type, &hashes)) {
        goto cleanup;
    }
    int hash_num = PyList_Size(hash_names);
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EHX( KSI_TreeLeafHandleList_new(&handle_list) );
    EH( KSI_TreeBuilder_new(ctx, KSI_getHashAlgorithmByName("default"), &builder) );

    int i;
    for (i = 0; i < hash_num; i++) {
        const char *hashalgname = NULL;
        char *hash_bytes;
        Py_ssize_t hash_len;
        hash_name_object = PyList_GetItem(hash_names, i);
        hash_object = PyList_GetItem(hashes, i);

        if (!PyArg_Parse(hash_name_object, "s", &hashalgname)) {
            goto cleanup;
        }
        PyBytes_AsStringAndSize(hash_object, &hash_bytes, &hash_len);
        int hashalgid = KSI_getHashAlgorithmByName(hashalgname);

        if (hashalgid == -1) {
            PyErr_SetString(import_exception("HashError"), "Unknown hash algorithm.");
            goto cleanup;
        } else if (!KSI_isHashAlgorithmTrusted(hashalgid)) {
            PyErr_SetString(import_exception("HashError"), KSI_getErrorString(KSI_UNTRUSTED_HASH_ALGORITHM));
            goto cleanup;
        }
        EH( KSI_DataHash_fromDigest(ctx, hashalgid,(const unsigned char*) hash_bytes, hash_len, &hash) );
        EHX( KSI_TreeBuilder_addDataHash(builder, hash, 0, &handle) );
        EHX( KSI_TreeLeafHandleList_append(handle_list, handle) );
        KSI_DataHash_free(hash);
        hash = NULL;
        handle = NULL;
    }
    KSI_TreeBuilder_close(builder);
    const unsigned char *digest = NULL;
    size_t digest_len = 0;
    KSI_DataHash_extract(builder->rootNode->hash, &builder->algo, &digest, &digest_len);
    PyObject *tree_builder = PyCapsule_New((void*) builder, "TREE_BUILDER", tree_builder_capsule_destroy);
    PyObject *tree_handles = PyCapsule_New((void*) handle_list, "TREE_HANDLES", tree_handles_capsule_destroy);
    py_result = Py_BuildValue("OO"_SoB_"i", tree_builder, tree_handles, digest, (int) digest_len, (int) builder->rootNode->level);
    Py_DECREF(tree_builder); Py_DECREF(tree_handles);
cleanup:
    builder = NULL;
    KSI_DataHash_free(hash);
    KSI_TreeLeafHandle_free(handle);
    return py_result;
}

static PyObject *
ksi_get_block_signatures(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;
    PyObject *tree_handles = NULL;

    KSI_LIST(KSI_TreeLeafHandle) *handle_list = NULL;
    KSI_Signature *root_sig = NULL;
    KSI_Signature *sig = NULL;
    KSI_AggregationHashChain *aggr = NULL;
    KSI_SignatureBuilder *sig_builder = NULL;
    unsigned char *leaf_serialized = NULL;

    if (!PyArg_ParseTuple(args, "O"_SoB_"O:ksi_get_block_signatures", &ctx_capsule, &serialized, &serialized_len, &tree_handles)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    handle_list = (KSI_LIST(KSI_TreeLeafHandle) *) PyCapsule_GetPointer(tree_handles, "TREE_HANDLES");
    int handles_len = KSI_TreeLeafHandleList_length(handle_list);
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &root_sig) );
    py_result = PyList_New((Py_ssize_t) handles_len);

    int i;
    for (i = 0; i < handles_len; i++) {
        sig = NULL;
        KSI_TreeLeafHandle *handle = NULL;
        size_t leaf_serialized_len = 0;
        EHX( KSI_TreeLeafHandleList_elementAt(handle_list, i, &handle) );
        EHX( KSI_TreeLeafHandle_getAggregationChain(handle, &aggr) );
        EHX( KSI_SignatureBuilder_openFromSignature(root_sig, &sig_builder) );
        EHX( KSI_SignatureBuilder_appendAggregationChain(sig_builder, aggr) );
        EHX( KSI_SignatureBuilder_close(sig_builder, 0, &sig) );
        EHX( KSI_Signature_serialize(sig, &leaf_serialized, &leaf_serialized_len) );
        PyList_SET_ITEM(py_result, i, Py_BuildValue(_SoB_, leaf_serialized, (int)leaf_serialized_len));
        KSI_SignatureBuilder_free(sig_builder); sig_builder = NULL;
        KSI_AggregationHashChain_free(aggr); aggr = NULL;
        KSI_Signature_free(sig); sig = NULL;
        KSI_free(leaf_serialized); leaf_serialized = NULL;
    }
cleanup:
    KSI_SignatureBuilder_free(sig_builder);
    KSI_AggregationHashChain_free(aggr);
    KSI_Signature_free(root_sig);
    KSI_Signature_free(sig);
    KSI_free(leaf_serialized);
    return py_result;
}

// TODO: consider integrating with other verification functions
static PyObject *
ksi_verify_sig(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_verify_sig", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    EH( KSI_verifySignature(ctx, sig) );
    py_result = Py_BuildValue("");
cleanup:
    KSI_Signature_free(sig);
    return py_result;
}

// TODO: consider removing later.
static PyObject *
ksi_verify_hash(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;
    const char *hashalgname = NULL;
    const unsigned char *hash_bytes = NULL;
    int hash_len = 0;

    KSI_Signature *sig = NULL;
    int hashalgid = 0;
    KSI_DataHash *hash = NULL;
    int ret = KSI_OK;

    if (!PyArg_ParseTuple(args, "O"_SoB_"s"_SoB_":ksi_verify_hash", &ctx_capsule, &serialized, &serialized_len, &hashalgname, &hash_bytes, &hash_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    hashalgid = KSI_getHashAlgorithmByName(hashalgname);
    if (hashalgid == -1) {
        PyErr_SetString(PyExc_Exception, "Unknown hash algorithm");
        goto cleanup;
    }
    EH( KSI_DataHash_fromDigest(ctx, hashalgid, hash_bytes, hash_len, &hash) );
    ret = KSI_verifyDataHash(ctx, sig, hash);
    switch(ret) {
        case KSI_OK:
            Py_INCREF(Py_True);
            py_result = Py_True;
            break;
        case KSI_VERIFICATION_FAILURE:
            Py_INCREF(Py_False);
            py_result = Py_False;
            break;
        default:
            EH( ret );
            break;
    }
cleanup:
    KSI_DataHash_free(hash);
    KSI_Signature_free(sig);
    return py_result;
}

static PyObject *
ksi_verify_hash_with_policy(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;
    const char *hashalgname = NULL;
    const unsigned char *hash_bytes = NULL;
    int hash_len = 0;
    int policy_int;

    const KSI_Policy *policy;
    int hashalgid = 0;
    KSI_DataHash *hash = NULL;
    KSI_VerificationContext context;
    KSI_Signature *sig = NULL;
    KSI_PolicyVerificationResult *result = NULL;
    PyObject *s;

    if (!PyArg_ParseTuple(args, "O"_SoB_"s"_SoB_"i:ksi_verify_hash_with_policy",
                              &ctx_capsule, &serialized, &serialized_len, &hashalgname,
                              &hash_bytes, &hash_len, &policy_int)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");

    switch(policy_int) {
        case POLICY_KEY_BASED:
            policy = KSI_VERIFICATION_POLICY_KEY_BASED;
            break;
        case POLICY_CALENDAR_BASED:
            policy = KSI_VERIFICATION_POLICY_CALENDAR_BASED;
            break;
        case POLICY_PUBLICATIONS_FILE_BASED:
        case POLICY_PUBLICATIONS_FILE_BASED_EXT:
            policy = KSI_VERIFICATION_POLICY_PUBLICATIONS_FILE_BASED;
            break;
        case POLICY_GENERAL:
        case POLICY_GENERAL_EXT:
            policy = KSI_VERIFICATION_POLICY_GENERAL;
            break;
        default:
            PyErr_SetString(PyExc_Exception, "Unsupported verification policy requested");
            goto cleanup;
    }

    hashalgid = KSI_getHashAlgorithmByName(hashalgname);
    if (hashalgid == -1) {
        PyErr_SetString(PyExc_Exception, "Unknown hash algorithm");
        goto cleanup;
    }
    EH( KSI_DataHash_fromDigest(ctx, hashalgid, hash_bytes, hash_len, &hash) );
    EH( KSI_VerificationContext_init(&context, ctx) );
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    context.signature = sig;
    context.documentHash = hash;
    context.extendingAllowed = (policy_int & POLICY_EXTEND) == POLICY_EXTEND;
    EH( KSI_SignatureVerifier_verify(policy, &context, &result) );

    switch(result->finalResult.resultCode) {
        case KSI_VER_RES_OK:     // ok, return true
            py_result = Py_BuildValue("(Oss)", Py_True, "OK", "OK");
            break;
        case KSI_VER_RES_FAIL:   // broken, return false.
            py_result = Py_BuildValue("(Oss)", Py_False,
                   KSI_VerificationErrorCode_toString(result->finalResult.errorCode),
                   KSI_Policy_getErrorString(result->finalResult.errorCode));
            break;
        case KSI_VER_RES_NA:     // no definitive answer.
        default:                 // Should not happen
            s = PyBytes_FromFormat("%s. Stopped at rule: %s",
                          KSI_Policy_getErrorString(result->finalResult.errorCode), result->finalResult.ruleName);
            PyErr_SetObject(PyExc_ValueError, s);
            Py_DECREF(s);
            goto cleanup;

    }

cleanup:
    KSI_VerificationContext_clean(&context);
    KSI_PolicyVerificationResult_free(result);
    KSI_DataHash_free(hash);
    KSI_Signature_free(sig);
    return py_result;
}

static PyObject *
ksi_get_hash_algorithm(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;
    KSI_HashAlgorithm alg_id;

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_get_hash_algorithm", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    EHX( KSI_Signature_getHashAlgorithm(sig, &alg_id) );
    const char * alg_name = KSI_getHashAlgorithmName(alg_id);
    if (alg_name == NULL) {
        PyErr_SetString(PyExc_Exception, "Unknown hash algorithm");
        goto cleanup;
    }
    py_result = Py_BuildValue("s", alg_name);
cleanup:
    KSI_Signature_free(sig);
    return py_result;
}

static PyObject *
ksi_get_data_hash(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;
    KSI_DataHash *dh = NULL;
    KSI_HashAlgorithm alg_id; // TODO: backward compatibility
    const unsigned char *digest;
    size_t digest_len;

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_get_data_hash", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    EHX( KSI_Signature_getDocumentHash(sig, &dh) );
    EHX( KSI_DataHash_extract(dh, &alg_id, &digest, &digest_len) );

    py_result = Py_BuildValue("(s:"_SoB_")",
                  KSI_getHashAlgorithmName(alg_id),
                  digest, digest_len);

cleanup:
    KSI_Signature_free(sig);
    return py_result;
}

static PyObject *
ksi_get_signing_time(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;
    KSI_Integer *sigTime = NULL;

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_get_signing_time", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    EHX( KSI_Signature_getSigningTime(sig, &sigTime) );
    py_result = PyLong_FromUnsignedLongLong(KSI_Integer_getUInt64(sigTime));
cleanup:
    // DO NOT FREE! KSI_Integer_free(sigTime);
    KSI_Signature_free(sig);
    return py_result;
}

static PyObject *
ksi_get_signer_id(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;
    KSI_HashChainLinkIdentityList *il = NULL;
    char id[512];

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_get_signer_id", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    EHX( KSI_Signature_getAggregationHashChainIdentity(sig, &il) );
    EHX( il == NULL ? KSI_INVALID_FORMAT : KSI_OK );
    size_t k;
    id[0] = '\0';
    for (k = 0; k < KSI_HashChainLinkIdentityList_length(il); k++) {
        size_t len = 0;
        KSI_HashChainLinkIdentity *identity = NULL;
        KSI_Utf8String *clientId = NULL;
        EHX( KSI_HashChainLinkIdentityList_elementAt(il, k, &identity));
        EHX( identity == NULL ? KSI_INVALID_FORMAT : KSI_OK );
        EHX( KSI_HashChainLinkIdentity_getClientId(identity, &clientId));
        EHX( identity == NULL ? KSI_INVALID_FORMAT : KSI_OK );
        len = strlen(id);
        snprintf(&id[len], sizeof(id) - len, "%s%s", (k > 0 ? " :: " : ""), KSI_Utf8String_cstr(clientId));
    }

    py_result = Py_BuildValue("s", id);
cleanup:
    KSI_HashChainLinkIdentityList_free(il);
    KSI_Signature_free(sig);
    return py_result;
}

static PyObject *
ksi_is_extended(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;
    KSI_PublicationRecord *pubrec = NULL;

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_is_extended", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    EHX( KSI_Signature_getPublicationRecord(sig, &pubrec) );
    if (pubrec != NULL) {
        Py_INCREF(Py_True);
        py_result = Py_True;
    } else {
        Py_INCREF(Py_False);
        py_result = Py_False;
    }
cleanup:
    KSI_Signature_free(sig);
    return py_result;
}

// extend signature token, return (true, extendedsig) if ok,
//     false if not yet possible, exc on error
static PyObject *
ksi_extend(PyObject *self, PyObject *args) {
    PyObject *py_result = NULL;
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;
    KSI_Signature *ext = NULL;
    unsigned char *serialized_ext = NULL;
    size_t serialized_ext_len = 0;

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_extend", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );

    int ret = KSI_extendSignature(ctx, sig, &ext);
    switch(ret) {
        case KSI_OK:
            EHX( KSI_Signature_serialize(ext, &serialized_ext, &serialized_ext_len) );
            py_result = Py_BuildValue("O"_SoB_"", Py_True, serialized_ext, (int) serialized_ext_len);
            break;
        case KSI_EXTEND_NO_SUITABLE_PUBLICATION:
            py_result = Py_BuildValue("O"_SoB_"", Py_False, serialized, (int) serialized_len);
            break;
        default:
            EH( ret );
            break;
    }
cleanup:
    KSI_Signature_free(sig);
    KSI_Signature_free(ext);
    KSI_free(serialized_ext);
    return py_result;
}

static PyObject *
ksi_get_publication_data(PyObject *self, PyObject *args) {
    PyObject *py_result = PyDict_New();
    PyObject *ctx_capsule = NULL;
    unsigned char *serialized = NULL;
    size_t serialized_len = 0;

    KSI_Signature *sig = NULL;
    KSI_PublicationRecord *pubrec = NULL;
    KSI_PublicationData *pubdata = NULL;
    char *pubstr = NULL;
    KSI_Integer *pubtime = NULL;
    PyObject *py_pubtime = NULL;
    KSI_LIST(KSI_Utf8String) *pubrefs = NULL;
    PyObject* py_pubref_list = NULL;
    size_t i;

    if (!PyArg_ParseTuple(args, "O"_SoB_":ksi_get_publication_data", &ctx_capsule, &serialized, &serialized_len)) {
        goto cleanup;
    }
    KSI_CTX *ctx = (KSI_CTX *) PyCapsule_GetPointer(ctx_capsule, "CTX");
    EH( KSI_Signature_parse(ctx, serialized, serialized_len, &sig) );
    EHX( KSI_Signature_getPublicationRecord(sig, &pubrec) );
    if (pubrec == NULL) {  // not extended / no pub. record
        py_result = Py_None;
        Py_INCREF(Py_None);
        goto cleanup;
    }
    EHX( KSI_PublicationRecord_getPublishedData(pubrec, &pubdata) );
    EHX( KSI_PublicationData_toBase32(pubdata, &pubstr) );
    EHX( KSI_PublicationData_getTime(pubdata, &pubtime) );

    py_pubtime = PyLong_FromUnsignedLongLong(KSI_Integer_getUInt64(pubtime));
    if (py_pubtime == NULL) {
        PyErr_SetString(PyExc_Exception, "PyLong_FromUnsignedLongLong() failed");
        goto cleanup;
    }
    EHX( KSI_PublicationRecord_getPublicationRefList(pubrec, &pubrefs) );
    if (pubrefs != NULL) {
        py_pubref_list = PyList_New(KSI_Utf8StringList_length(pubrefs));
        for (i = 0; i < KSI_Utf8StringList_length(pubrefs); i++) {
            KSI_Utf8String *ref = NULL;
            EHX( KSI_Utf8StringList_elementAt(pubrefs, i, &ref) );
            PyList_SET_ITEM(py_pubref_list, i, PyUnicode_FromString(KSI_Utf8String_cstr(ref)));
        }
    }

    py_result = Py_BuildValue("{s:s,s:O,s:O}",
                  "publication", pubstr,
                  "publishing_time_t", py_pubtime,
                  "refs", py_pubref_list
                  );
cleanup:
    KSI_Signature_free(sig);
    KSI_free(pubstr);
    return py_result;
}


static PyMethodDef _KSIMethods[] = {
     {"ksi_init", ksi_init, METH_VARARGS, "Initialize KSI context."},
     {"ksi_get_aggr_config", ksi_get_aggr_config, METH_VARARGS, "Return aggregation server max request number for given context"},
     {"ksi_set_async_config", ksi_set_async_config, METH_VARARGS, "Set asynchronous signing service max request number and max request cache size"},
     {"ksi_new_async_service", ksi_new_async_service, METH_VARARGS, "Create a new asynchronous signing service"},
     {"ksi_new_async_sign_request", ksi_new_async_sign_request, METH_VARARGS, "Add a request to the asynchronous signing service"},
     {"ksi_run_async_service", ksi_run_async_service, METH_VARARGS, "Return signature if a signing response has been received"},
     {"ksi_build_block", ksi_build_block, METH_VARARGS, "Build a hash tree from given hashes"},
     {"ksi_get_block_signatures", ksi_get_block_signatures, METH_VARARGS, "Get all leaf signatures from a hash tree whose root has been signed"},
     {"ksi_verify_sig", ksi_verify_sig, METH_VARARGS, "Verify signature. Exception on any problems"},
     {"ksi_verify_hash", ksi_verify_hash, METH_VARARGS, "Check signature validity. Exception if unable."},
     {"ksi_verify_hash_with_policy", ksi_verify_hash_with_policy, METH_VARARGS, "Check signature validity. Exception if unable."},
     {"ksi_get_hash_algorithm", ksi_get_hash_algorithm, METH_VARARGS, "Get hash algorithm name."},
     {"ksi_get_data_hash", ksi_get_data_hash, METH_VARARGS, "Extract signed data hash from signature."},
     {"ksi_get_signing_time", ksi_get_signing_time, METH_VARARGS, "Get signing time."},
     {"ksi_get_signer_id", ksi_get_signer_id, METH_VARARGS, "Get signer's identity."},
     {"ksi_is_extended", ksi_is_extended, METH_VARARGS, "Check if signature token is extended."},
     {"ksi_extend", ksi_extend, METH_VARARGS, "Create an extended signature if possible."},
     {"ksi_get_publication_data", ksi_get_publication_data, METH_VARARGS, "Return publication properties from extended signature."},
     {NULL, NULL, 0, NULL}
};

PyObject *add_structs(PyObject *m) {
    // todo: namespace
    PyModule_AddIntMacro(m, POLICY_KEY_BASED);
    PyModule_AddIntMacro(m, POLICY_CALENDAR_BASED);
    PyModule_AddIntMacro(m, POLICY_PUBLICATIONS_FILE_BASED);
    PyModule_AddIntMacro(m, POLICY_PUBLICATIONS_FILE_BASED_EXT);
    PyModule_AddIntMacro(m, POLICY_GENERAL);
    PyModule_AddIntMacro(m, POLICY_GENERAL_EXT);

    return m;
}

#if PY_MAJOR_VERSION >= 3
    static struct PyModuleDef moduledef = {
            PyModuleDef_HEAD_INIT,
            "_ksi",
            NULL,
            0,
            _KSIMethods,
            NULL, NULL, NULL, NULL
    };

    PyObject *
    PyInit__ksi(void)
    {
        return add_structs(PyModule_Create(&moduledef));
    }

#else  // python 2.x

    PyMODINIT_FUNC init_ksi(void)
    {
        (void) add_structs(Py_InitModule("_ksi", _KSIMethods));
    }

#endif
