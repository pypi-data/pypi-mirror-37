DJFlocash
###########

|pypi-version| |travis|

Python helpers to use https://www.flocash.com/ Payement API in Django.

This product is not complete, but contributions are welcome.

Flocash is a gateway payement API
enabling payement in a lot of african countries
through credit cards, mobile phone payements and more.

This library gives you some re-usable components to use in your Django application.

At the moment, it implements the redirect style API
(not the one based on webservices).

.. important:: This program IS NOT an official library of flocash.
     flocash is a registered trademark of Flocash ltd.


Setting up
==========

In your project, you can either create your own models that inherit the base one,
or use the proposed one directly.

In the first case, you may want to connect your model to handlers defined in `signals.py`.

For both cases, add djflocash to your `INSTALLED_APPS` setting.

You have to define some mandatory settings:

* FLOCASH_BASE_URL the base url of flocash service
* FLOCASH_PAYMENT_URI the uri handling ecommerce payment (will be urljoined to base url)
* FLOCASH_MERCHANT, FLOCASH_MERCHANT_NAME your merchant account and display name
* FLOCASH_NOTIFICATION_TOKEN is a token that will be added to your notification url
  in order to make it unpredictable, so it is a shared secret between you and flocash
  (you will set flocash notification url in their backend).

  Note that djflocash also use notification validation using flocash dedicated service.

and some optionnal one:

* FLOCASH_PAYMENT_MODEL is the payment model in case you don't use provided model.

Usage
=====


The idea is that your visitor will submit a payment through his browser.
For this you need to build the form, you can do this using `forms.OrderForm`,
if you submit it through javascript you may use the `to_dict` method.

You can expose the `views.NotificationReceive` view (or your own based on it)
to get notifications (successful or canceled) payment.
It creates a `models.Notification` instance
and associate it to the `models.Payment` having same `order_id` if it exists.

You have to provide the notification URL to Flocash in the Flocash backoffice.
By default it is `https://your.server.com/notification/xxxxxxxx/`,
where `xxxxxxxx` is `FLOCASH_NOTIFICATION_TOKEN` setting.

A possible workflow is thus the following:

- you create a `models.Payment` corresponding to your visitor basket
- you use `forms.OrderForm.from_payment` to generate corresponding form
  and render it in visitor browser (using hidden fields)
- visitor submit the form to flocash and is redirected to flocash payment portal
  where he completes the transaction
- flocash submit the payment notification through `views.NotificationReceive`,
  and some custom handler you attached on eg. `post_save` signal
  make the order effective in your system
- visitors gets back to your site where you tell him his purchase is effective

When the response for payment is PENDING, djflocash tracks the payment status
and keep it pending, until a payment or non payment notifications arrives
(see `Payment.is_pending` and `PaymentManager.pending`.
It's up to you to use this information to notify your customers,
that a pending payment is already in progress.

.. |pypi-version| image:: https://img.shields.io/pypi/v/djflocash.svg
    :target: https://pypi.python.org/pypi/djflocash
    :alt: Latest PyPI version

.. |travis| image:: http://img.shields.io/travis/jurismarches/djflocash/master.svg?style=flat
    :target: https://travis-ci.org/jurismarches/djflocash
    :alt: Travis status

.. |license| image:: https://img.shields.io/github/license/jurismarches/djflocash.svg   
    :target: https://github.com/jurismarches/djflocash/blob/master/LICENSE
    :alt: LGPL license
