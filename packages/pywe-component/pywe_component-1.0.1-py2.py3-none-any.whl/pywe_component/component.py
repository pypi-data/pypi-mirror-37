# -*- coding: utf-8 -*-


def get_pre_auth_url(component_appid, pre_auth_code=None, redirect_uri=None, auth_type=3, biz_appid='', mobi=False):
    if mobi:
        return get_mobi_pre_auth_url(component_appid, pre_auth_code=pre_auth_code, redirect_uri=redirect_uri, auth_type=auth_type, biz_appid=biz_appid)
    return 'https://mp.weixin.qq.com/cgi-bin/componentloginpage?component_appid={component_appid}&pre_auth_code={pre_auth_code}&redirect_uri={redirect_uri}&auth_type={auth_type}&biz_appid={biz_appid}'.format(
        component_appid=component_appid,
        pre_auth_code=pre_auth_code,
        redirect_uri=redirect_uri,
        auth_type=auth_type,
        biz_appid=biz_appid,
    )


def get_mobi_pre_auth_url(component_appid, pre_auth_code=None, redirect_uri=None, auth_type=3, biz_appid=''):
    return 'https://mp.weixin.qq.com/safe/bindcomponent?action=bindcomponent&no_scan=1&component_appid={component_appid}&pre_auth_code={pre_auth_code}&redirect_uri={redirect_uri}&auth_type={auth_type}&biz_appid={biz_appid}#wechat_redirect'.format(
        component_appid=component_appid,
        pre_auth_code=pre_auth_code,
        redirect_uri=redirect_uri,
        auth_type=auth_type,
        biz_appid=biz_appid,
    )
