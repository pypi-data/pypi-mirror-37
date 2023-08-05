# -*- coding: utf8 -*-
import os

import fudge
from fudge.inspector import arg
from google.auth import app_engine
from six import StringIO

from missinglink.legit.gcp_services import GCPServices, GoogleCredentialsFile
from missinglink.legit.gcs_utils import do_download, GCSDownloadDirectDownload, do_delete_all, do_upload
from tests.base import BaseTest
import httpretty


class TestGCSOperations(BaseTest):
    bucket_name = 'missinglink-public'
    s3_bucket_name = 's3://missinglink-public'
    object_name_1 = 'test_files_dont_delete/1.txt'
    s3_object_name_1 = '{bucket}/{object_name}'.format(bucket=s3_bucket_name, object_name=object_name_1)

    def setUp(self):
        super(TestGCSOperations, self).setUp()

        GoogleCredentialsFile._clear_files_cache()

    def _wrap_local_s3_auth(self, actual_test):
        def wrap():
            ACCESS_KEY = 'AWS_ACCESS_KEY_ID'
            SECRET_KEY = 'AWS_SECRET_ACCESS_KEY'

            os.environ[ACCESS_KEY] = self.some_random_shit(ACCESS_KEY)
            os.environ[SECRET_KEY] = self.some_random_shit(SECRET_KEY)

            actual_test()

        wrap()

    def _wrap_local_auth_files(self, actual_test):
        @fudge.patch('missinglink.legit.gcp_services.GoogleCredentialsFile._get_auth_config_from_default_file')
        @fudge.patch('missinglink.legit.gcp_services.GCPServices.get_default_project_id')
        def wrap(mock__get_auth_config_from_default_file, mock_get_default_project_id):
            client_secret = self.some_random_shit('client_secret')
            refresh_token = self.some_random_shit('refresh_token')
            client_id = self.some_random_shit('client_id')

            auth_info = {
                'client_secret': client_secret,
                'refresh_token': refresh_token,
                'client_id': client_id,
                'type': 'authorized_user'
            }

            mock__get_auth_config_from_default_file.expects_call().returns(auth_info)

            project_id = self.some_random_shit('project_id')

            mock_get_default_project_id.expects_call().returns(project_id)

            actual_test()

        wrap()

    @httpretty.activate
    @fudge.patch('google.cloud.storage.Blob.upload_from_file')
    def test_upload_gcloud_method(self, mock_upload_from_file):
        def actual_test():
            full_path_to_data = StringIO('1234')
            content_type = self.some_random_shit('content_type')

            mock_upload_from_file.expects_call().with_args(full_path_to_data, content_type)

            credentials = None
            auth_method = None
            bucket_name = self.some_random_shit('bucket_name')
            object_name = self.some_random_shit('object_name')

            headers = {'Content-Type': content_type}
            head_url = None
            put_url = None
            callback = None
            do_upload(credentials, auth_method, bucket_name, object_name, full_path_to_data, headers, head_url, put_url, callback)

        self._wrap_local_auth_files(actual_test)

    @httpretty.activate
    @fudge.patch('requests.Session.head')
    @fudge.patch('requests.Session.put')
    def test_upload_secure_url_method(self, mock_session_head, mock_session_put):
        full_path_to_data = StringIO('1234')
        content_type = self.some_random_shit('content_type')

        credentials = None
        auth_method = None
        bucket_name = self.some_random_shit('bucket_name')
        object_name = self.some_random_shit('object_name')

        headers = {'Content-Type': content_type}
        head_url = self.some_random_shit('head_url')
        put_url = self.some_random_shit('put_url')
        callback = None

        fake_response = fudge.Fake().has_attr(status_code=404)
        mock_session_head.expects_call().with_args(head_url).returns(fake_response)

        def fake_put(url, data, headers):
            data.read(4)

            fake_put_response = fudge.Fake().has_attr(status_code=200).provides('raise_for_status')

            return fake_put_response

        mock_session_put.expects_call().with_args(put_url, data=arg.any(), headers=headers).calls(fake_put)

        do_upload(credentials, auth_method, bucket_name, object_name, full_path_to_data, headers, head_url, put_url, callback)

    @httpretty.activate
    @fudge.patch('google.cloud.storage.Blob.download_as_string')
    def test_download_no_auth_method_with_bucket(self, mock_download_as_string):
        def actual_test():
            download_result = self.some_random_shit('result')
            mock_download_as_string.expects_call().with_args().returns(download_result)
            result = do_download(None, self.bucket_name, self.object_name_1)
            self.assertEqual(result, download_result)

        self._wrap_local_auth_files(actual_test)

    @httpretty.activate
    def test_s3_download(self):
        @fudge.patch('boto3.resource')
        def actual_test(mock_boto_resource):
            download_result = self.some_random_shit('result')
            file_obj = StringIO(download_result)
            fake_s3_object = fudge.Fake().provides('get').returns({'Body': file_obj})
            fake_s3 = fudge.Fake().provides('Object').with_args(self.bucket_name, self.object_name_1).returns(fake_s3_object)
            mock_boto_resource.expects_call().with_args('s3').returns(fake_s3)
            result = do_download(None, self.s3_bucket_name, self.object_name_1)
            self.assertEqual(result, download_result)

        self._wrap_local_s3_auth(actual_test)

    @httpretty.activate
    def test_s3_download_moniker_in_object_name(self):
        @fudge.patch('boto3.resource')
        def actual_test(mock_boto_resource):
            download_result = self.some_random_shit('result')
            file_obj = StringIO(download_result)
            fake_s3_object = fudge.Fake().provides('get').returns({'Body': file_obj})
            fake_s3 = fudge.Fake().provides('Object').with_args(self.bucket_name, self.object_name_1).returns(fake_s3_object)
            mock_boto_resource.expects_call().with_args('s3').returns(fake_s3)
            result = do_download(None, None, self.s3_object_name_1)
            self.assertEqual(result, download_result)

        self._wrap_local_s3_auth(actual_test)

    @httpretty.activate
    @fudge.patch('requests.get')
    def test_download_using_secure_url(self, mock_get):
        singed_url = self.some_random_shit('singed_url')
        content = self.some_random_shit('content')
        fake_response = fudge.Fake().provides('raise_for_status').has_attr(content=content)
        mock_get.expects_call().with_args(singed_url).returns(fake_response)
        signed_url_service = fudge.Fake().provides('get_signed_urls').with_args(['GET'], [self.object_name_1]).returns({'GET': [singed_url]})
        result = do_download(None, self.bucket_name, self.object_name_1, signed_url_service=signed_url_service)
        self.assertEqual(result, content)

    @httpretty.activate
    @fudge.patch('google.cloud.storage.Blob.download_as_string')
    def test_download_under_gae(self, mock_download_as_string):
        download_result = self.some_random_shit('result')
        mock_download_as_string.expects_call().with_args().returns(download_result)

        access_token = self.some_random_shit('access_token')
        project_id = self.some_random_shit('project_id')
        ttl = 3600
        app_engine.app_identity = fudge.Fake().provides('get_access_token').returns((access_token, ttl)).provides('get_application_id').returns(project_id)
        credentials = GCPServices.gcp_default_credentials(scopes=['read-only'])
        try:
            result = GCSDownloadDirectDownload(credentials).download(self.bucket_name, self.object_name_1)
            self.assertEqual(result, download_result)
        finally:
            app_engine.app_identity = None

    @httpretty.activate
    @fudge.patch('google.cloud.storage.Bucket.list_blobs')
    @fudge.patch('google.cloud.storage.Bucket.delete_blob')
    def test_delete_all(self, mock_list_blobs, mock_delete_blob):
        def actual_test():
            volume_id = self.some_random_shit_number_int63()

            fake_blob1 = fudge.Fake().has_attr(name='1')
            mock_list_blobs.expects_call().with_args(prefix=str(volume_id)).returns([fake_blob1])
            mock_delete_blob.expects_call().with_args('1')

            bucket_name = self.some_random_shit('bucket_name')
            max_files = 1000
            do_delete_all(bucket_name, volume_id, max_files)

        self._wrap_local_auth_files(actual_test)
