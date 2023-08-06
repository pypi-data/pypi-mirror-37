"""Forms corresponding to gateway api
"""
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.forms import models as forms_models

from . import codes
from . import models


class MerchantForm(forms.Form):
    """Base info on merchant
    """
    merchant_name = forms.CharField(required=True, max_length=100)
    image_url = forms.CharField(required=False, max_length=250)
    return_url = forms.CharField(required=False, max_length=250)
    cancel_url = forms.CharField(required=False, max_length=250)
    notify_url = forms.CharField(required=False, max_length=250)


class BaseOrderMixin(forms.Form):
    """Base fields constituting forms
    """
    merchant = forms.CharField(required=True, max_length=50)
    custom = forms.CharField(required=True, max_length=25)
    order_id = forms.CharField(required=True, max_length=25)
    amount = forms.FloatField(required=True)
    item_name = forms.CharField(required=True, max_length=250)
    item_price = forms.FloatField(required=True)
    currency_code = forms.ChoiceField(
        required=True,
        choices=sorted(codes.CURRENCY_LABEL.items(), key=lambda c: c[1]),
    )
    quantity = forms.IntegerField(required=True, initial=1)


class OrderForm(BaseOrderMixin, MerchantForm):
    """Form to be submitted to flocash ecommerce service
    """

    SETTINGS_PREFIX = "FLOCASH_"
    SETTINGS_FIELDS = ['merchant_name', 'merchant', 'image_url', 'return_url', 'cancel_url']

    country = forms.ChoiceField(
        required=False,
        choices=sorted(codes.COUNTRY_LABEL.items(), key=lambda c: c[1]),
    )
    user_firstname = forms.CharField(required=False, max_length=250)
    user_lastname = forms.CharField(required=False, max_length=250)
    user_address = forms.CharField(required=False, max_length=250)
    user_city = forms.CharField(required=False, max_length=50)
    user_state = forms.CharField(required=False, max_length=250)
    user_postalcode = forms.CharField(required=False, max_length=250)
    user_email = forms.CharField(required=False, max_length=250)
    user_mobile = forms.CharField(required=False, max_length=250)
    payment_option = forms.CharField(required=False, max_length=250)

    def to_dict(self):
        """generate a dict, this is useful if form will be submitted through javascript"""
        if not self.is_valid():
            raise ValidationError("Form must be valid")
        data = self.cleaned_data
        for fname, value in dict(data).items():
            if (value is None or value == "") and not self.fields[fname].required:
                del data[fname]
        return data

    @classmethod
    def from_payment(cls, payment, **overrides):
        """generate a form from a payment model

        This is voluntarily a bit minimalistic (we do not copy user data)

        The SETTINGS_FIELDS and SETTINGS_PREFIX control how some data are fetch from settings.

        :param payment: a payment model
        :type payment: :py:cls:`djflocash.model.Payment`

        return: an instance of this class
          with attributes taken from overrides, model, and settings (in this order of priority)
        """
        order_data = {}
        # add some fields from settings
        prefix = cls.SETTINGS_PREFIX
        for fname in cls.SETTINGS_FIELDS:
            order_data[fname] = getattr(settings, "%s%s" % (prefix, fname.upper()), None)
        # copy model fields
        model_data = forms_models.model_to_dict(payment, fields=cls().fields.keys())
        order_data.update(model_data)
        # add overrides
        order_data.update(overrides)
        order = cls(order_data)
        return order


class NotificationForm(forms.ModelForm, BaseOrderMixin):
    """Form for notifications received from flocash
    """

    class Meta:
        model = models.Notification
        exclude = ["created", "payment"]

    sender_acct = forms.CharField(required=False, max_length=50)
    trans_id = forms.CharField(max_length=50)
    fpn_id = forms.CharField(max_length=50)
    status = forms.IntegerField()
    status_msg = forms.CharField(max_length=250)
    customer = forms.CharField(required=False, max_length=250)
    payer_email = forms.CharField(required=False, max_length=250)
    payment_channel = forms.CharField(max_length=250)
    txn_partner_ref = forms.CharField(required=False, max_length=250)
