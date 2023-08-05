"""Allows to run HIRE locally outside the SMIF framework
# After smif upgrade:
#   make that automatically the parameters can be generated to be copied into smif format
# REMOVE HDD CODE PLOTTING
#TODO Revisit the writing out of np. files...(most complete: enduse, region, fueltype, hours)
#TODO Test if technology type can be left empty in technology spreadsheet, Try to remove tech_type
#TODO Write out full result. Then write function to aggregate accordingly
#TODO SIMple aggregation. Write out sectormodel, enduse, region, fueltypes.... --> Do all aggregation based on that
# MAKE SIMLPLE TABLE FOR READING IN FUELS
# correction factors on LAD level disaggregation? (load non-residential demand)
# Improve plotting and processing (e.g. saisonal plots)
# Weather station cleaning: Replace days with missing values
#TODO IMROVE PLOTTING (second round of geopanda classification)
#     Note
    ----
    Always execute from root folder. (e.g. energy_demand/energy_demand/main.py)

# Fix regional plots
# TEST NON CONSTRAINED MODE
"""
import os
import sys
import time
import logging
from collections import defaultdict
import numpy as np

from energy_demand.basic import basic_functions
from energy_demand.charts import resilience_project
from energy_demand.basic import date_prop
from energy_demand import model
from energy_demand.basic import testing_functions
from energy_demand.basic import lookup_tables
from energy_demand.assumptions import general_assumptions
from energy_demand.assumptions import strategy_vars_def
from energy_demand.read_write import data_loader
from energy_demand.read_write import write_data
from energy_demand.read_write import read_data
from energy_demand.scripts import s_disaggregation
from energy_demand.validation import lad_validation
from energy_demand.basic import demand_supply_interaction
from energy_demand.scripts import s_scenario_param
from energy_demand.scripts import init_scripts
from energy_demand.basic import logger_setup
from energy_demand.plotting import fig_enduse_yh
from energy_demand.geography import weather_region

def energy_demand_model(
        regions,
        data,
        assumptions,
        weather_stations,
        weather_yr,
        weather_by
    ):
    """Main function of energy demand model to calculate yearly demand

    Arguments
    ----------
    regions : list
        Regions
    data : dict
        Data container
    assumptions : dict
        Assumptions
    weather_yr: int
        Year of weather data

    Returns
    -------
    result_dict : dict
        A nested dictionary containing all data for energy supply model with
        timesteps for every hour in a year.
        [fueltype : region : timestep]
    modelrun_obj : dict
        Object of a yearly model run

    Note
    ----
    This function is executed in the wrapper
    """
    logging.info("... Number of modelled regions: %s", len(regions))

    modelrun = model.EnergyDemandModel(
        regions=regions,
        data=data,
        assumptions=assumptions,
        weather_stations=weather_stations,
        weather_yr=weather_yr,
        weather_by=weather_by)

    # Calculate base year demand
    fuels_in = testing_functions.test_function_fuel_sum(
        data, data['fuel_disagg'], data['criterias']['mode_constrained'], assumptions.enduse_space_heating)

    # Log model results
    write_data.logg_info(modelrun, fuels_in, data)

    return modelrun

if __name__ == "__main__":
    """
    """
    data = {}

    # Local path
    local_data_path = os.path.abspath('data')

    path_main = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), '..', "energy_demand/config_data"))

    # Load data
    data['criterias'] = {}
    data['criterias']['mode_constrained'] = True                    # True: Technologies are defined in ED model and fuel is provided, False: Heat is delievered not per technologies
    data['criterias']['virtual_building_stock_criteria'] = True     # True: Run virtual building stock model
    data['criterias']['spatial_calibration'] = False

    fast_model_run = False
    if fast_model_run == True:
        data['criterias']['write_txt_additional_results'] = False
        data['criterias']['validation_criteria'] = False    # For validation, the mode_constrained must be True
        data['criterias']['plot_crit'] = False
        data['criterias']['crit_plot_enduse_lp'] = False
        data['criterias']['writeYAML_keynames'] = False
    else:
        data['criterias']['write_txt_additional_results'] = True
        data['criterias']['validation_criteria'] = True
        data['criterias']['plot_crit'] = False
        data['criterias']['crit_plot_enduse_lp'] = True
        data['criterias']['writeYAML_keynames'] = True

    # -------------------
    # Other configuration
    # -------------------
    RESILIENCEPAPERPOUTPUT = True     # Output data for resilience paper

    # If the smif configuration files what to be written, set this to true. The program will abort after they are written to YAML files
    data['criterias']['writeYAML'] = False
    data['criterias']['reg_selection'] = False
    data['criterias']['reg_selection_csv_name'] = "msoa_regions_ed.csv" # CSV file stored in 'region' folder with simulated regions
    data['criterias']['MSOA_crit'] = False

    # --- Model running configurations
    user_defined_base_yr = 2015
    user_defined_weather_by = 2015
    user_defined_simulation_end_yr = 2050  # Used to create standard narrative

    # Simulated yrs
    simulated_yrs = [user_defined_base_yr, user_defined_simulation_end_yr]
    
    if len(sys.argv) > 1: #user defined arguments are provide
        weather_yrs_scenario = [2015]
        weather_yrs_scenario.append(int(sys.argv[1]))        # Weather year
        try:
            weather_station_count_nr = sys.argv[2]          # Weather station cnt
        except:
            weather_station_count_nr = []
    else:
        weather_yrs_scenario = [2015]                   # Default weather year
        weather_station_count_nr = []                   # Default weather year

    print("Information")
    print("-------------------------------------")
    print("weather_yrs_scenario:        " + str(weather_yrs_scenario))
    print("weather_station_count_nr:    " + str(weather_station_count_nr))

    # --- Region definition configuration
    name_region_set = os.path.join(local_data_path, 'region_definitions', "lad_2016_uk_simplified.shp")        # LAD

    #name_population_dataset = os.path.join(local_data_path, 'scenarios', 'uk_pop_high_migration_2015_2050.csv')
    #name_population_dataset = os.path.join(local_data_path, 'scenarios', 'uk_pop_constant_2015_2050.csv') # Constant scenario
    name_population_dataset = os.path.join(local_data_path, 'scenarios', 'MISTRAL_pop_gva', 'data', 'pop-a_econ-c_fuel-c/population__lad.csv') # Constant scenario
    # MSOA model run
    #name_region_set_selection = "msoa_regions_ed.csv"
    #name_region_set = os.path.join(local_data_path, 'region_definitions', 'msoa_uk', "msoa_lad_2015_uk.shp")    # MSOA
    #name_population_dataset = os.path.join(local_data_path, 'scenarios', 'uk_pop_high_migration_2015_2050.csv')

    # GVA datasets
    name_gva_dataset = os.path.join(local_data_path, 'scenarios', 'MISTRAL_pop_gva', 'data', 'pop-a_econ-c_fuel-c/gva_per_head__lad_sector.csv') # Constant scenario
    name_gva_dataset_per_head = os.path.join(local_data_path, 'scenarios', 'MISTRAL_pop_gva', 'data', 'pop-a_econ-c_fuel-c/gva_per_head__lad.csv') # Constant scenario

    # --------------------
    # Paths
    # --------------------
    name_scenario_run = "_result_local_{}".format(str(time.ctime()).replace(":", "_").replace(" ", "_"))

    data['paths'] = data_loader.load_paths(path_main)
    data['local_paths'] = data_loader.get_local_paths(local_data_path)

    path_new_scenario = os.path.abspath(os.path.join(os.path.dirname(local_data_path), "results", name_scenario_run))
    data['path_new_scenario'] = path_new_scenario
    data['result_paths'] = data_loader.get_result_paths(path_new_scenario)

    basic_functions.create_folder(path_new_scenario)
    logger_setup.set_up_logger(os.path.join(path_new_scenario, "plotting.log"))

    # ----------------------------------------------------------------------
    # Load data
    # ----------------------------------------------------------------------
    data['scenario_data'] = defaultdict(dict)
    data['lookups'] = lookup_tables.basic_lookups()
    data['enduses'], data['sectors'], data['fuels'] = data_loader.load_fuels(
        data['lookups']['submodels_names'], data['paths'], data['lookups']['fueltypes_nr'])

    data['regions'] = read_data.get_region_names(name_region_set)
    data['reg_nrs'] = len(data['regions']) #TODO MOVE TO ASSUMPTIONS

    reg_centroids = read_data.get_region_centroids(name_region_set)
    data['reg_coord'] = basic_functions.get_long_lat_decimal_degrees(reg_centroids)
    data['scenario_data']['population'] = data_loader.read_scenario_data(name_population_dataset)

    # Read GVA sector specific data
    data['scenario_data']['gva_industry'] = data_loader.read_scenario_data_gva(name_gva_dataset, all_dummy_data=False)
    data['scenario_data']['gva_per_head'] = data_loader.read_scenario_data(name_gva_dataset_per_head)

    # -----------------------------------------------------------------------
    # Create new folders
    # -----------------------------------------------------------------------
    basic_functions.del_previous_setup(data['result_paths']['data_results'])

    folders_to_create = [
        data['result_paths']['data_results_model_run_pop'],
        data['result_paths']['data_results_validation']]
    for folder in folders_to_create:
        basic_functions.create_folder(folder)

    # -----------------------------
    # Assumptions
    # -----------------------------
    data['assumptions'] = general_assumptions.Assumptions(
        submodels_names=data['lookups']['submodels_names'],
        base_yr=user_defined_base_yr,
        weather_by=user_defined_weather_by,
        simulation_end_yr=user_defined_simulation_end_yr,
        curr_yr=2015,
        simulated_yrs=simulated_yrs,
        paths=data['paths'],
        local_paths=data['local_paths'],
        enduses=data['enduses'],
        sectors=data['sectors'],
        fueltypes=data['lookups']['fueltypes'],
        fueltypes_nr=data['lookups']['fueltypes_nr'])

    # -----------------------------------------------------------------------------
    # Calculate population density for base year
    # -----------------------------------------------------------------------------
    region_objects = read_data.get_region_objects(name_region_set)
    data['pop_density'] = {}
    for region in region_objects:
        region_name = region['properties']['name']
        region_area = region['properties']['st_areasha']
        data['pop_density'][region_name] = data['scenario_data']['population'][data['assumptions'].base_yr][region_name] / region_area

    # -----------------------------------------------------------------------------
    # Load standard strategy variable values from .py file
    # Containing full information
    # -----------------------------------------------------------------------------
    default_streategy_vars = strategy_vars_def.load_param_assump(
        data['paths'],
        data['local_paths'],
        data['assumptions'],
        writeYAML=data['criterias']['writeYAML'])

    # -----------------------------------------------------------------------------
    # Load standard smif parameters and generate standard single timestep narrative for year 2050
    # -----------------------------------------------------------------------------
    strategy_vars = strategy_vars_def.load_smif_parameters(
        data_handle=default_streategy_vars,
        assumptions=data['assumptions'],
        default_streategy_vars=default_streategy_vars,
        mode='local')

    # -----------------------------------------
    # User defines stragey variable from csv files
    # -----------------------------------------
    _user_defined_vars = data_loader.load_user_defined_vars(
        default_strategy_var=default_streategy_vars,
        path_csv=data['local_paths']['path_strategy_vars'],
        simulation_base_yr=data['assumptions'].base_yr)

    strategy_vars = data_loader.replace_variable(_user_defined_vars, strategy_vars)

    # Replace strategy variables not defined in csv files)
    strategy_vars_out = strategy_vars_def.autocomplete_strategy_vars(
        strategy_vars, narrative_crit=True)
    data['assumptions'].update('strategy_vars', strategy_vars_out)

    # -----------------------------------------------------------------------------
    # Load necessary data
    # -------------------------------------------------------------------------------
    data['tech_lp'] = data_loader.load_data_profiles(
        data['paths'], data['local_paths'],
        data['assumptions'].model_yeardays,
        data['assumptions'].model_yeardays_daytype,)

    data['technologies'] = general_assumptions.update_technology_assumption(
        data['assumptions'].technologies,
        data['assumptions'].strategy_vars['f_eff_achieved'],
        data['assumptions'].strategy_vars['gshp_fraction_ey'])

    if data['criterias']['virtual_building_stock_criteria']:
        data['scenario_data']['floor_area']['rs_floorarea'], data['scenario_data']['floor_area']['ss_floorarea'], data['service_building_count'], rs_regions_without_floorarea, ss_regions_without_floorarea = data_loader.floor_area_virtual_dw(
            data['regions'],
            data['sectors'],
            data['local_paths'],
            data['scenario_data']['population'][data['assumptions'].base_yr],
            data['assumptions'].base_yr)

        # Add all areas with no floor area data
        data['assumptions'].update("rs_regions_without_floorarea", rs_regions_without_floorarea)
        data['assumptions'].update("ss_regions_without_floorarea", ss_regions_without_floorarea)

    print("Start Energy Demand Model with python version: " + str(sys.version), flush=True)
    print("-----------------------------------------------", flush=True)
    print("Number of Regions                        " + str(data['reg_nrs']), flush=True)

    # Obtain population data for disaggregation
    if data['criterias']['MSOA_crit']:
        name_population_dataset = data['local_paths']['path_population_data_for_disaggregation_MSOA']
    else:
        name_population_dataset = data['local_paths']['path_population_data_for_disaggregation_LAD']
    data['pop_for_disag'] =  data_loader.read_scenario_data(name_population_dataset)

    # Load weather temperature
    data['weather_stations'], data['temp_data'] = data_loader.load_temp_data(
        data['local_paths'],
        weather_yrs_scenario=weather_yrs_scenario,
        save_fig=path_new_scenario)

    # ------------------------------------------------------------
    # Disaggregate national energy demand to regional demands
    # ------------------------------------------------------------
    data['fuel_disagg'] = s_disaggregation.disaggr_demand(
        data, spatial_calibration=data['criterias']['spatial_calibration'])

    # ------------------------------------------------------------
    # Calculate spatial diffusion factors
    # ------------------------------------------------------------
    real_values = data['pop_density']
    f_reg, f_reg_norm, f_reg_norm_abs, crit_all_the_same = init_scripts.create_spatial_diffusion_factors(
        narrative_spatial_explicit_diffusion=data['assumptions'].strategy_vars['spatial_explicit_diffusion'],
        fuel_disagg=data['fuel_disagg'],
        regions=data['regions'],
        real_values=real_values,
        narrative_speed_con_max=data['assumptions'].strategy_vars['speed_con_max'])

    print("Criteria all regions the same:           " + str(crit_all_the_same), flush=True)

    # ------------------------------------------------
    # Calculate parameter values for every region
    # ------------------------------------------------
    regional_vars = init_scripts.spatial_explicit_modelling_strategy_vars(
        data['assumptions'].strategy_vars,
        data['assumptions'].spatially_modelled_vars,
        data['regions'],
        data['fuel_disagg'],
        f_reg,
        f_reg_norm,
        f_reg_norm_abs)
    data['assumptions'].update('strategy_vars', regional_vars)

    # -----------------------------------------------------------------
    # Calculate parameter values for every simulated year based on narratives
    # and add also general information containter for every parameter
    # -----------------------------------------------------------------
    print("... starting calculating values for every year", flush=True)
    regional_vars, non_regional_vars = s_scenario_param.generate_annual_param_vals(
        data['regions'],
        data['assumptions'].strategy_vars,
        simulated_yrs)

    # ------------------------------------------------
    # Calculate switches
    # ------------------------------------------------
    print("... starting calculating switches", flush=True)
    annual_tech_diff_params = init_scripts.switch_calculations(
        simulated_yrs,
        data,
        f_reg,
        f_reg_norm,
        f_reg_norm_abs,
        crit_all_the_same)
    for region in data['regions']:
        regional_vars[region]['annual_tech_diff_params'] = annual_tech_diff_params[region]

    data['assumptions'].update('regional_vars', regional_vars)
    data['assumptions'].update('non_regional_vars', non_regional_vars)

    # ------------------------------------------------
    # Spatial Validation
    # ------------------------------------------------
    if data['criterias']['validation_criteria'] == True:
        lad_validation.spatial_validation_lad_level(
            data['fuel_disagg'],
            data['lookups'],
            data['result_paths'],
            data['paths'],
            data['regions'],
            data['reg_coord'],
            data['criterias']['plot_crit'])

    # -----------------------------------
    # Only selection of regions to simulate
    # -------------------------------------
    if data['criterias']['reg_selection']:
        region_selection = read_data.get_region_selection(
            os.path.join(
                data['local_paths']['local_path_datafolder'],
                "region_definitions",
                data['criterias']['reg_selection_csv_name']))
        #region_selection = ['E02003237', 'E02003238']

        data['reg_nrs'] = len(region_selection)
    else:
        region_selection = data['regions']

    # -------------------------------------------
    # Create .ini file with simulation information
    # -------------------------------------------
    write_data.write_simulation_inifile(
        data['result_paths']['data_results'],
        data,
        region_selection)

    # Write population data to file
    for sim_yr in data['assumptions'].simulated_yrs:
        write_data.write_scenaric_population_data(
            sim_yr,
            os.path.join(data['path_new_scenario'], 'model_run_pop'),
            list(data['scenario_data']['population'][sim_yr].values()))

    # -----------------------
    # Main model run function
    # -----------------------
    for weather_yr in weather_yrs_scenario:
        print("... weather year: " + str(weather_yr), flush=True)
 
        # ---------------------------------------------
        # Make selection of weather stations and data
        # ---------------------------------------------
        if weather_station_count_nr == []:
            single_weather_station_crit = False
            weather_stations_cnt = range(1)  # use one to itearte over al
        else:
            single_weather_station_crit = True
            weather_stations_cnt = weather_station_count_nr

        for counter in weather_stations_cnt:

            if single_weather_station_crit:
                weather_stations, continue_calculation, station_id = weather_region.get_weather_station_selection(
                    data['weather_stations'],
                    counter=counter,
                    weather_yr=weather_yr,
                    weather_by=data['assumptions'].weather_by)
                simulation_name = str(weather_yr) + "__" + str(station_id)
            else:
                simulation_name = str(weather_yr) + "__" + "all_stations"
                continue_calculation = True
                weather_stations = data['weather_stations']

            if continue_calculation:

                for sim_yr in data['assumptions'].simulated_yrs:
                    print("Loal simulation for year:  " + str(sim_yr), flush=True)

                    # Set current year
                    setattr(data['assumptions'], 'curr_yr', sim_yr)

                    # --------------------------------------
                    # Update result_paths and create folders
                    # --------------------------------------
                    path_folder_weather_yr = os.path.join(data['path_new_scenario'], str(weather_yr))

                    data['result_paths'] = data_loader.get_result_paths(path_folder_weather_yr)

                    folders_to_create = [
                        path_folder_weather_yr,
                        data['result_paths']['data_results'],
                        data['result_paths']['data_results_PDF'],
                        data['result_paths']['data_results_validation'],
                        data['result_paths']['data_results_model_runs']]
                    for folder in folders_to_create:
                        basic_functions.create_folder(folder)

                    data['technologies'] = general_assumptions.update_technology_assumption(
                        data['assumptions'].technologies,
                        narrative_f_eff_achieved=data['assumptions'].non_regional_vars['f_eff_achieved'][sim_yr],
                        narrative_gshp_fraction_ey=data['assumptions'].non_regional_vars['gshp_fraction_ey'][sim_yr],
                        crit_narrative_input=False)

                    # ------------------------------------------
                    # Run model
                    # -------------------------------------------
                    sim_obj = energy_demand_model(
                        region_selection,
                        data,
                        data['assumptions'],
                        weather_stations,
                        weather_yr=weather_yr,
                        weather_by=data['assumptions'].weather_by)

                    # ------------------------------------------------
                    # Temporal Validation
                    # ------------------------------------------------
                    if data['criterias']['validation_criteria'] == True and sim_yr == data['assumptions'].base_yr:
                        lad_validation.spatio_temporal_val(
                            sim_obj.ed_fueltype_national_yh,
                            sim_obj.ed_fueltype_regs_yh,
                            data['lookups']['fueltypes'],
                            data['result_paths'],
                            data['paths'],
                            region_selection,
                            data['assumptions'].seasons,
                            data['assumptions'].model_yeardays_daytype,
                            data['criterias']['plot_crit'])

                    # -------------------------
                    # Write for resilience paper
                    # -------------------------
                    if RESILIENCEPAPERPOUTPUT:

                        if round(np.sum(sim_obj.ed_fueltype_national_yh), 2) != round(np.sum(sim_obj.results_unconstrained), 2):
                            print(round(np.sum(sim_obj.ed_fueltype_national_yh), 2))
                            print(round(np.sum(sim_obj.results_unconstrained), 2))
                            raise Exception("Should be the same")

                        resilience_project.resilience_paper(
                            sim_yr,
                            data['result_paths']['data_results_model_runs'],
                            "resilience_paper",
                            "result_risk_paper_{}_".format(sim_yr),
                            sim_obj.results_unconstrained,
                            ['residential', 'service', 'industry'],
                            data['regions'],
                            data['lookups']['fueltypes'],
                            fueltype_str='electricity')

                    # -------------------------------------
                    # # Generate YAML file with keynames for `sector_model`
                    # -------------------------------------
                    if data['criterias']['writeYAML_keynames']:
                        if data['criterias']['mode_constrained']:

                            supply_results = demand_supply_interaction.constrained_results(
                                sim_obj.results_constrained,
                                sim_obj.results_unconstrained,
                                data['assumptions'].submodels_names,
                                data['lookups']['fueltypes'],
                                data['technologies'])

                            write_data.write_yaml_output_keynames(
                                data['local_paths']['yaml_parameters_keynames_constrained'], supply_results.keys())
                        else:
                            supply_results = demand_supply_interaction.unconstrained_results(
                                sim_obj.results_unconstrained,
                                data['assumptions'].submodels_names,
                                data['lookups']['fueltypes'])

                            write_data.write_yaml_output_keynames(
                                data['local_paths']['yaml_parameters_keynames_unconstrained'], supply_results.keys())

                    # --------------------------
                    # Write out all calculations
                    # --------------------------
                    if data['criterias']['write_txt_additional_results']:

                        if data['criterias']['crit_plot_enduse_lp']:

                            # Maybe move to result folder in a later step
                            path_folder_lp = os.path.join(data['result_paths']['data_results'], 'individual_enduse_lp')
                            basic_functions.delete_folder(path_folder_lp)
                            basic_functions.create_folder(path_folder_lp)

                            winter_week, _, _, _ = date_prop.get_seasonal_weeks()

                            # Plot electricity
                            for enduse, ed_yh in sim_obj.tot_fuel_y_enduse_specific_yh.items():
                                fig_enduse_yh.run(
                                    name_fig="individ__electricity_{}_{}".format(enduse, sim_yr),
                                    path_result=path_folder_lp,
                                    ed_yh=ed_yh[data['lookups']['fueltypes']['electricity']],
                                    days_to_plot=winter_week)

                        # -------------------------------------------
                        # Write annual results to txt files
                        # -------------------------------------------
                        print("... Start writing results to file")
                        path_runs = data['result_paths']['data_results_model_runs']

                        write_data.write_supply_results(
                            sim_yr,
                            "result_tot_yh",
                            path_runs,
                            sim_obj.ed_fueltype_regs_yh,
                            "result_tot_submodels_fueltypes")
                        write_data.write_enduse_specific(
                            sim_yr,
                            path_runs,
                            sim_obj.tot_fuel_y_enduse_specific_yh,
                            "out_enduse_specific")
                        write_data.write_lf(
                            path_runs,
                            "result_reg_load_factor_y",
                            [sim_yr],
                            sim_obj.reg_load_factor_y,
                            'reg_load_factor_y')
                        write_data.write_lf(
                            path_runs,
                            "result_reg_load_factor_yd",
                            [sim_yr],
                            sim_obj.reg_load_factor_yd,
                            'reg_load_factor_yd')
                        '''write_data.write_lf(
                            path_runs,
                            "result_reg_load_factor_winter",
                            [sim_yr],
                            sim_obj.reg_seasons_lf['winter'],
                            'reg_load_factor_winter')
                        write_data.write_lf(
                            path_runs,
                            "result_reg_load_factor_spring",
                            [sim_yr],
                            sim_obj.reg_seasons_lf['spring'],
                            'reg_load_factor_spring')
                        write_data.write_lf(
                            path_runs,
                            "result_reg_load_factor_summer",
                            [sim_yr],
                            sim_obj.reg_seasons_lf['summer'],
                            'reg_load_factor_summer')
                        write_data.write_lf(
                            path_runs,
                            "result_reg_load_factor_autumn",
                            [sim_yr],
                            sim_obj.reg_seasons_lf['autumn'],
                            'reg_load_factor_autumn')'''

                        print("... Finished writing results to file")

                    #remove garbage
                    del sim_obj

    print("-------------------------")
    print("... Finished running HIRE")
    print("-------------------------")
