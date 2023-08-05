# -*- coding: utf8 -*-
import logging
from collections import OrderedDict

from ...gcp_services import GCPServices
from ...gcs_utils import do_upload, do_delete_all, do_download, s3_moniker
from ...connection_mixin import ConnectionMixin
from ...dulwich.object_store import BaseObjectStore
from ...dulwich.objects import hex_to_filename, Blob


class GCSObjectStore(ConnectionMixin, BaseObjectStore):
    def __init__(self, connection):
        super(GCSObjectStore, self).__init__(connection)
        self.__upload_pool = None
        self._object_store_auth = connection.data_volume_config.object_store_config.get('auth')
        self.__bucket_name = connection.data_volume_config.object_store_config.get('bucket_name')
        self.__embedded = connection.data_volume_config.embedded
        self.__volume_id = self._connection.data_volume_config.volume_id
        self._signed_url_service = None
        self.__multi_process_control = None
        self.__gcp_credentials = None

    def delete_all(self, max_files=None):
        return do_delete_all(self.__bucket_name, self.__volume_id, max_files)

    def set_multi_process_control(self, multi_process_control):
        self.__multi_process_control = multi_process_control

    @classmethod
    def get_content_headers(cls, content_type=None, is_s3=False):

        headers = OrderedDict()
        if content_type:
            headers['Content-Type'] = content_type

        if not is_s3:
            headers['x-goog-acl'] = 'public-read'
            headers['x-goog-if-generation-match'] = '0'

        return headers

    @classmethod
    def _get_shafile_path(cls, sha):
        # Check from object dir
        return hex_to_filename('objects', sha)

    @classmethod
    def on_upload_error(cls, ex):
        raise ex

    def upload_async(self, obj, head_url=None, put_url=None, callback=None):
        args = self._gen_upload_sync_args(obj, head_url, put_url)

        def on_finish(result):
            callback(obj)

        self.__multi_process_control.execute(do_upload, args=args, callback=on_finish if callback else None)

    def _load_gcp_credentials(self, scopes=None, **kwargs):
        if self.__gcp_credentials is None:
            self.__gcp_credentials = GCPServices.gcp_default_credentials(scopes, **kwargs)

        return self.__gcp_credentials

    @property
    def _is_s3_bucket(self):
        return self.__bucket_name and self.__bucket_name.startswith(s3_moniker)

    def _gen_upload_sync_args(self, obj, head_url=None, put_url=None):
        object_name = self._get_shafile_path(obj.sha)

        if self.__bucket_name and not self._is_s3_bucket:
            credentials = self._load_gcp_credentials(['read-write'])
        else:
            credentials = None

        content_type = obj.content_type
        headers = GCSObjectStore.get_content_headers(content_type, self._is_s3_bucket)

        object_name = '%s/%s' % (self.__volume_id, object_name)

        return credentials, self._object_store_auth, self.__bucket_name, object_name, obj.full_path, headers, head_url, put_url,

    def _get_loose_object(self, metadata):
        logging.debug('get object %s', metadata)

        sha = metadata['@id']

        if self.__embedded or self.__bucket_name is not None:
            object_name = '%s/%s' % (self.__volume_id, self._get_shafile_path(sha))
        else:
            object_name = metadata['@url']

        data = do_download(
            self._object_store_auth, self.__bucket_name, object_name, signed_url_service=self._signed_url_service)

        blob = Blob()
        blob.set_raw_chunks([data], sha)
        return blob

    def get_raw(self, metadata):
        """Obtain the raw text for an object.

        :param metadata: metadata for the object.
        :return: tuple with numeric type and object contents.
        """
        ret = self._get_loose_object(metadata)
        if ret is not None:
            return ret.type_num, ret.as_raw_string()

        raise KeyError(metadata)

    @property
    def packs(self):
        raise NotImplementedError(self.packs)

    def __iter__(self):
        raise NotImplementedError(self.__iter__)

    def add_objects_async(self, objects, callback=None):
        for obj in objects:
            self.upload_async(obj, callback=callback)

    def contains_packed(self, sha):
        raise NotImplementedError(self.contains_packed)

    def contains_loose(self, sha):
        raise NotImplementedError(self.contains_loose)
