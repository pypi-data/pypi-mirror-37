# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import datetime
import httpretty
import json
import uuid

from collections import Mapping

from tests.test_api.utils import TestBaseApi

from polyaxon_client.api.base import BaseApiHandler
from polyaxon_client.api.build_job import BuildJobApi
from polyaxon_client.schemas import JobConfig, JobStatusConfig


class TestBuildJobApi(TestBaseApi):

    def setUp(self):
        super(TestBuildJobApi, self).setUp()
        self.api_handler = BuildJobApi(transport=self.transport, config=self.api_config)

    @httpretty.activate
    def test_get_build(self):
        job = JobConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1
            ),
            body=json.dumps(job),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.get_build('username', 'project_name', 1)
        assert result.to_dict() == job

        # Raw response
        self.set_raw_response()
        result = self.api_handler.get_build('username', 'project_name', 1)
        assert result == job

    @httpretty.activate
    def test_update_build(self):
        job = JobConfig(config={}).to_dict()
        httpretty.register_uri(
            httpretty.PATCH,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1),
            body=json.dumps(job),
            content_type='application/json',
            status=200)

        # Schema response
        result = self.api_handler.update_build('username', 'project_name', 1, {'name': 'new'})
        assert result.to_dict() == job

        # Raw response
        self.set_raw_response()
        result = self.api_handler.update_build('username', 'project_name', 1, {'name': 'new'})
        assert result == job

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.update_build(
                'username', 'project_name', 1, {'name': 'new'}, background=True),
            method='patch')

    @httpretty.activate
    def test_delete_build(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1),
            content_type='application/json',
            status=204)
        result = self.api_handler.delete_build('username', 'project_name', 1)
        assert result.status_code == 204

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.delete_build(
                'username', 'project_name', 1, background=True),
            method='delete')

    @httpretty.activate
    def test_get_job_statuses(self):
        job = JobStatusConfig(id=1,
                              uuid=uuid.uuid4().hex,
                              job=1,
                              created_at=datetime.datetime.now(),
                              status='Running').to_dict()
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'statuses'),
            body=json.dumps({'results': [job], 'count': 1, 'next': None}),
            content_type='application/json',
            status=200)

        # Schema response
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], JobStatusConfig)

        # Raw response
        self.set_raw_response()
        response = self.api_handler.get_statuses('username', 'project_name', 1)
        assert len(response['results']) == 1
        assert isinstance(response['results'][0], Mapping)

    @httpretty.activate
    def test_stop_build(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'stop'),
            content_type='application/json',
            status=200)
        result = self.api_handler.stop('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.stop(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_bookmark_build(self):
        httpretty.register_uri(
            httpretty.POST,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'bookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.bookmark('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.bookmark(
                'username', 'project_name', 1, background=True),
            method='post')

    @httpretty.activate
    def test_unbookmark_build(self):
        httpretty.register_uri(
            httpretty.DELETE,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'unbookmark'),
            content_type='application/json',
            status=200)
        result = self.api_handler.unbookmark('username', 'project_name', 1)
        assert result.status_code == 200

        # Async
        self.assert_async_call(
            api_handler_call=lambda: self.api_handler.unbookmark(
                'username', 'project_name', 1, background=True),
            method='delete')

    @httpretty.activate
    def test_job_logs(self):
        httpretty.register_uri(
            httpretty.GET,
            BaseApiHandler.build_url(
                self.api_config.base_url,
                '/',
                'username',
                'project_name',
                'builds',
                1,
                'logs'
            ),
            body='some text',
            content_type='text/plain',
            status=200)

        response = self.api_handler.logs('username', 'project_name', 1, stream=False)
        assert response.content.decode() == 'some text'
