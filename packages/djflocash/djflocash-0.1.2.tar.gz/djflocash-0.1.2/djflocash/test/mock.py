from unittest import mock


def validate_notification_request_ok():
    return mock.patch(
        'djflocash.views.validate_notification_request',
        return_value=True,
    )


def validate_notification_request_ko():
    return mock.patch(
        'djflocash.views.validate_notification_request',
        return_value=False,
    )
