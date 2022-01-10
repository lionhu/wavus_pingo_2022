from templated_mail.mail import BaseEmailMessage
import logging

logger = logging.getLogger("error_logger")

class NotificationRegisterEmail(BaseEmailMessage):
    template_name = "email/notification_register.html"

    def get_context_data(self, **kwargs):
        ctx = super(BaseEmailMessage, self).get_context_data(**kwargs)
        context = dict(ctx, **self.context)
        logger.error("get_context_data")
        logger.error(context)
        context.update({"company": "WAVUS Co.,LTD"})
        return context
