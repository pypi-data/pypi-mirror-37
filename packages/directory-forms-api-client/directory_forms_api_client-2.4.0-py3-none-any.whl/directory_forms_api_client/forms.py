from django.forms import Form

from directory_forms_api_client import actions


class EmailActionMixin:
    action_class = actions.EmailAction

    def save(self, recipients, subject, reply_to, *args, **kwargs):
        action = self.action_class(
            recipients=recipients,
            subject=subject,
            reply_to=reply_to,
        )
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return {
            'text_body': self.text_body,
            'html_body': self.html_body,
        }

    @property
    def text_body(self):
        raise NotImplementedError()

    @property
    def html_body(self):
        raise NotImplementedError()


class ZendeskActionMixin:
    action_class = actions.ZendeskAction

    def save(
        self, email_address, full_name, subject, subdomain=None, *args,
        **kwargs
    ):
        action = self.action_class(
            email_address=email_address,
            full_name=full_name,
            subject=subject,
            subdomain=subdomain
        )
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return self.cleaned_data


class GovNotifyActionMixin:
    action_class = actions.GovNotifyAction

    def save(self, template_id, email_address, *args, **kwargs):
        action = self.action_class(
            template_id=template_id,
            email_address=email_address,
        )
        return action.save(self.serialized_data)

    @property
    def serialized_data(self):
        return self.cleaned_data


class EmailAPIForm(EmailActionMixin, Form):
    pass


class ZendeskAPIForm(ZendeskActionMixin, Form):
    pass


class GovNotifyAPIForm(GovNotifyActionMixin, Form):
    pass
