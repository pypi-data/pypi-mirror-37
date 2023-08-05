from hikyaku.channels import email, slack


def send_slack_notification(settings, notification):
    assert(isinstance(settings,slack.SlackSettings))
    assert(isinstance(notification, slack.SlackNotification))
    return slack.SlackNotifier(settings=settings,notification=notification).send()


def send_aws_email_notification(settings, notification):
    assert(isinstance(settings,email.AmazonEmailSettings))
    assert(isinstance(notification, email.EmailNotification))
    return email.AmazonEmailNotifier(settings=settings,notification=notification).send()


def send_smtp_email_notification(settings, notification):
    assert(isinstance(settings,email.SmtpEmailSettings))
    assert(isinstance(notification, email.EmailNotification))
    return email.SmtpEmailNotifier(settings=settings,notification=notification).send()

