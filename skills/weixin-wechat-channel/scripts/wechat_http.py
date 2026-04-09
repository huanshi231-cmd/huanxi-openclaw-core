# -*- coding: utf-8 -*-
"""
微信公众号接口 HTTP 会话：直连 api.weixin.qq.com，不读取 HTTP_PROXY/HTTPS_PROXY。

微信开放平台接口在国内可直连；避免被全局代理环境变量劫持。
"""
from __future__ import annotations

import requests


def session() -> requests.Session:
    s = requests.Session()
    s.trust_env = False  # 忽略环境变量中的代理设置
    return s


def get(url: str, **kwargs) -> requests.Response:
    kwargs.setdefault("timeout", 60)
    return session().get(url, **kwargs)


def post(url: str, **kwargs) -> requests.Response:
    kwargs.setdefault("timeout", 120)
    return session().post(url, **kwargs)
