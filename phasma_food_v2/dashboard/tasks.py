import os
import shutil
from typing import List

from django.conf import settings
from django.core.mail import EmailMessage
from celery import shared_task

from phasma_food_v2.measurements.models import Measurement
from phasma_food_v2.samples.mongo_db import MongoDB
from .utils import excel_zip


@shared_task
def create_excel_to_zip(email: str, measurements: List[str]) -> None:
    """Task check if excel files and zip are prepared.
    If not, it will create them and send via email.
    """
    folder_name = email.split("@")[0]
    location = settings.MEDIA_ROOT
    full_folder_path = "{}/excel/".format(location)
    if not os.path.exists("{}{}".format(full_folder_path, folder_name)):
        full_folder_path, folder_name = excel_zip(
            email=email,
            measurements=measurements
        )
    message = EmailMessage(
        subject="Collection of PhasmaFOOD measurements",
        body="In the attached .zip archive you have Excel tables for all measurements which "
             "you have selected for download on the Phasma Food web dashboard.",
        from_email=settings.ADMINS[0][1],
        to=[email],
    )
    message.content_subtype = "html"
    message.attach_file("{}{}.zip".format(
        full_folder_path,
        folder_name.replace(".", ""))
    )
    message.send()
    shutil.rmtree("{}{}".format(
        full_folder_path,
        folder_name)
    )
    os.remove("{}{}.zip".format(
        full_folder_path,
        folder_name.replace(".", ""))
    )


@shared_task
def save_to_mongo(
    measurements: List[str], db: str = settings.MONGO_DEFAULT_DB, collection: str = settings.MONGO_DEFAULT_COLLECTION
) -> None:
    """Push measurement from Postgresql to Mongo DB."""

    measurements_all = Measurement.objects.all()
    measurements_filtered = measurements_all.filter(sample_id__in=measurements)
    for measurement in measurements_filtered:
        measurement_data_time = measurement.date_created
        white_reference = measurements_all.filter(
            use_case="White Reference"
        ).filter(
            date_created__lt=measurement_data_time
        ).order_by(
            '-date_created'
        ).first()
        mongo_dict = {"sampleId": measurement.sample_id, "laboratory": measurement.laboratory,
                      "foodType": measurement.food_type, "useCase": measurement.use_case,
                      "granularity": measurement.granularity, "mycotoxins": measurement.mycotoxins,
                      "temperature": measurement.temperature,
                      "tempExposureHours": measurement.temperature_exposure_hours,
                      "microbioSampleId": measurement.microbiological_id,
                      "microbiologicalUnit": measurement.microbiological_unit,
                      "microbiologicalValue": measurement.microbiological_value,
                      "otherSpecies": measurement.other_species, "foodSubtype": measurement.food_subtype,
                      "adulterationSampleId": measurement.adulteration_id, "alcoholLabel": measurement.alcohol_label,
                      "authentic": measurement.authentic, "puritySMP": measurement.purity_smp,
                      "lowValueFiller": measurement.low_value_filler, "nitrogenEnhancer": measurement.nitrogen_enhancer,
                      "hazardOneName": measurement.hazard_one_name, "hazardOnePct": measurement.hazard_one_pct,
                      "hazardTwoName": measurement.hazard_two_name, "hazardTwoPct": measurement.hazard_two_pct,
                      "dilutedPct": measurement.diluted_pct, "package": measurement.package,
                      "dateTime": measurement.date_created.isoformat(), "adul": measurement.adulterated,
                      "configuration": measurement.configuration,
                      "whiteReferenceTime": measurement.white_reference_time,
                      "aflatoxin": {
                          "name": measurement.aflatoxin_name,
                          "value": measurement.aflatoxin_value,
                          "unit": measurement.aflatoxin_unit
                      }
                      }

        if measurement.vis:
            wave = [data["wave"] for data in measurement.vis["rawData"][0]]
            mongo_dict["VIS"] = {"wave": wave}

            raw_data = [x["measurement"] for data in measurement.vis["rawData"] for x in data]
            mongo_dict["VIS"] = {"data": raw_data}

            avg_data = [data["measurement"] for data in measurement.vis["avgData"]]
            mongo_dict["VIS"].update({"avgData": avg_data})

            if white_reference:
                raw_dark_for_white = [data["measurement"] for data in white_reference.vis["rawDark"]]
                mongo_dict["VIS"].update({"dark_for_white": raw_dark_for_white})

            raw_dark = [x["measurement"] for data in measurement.vis["rawDark"] for x in data]
            mongo_dict["VIS"].update({"dark": raw_dark})

            avg_dark = [data["measurement"] for data in measurement.vis["avgDark"]]
            mongo_dict["VIS"].update({"avgDark": avg_dark})

            raw_white = [x["measurement"] for data in measurement.vis["rawWhite"] for x in data]
            mongo_dict["VIS"].update({"white": raw_white})

            avg_white = [data["measurement"] for data in measurement.vis["avgWhite"]]
            mongo_dict["VIS"].update({"avgWhite": avg_white})

            preprocessed = [data["measurement"] for data in measurement.vis["preprocessed"]]
            mongo_dict["VIS"].update({"preprocessed": preprocessed})

            dark_reference = [data["measurement"] for data in measurement.vis["darkReference"]]
            mongo_dict["VIS"].update({"darkReference": dark_reference})

            white_reference = [data["measurement"] for data in measurement.vis["whiteReference"]]
            mongo_dict["VIS"].update({"whiteReference": white_reference})
        else:
            mongo_dict["VIS"] = {}

        if measurement.nir:
            wave = [data["wave"] for data in measurement.nir["preprocessed"]]
            mongo_dict["NIR"] = {"wave": wave}

            preprocessed = [data["measurement"] for data in measurement.nir["preprocessed"]]
            mongo_dict["NIR"] = {"preprocessed": preprocessed}

            dark_reference = [data["measurement"] for data in measurement.nir["darkReference"]]
            mongo_dict["NIR"].update({"darkReference": dark_reference})

            white_reference = [data["measurement"] for data in measurement.nir["whiteReference"]]
            mongo_dict["NIR"].update({"whiteReference": white_reference})
        else:
            mongo_dict["NIR"] = {}

        if measurement.fluo:
            wave = [data["wave"] for data in measurement.fluo["rawData"][0]]
            mongo_dict["FLUO"] = {"wave": wave}

            raw_data = [x["measurement"] for data in measurement.fluo["rawData"] for x in data]
            mongo_dict["FLUO"] = {"data": raw_data}

            avg_data = [data["measurement"] for data in measurement.fluo["avgData"]]
            mongo_dict["FLUO"].update({"avgData": avg_data})

            raw_dark = [x["measurement"] for data in measurement.fluo["rawDark"] for x in data]
            mongo_dict["FLUO"].update({"dark": raw_dark})

            avg_dark = [data["measurement"] for data in measurement.fluo["avgDark"]]
            mongo_dict["FLUO"].update({"avgDark": avg_dark})

            raw_white = [x["measurement"] for data in measurement.fluo["rawWhite"] for x in data]
            mongo_dict["FLUO"].update({"white": raw_white})

            avg_white = [data["measurement"] for data in measurement.fluo["avgWhite"]]
            mongo_dict["FLUO"].update({"avgWhite": avg_white})

            preprocessed = [data["measurement"] for data in measurement.fluo["preprocessed"]]
            mongo_dict["FLUO"].update({"preprocessed": preprocessed})

            dark_reference = [data["measurement"] for data in measurement.fluo["darkReference"]]
            mongo_dict["FLUO"].update({"darkReference": dark_reference})

            white_reference = [data["measurement"] for data in measurement.fluo["whiteReference"]]
            mongo_dict["FLUO"].update({"whiteReference": white_reference})
        else:
            mongo_dict["FLUO"] = {}

        client = MongoDB()
        client.insert_one(
            measurement=mongo_dict,
            db=db,
            collection=collection
        )
