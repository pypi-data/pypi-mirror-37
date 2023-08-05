# -*- coding: utf-8 -*-

from pywe_token import BaseToken, final_access_token


class CustomMessage(BaseToken):
    def __init__(self, appid=None, secret=None, token=None, storage=None):
        super(CustomMessage, self).__init__(appid=appid, secret=secret, token=token, storage=storage)
        # 客服消息接口, Refer: https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140547
        # 客服帐号管理
        # 添加客服帐号
        self.WECHAT_CUSTOM_ADD_KFACCOUNT = self.API_DOMAIN + '/customservice/kfaccount/add'
        # 修改客服帐号
        self.WECHAT_CUSTOM_UPDATE_KFACCOUNT = self.API_DOMAIN + '/customservice/kfaccount/update'
        # 删除客服帐号
        self.WECHAT_CUSTOM_DEL_KFACCOUNT = self.API_DOMAIN + '/customservice/kfaccount/del'
        # 设置客服帐号的头像
        self.WECHAT_CUSTOM_UPLOAD_HEADIMG = self.API_DOMAIN + '/customservice/kfaccount/uploadheadimg'
        # 获取所有客服账号
        self.WECHAT_CUSTOM_GET_KFLIST = self.API_DOMAIN + '/cgi-bin/customservice/getkflist?access_token={access_token}'
        # 客服接口
        # 客服接口-发消息
        self.WECHAT_CUSTOM_MESSAGE_SEND = self.API_DOMAIN + '/cgi-bin/message/custom/send'
        # 客服接口-客服输入状态
        self.WECHAT_CUSTOM_TYPING = self.API_DOMAIN + '/cgi-bin/message/custom/typing'

    def add_kfaccount(self, kf_account, nickname, password, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CUSTOM_ADD_KFACCOUNT,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'kf_account': kf_account,
                'nickname': nickname,
                'password': password,
            },
        )

    def update_kfaccount(self, kf_account, nickname, password, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CUSTOM_UPDATE_KFACCOUNT,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'kf_account': kf_account,
                'nickname': nickname,
                'password': password,
            },
        )

    def del_kfaccount(self, kf_account, nickname, password, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CUSTOM_DEL_KFACCOUNT,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'kf_account': kf_account,
                'nickname': nickname,
                'password': password,
            },
        )

    def upload_headimg(self, kf_account, media_file=None, media_file_path=None, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CUSTOM_DEL_KFACCOUNT,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
                'kf_account': kf_account,
            },
            files={
                'media': media_file or open(media_file_path, 'rb'),
            },
        )

    def get_kflist(self, appid=None, secret=None, token=None, storage=None):
        return self.get(self.WECHAT_CUSTOM_GET_KFLIST, access_token=final_access_token(self, appid=appid, secret=secret, token=token, storage=storage))

    def send_custom_message(self, data, account=None, appid=None, secret=None, token=None, storage=None):
        if account:
            data['customservice'] = {'kf_account': account}
        return self.post(
            self.WECHAT_CUSTOM_MESSAGE_SEND,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data=data,
        )

    def send_custom_text_message(self, openid=None, content=None, appid=None, secret=None, token=None, storage=None):
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'text',
            'text': {
                'content': content,
            },
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_text_message(self, openid=None, content=None, appid=None, secret=None, token=None, storage=None):
        """
        发送文本消息时，支持插入跳小程序的文字链

        文本内容<a href="http://www.qq.com" data-miniprogram-appid="appid" data-miniprogram-path="pages/index/index">点击跳小程序</a>

        说明：
        1.data-miniprogram-appid 项，填写小程序appid，则表示该链接跳小程序；
        2.data-miniprogram-path项，填写小程序路径，路径与app.json中保持一致，可带参数；
        3.对于不支持data-miniprogram-appid 项的客户端版本，如果有herf项，则仍然保持跳href中的网页链接；
        4.data-miniprogram-appid对应的小程序必须与公众号有绑定关系。
        """
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'text',
            'text': {
                'content': content,
            },
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_image_message(self, openid=None, media_id=None, appid=None, secret=None, token=None, storage=None):
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'image',
            'image': {
                'media_id': media_id,
            },
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_voice_message(self, openid=None, media_id=None, appid=None, secret=None, token=None, storage=None):
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'voice',
            'voice': {
                'media_id': media_id,
            },
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_video_message(self, openid=None, media_id=None, thumb_media_id=None, title=None, description=None, appid=None, secret=None, token=None, storage=None):
        data = {
            'media_id': media_id,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            data['title'] = title
        if description:
            data['description'] = description
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'video',
            'video': data,
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_music_message(self, openid=None, musicurl=None, hqmusicurl=None, thumb_media_id=None, title=None, description=None, appid=None, secret=None, token=None, storage=None):
        data = {
            'musicurl': musicurl,
            'hqmusicurl': hqmusicurl,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            data['title'] = title
        if description:
            data['description'] = description
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'music',
            'music': data,
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_news_message(self, openid=None, url=None, picurl=None, title=None, description=None, appid=None, secret=None, token=None, storage=None):
        data = {
            'url': url,
            'picurl': picurl,
        }
        if title:
            data['title'] = title
        if description:
            data['description'] = description
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'articles',
            'articles': [data],
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_mpnews_message(self, openid=None, media_id=None, appid=None, secret=None, token=None, storage=None):
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'mpnews',
            'mpnews': {
                'media_id': media_id,
            },
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_card_message(self, openid=None, card_id=None, appid=None, secret=None, token=None, storage=None):
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'wxcard',
            'wxcard': {
                'card_id': card_id,
            },
        }, appid=appid, secret=secret, token=token, storage=storage)

    def send_custom_wxa_message(self, openid=None, miniappid=None, pagepath=None, thumb_media_id=None, title=None, appid=None, secret=None, token=None, storage=None):
        data = {
            'appid': miniappid,
            'pagepath': pagepath,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            data['title'] = title
        return self.send_custom_message({
            'touser': openid,
            'msgtype': 'miniprogrampage',
            'miniprogrampage': data,
        }, appid=appid, secret=secret, token=token, storage=storage)

    def custom_typing(self, openid=None, typing=True, appid=None, secret=None, token=None, storage=None):
        return self.post(
            self.WECHAT_CUSTOM_TYPING,
            params={
                'access_token': final_access_token(self, appid=appid, secret=secret, token=token, storage=storage),
            },
            data={
                'touser': openid,
                'command': 'Typing' if typing else 'CancelTyping',
            },
        )


tmpmsg = CustomMessage()
add_kfaccount = tmpmsg.add_kfaccount
update_kfaccount = tmpmsg.update_kfaccount
del_kfaccount = tmpmsg.del_kfaccount
upload_headimg = tmpmsg.upload_headimg
get_kflist = tmpmsg.get_kflist
send_custom_message = tmpmsg.send_custom_message
send_custom_text_message = tmpmsg.send_custom_text_message
send_custom_image_message = tmpmsg.send_custom_image_message
send_custom_voice_message = tmpmsg.send_custom_voice_message
send_custom_video_message = tmpmsg.send_custom_video_message
send_custom_news_message = send_custom_articles_message = tmpmsg.send_custom_news_message
send_custom_mpnews_message = tmpmsg.send_custom_mpnews_message
send_custom_card_message = tmpmsg.send_custom_card_message
send_custom_wxa_message = tmpmsg.send_custom_wxa_message
custom_typing = tmpmsg.custom_typing
