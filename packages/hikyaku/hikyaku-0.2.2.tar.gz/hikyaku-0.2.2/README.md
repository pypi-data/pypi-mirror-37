# Hikyaku

This library is intended to make it extremely easy to send messages to recipients through multiple 
communication platforms including email, SES and Slack.

## Why hikyaku
    Hikyaku were couriers or messengers active in the medieval and early modern periods, 
    who transported currency, letters, packages, and the like. In the Edo period, the 
    network of hikyaku messengers expanded dramatically, and also became more organized 
    and systematized.
   
(from https://wiki.samurai-archives.com/index.php?title=Hikyaku)

     
## Installing

To install

    pip install hikyaku
    
## Using 

The easiest way to get started is to use the convenience functions.  For example, to send a slack
message:

    from hikyaku import send_slack_notification
    from hikyaku.channels.slack import SlackSettings, SlackNotification
    result = hikyaku.send_slack_notification(
                    SlackSettings(api_token="<api_token>"),
                    SlackNotification(text="Test Message",channel="test-channel")
                    
    assert result == True        

But in general, all methods work in a similar way.

1. Create a settings object for the type of channel you will be communicating through
2. Create a notification object that contains the content of the message being sent.  
3. Send using one of these two methods:
    1. Either call the convenience function passing in the settings and notification object 
    2. Instantiate the notifier object passing in the settings and notification object then call send
4. The return value in either method is always a boolean value. To get more information, the result
    info is always stored in the notifier object's last_result property.
    
## Easy Configuration Loading

Each settings object can load info from a JSON file that is structured to have the channel
settings organized as expected.  

This allows you to have a single config file that has communication settings aggregated into groups 
as follows:

    {
      "smtp": {
        "host": "",
        "port": "",
        "username": "",
        "password": "",
        "mode": ""
      },
      "aws": {
        "region_name": "",
        "charset": ""
      },
      "slack":{
        "api_token": ""
      }
    } 

The `import_json` method can accept a filename, a file object or a dictionary that has the above 
structure.  It will ignore all other key in the structure passed.


    
 