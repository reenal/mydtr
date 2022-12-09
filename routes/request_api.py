"""The Endpoints to manage the BOOK_REQUESTS"""
import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
from validate_email import validate_email
from IEC_model_HST_LOL_v3 import *

REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/requestwelcome', methods=['GET'])
def welcome():
    """Return Welcome message

    """
    return "Welcome All"


@REQUEST_API.route('/transformer_specification_IEC', methods=["POST"])
def transformer_specification_IEC():
    """ thia api for is transformer specification for IEC model.
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    if not data.get('power'):
        abort(400)

    # P = data.get("power")
    # V1 = data.get("primary voltage")
    # V2 = data.get("secondary voltage")
    # LOL_rated = data.get("loss ratio at rated load")
    # T_ref = data.get("temperature reference")
    # Theta_t  = data.get("temperature rise of top oil over ambient")
    # T_avg  = data.get("temperature rise of average oil")
    # T_w  = data.get("temperature rise of winding")
    # HST_w = data.get("hot spot temperature rise of winding")
    # T_amb = data.get("rated ambient temperature")
    # F_hst1 = data.get("primary winding hotspot factor")
    # F_hst2 = data.get("secondary winding hotspot factor")
    # I_hv = data.get("rated HV current")
    # I_lv  = data.get("rated LV current")
    # Rc_hv = data.get("cold resistance of HV winding")
    # Rc_lv   = data.get("cold resistance of LV winding")
    # Rh_hv = data.get("hot resistance of HV winding")
    # Rh_lv  = data.get("hot resistance of LV winding")
    # W_s = data.get("weight core")
    # W_t = data.get("weight tank")
    # W_o = data.get("weight oil")
    # W_w = data.get("weight coil")
    # Tau = data.get("oil time constant")
    # Mode = data.get("cooling operation")

    # return "Hello data sumbited"
    return jsonify({"power": data['power']})


@REQUEST_API.route('/api/v1/model/iec/format/raw_IEC', methods=["POST"])
def iec_raw_IEC():
    """ this api for /api/v1/model/iec/format/raw_IEC.
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    collectedData = data.get("collectedData")
    transformerSpec = data.get("transformerSpec")

    # working
    # transformerSpec['power']

    return jsonify({"temp": collectedData[0]['temperature']})


@REQUEST_API.route('/api/v1/model/iec/format/current', methods=["POST"])
def iec_raw_per_timestamp():
    """ this api for /api/v1/model/iec/format/current.
    """
    is_old = ""
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    current_collected_data = data.get("current_data_per_timestamp")
    transformer_spec = data.get("transformer_spec")

    # working
    # transformerSpec['power']
    # current_data_per_timestamp['time_step_in_minutes']
    # current_data_per_timestamp['temperature']

    prev_output = data.get("prev_output")  # {is_old: 1, T_o: 12, Dt_h1: 14, Dt_h2: 15, LOL:99}
    if not prev_output:
        prev_output = {"status": 'no_prev_value'}
        # prev_output={"status": 'has_prev_value', "T_o": 12, "Dt_h1": 14, "Dt_h2": 15, "LOL": 99}
        # prev_output = {"is_old": 0,"Tim": "2017-02-14 01:00:00"}

    else:
        try:
            if not prev_output['T_o'] or not prev_output['Dt_h1'] or not prev_output['Dt_h2'] \
                    or not prev_output['LOL'] or not current_collected_data["time_step_in_minutes"] \
                    or not current_collected_data["temperature"] or not current_collected_data["load"] \
                    or not transformer_spec["rated_hot_spot_temperature"] or not transformer_spec[
                "rated_activation_energy_paper"] \
                    or not transformer_spec["activation_energy_paper"] or not transformer_spec[
                "a_rated_paper_insulation"] \
                    or not transformer_spec["a_paper_insulation"] or not transformer_spec["exp_power_of_oil_exponent"] \
                    or not transformer_spec["empirical_constant_3"] or not transformer_spec["empirical_constant_2"] \
                    or not transformer_spec["empirical_constant_1"] or not transformer_spec[
                "exp_power_of_winding_exponent"] \
                    or not transformer_spec["loss_ration_at_rated_load"] or not transformer_spec[
                "winding_time_constant"] \
                    or not transformer_spec["oil_time_constant"] or not transformer_spec["temp_rise_oil"] \
                    or not transformer_spec["hot_spot_to_top_oil"]:
                return jsonify({"status": 'error', "errorType": 'error_missing_parameter', "error": "parameter is empty"})
            else:
                output = IEC60076in(current_collected_data, transformer_spec, prev_output)
                if type(output) is dict:
                    return jsonify({"output": output, "status": 'calculated'})
                else:
                    return jsonify({"status": 'error', "errorType": output, "error": "divide by zero exception "})
        except KeyError:
            return jsonify({'status': "error", 'errorType': "json_not_proper", "error": "keyError key is missing in json"})


@REQUEST_API.route('/api/v1/model/ieee/format/raw_IEEE', methods=["POST"])
def ieee_raw_IEEE():
    """ this api for api/v1/model/ieee/format/raw_IEEE.
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    collectedData = data.get("collectedData")
    transformerSpec = data.get("transformerSpec")

    # working
    # transformerSpec['power']

    return jsonify({"temp": collectedData[0]['temperature']})
