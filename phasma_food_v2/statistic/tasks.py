from collections import Counter

from django.contrib.auth import get_user_model
from django.db.models import Count

from fcm_django.models import FCMDevice
from celery import shared_task

from phasma_food_v2.samples.mongo_db import MongoDB
from phasma_food_v2.devices.models import PhasmaDevice
from phasma_food_v2.measurements.models import Measurement, Result

from .models import PlatformStatistic

User = get_user_model()


@shared_task
def calculate_platform_statistic() -> None:
    """A Celery task that calculates platform statistic about
    users, measurements, trained models, use cases, food type

    Returns:
        None
    """
    users_dict = users_statistic()

    platform_dict = platform_statistic()

    mongo_dict = mongo_statistic()

    postgres_dict = postgres_statistic()

    statistic = PlatformStatistic.objects.first()
    if statistic:
        statistic.users = users_dict
        statistic.platform = platform_dict
        statistic.mongo = mongo_dict
        statistic.postgres = postgres_dict
        statistic.save()
    else:
        PlatformStatistic.objects.create(users=users_dict,
                                         platform=platform_dict,
                                         mongo=mongo_dict,
                                         postgres=postgres_dict
                                         )

    return None


def users_statistic() -> dict:
    users = User.objects.all()
    return {
        "total": users.count(),
        "expert": users.filter(user_type__iexact="EXPERT").count(),
        "basic": users.filter(user_type__iexact="BASIC").count()
    }


def platform_statistic() -> dict:
    return {
        "mobile": FCMDevice.objects.count(),
        "phasma_devices": PhasmaDevice.objects.count()
    }


def mongo_statistic() -> dict:
    collections = ["AltSplitSamples", "AlcoholicBeverages", "AltJsonSamples",
                   "EdibleOils", "SkimmedMilkPowder", "UseCaseOne", "UseCaseTwo"]
    mongo_dict = {
        "measurements": {

        }
    }
    for collection in collections:
        use_cases_and_food_types = MongoDB().find_distinct_values(values=["useCase", "foodType"],
                                                                  collection=collection
                                                                  )
        use_cases = use_cases_and_food_types["useCase"]
        food_type_per_use_case = MongoDB().find_distinct_values_for_use_case(use_cases=use_cases,
                                                                             collection=collection
                                                                             )
        food_count_per_use_case = {}
        for case, foods in food_type_per_use_case.items():
            sum_measurements = 0
            for food in foods:
                total = MongoDB().counter({"foodType": food},
                                          collection=collection
                                          )
                sum_measurements += total
                if case in food_count_per_use_case:
                    food_count_per_use_case[case].update({food: total})
                else:
                    food_count_per_use_case[case] = {food: total}
            food_count_per_use_case[case].update({"total": sum_measurements})

        mongo_dict["measurements"].update(
            {
                collection: {
                    "total": MongoDB().counter(item={}, collection=collection),
                    "use_cases": food_count_per_use_case
                }
            }
        )

    mongo = mongo_dict.get("measurements")
    edible_oils = mongo.get("EdibleOils")
    skimmed_milk_powder = mongo.get("SkimmedMilkPowder")
    alcoholic_beverages = mongo.get("AlcoholicBeverages")
    total = int(edible_oils.get("total")) + int(skimmed_milk_powder.get("total")) + int(
        alcoholic_beverages.get("total"))
    mongo.update({
        "UseCaseThree": {
            "total": total,
            "use_cases": {
                "Food adulteration": {
                    "total": total,
                    "Edible Oils": int(edible_oils.get("total")),
                    "Skimmed milk powder": int(skimmed_milk_powder.get("total")),
                    "Alcoholic beverages": int(alcoholic_beverages.get("total"))
                }
            }
        }
    })
    del mongo_dict["measurements"]["EdibleOils"]
    del mongo_dict["measurements"]["SkimmedMilkPowder"]
    del mongo_dict["measurements"]["AlcoholicBeverages"]

    alt_json = mongo.get("AltJsonSamples")
    uc_one = mongo.get("UseCaseOne")
    uc_two = mongo.get("UseCaseTwo")
    uc_three = mongo.get("UseCaseThree")
    mongo_dict["measurements"]["AltJsonSamples"]["total"] = alt_json["total"] + uc_one["total"] + uc_two["total"] + \
                                                            uc_three["total"]
    uc_one_counter = Counter(uc_one["use_cases"]["Mycotoxins detection"])
    uc_two_counter = Counter(uc_two["use_cases"]["Food spoilage"])
    uc_three_counter = Counter(uc_three["use_cases"]["Food adulteration"])
    alt_json_uc_one_counter = Counter(alt_json["use_cases"]["UseCase1"])
    alt_json_uc_two_counter = Counter(alt_json["use_cases"]["UseCase2"])
    alt_json_uc_three_counter = Counter(alt_json["use_cases"]["UseCase3"])
    one = uc_one_counter + alt_json_uc_one_counter
    two = uc_two_counter + alt_json_uc_two_counter
    three = uc_three_counter + alt_json_uc_three_counter
    mongo_dict["measurements"]["AltJsonSamples"]["use_cases"]["UseCase1"] = dict(one)
    mongo_dict["measurements"]["AltJsonSamples"]["use_cases"]["UseCase2"] = dict(two)
    mongo_dict["measurements"]["AltJsonSamples"]["use_cases"]["UseCase3"] = dict(three)

    return mongo_dict


def postgres_statistic() -> dict:
    measurements = Measurement.objects.all()
    postgres_use_cases_dict = {}
    postgres_uc_total = measurements.values(
        "use_case"
    ).order_by(

    ).annotate(
        total=Count("use_case")
    )
    for use_case in list(postgres_uc_total):
        dict_key = None
        for k, v in use_case.items():
            if k == "use_case":
                dict_key = v
                postgres_use_cases_dict[dict_key] = {}

            postgres_use_cases_dict[dict_key].update({k: v})
            postgres_ft_total = measurements.filter(
                use_case=dict_key
            ).values(
                "food_type"
            ).order_by(

            ).annotate(
                total=Count("food_type")
            )
            food_key = None
            for food_type in postgres_ft_total:
                for value in food_type.values():
                    if isinstance(value, str):
                        food_key = value
                    else:
                        postgres_use_cases_dict[dict_key].update({food_key: value})

    return {
        "measurements": {
            "total": measurements.count(),
            "use_cases": postgres_use_cases_dict
        },
        "results": {
            "total": Result.objects.count()
        }
    }
