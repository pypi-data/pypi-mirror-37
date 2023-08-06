==========
pywe-oauth
==========

Wechat Oauth Module for Python.

Installation
============

::

    pip install pywe-oauth


Usage
=====

::

    from pywe_oauth import get_access_info, get_oauth_code_url, get_userinfo, get_component_access_info, get_component_oauth_code_url, get_component_userinfo, get_oauth_redirect_url


Method
======

::

    def get_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, component=False, component_appid=None):

    def get_access_info(self, appid=None, secret=None, code=None, component=False, component_appid=None, component_access_token=None):

    def get_userinfo(self, access_token=None, openid=None, component=False):

    def get_component_oauth_code_url(self, appid=None, redirect_uri=None, scope='snsapi_base', redirect_url=None, component_appid=None):

    def get_component_access_info(self, appid=None, code=None, component_appid=None, component_access_token=None):

    def get_component_userinfo(self, access_token=None, openid=None):

    def get_oauth_redirect_url(self, oauth_uri, scope='snsapi_base', redirect_url=None, default_url=None, direct_redirect=None, random_str=True):

