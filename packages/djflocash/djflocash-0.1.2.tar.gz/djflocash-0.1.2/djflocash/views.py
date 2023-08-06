import json
import logging

from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView

from .forms import NotificationForm
from .models import Notification
from .utils import get_ip_address, validate_notification_request


log = logging.getLogger(__name__)


class NotificationReceive(CreateView):

    http_method_names = {'post'}  # only post
    model = Notification
    form = NotificationForm
    fields = list(set(NotificationForm().fields.keys()) - {"merchant"})
    response_class = HttpResponse

    FORM_ERROR_STATUS = 422
    SUCCESS_CONTENT = "00"

    # we need to be exempt from CSRF if activated for flocash won't have a CSRF token
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # verify post is from Flocash
        if validate_notification_request(request.POST.dict()):
            return super().post(request, *args, **kwargs)
        else:
            return HttpResponse("INVALID", status=409)

    def get(self, *args, **kwargs):
        # just to be sure, for because of http_method_names, this should never be executed
        raise NotImplementedError("Post data directly")

    def form_valid(self, form):
        # associate payment if possible
        self.object = form.save()
        return self.response_class(self.SUCCESS_CONTENT, content_type="text/plain")

    def form_invalid(self, form):
        log.error(
            "Error while processing notification received from %s",
            get_ip_address(self.request),
            extra={"data": form.data, "errors": form.errors},
        )
        return self.response_class(
            status=self.FORM_ERROR_STATUS,
            content=json.dumps(form.errors),
            content_type="application/json",
        )
