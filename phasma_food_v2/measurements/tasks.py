import pickle
import numpy as np
from django.conf import settings
from celery import shared_task

from .models import Measurement, Result
from .utils import _sensors


@shared_task
def measurement_rule_engine(validated_data: dict) -> None:
    results_final = get_results(validated_data)
    measurement = Measurement.objects.select_related(
        "mobile"
    ).get(
        sample_id=validated_data.get("sample_id")
    )
    fcm_mobile = measurement.mobile
    context = {"sampleID": measurement.sample_id,
               "VIS": results_final["VIS"],
               "NIR": results_final["NIR"],
               "FLUO": results_final["FLUO"],
               "FUSION": results_final["FUSION"]
               }

    fcm_mobile.send_message(title="PhasmaFood notification for {}".format(measurement.owner.email),
                            body=context
                            )

    results = [result for result in results_final.values()]

    Result.objects.create(measurement=measurement, data=results)


def get_results(validated_data: dict) -> dict:
    result = {}
    for s in _sensors:
        result[s] = "N/A"

    loaded = load_model("{}{}".format(settings.MEDIA_ROOT, "/trained_models/smp_fusion_bagging.pkl"))
    vis = np.asarray([float(d['measurement']) for d in validated_data['vis']['preprocessed']]).reshape(1, -1)
    fluo = np.asarray([float(d['measurement']) for d in validated_data['fluo']['preprocessed']]).reshape(1, -1)
    nir = np.asarray([float(d['measurement']) for d in validated_data['nir']['preprocessed']]).reshape(1, -1)
    fusion = np.concatenate([vis, fluo, nir], axis=1)
    result['FUSION'] = loaded.predict(fusion)[0]
    return result


def load_model(path: str) -> pickle:
    with open(path, 'rb') as file:
        model = pickle.load(file)
    return model
