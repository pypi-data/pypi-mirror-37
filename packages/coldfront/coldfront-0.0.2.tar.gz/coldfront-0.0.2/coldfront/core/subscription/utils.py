from django.db.models import Q

from coldfront.core.resources.models import Resource
from coldfront.core.subscription.models import (SubscriptionUser,
                                                 SubscriptionUserStatusChoice)


def set_subscription_user_status_to_error(subscription_user_pk):
    subscription_user_obj = SubscriptionUser.objects.get(pk=subscription_user_pk)
    error_status = SubscriptionUserStatusChoice.objects.get(name='Error')
    subscription_user_obj.status = error_status
    subscription_user_obj.save()


def generate_guauge_data_from_usage(name, value, usage):

    label = "%s: %d of %d" % (name, usage, value)

    percent = (usage/value)*100

    if percent < 80:
        color = "#6da04b"
    elif percent >= 80 and percent < 90:
        color = "#ffc72c"
    else:
        color = "#e56a54"

    usage_data = {
        "columns": [
            [label, percent],
        ],
        "type": 'gauge',
        "colors": {
            label: color
        }
    }

    return usage_data


def get_user_resources(user_obj):

    if user_obj.is_superuser:
        resources = Resource.objects.filter(is_subscribable=True)
    else:
        resources = Resource.objects.filter(
            Q(is_subscribable=True) &
            Q(is_available=True) &
            (Q(is_public=True) | Q(allowed_groups__in=user_obj.groups.all()))
        ).distinct()

    return resources


def test_subscription_function(subcription_pk):
    print('test_subscription_function', subcription_pk)
