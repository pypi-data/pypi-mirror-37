# Copyright 2018 Xaptum, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License

from __future__ import absolute_import
from __future__ import print_function

from xtt._ffi import ffi as _ffi
from xtt._ffi import lib as _lib
from xtt._ffi_utils import to_bytes, to_text, DataStruct

from xtt.exceptions import error_from_code, ReturnCode as RC

__all__ = [
    'create_ecdsap256_key_pair',
    'ECDSAP256PublicKey', 'ECDSAP256PrivateKey'
]

class ECDSAP256PublicKey(DataStruct):
    struct = "xtt_ecdsap256_pub_key"

class ECDSAP256PrivateKey(DataStruct):
    struct = "xtt_ecdsap256_priv_key"

def create_ecdsap256_key_pair():
    """
    Create a new ECDSAP256 key pair.

    :returns: a tuple of the public and private keys
    """
    pub  = ECDSAP256PublicKey()
    priv = ECDSAP256PrivateKey()
    rc = _lib.xtt_crypto_create_ecdsap256_key_pair(pub.native, priv.native)
    if rc == RC.SUCCESS:
        return (pub, priv)
    else:
        raise error_from_code(rc)
