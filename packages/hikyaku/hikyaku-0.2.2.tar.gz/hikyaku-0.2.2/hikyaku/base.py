import json

from munch import Munch


class HikyakuSettings(Munch):
    """
    The settings object contains information about how to send the notification within the given notifier type. This
    is almost always specific to the notifier.
    """
    def __init__(self, *args, **kwargs):
        super(HikyakuSettings, self).__init__(*args,**kwargs)

    def get_config_name(self):
        raise NotImplementedError()

    def import_json(self, json_file_or_ob):

        json_ob = None

        if isinstance(json_file_or_ob,str):
            with open(json_file_or_ob,'r+') as f:
                json_ob = json.load(f)
        elif isinstance(json_file_or_ob,(dict)):
            json_ob = json_file_or_ob
        elif isinstance(json_file_or_ob, file):
            json_ob = json.load(json_file_or_ob)

        if not json_ob:
            raise ValueError("Unable to import given json data because the given value "
                             "is not a file object, path to file or dictionary")

        if self.get_config_name() not in json_ob:
            raise ValueError("Unable to import settings from config because a key "
                             "called %s could not be found"%self.get_config_name())

        config_data = json_ob[self.get_config_name()]
        assert isinstance(config_data,dict)
        for k,v in config_data.items():
            if hasattr(self,k):
                if isinstance(v,str):
                    # convert to unicode if necessary
                    v = str(v)

                setattr(self,k,v)


class HikyakuNotification(Munch):
    """
    This is the base class which contains data that is part of the payload being sent via the notifier.
    While there is not necessarily a notification class for each notifier, in many cases notifiers can send
    information in ways that are unique to that delivery channel
    """
    def __init__(self, *args, **kwargs):
        super(HikyakuNotification, self).__init__(*args, **kwargs)


class HikyakuNotifier(object):
    """
    This is the base class for all notifiers.  Derived classes must implement the `send` method.
    """
    def __init__(self, settings, notification):
        self.settings = settings
        self.notification = notification

    def send(self):
        raise NotImplementedError()
