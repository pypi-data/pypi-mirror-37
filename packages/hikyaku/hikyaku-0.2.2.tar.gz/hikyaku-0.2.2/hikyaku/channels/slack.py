import copy

from munch import Munch

from hikyaku.base import HikyakuNotifier, HikyakuSettings, HikyakuNotification
from slackclient import SlackClient


class SlackSettings(HikyakuSettings):

    def __init__(self, slack_api_token=None, **kwargs):
        super(SlackSettings, self).__init__(**kwargs)
        self.api_token = slack_api_token

    def get_config_name(self):
        return "slack"


class SlackAttachmentField(Munch):

    def __init__(self,*args,**kwargs):
        self.title = kwargs.pop('title',"")
        self.value = kwargs.pop('value',"")
        self.short = kwargs.pop('short',False)
        super(SlackAttachmentField, self).__init__(*args,**kwargs)

    def validate(self):
        if not self.title:
            raise ValueError("You must give a field a title")

        if not self.value:
            raise ValueError("You must give a field a value")

        if not isinstance(self.short,bool):
            raise ValueError("Unrecognized type given for 'short' field attribute")


class SlackAttachment(Munch):
    def __init__(self, *args, **kwargs):
        self.fields = []
        self.fallback = kwargs.pop('fallback',"")
        self.color = kwargs.pop('color',"")
        self.pretext = kwargs.pop('pretext',"")
        self.author_name = kwargs.pop('author_name',"")
        self.author_link = kwargs.pop('author_link',"")
        self.author_icon = kwargs.pop('author_icon',"")
        self.title = kwargs.pop('title',"")
        self.title_link = kwargs.pop('title_link',"")
        self.text = kwargs.pop('text',"")
        self.image_url = kwargs.pop('image_url',"")
        self.thumb_url = kwargs.pop('thumb_url',"")
        self.footer = kwargs.pop('footer',"")
        self.footer_icon = kwargs.pop('footer_icon',"")
        self.ts = kwargs.pop('ts', 0)
        super(SlackAttachment, self).__init__(*args,**kwargs)

    def add_field(self, field):
        assert isinstance(field,SlackAttachmentField)
        self.fields.append(field)

    def validate(self):
        if not self.fallback:
            raise ValueError("You must specify fallback text for a slack attachment")

        for field in self.fields:
            field.validate()


class SlackNotification(HikyakuNotification):
    """
    Slack notifications use  the python slack API.


    Direct messages use the conversation api:
    http://slackapi.github.io/python-slackclient/conversations.html#creating-a-direct-message-or-multi-person-direct-message

    Channel messages use the chat API:


    """
    def __init__(self, **kwargs):
        self.channel = kwargs.pop('channel',None)
        self.users = kwargs.pop('users',None)
        self.text = kwargs.pop('text',None)
        self.attachments = kwargs.pop('attachments',None)
        self.username = kwargs.pop('username',None)
        self.icon_url = kwargs.pop('icon_url',None)
        self.icon_emoji = kwargs.pop('icon_emoji',None)

        super(SlackNotification, self).__init__(**kwargs)


class SlackNotifier(HikyakuNotifier):

    def __init__(self,*args,**kwargs):
        self.last_result = None
        super(SlackNotifier, self).__init__(*args,**kwargs)

    def send(self):
        slack_token = self.settings.api_token
        sc = SlackClient(slack_token)

        if self.notification.channel:
            # if a specific channel was given we can just post a message to the existing channel.
            self.last_result = sc.api_call(
                "chat.postMessage",
                **self.notification
            )
            if self.last_result and self.last_result['ok']:
                return True
            else:
                return False
        elif self.notification.users:

            if isinstance(self.notification.users,(list,tuple)):
                users = ",".join(self.notification.users)
            else:
                users = self.notification.users

            # first we need to either create or get the conversation with the person or persons given
            result = sc.api_call(
                "conversations.open",
                users=users
            )

            if result and result['ok']:
                # now send the message to the "channel" which is either a direct message or multi-direct message
                notification = copy.deepcopy(self.notification)
                notification.channel = result['channel']['id']
                notification.users = None

                self.last_result = sc.api_call(
                    "chat.postMessage",
                    **notification
                )
                if self.last_result:
                    return 'ok' in self.last_result and self.last_result['ok']
                else:
                    return False

        else:
            raise ValueError("Request for notification did not contain channel or user recipients")
