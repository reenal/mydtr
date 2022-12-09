# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 16:26:00 2021
@author: kmor
edited: lenaar
install pytest and run test:
> pip install -U pytest
> pytest IEC_model_HST_LOL_v2.py
"""

import numpy as np
import math
# 0. Constants
RG = 8.314  # Gas Constant [J/K.mol]


def IEC60076in(current_data_per_timestamp, transformer_spec, pre_value):

    #tspec={}y
    try:
        tspec = transformer_spec
        cdata = current_data_per_timestamp
        prev = pre_value
        output = {}

        #tspec["DT_hr"] = transformer_spec["hot_spot_to_top_oil"]
        tspec["DT_hr"] = tspec["hot_spot_to_top_oil"]
        tspec["DT_or"] = tspec["temp_rise_oil"]
        tspec["ta_o"] = tspec["oil_time_constant"]
        tspec["ta_w"] = tspec["winding_time_constant"]
        tspec["R"] = tspec["loss_ration_at_rated_load"]
        tspec["y"] = tspec["exp_power_of_winding_exponent"]
        tspec["k11"] = tspec["empirical_constant_1"]
        tspec["k21"] = tspec["empirical_constant_2"]
        tspec["k22"] = tspec["empirical_constant_3"]
        tspec["x"] = tspec["exp_power_of_oil_exponent"]
        tspec["A"] = tspec["a_paper_insulation"]
        tspec["Ar"] = tspec["a_rated_paper_insulation"]
        tspec["Ea"] = tspec["activation_energy_paper"]
        tspec["Ear"] = tspec["rated_activation_energy_paper"]
        tspec["t_hr"] = tspec["rated_hot_spot_temperature"]

        cdata["K_m"] = cdata["load"]
        cdata["T_amb"] = cdata["temperature"]
        #cdata["Time"] = cdata["timestamp"]

        # Calculate the initial conditions
        # Initialize variables

        T_o = 0   # internal Top-oil temperature
        Dt_h2 = 0   # \Delta t_{h2}
        DDt_h2 = 0   # D\Delta t_{h2}
        Dt_h1 = 0   # \Delta t_{h1}
        DDt_h1 = 0   # D\Delta t_{h1}
        Dt_o = 0   # D t_{o}
        Dt_h = 0   # D t_{h}
        t_h = 0   # t_{h}
        DLOL = 0   # D.LOL
        LOLnew = 0   # LOL
        T_onew = 0
        Dt_h1new = 0
        Dt_h2new = 0
        V = 0      # Aging
        a1 = 0
        a2 = 0

        # time interval from a collected data
        minutes_step = cdata["time_step_in_minutes"]


    # This part decided where it is the first time running the code or not
        if prev and prev["status"] == 'has_prev_value':
            T_o = prev["T_o"]
            Dt_h1 = prev["Dt_h1"]
            Dt_h2 = prev["Dt_h2"]
            LOL = prev["LOL"]
        else:  # no_prev_value
            T_o = (((1+(cdata["K_m"]**(2))*tspec["R"])/(1+tspec["R"])) **
                   (tspec["x"]))*tspec["DT_or"] + cdata["T_amb"]  # Eq. 5 [°C]
            # Initial value of \theta_{h1}
            Dt_h1 = tspec["k21"] * \
                cdata["K_m"]**(tspec["y"])*tspec["DT_hr"]   # Eq. 7 [K]
            # Initial value of \theta_{h2}
            Dt_h2 = (tspec["k21"]-1)*cdata["K_m"]**(tspec["y"]) * \
                tspec["DT_hr"]    # Eq.8 [K]
            # Initial value Loss of Life
            LOL = 0

        # 4. Solve the difference equation
        # Calculate D\theta_{o} Eq. 18 [°C]
        a1 = (minutes_step/(tspec["k11"]*tspec["ta_o"]))
        a2 = (1+(cdata["K_m"]**2)*tspec["R"])/(1+tspec["R"])
        Dt_o = a1*(tspec["DT_or"]*a2**(tspec["x"])-(T_o-cdata["T_amb"]))
        # Dt_o = ((1+cdata["K_m"]**2*tspec["R"])/(1+tspec["R"]))**(tspec["x"])*Delta_theta_or-(theta_o[t-1]-theta_a[t])
        # Calculate \theta_{o} Eq. 19 [°C]
        T_onew = T_o + Dt_o
        # Calculate D\theta_{h1} Eq. 20 [°C]
        b1 = (minutes_step/(tspec["k22"]*tspec["ta_w"]))
        DDt_h1 = b1*(tspec["k21"]*tspec["DT_hr"]*cdata["K_m"]
                     ** (tspec["y"]) - Dt_h1)

        Dt_h1new = Dt_h1 + DDt_h1
        # Calculate D\theta_{h2} Eq.21 [°C]
        c1 = (minutes_step/((1/tspec["k22"])*tspec["ta_o"]))
        DDt_h2 = c1*((tspec["k21"]-1)*tspec["DT_hr"] *
                     cdata["K_m"]**(tspec["y"]) - Dt_h2)
        Dt_h2new = Dt_h2 + DDt_h2
        # Total hot-spot temperature Eq.22 [°C]
        Dt_h = Dt_o + Dt_h1new - Dt_h2new
        # Hot spot temperature [°C]
        t_h = T_onew + Dt_h
        # Relative aging Eq. A4 []
        V = (tspec["A"]/tspec["Ar"])*np.exp((1/RG) *
                                            ((tspec["Ear"]/(tspec["t_hr"] + 273)) - (tspec["Ea"]/(t_h + 273))))
        # Loss of lige Eq. 4 [min]
        DLOL = V*minutes_step
        LOLnew = DLOL + LOL

        output["time_step_in_minutes"] = minutes_step  # to keep history
        output["T_o"] = T_o  # top oil temperature
        output["T_hst"] = t_h  # hot spot temperature
        output["T_amb"] = cdata["T_amb"]  # ambient temperature
        output["DLOL"] = DLOL  # loss of live
        output["LOL"] = LOLnew  # cummulative loss of life
        # moved from prev
        output["Dt_h1"] = Dt_h1
        output["Dt_h2"] = Dt_h2

        print("Data has been calculated successfully", output)
        return output
    except Exception as err:
        exception_type = type(err).__name__
        #print(exception_type)
        return exception_type

# to run test you need install pytest
# run pip install -U pytest
# run in terminal (you should be in the same folder as test file)
# pytest name_of_your_file.py, f.e.:
# pytest IEC_model_HST_LOL.py


def test_without_prev_value_IEC60076in_1():
    test_current_data_per_timestamp_1 = {
        "time_step_in_minutes": 2,
        "temperature": 30,  # Vector with the ambient temperature in °C # temperature??
        "load": 150  # Load factor Data
    }
    test_transformer_spec_1 = {
        # Top-oil (in tank) temperature rise in steady state at rated losses [K]
        "temp_rise_oil": 1,
        # Hot-spot-to-top-oil (in tank) gradient at rated current [K]
        "hot_spot_to_top_oil": 2,
        "oil_time_constant": 3,  # Oil time constant  [min]
        "winding_time_constant": 4,  # Winding time constant [min]
        "loss_ration_at_rated_load": 5,  # Ratio of load losses ar rated current to no-load losses at rated voltage []
        # Exponential power of current vs winding temperature rise (winding exponent)
        "exp_power_of_winding_exponent": 6,
        "empirical_constant_1": 7,  # Empirical Constant []
        "empirical_constant_2": 8,  # Empirical Constant []
        "empirical_constant_3": 9,  # Empirical Constant []
        # Exponential power of total losses vs top-oil(in tank) temperature rise (oil-exponent)
        "exp_power_of_oil_exponent": 10,
        "a_paper_insulation": 11,  # A-value for paper insulation [1/hour]
        "a_rated_paper_insulation": 12,  # A-value for paper insulation rated [1/hour]
        "activation_energy_paper": 14,  # Activation energy paper (kJ/mol)
        "rated_activation_energy_paper": 15,  # Rated activation energy paper (kJ/mol)
        "rated_hot_spot_temperature": 17,  # Rated hot spot temperature (°C)
    }

    test_prev_output_1 = {
        "status": 'no_prev_value'
    }

    test_output_1 = {
        "time_step_in_minutes": 2,
        "T_o": 5.37095265917351e+42,  # 5.37095265917351e+42,
        "T_hst": 5.37095265917351e+42,  # 6.393991260920845e+42,
        "T_amb": 30,  # 30,
        "DLOL":  1.8447746582949462,  # 1.8447746582949462,
        "LOL":  1.8447746582949462,  # 1.8447746582949462,
        "Dt_h1": 182250000000000,  # 182250000000000,
        "Dt_h2":  159468750000000  # 159468750000000
    }

    assert IEC60076in(test_current_data_per_timestamp_1, test_transformer_spec_1,
                      test_prev_output_1) == test_output_1


# Output is taken from prev version  which was wrong, it took prev data instead of calculated, while LOL was taken from calculated
# old {'name': 'model_3', 'is_old': 1, 'T_o': 5.37095265917351e+42, 'Dt_h1': 182250000000000, 'Dt_h2': 159468750000000, 'LOL': 1.8447746582949462, 'Tim': 3}
# OUT {'name': 'model_4', 'Time': 3, 'T_o': 5.37095265917351e+42, 'T_hst': 6.393991260920845e+42, 'DLOL': 1.8447746582949462, 'LOL': 1.8447746582949462, 'T_amb': 30}

# new data when all data is calculated and not taken from prev
# Data has been calculated successfully
# {'Time': 3, 'T_o': 5.37095265917351e+42, 'T_hst': 5.37095265917351e+42, 'T_amb': 30, 'DLOL': 1.8447746582949462, 'LOL': 1.8447746582949462, 'Dt_h1': 182250000000000, 'Dt_h2': 159468750000000}

def test_with_prev_value_IEC60076in_2():

    test_current_data_per_timestamp_1 = {
        "time_step_in_minutes": 2,
        "temperature": 30,  # Vector with the ambient temperature in °C # temperature??
        "load": 150 , # Load factor Data
        #"timestamp":""

    }
    test_transformer_spec_1 = {
        # Top-oil (in tank) temperature rise in steady state at rated losses [K]
        "temp_rise_oil": 1,
        # Hot-spot-to-top-oil (in tank) gradient at rated current [K]
        "hot_spot_to_top_oil": 2,
        "oil_time_constant": 3,  # Oil time constant  [min]
        "winding_time_constant": 4,  # Winding time constant [min]
        "loss_ration_at_rated_load": 5,  # Ratio of load losses ar rated current to no-load losses at rated voltage []
        # Exponential power of current vs winding temperature rise (winding exponent)
        "exp_power_of_winding_exponent": 6,
        "empirical_constant_1": 7,  # Empirical Constant []
        "empirical_constant_2": 8,  # Empirical Constant []
        "empirical_constant_3": 9,  # Empirical Constant []
        # Exponential power of total losses vs top-oil(in tank) temperature rise (oil-exponent)
        "exp_power_of_oil_exponent": 10,
        "a_paper_insulation": 11,  # A-value for paper insulation [1/hour]
        "a_rated_paper_insulation": 12,  # A-value for paper insulation rated [1/hour]
        "activation_energy_paper": 14,  # Activation energy paper (kJ/mol)
        "rated_activation_energy_paper": 15,  # Rated activation energy paper (kJ/mol)
        "rated_hot_spot_temperature": 17,  # Rated hot spot temperature (°C)
    }

    test_prev_output_1 = {
        # Boolean with information if there is information about old data
        "status": 'has_prev_value',
        "T_o": 70,  # Top-oil temperature at the load considered [K]
        "Dt_h1": 5.5,  # Hot-spot-to-top-oil gradient at the load in 1 [K]
        "Dt_h2": 98,  # Hot-spot-to-top-oil gradient at the load in 1 [K]
        "LOL": 0.4,  # Loss of life [hours/hour]
        "Tim": 1,  # Previous timestamp
    }

    test_output_1 = {
        "time_step_in_minutes": 2,
        "T_o": 70,  # 5.37095265917351e+42,
        "T_hst": 1.0230386017473352e+42,  # 6.393991260920845e+42,
        "T_amb": 30,  # 30,
        "DLOL": 1.8447746582949462,  # 1.8447746582949462,
        "LOL": 2.244774658294946,  # 1.8447746582949462,
        "Dt_h1": 5.5,  # 182250000000000,
        "Dt_h2": 98  # 159468750000000
    }

    assert IEC60076in(test_current_data_per_timestamp_1,
                      test_transformer_spec_1,test_prev_output_1) == test_output_1

# after all data are taken from prev value
# Data has been calculated successfully {'Time': 3, 'T_o': 70, 'T_hst': 1.0230386017473352e+42, 'T_amb': 30, 'DLOL': 1.8447746582949462, 'LOL': 2.244774658294946, 'Dt_h1': 5.5, 'Dt_h2': 98}