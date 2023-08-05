import abc

from directory_forms_api_client.client import forms_api_client


class AbstractAction(abc.ABC):

    def __init__(self, client=forms_api_client, *args, **kwargs):
        self.client = client
        super().__init__(*args, **kwargs)

    @property
    @abc.abstractmethod
    def name(self):
        return ''

    def serialize_data(self, data):
        return {
            'data': data,
            'meta': self.serialize_meta()
        }

    def serialize_meta(self):
        return {
            'action_name': self.name,
            **self.meta,
        }

    def save(self, data):
        serialized_data = self.serialize_data(data)
        return self.client.submit_generic(serialized_data)


class EmailAction(AbstractAction):
    name = 'email'

    def __init__(self, recipients, subject, reply_to, *args, **kwargs):
        self.meta = {
            'recipients': recipients,
            'subject': subject,
            'reply_to': reply_to,
        }
        super().__init__(*args, **kwargs)


class ZendeskAction(AbstractAction):
    name = 'zendesk'

    def __init__(
        self, subject, full_name, email_address, subdomain=None, *args,
        **kwargs
    ):
        self.meta = {
            'full_name': full_name,
            'email_address': email_address,
            'subject': subject,
        }
        # if empty Forms API will use the default configured zendesk subdomain
        if subdomain:
            self.meta['subdomain'] = subdomain
        super().__init__(*args, **kwargs)


class GovNotifyAction(AbstractAction):
    name = 'gov-notify'

    def __init__(self, template_id, email_address, *args, **kwargs):
        self.meta = {
            'template_id': template_id,
            'email_address': email_address
        }
        super().__init__(*args, **kwargs)
