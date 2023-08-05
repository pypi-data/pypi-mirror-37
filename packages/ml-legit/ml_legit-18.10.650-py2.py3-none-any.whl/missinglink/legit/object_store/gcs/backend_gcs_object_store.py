# -*- coding: utf8 -*-
from missinglink.core.api import ApiCaller
from ...backend_mixin import BackendMixin
from .gcs_object_store import GCSObjectStore


class BackendGCSSignedUrlService(BackendMixin):
    def __init__(self, connection, config, session):
        super(BackendGCSSignedUrlService, self).__init__(connection, config, session)

    def get_signed_urls(self, methods, object_names, content_type=None, **kwargs):
        headers = []
        for key in sorted(kwargs.keys()):
            val = kwargs[key]
            headers.append('%s:%s' % (key, val))

        msg = {
            'methods': methods,
            'paths': object_names,
            'headers': headers,
        }

        if content_type:
            msg['content_type'] = content_type

        url = 'data_volumes/{volume_id}/gcs_urls'.format(volume_id=self._volume_id)

        result = ApiCaller.call(self._config, self._session, 'post', url, msg)
        res = {method: result.get(method.lower(), []) for method in methods}

        return res


class BackendGCSObjectStore(BackendMixin, GCSObjectStore):
    def __init__(self, connection, config, session):
        super(BackendGCSObjectStore, self).__init__(connection, config, session)
        self.__bucket_name = None

        self._signed_url_service = BackendGCSSignedUrlService(connection, config, session)

    def __iter__(self):
        return super(BackendGCSObjectStore, self).__iter__()

    def close(self):
        super(BackendGCSObjectStore, self).close()

    @classmethod
    def _group_files_by_meta(cls, objects):
        content_type_grouped = {}
        for obj in objects:
            if obj.content_type not in content_type_grouped:
                content_type_grouped[obj.content_type] = []

            content_type_grouped[obj.content_type].append(obj)

        return content_type_grouped

    def _get_urls_for_paths(self, paths, content_type, headers):
        urls = self._signed_url_service.get_signed_urls(['HEAD', 'PUT'], paths, content_type, **headers)
        head_urls = urls['HEAD']
        put_urls = urls['PUT']
        return head_urls, put_urls

    def _upload_batch_async(self, content_type, files_info, callback):
        content_headers = self.get_content_headers()
        upload_paths = list(map(lambda x: GCSObjectStore._get_shafile_path(x.sha), files_info))
        if self._signed_url_service is not None:
            head_urls, put_urls = self._get_urls_for_paths(upload_paths, content_type, content_headers)
        else:
            put_urls = upload_paths
            head_urls = [None] * len(upload_paths)

        for cur_file, head_url, put_url in zip(files_info, head_urls, put_urls):
            self.upload_async(cur_file, head_url, put_url, callback=callback)

    def add_objects_async(self, objects, callback=None):
        grouped_files = self._group_files_by_meta(objects)
        for content_type in grouped_files:
            grouped_objects = grouped_files[content_type]
            self._upload_batch_async(content_type, grouped_objects, callback)

    @property
    def packs(self):
        return super(BackendGCSObjectStore, self).packs

    def contains_loose(self, sha):
        return super(BackendGCSObjectStore, self).contains_loose(sha)

    def contains_packed(self, sha):
        return super(BackendGCSObjectStore, self).contains_packed(sha)
