# -*- coding: utf8 -*-
import logging
import six
from requests import HTTPError
from requests.exceptions import MissingSchema, InvalidSchema
from .gcp_services import GCPServices, GooglePackagesMissing, GoogleAuthError
from missinglink.core.exceptions import NonRetryException, NotFound, AccessDenied
from .path_utils import remove_moniker


class closing_with_condition(object):
    def __init__(self, thing, should_close):
        self.thing = thing
        self.should_close = should_close

    def __enter__(self):
        return self.thing

    def __exit__(self, *exc_info):
        if self.should_close:
            self.thing.close()


class CloudService(object):
    RETRYABLE_ERRORS = (IOError, )
    DEFAULT_MIMETYPE = 'application/octet-stream'
    NUM_RETRIES = 5

    def __init__(self, signed_url_service):
        self.signed_url_service = signed_url_service


class GCSService(CloudService):
    def __init__(self, signed_url_service, credentials=None):
        super(GCSService, self).__init__(signed_url_service)

        self._credentials = credentials


class GCSDownload(GCSService):
    def __init__(self, auth_method, signed_url_service, credentials=None):
        super(GCSDownload, self).__init__(signed_url_service, credentials)
        self._auth_method = auth_method

    def download(self, object_name):
        import requests

        signed_urls = self.signed_url_service.get_signed_urls(['GET'], [object_name])
        url = signed_urls['GET'][0]

        r = requests.get(url)  # allowed to use requests
        r.raise_for_status()
        data = r.content

        logging.debug('downloaded  %s(%s)', object_name, len(data))

        return data


class GCSDownloadDirectDownload(GCSService):
    def __init__(self, credentials=None):
        super(GCSDownloadDirectDownload, self).__init__(None, credentials)

    def download(self, bucket_name, object_name):
        import google.auth.exceptions as google_auth_exceptions

        bucket_name = remove_moniker(bucket_name)

        gcs = GCPServices.gcs_service(self._credentials)

        blob = gcs.bucket(bucket_name).blob(object_name)
        try:
            return blob.download_as_string()
        except google_auth_exceptions.GoogleAuthError:
            raise GoogleAuthError()


def _wrap_s3_call(callback, bucket_name, key):
    from botocore.exceptions import ClientError, BotoCoreError
    import boto3

    bucket_name = remove_moniker(bucket_name)

    s3_client = boto3.client('s3')

    try:
        return callback(s3_client, bucket_name, key)
    except s3_client.exceptions.NoSuchBucket:
        raise NotFound('No such S3 Bucket %s' % bucket_name)
    except BotoCoreError as ex:
        raise NonRetryException('%s (s3://%s/%s)' % (ex, bucket_name, key))
    except ClientError as ex:
        if ex.response.get('Error', {}).get('Code') == 'RequestTimeout':
            raise

        if ex.response.get('Error', {}).get('Code') == 'AccessDenied':
            raise AccessDenied('Access Denied s3://%s/%s' % (bucket_name, key))

        if ex.response.get('Error', {}).get('Code') == 'NoSuchKey':
            raise NotFound('Object not found s3://%s/%s' % (bucket_name, key))

        raise NonRetryException('%s (s3://%s/%s)' % (ex, bucket_name, key))


def _open_file_with_exp(full_path_to_data):
    try:
        return open(full_path_to_data, 'rb')
    except (IOError, OSError):
        raise NonRetryException('failed to open %s' % full_path_to_data)


def _handle_file_object(full_path_to_data, callback_with_file_obj):
    if hasattr(full_path_to_data, 'read'):
        full_path_to_data.seek(0)
        should_close = False
        file_obj = full_path_to_data
    else:
        should_close = True
        file_obj = _open_file_with_exp(full_path_to_data)

    try:
        return callback_with_file_obj(file_obj)
    finally:
        if should_close:
            file_obj.close()


class S3DownloadDirectDownload(CloudService):
    def __init__(self):
        super(S3DownloadDirectDownload, self).__init__(None)

    @classmethod
    def download(cls, bucket_name, object_name):
        def s3_call(_s3_client, s3_bucket_name, s3_object_name):
            import boto3

            s3_resource = boto3.resource('s3')

            obj = s3_resource.Object(s3_bucket_name, s3_object_name)
            return obj.get()['Body'].read()

        return _wrap_s3_call(s3_call, bucket_name, object_name)


class GCSUploadDirect(GCSService):
    def __init__(self, credentials):
        super(GCSUploadDirect, self).__init__(None, credentials=credentials)

    def upload(self, bucket_name, object_name, full_path_to_data, headers):
        logging.info('gcs upload (direct) bucket: %s %s', bucket_name, object_name)

        try:
            import google.api_core.exceptions as google_exceptions
        except ImportError:
            raise GooglePackagesMissing()

        bucket_name = remove_moniker(bucket_name)

        gcs = GCPServices.gcs_service(self._credentials)

        blob = gcs.bucket(bucket_name).blob(object_name)

        content_type = (headers or {}).get('Content-Type')

        def handle_upload(file_obj):
            blob.upload_from_file(file_obj, content_type)

        try:
            _handle_file_object(full_path_to_data, handle_upload)
        except google_exceptions.NotFound:
            raise NotFound('bucket %s not found' % bucket_name)
        except google_exceptions.PermissionDenied:
            raise AccessDenied('access denied to bucket %s' % bucket_name)


class S3UploadDirect(CloudService):
    def __init__(self):
        super(S3UploadDirect, self).__init__(None)

    # noinspection PyUnusedLocal
    @classmethod
    def upload(cls, bucket_name, object_name, full_path_to_data, headers, credentials=None):
        logging.info('s3 upload %s %s %s %s', bucket_name, object_name, full_path_to_data, headers)

        def s3_call(s3_client, s3_bucket_name, s3_object_name):
            _handle_file_object(full_path_to_data, lambda file_obj: s3_client.upload_fileobj(file_obj, s3_bucket_name, s3_object_name))

            logging.info('s3 uploaded %s %s', bucket_name, object_name)

        return _wrap_s3_call(s3_call, bucket_name, object_name)

    @classmethod
    def copy(cls, src, dest):
        logging.info('s3 copy %s => %s', src, dest)

        bucket_name, key = dest.split('/', 1)

        def s3_call(s3_client, s3_bucket_name, s3_key):
            s3_client.copy_object(Bucket=s3_bucket_name, CopySource=src, Key=s3_key)
            logging.info('s3 copied %s => %s', src, dest)

        logging.info('s3 copy %s => %s', src, dest)

        return _wrap_s3_call(s3_call, bucket_name, key)


class FileWithCallback(object):
    def __init__(self, file_obj, callback):
        file_obj.seek(0, 2)
        self._total = file_obj.tell()
        file_obj.seek(0)

        self._callback = callback
        self._file_obj = file_obj

    def __len__(self):
        return self._total

    def read(self, size):
        data = self._file_obj.read(size)
        if not six.PY2 and isinstance(data, six.string_types):
            data = data.encode()

        if six.PY3 and isinstance(data, six.string_types):
            data = data.encode()

        if self._callback is not None:
            self._callback(len(data))

        return data


class GCSUpload(GCSService):
    # upload with auth_method is when uploading from local dev where the secure urls will not work
    # in such case we set the auth to gcloud and it will override the secure url check
    def __init__(self, credentials, auth_method, head_url, put_url):
        super(GCSUpload, self).__init__(None, credentials)
        self._head_url = head_url
        self._put_url = put_url
        self._auth_method = auth_method

    def upload(self, full_path_to_data, headers, progress_callback=None):
        logging.info('gcs upload head: %s put: %s', self._head_url, self._put_url)

        with GCPServices.get_auth_session(self._auth_method, self._credentials) as auth_session:
            resp = None

            if self._head_url:
                logging.debug('try head url')
                resp = auth_session.head(self._head_url)

                logging.debug('try head resp %s', resp)

                if resp.status_code in (204, 404):
                    logging.debug('file not found, uploading')
                    resp = None

            if resp is None:
                def put_file(file_obj):
                    file_obj_with_callback = FileWithCallback(file_obj, progress_callback)

                    logging.debug('put url')
                    put_resp = auth_session.put(self._put_url, data=file_obj_with_callback, headers=headers)
                    logging.debug('put url done %s', put_resp)

                    return put_resp

                resp = _handle_file_object(full_path_to_data, put_file)

            if resp.status_code in (401, 403):
                raise NonRetryException()

            resp.raise_for_status()


class GCSDeleteAll(GCSService):
    def delete_all(self, bucket_name, volume_id, max_files=None):
        try:
            import google.api_core.exceptions as google_exceptions
        except ImportError:
            raise GooglePackagesMissing()

        logging.info('delete all at %s/%s', bucket_name, volume_id)
        gcs = GCPServices.gcs_service(self._credentials)

        try:
            list_iter = gcs.bucket(bucket_name).list_blobs(prefix=str(volume_id))
        except google_exceptions.NotFound:
            logging.warning('bucket %s was not found', bucket_name)
            return

        total_deleted = 0
        for blob in list_iter:
            try:
                gcs.bucket(bucket_name).delete_blob(blob.name)
            except google_exceptions.NotFound:
                pass

            total_deleted += 1

            if max_files is not None and max_files == total_deleted:
                break

        logging .info('total deleted %s', total_deleted)

        return total_deleted


s3_moniker = 's3://'


def __retry_if_retry_possible_error(exception):
    logging.debug('got retry exception (upload/download) (%s, %s)', exception, type(exception))

    return not isinstance(exception, (AssertionError, ValueError, NonRetryException))


def _default_retry():
    from retrying import retry

    def decor(f):
        return retry(retry_on_exception=__retry_if_retry_possible_error, wait_exponential_multiplier=50, wait_exponential_max=5000)(f)

    return decor


class _CloudUploader(object):
    @classmethod
    @_default_retry()
    def with_retry_to_s3(cls, bucket_name, object_name, full_path_to_data, headers):
        bucket_name = remove_moniker(bucket_name)
        S3UploadDirect().upload(bucket_name, object_name, full_path_to_data, headers)

    @classmethod
    @_default_retry()
    def with_retry_transfer_s3(cls, bucket_name, object_name, full_path_to_data):
        full_s3_path = remove_moniker(full_path_to_data)
        object_name_with_bucket = remove_moniker(bucket_name) + '/' + object_name
        S3UploadDirect().copy(full_s3_path, object_name_with_bucket)

    @classmethod
    @_default_retry()
    def with_retry_to_gcs(cls, credentials, auth_method, put_url, head_url, headers, progress_callback, full_path_to_data):
        try:
            GCSUpload(credentials, auth_method, head_url, put_url).upload(full_path_to_data, headers, progress_callback)
        except (MissingSchema, InvalidSchema, MissingSchema):
            logging.exception('Invalid request')
            raise NonRetryException('Invalid request')
        except HTTPError as e:
            if e.response.status_code != 412:  # precondition
                return

            raise

    @classmethod
    @_default_retry()
    def with_retry_to_gcs_direct(cls, credentials, bucket_name, object_name, headers, full_path_to_data):
        credentials = credentials or GCPServices.gcp_default_credentials(scopes=['https://www.googleapis.com/auth/devstorage.read-write'])

        GCSUploadDirect(credentials).upload(bucket_name, object_name, full_path_to_data, headers)


class _S3Upload(object):
    def __init__(self, full_path_to_data, headers):
        self._full_path_to_data = full_path_to_data
        self._headers = headers

    def upload(self, bucket_name, object_name):
        if self._full_path_to_data.startswith(s3_moniker):
            _CloudUploader.with_retry_transfer_s3(bucket_name, object_name, self._full_path_to_data)
            return

        _CloudUploader.with_retry_to_s3(bucket_name, object_name, self._full_path_to_data, self._headers)


class _GCSUpload(object):
    def __init__(self, full_path_to_data, headers):
        self._full_path_to_data = full_path_to_data
        self._headers = headers

    def upload(self, credentials, auth_method, bucket_name, object_name, head_url, put_url, callback):

        if put_url:
            _CloudUploader.with_retry_to_gcs(credentials, auth_method, put_url, head_url, self._headers, callback, self._full_path_to_data)
            return

        _CloudUploader.with_retry_to_gcs_direct(credentials, bucket_name, object_name, self._headers, self._full_path_to_data)


def do_upload(credentials, auth_method, bucket_name, object_name, full_path_to_data, headers, head_url, put_url, callback=None):
    if bucket_name is not None and bucket_name.startswith(s3_moniker):
        _S3Upload(full_path_to_data, headers).upload(bucket_name, object_name)
        return

    _GCSUpload(full_path_to_data, headers).upload(credentials, auth_method, bucket_name, object_name, head_url, put_url, callback)


def __handle_s3_download_if_needed(bucket_name, object_name):
    @_default_retry()
    def with_retry_s3():
        return S3DownloadDirectDownload().download(bucket_name, object_name)

    if object_name.startswith(s3_moniker):
        object_name = remove_moniker(object_name)
        bucket_name, object_name = object_name.split('/', 1)
        return with_retry_s3(), True
    elif bucket_name is not None and bucket_name.startswith(s3_moniker):
        return with_retry_s3(), True

    return None, False


def do_download(auth_method, bucket_name, object_name, signed_url_service=None):
    data, handled = __handle_s3_download_if_needed(bucket_name, object_name)

    if handled:
        return data

    @_default_retry()
    def with_retry():
        try:
            from google.auth.exceptions import DefaultCredentialsError
        except ImportError:
            raise GooglePackagesMissing()

        if signed_url_service:
            return GCSDownload(auth_method, signed_url_service).download(object_name)

        try:
            credentials = GCPServices.gcp_default_credentials(scopes=['https://www.googleapis.com/auth/devstorage.read-only'])

            return GCSDownloadDirectDownload(credentials).download(bucket_name, object_name)
        except DefaultCredentialsError as ex:
            logging.info('Failed to get GCP credentials %s', ex)
            raise NonRetryException(ex)

    return with_retry()


def do_delete_all(bucket_name, volume_id, max_files):
    credentials = GCPServices.gcp_default_credentials(scopes=['https://www.googleapis.com/auth/devstorage.read_write'])

    return GCSDeleteAll(signed_url_service=None, credentials=credentials).delete_all(bucket_name, volume_id, max_files)
