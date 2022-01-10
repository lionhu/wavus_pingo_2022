from templated_mail.mail import BaseEmailMessage

__all__ = [
    "CommonNotificationEmail"
]


class CommonNotificationEmail(BaseEmailMessage):
    template_name = "email/notification.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["subject"] = context.get("subject")
        context["type"] = context.get("type")
        context["content"] = context.get("content")

        context["button_blue_text"] = context.get("button_blue_text")
        context["button_blue_url"] = context.get("button_blue_url")
        context["button_grey_text"] = context.get("button_grey_text")
        context["button_grey_url"] = context.get("button_grey_url")
        return context
