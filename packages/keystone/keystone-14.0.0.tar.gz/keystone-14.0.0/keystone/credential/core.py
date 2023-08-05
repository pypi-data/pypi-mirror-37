# Copyright 2013 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

"""Main entry point into the Credential service."""

import json

from keystone.common import driver_hints
from keystone.common import manager
from keystone.common import provider_api
import keystone.conf
from keystone import exception


CONF = keystone.conf.CONF
PROVIDERS = provider_api.ProviderAPIs


class Manager(manager.Manager):
    """Default pivot point for the Credential backend.

    See :mod:`keystone.common.manager.Manager` for more details on how this
    dynamically calls the backend.

    """

    driver_namespace = 'keystone.credential'
    _provides_api = 'credential_api'

    def __init__(self):
        super(Manager, self).__init__(CONF.credential.driver)

    def _decrypt_credential(self, credential):
        """Return a decrypted credential reference."""
        if credential['type'] == 'ec2':
            decrypted_blob = json.loads(
                PROVIDERS.credential_provider_api.decrypt(
                    credential['encrypted_blob'],
                )
            )
        else:
            decrypted_blob = PROVIDERS.credential_provider_api.decrypt(
                credential['encrypted_blob']
            )
        credential['blob'] = decrypted_blob
        credential.pop('key_hash', None)
        credential.pop('encrypted_blob', None)
        return credential

    def _encrypt_credential(self, credential):
        """Return an encrypted credential reference."""
        credential_copy = credential.copy()
        if credential.get('type', None) == 'ec2':
            # NOTE(lbragstad): When dealing with ec2 credentials, it's possible
            # for the `blob` to be a dictionary. Let's make sure we are
            # encrypting a string otherwise encryption will fail.
            encrypted_blob, key_hash = (
                PROVIDERS.credential_provider_api.encrypt(
                    json.dumps(credential['blob'])
                )
            )
        else:
            encrypted_blob, key_hash = (
                PROVIDERS.credential_provider_api.encrypt(
                    credential['blob']
                )
            )
        credential_copy['encrypted_blob'] = encrypted_blob
        credential_copy['key_hash'] = key_hash
        credential_copy.pop('blob', None)
        return credential_copy

    @manager.response_truncated
    def list_credentials(self, hints=None):
        credentials = self.driver.list_credentials(
            hints or driver_hints.Hints()
        )
        for credential in credentials:
            credential = self._decrypt_credential(credential)
        return credentials

    def list_credentials_for_user(self, user_id, type=None):
        """List credentials for a specific user."""
        credentials = self.driver.list_credentials_for_user(user_id, type=type)
        for credential in credentials:
            credential = self._decrypt_credential(credential)
        return credentials

    def get_credential(self, credential_id):
        """Return a credential reference."""
        credential = self.driver.get_credential(credential_id)
        return self._decrypt_credential(credential)

    def create_credential(self, credential_id, credential):
        """Create a credential."""
        credential_copy = self._encrypt_credential(credential)
        ref = self.driver.create_credential(credential_id, credential_copy)
        ref.pop('key_hash', None)
        ref.pop('encrypted_blob', None)
        ref['blob'] = credential['blob']
        return ref

    def _validate_credential_update(self, credential_id, credential):
        # ec2 credentials require a "project_id" to be functional. Before we
        # update, check the case where a non-ec2 credential changes its type
        # to be "ec2", but has no associated "project_id", either in the
        # request or already set in the database
        if (credential.get('type', '').lower() == 'ec2' and
                not credential.get('project_id')):
            existing_cred = self.get_credential(credential_id)
            if not existing_cred['project_id']:
                raise exception.ValidationError(attribute='project_id',
                                                target='credential')

    def update_credential(self, credential_id, credential):
        """Update an existing credential."""
        self._validate_credential_update(credential_id, credential)
        if 'blob' in credential:
            credential_copy = self._encrypt_credential(credential)
        else:
            credential_copy = credential.copy()
            existing_credential = self.get_credential(credential_id)
            existing_blob = existing_credential['blob']
        ref = self.driver.update_credential(credential_id, credential_copy)
        ref.pop('key_hash', None)
        ref.pop('encrypted_blob', None)
        # If the update request contains a `blob` attribute - we should return
        # that in the update response. If not, then we should return the
        # existing `blob` attribute since it wasn't updated.
        if credential.get('blob'):
            ref['blob'] = credential['blob']
        else:
            ref['blob'] = existing_blob
        return ref
