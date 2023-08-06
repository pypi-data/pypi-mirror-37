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

import unittest
import xtt

from pyasn1.codec.der.decoder import decode as der_decode
from pyasn1_modules import rfc5208, rfc5280


class TestASN1(unittest.TestCase):

    def test_x509_from_ecdsap256_key_pair(self):
        pub = xtt.ECDSAP256PublicKey(
            b"""\x04\x7E\x65\x37\x53\x13\x42\xF4\x8A\xC4\x64\x69\x8C\x4C\xD0\x23\xD7\xE4\xD9\x4C\xE5\x0A\x5D\x8B\xCC\x3C\x94\x13\x00\xA3\x48\xF5\x65\xCC\x56\xBF\x77\xC5\x4D\x1C\x7D\xB9\x45\x5D\xF0\x89\x67\x29\x39\xF3\x63\x70\xF2\xB9\x28\x21\x0A\x65\x78\x70\x8B\xE1\xF8\x86\x9A"""
        )
        priv = xtt.ECDSAP256PrivateKey(
            b"""\xE7\xAC\x0C\x71\xD7\xA0\xDF\x86\xD2\x7B\x82\xAC\x0F\x0C\xFC\xD1\xB1\xC0\x91\xB2\xAA\xC0\xE8\xE0\x9D\xC5\x04\x5C\x40\xCD\x28\x36"""
        )
        common_name = xtt.Identity(b'\xfd\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        cert = xtt.x509_from_ecdsap256_key_pair(pub, priv, common_name)

        decoded = der_decode(cert, asn1Spec=rfc5280.Certificate(), decodeOpenTypes=True)[0]
        decoded_common_name = decoded['tbsCertificate']['subject'][0][0][0]['value']['utf8String']
        self.assertEqual(decoded_common_name, "FD000000000000000000000000000000")

    def test_asn1_from_ecdsap256_private_key(self):
        pub = xtt.ECDSAP256PublicKey(
            b"""\x04\x7E\x65\x37\x53\x13\x42\xF4\x8A\xC4\x64\x69\x8C\x4C\xD0\x23\xD7\xE4\xD9\x4C\xE5\x0A\x5D\x8B\xCC\x3C\x94\x13\x00\xA3\x48\xF5\x65\xCC\x56\xBF\x77\xC5\x4D\x1C\x7D\xB9\x45\x5D\xF0\x89\x67\x29\x39\xF3\x63\x70\xF2\xB9\x28\x21\x0A\x65\x78\x70\x8B\xE1\xF8\x86\x9A"""
        )
        priv = xtt.ECDSAP256PrivateKey(
            b"""\xE7\xAC\x0C\x71\xD7\xA0\xDF\x86\xD2\x7B\x82\xAC\x0F\x0C\xFC\xD1\xB1\xC0\x91\xB2\xAA\xC0\xE8\xE0\x9D\xC5\x04\x5C\x40\xCD\x28\x36"""
        )
        asn1 = xtt.asn1_from_ecdsap256_private_key(priv, pub)

        decoded = der_decode(asn1)[0]
        decoded_private_key = decoded['field-1'].asOctets()  # we use the OpenSSL format, which doesn't exactly parse as RFC 5208, but the private key is field-1
        self.assertEqual(decoded_private_key, priv.data[:32])
