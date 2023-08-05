import requests
import os
import json
import uuid
import time
from enum import Enum
from oauthlib.oauth2 import LegacyApplicationClient, InvalidGrantError
from requests_oauthlib import OAuth2Session
import atexit
import numbers

from openlab import credentials, login, piController, logger


valid_results = [
        "SPP","DownholeECD","FlowRateOut","HookLoad","SurfaceTorque",
        "BitDepth", "TD", "ChokeOpening", "DownholePressure", "ChokePressure",
        "FluidTemperatureOut", "WOB", "InstantaneousROP", "BOPChokeOpening",
        "FlowRateIn", "TopOfStringVelocity", "SurfaceRPM", "ChokePumpFlowRateIn",
        "DrillstringTemperature", "TotalInfluxMass", "CalculatedPressureBottomHole",
        "CuttingsMassFractionTransient", "GasVolumeFraction", "DrillstringBucklingLimit",
        "FluidTemperatureIn", "AnnulusECD", "DrillstringTorqueLimit", "AnnulusTemperature",
        "DrillstringTension", "AnnulusFluidVelocity", "DrillstringFluidVelocity", "CuttingsBedHeight",
        "AnnulusDensity", "DrillstringTorque", "ActivePit", "TotalMudLossMass", "Connection",
        "TopOfStringPosition"
        ]

class http_client(object):
    sim = None
    max_results_attempts=50
    max_init_attempts=100
    """
    A utility class for using the openLab RESTfull API
    """ 
    def __init__(self, proxies = {}):
        print("Initializing http client...")
        self.url= credentials.OPENLAB_URL
        self.user = credentials.email
        self.openlab = credentials.client_id # UNUSED - DELETE THIS 
        self.api_key = credentials.api_key
        if self.user == "email@domain.com":
            raise Exception("You need to enter your email address associated with your OpebLab account in credientials.py and re-install OpenLab package with pip")
        if self.api_key == 'PUT API KEY HERE':
            raise Exception("You need to enter your API Key in credientials.py before you can use the client and re-install OpenLab package with pip")

        #create and validate the oauth client
        self.client= login.create_token(proxies = proxies) # returns an oauth session
        self.check_login_worked()

        # see if there there is another server url that the web client has decided would be better to use
        if 'EndpointUrl' in self.whoami().keys():
            self.url = self.whoami()['EndpointUrl']

    def check_login_worked(self):
        #first, we check for invalid grant errors
        try:
            r=self.client.get(self.url+"/users/whoami") #random method to call web api, so that we can check the response code
            if r.status_code != 200:
                print("Call to whoami failed with HTTP Code: {}. Attempting to create new token".format(r.status_code))
                self.client = login.create_token()
            else:
                print("Login Succesfull")

        except InvalidGrantError:
            print("Invalid Grant Exception Thrown. Attempting to create new token")
            self.client = login.create_token()
        return 

    def get_custom_endpoint(self, endpoint_url):
        """Call a custom endpoint url.
        Current endpoint urls can be found at openlab.iris.no/swagger"""
        r = self.client.get(self.url + endpoint_url)
        return r.json()

    def labels(self):
        r=self.client.get(self.url+"/labels/")
        return self.standard_response(r, 200) 

    def labels_by_id(self, config_id):
        r=self.client.get(self.url+"/configurations/" + str(config_id) + "/labels")
        return self.standard_response(r, 200)     

    @staticmethod
    def standard_response(response, success_status_code):
        if response.status_code == success_status_code:
            return response.json()
        else:
            raise Exception("Error getting response from web_client:" + str(response))
            
    def whoami(self):
        """
        Returns information about the current user
        """
        r=self.client.get(self.url+"/users/whoami")
        return self.standard_response(r, 200)

    def alive(self):
        """
        Pings the API and returns True if alive
        """
        r=self.client.get(self.url+"/alive")
        return True if r.status_code == 204 else False

    def version(self):
        """
        The API version
        """
        r=self.client.get(self.url+"/version")
        return self.standard_response(r, 200)

    def user_limits(self):
        """Returns the user limits"""
        r = self.client.get(self.url + "/users/limits")
        return self.standard_response(r,200)

    def simulations(self):
        """
        Returns all simulations of the current user
        """        
        r=self.client.get(self.url+"/simulations")
        return self.standard_response(r, 200)

    def check_if_simulation_exists(self,sim_id):
        simulations = self.simulations()
        sim_exists = False
        for simulation in simulations:
            if simulation['SimulationID'] == sim_id:
                sim_exists = True
        if not sim_exists:
            raise Exception("Simulation {} does not exist".format(sim_id))

    def set_setpoints(self, sim_id, step, setpoints):
        """
        Sends setpoints to a given simulation
        """
        data= self.format_set_point_data(step, setpoints)
        r=self.client.post(self.url+"/simulations/"+sim_id+"/setpoints", json= data)
        if r.status_code == 404:
            self.check_if_simulation_exists(sim_id)

        return self.standard_response(r, 200)
    
    def all_setpoints(self,sim_id):
        """
        Returns all the set points of a simulation
        """
        #timestep = self.last_timestep(sim_id)
        r=self.client.get(self.url+"/simulations/"+ sim_id+ "/setpoints")
        
        if r.status_code == 404:
            self.check_if_simulation_exists(sim_id)
        
        return self.standard_response(r, 200)

    def last_setpoint(self, sim_id):
        """
        Returns the last set points of a simulation
        """
        #timestep = self.last_timestep(sim_id)
        r=self.client.get(self.url+"/simulations/"+ sim_id+ "/setpoints/last")

        if r.status_code == 404:
            self.check_if_simulation_exists(sim_id)
        
        return self.standard_response(r, 200)

    def last_timestep(self, sim_id):
        """
        Returns the last timestep of a simulation
        """
        r=self.client.get(self.url+"/simulations/"+ sim_id+ "/timestep")

        if r.status_code == 404:
            self.check_if_simulation_exists(sim_id)

        return self.standard_response(r, 200)
    
    def get_simulation_status(self,sim_id):
        r = self.client.get(self.url+"/simulations/"+sim_id+"/status")

        if r.status_code == 404:
            self.check_if_simulation_exists(sim_id)

        return self.standard_response(r, 200)

    def get_simulation_results(self, sim_id, from_step, to_step, filter_depth, tags: list):
        """
        Gets the simuation results of a given simulation for a given time interval.
        Setting filter_depth = True filers out the depth based results profiles for all but the last setpoints
        Returns a dictonary of dictonaries e.g. results[timeStep]["tag"]
        """
        query=dict()
        query["timestepfrom"]= str(from_step)
        if to_step is not from_step:
            query["timestepto"]=str(to_step)
        for tag in tags:
            if tag not in valid_results:
                raise Exception("'{}' is not a valid OpenLab result tag. Check spelling and capitilization".format(tag))
            query[tag]="true"
        query["filterDepth"]=str(filter_depth)

        attempts = 0
        #loop until we get data or reach the max amount of attempts
        while(True):
            #send get request to OpenLab   
            r=self.client.get(self.url+"/simulations/"+ str(sim_id)+ "/results?", params= query)
            res = r.json()
            
            #break out of while loop once there are results
            if len(res) > 0:
                break

            elif attempts == self.max_results_attempts:               
                print("Failed to get data from timeSteps: {} to {}. Max attempts reached".format(from_step,to_step))
                return
            
            else:
                attempts = attempts + 1
                time.sleep(0.02)
        
        #convert the json to a dictionary of the requested results tags
        result=dict()
        timeStep = from_step
        for timeStep in range(from_step,to_step+1):
            result[timeStep] = self.collect_timebased_results(timeStep, res, tags)
        return result

    def configurations(self):
        """
        Returns all configurations of the current user
        """
        r=self.client.get(self.url+"/configurations") #r is of class response
        return self.standard_response(r, 200)

    def check_if_configuration_id_exists(self,config_id):
        configurations = self.configurations()
        config_exists = False
        for configuration in configurations:
            if configuration['ConfigurationID'] == config_id:
                config_exists = True
        if not config_exists:
            raise Exception("Configuration {} does not exist".format(config_id))

    def check_if_configuration_name_exists(self,config_name):
        configurations = self.configurations()
        config_exists = False
        for configuration in configurations:
            if configuration['Name'] == config_name:
                config_exists = True
        if not config_exists:
            raise Exception("Configuration {} does not exist".format(config_name))

    def configuration_info(self, config_id):
        """
        Returns all configuration info and data of the given configuration
        """
        r=self.client.get(self.url+"/configurations/"+ config_id)

        if r.status_code == 404:
            self.check_if_configuration_id_exists(config_id)

        return self.standard_response(r, 200)

    def configuration_id(self, name):
        """
        Returns configuration id with a given name
        """
        r=self.client.get(self.url+"/configurations/"+ name)

        if r.status_code == 404:
            self.check_if_configuration_name_exists(name)

        return self.standard_response(r, 200)

    def configuration_data(self, config_id):
        """Returns a dictionary of configuration data such as Trajectory, Architecture, Fluids etc..."""
        config = self.configuration_info(config_id)
        return config['Data']

    def configuration_simulations(self, config_id):
        """
        Returns all the simulations for a given configuration ID
        """
        r = self.client.get(self.url+"/configurations/"+str(config_id)+"/simulations")

        if r.status_code == 404:
            self.check_if_configuration_id_exists(config_id)

        return self.standard_response(r, 200)

    def delete_simulation(self, simulationID):
        """
        Deletes a given simulation
        Prompt will be given to confirm
        """
        answer = input("Are you sure you want to delete Simulation {}\t(y/n)".format(simulationID))
        if answer == "y":
            self.client.delete(self.url+"/simulations/"+simulationID)
            print("Simulation {} was deleted".format(simulationID))
        else:
            return

    def simulation_by_id(self, sim_id):
        """
        Returns simulation with a given id
        **Note you must use the id, not the name, as multiple simulations can have the same name
        """
        if type(sim_id) is not str:
            return print("Error. Sim-id must be a string")

        r=self.client.get(self.url+"/simulations/"+ sim_id)

        if r.status_code == 404:
            self.check_if_simulation_exists(sim_id)
            
        return self.standard_response(r, 200)
    
    def create_simulation(self, config_name, sim_name, initial_bit_depth, **kwargs):
        """
        Creates a simulation
        **kwargs influx_type and TimeStep
        Run by calling step() method
        Returns a Simulation Class
        """
        kwargs.setdefault('influx_type', {})
        kwargs.setdefault('TimeStep', 1)
        
        influx_type = kwargs.get('influx_type')
        if not isinstance(influx_type, dict):
            raise TypeError("influx_type has be a dictionary")

        #create a sim_id but the web_client overwrites this
        sim_id= str(uuid.uuid4())
        config_id = self.configuration_id(config_name)
        
        #check initial bit depth is valid
        max_depth = self.max_configuration_depth(config_id)
        if initial_bit_depth > max_depth:
            return print("Initial bit depth {} can not be greater then configurations maximum openhole depth {}".format(
                initial_bit_depth,max_depth))

        #check if max simulation capacity already reached
        user_limits = self.user_limits()
        if type(user_limits) is dict and "MaxConcurrentSimulations" in user_limits.keys():
            simulation_capacity = user_limits['MaxConcurrentSimulations']
            active_simulations = 0
            simulations = self.simulations()
            for sim in simulations:
                status = sim['Status']
                if status != "Completed":
                    active_simulations = active_simulations + 1
            if active_simulations >= simulation_capacity:
                return print("Max conccurent simulation capacity of {} reached. Please stop/complete a running simulation to continue".format(
                    simulation_capacity))

        # format the data to send web_client
        simulation= self.format_simulation_meta_data(sim_id, config_id, sim_name,initial_bit_depth, **kwargs)
        #print("simulation: ", simulation)
        self.url = credentials.OPENLAB_URL
        r=self.client.post(self.url+"/simulations", json = simulation)
        self.standard_response(r, 200)

        # get the simulation id that the web_client created
        simulation_id = r.json()["SimulationID"]
        
        for x in range(self.max_init_attempts):
             r=self.client.get(self.url+"/simulations/"+str(simulation_id)+"/status")          
             if r.json()["Status"] == "Running":
                 print("Simulation Initialized")
                 #create a simulation class and return it to the caller
                 return Simulation(config_id, simulation_id, self)
             else: 
                 time.sleep(0.2)
                 x = x + 1        
        raise Exception("Failed to start simulation " + sim_name + "\nMax attempts reached") 

    def simulation_timestep(self, sim_id):
        r = self.client.get(self.url+"/simulations/"+sim_id+"/timestep")

        if r.status_code == 404:
            self.check_if_simulation_exists(sim_id)

        return self.standard_response(r, 200)

    def max_configuration_depth(self,config_id):
        """
        Returns the maximum openhole depth of a configuration in meters
        """
        depth = self.configuration_info(config_id)['Data']['Architecture']['OpenHole']['DepthInterval']['MaxX']
        return depth
      
    @staticmethod
    def end_simulation(self, sim_id):
        data = [{"ShouldComplete": True}]
        r=self.client.post(self.url+"/simulations/"+sim_id+"/setpoints", json= data)
        return self.standard_response(r, 200)

    @staticmethod
    def format_configuration_meta_data(id,name,description,data):
        return { 'ConfigurationID': id, 'Data': data, 'Description': description, 'Name': name}

    @staticmethod
    def format_simulation_meta_data(sim_id, config_id, name, initial_bit_depth, **kwargs):
        kwargs.setdefault('influx_type', {})
        kwargs.setdefault('TimeStep',1)

        ## TODO Add check for key in kwargs.keys(): check if valid kwarg
        model_configuration = {}

        influx_type = kwargs.get('influx_type')
        step_duration = kwargs.get('TimeStep')
        
        print("influx_type: ", influx_type)
        # do some influx type validations if it was passed in
        if influx_type != {}:
            if "Id" not in influx_type.keys():
                raise Exception("Influx Id key was not entered")

            #check if influx id is one of the client's supported influx types
            if influx_type['Id'] in influx_types:
                print("{} mode selected".format(influx_type['Id']))
                for k in influx_type.keys():
                    #append model configuration with influx dict
                    model_configuration[k] = influx_type[k]
            else:
                raise Exception("Invalid influx type '{}' entered. Available influx types are {}".format(
                    influx_type['Id'],influx_types))
        else:
            print("No influx mode selected. Defaulting to 'no influx and loss'")
            model_configuration['Id'] = "NoInfluxLoss"
            model_configuration['ManualReservoirMode'] = False
            model_configuration['UseReservoirModel'] = False

        if step_duration > 1:
            raise Exception("Step Duration must less than or equal to 1")
        elif step_duration <= 0:
            raise Exception("Step Duration must be greater than 0")
        elif step_duration != 1:
            print("Using Transient Mechanical Model with time step: ", step_duration)
            model_configuration['UseTransientMechanicalModel'] = True
            model_configuration['StepDuration'] = step_duration
        else:
            print("Using non-transient model")

        #print("Model Configuration: ", model_configuration)

        return  {"Name": name,"SimulationID": sim_id,"ConfigurationID": config_id,  "Status": "Created", 
                 "InitialValues": {"BitDepth":initial_bit_depth}, "ModelConfiguration": model_configuration} 

    @staticmethod 
    def collect_timebased_results(timestep, data, tags: list):
        """
        Collects the given tags from the result set
        """
        result=dict()
        for tag in tags:
            for i in range(0, len(data)):
                if tag == data[i]['t'] and timestep == data[i]['s']:
                    if data[i]['v'] is not None and len(data[i]['v'][0]) > 0:
                        if isinstance(data[i]['v'][0]['d'], numbers.Number): #depth based because it has a numeric depth (not NaN)
                            result[tag] = data[i]['v']  #dump all the depths/value pairs into the result
                        else: # time based
                            result[tag]= data[i]['v'][0]['v'] #drop the NaN depth
        return result

    @staticmethod
    def format_set_point_data(timestep, setpoints: dict):
            Data=dict()
            for k in setpoints.keys():
                Data[k]=setpoints[k]
            return [{"TimeStep":timestep, "Data": Data }]

class setpointsClass():
    """
    A class property for the setpoints
    """
    def __init__(self):
        self.ChokeOpening = 1 # 0=closed 1=Open
        self.DensityIn = None
        self.FlowRateIn = None
        self.TopOfStringVelocity = None
        self.DesiredROP  = None
        self.SurfaceRPM = None
        self.ChokePumpFlowRateIn = None
        self.BOPChokeOpening = 1 # 0=closed 1=Open
        self.ActiveFluidIndex = 0 # fluid 1
    
    @property
    def ChokeOpening(self): return self.__ChokeOpening
    @ChokeOpening.setter
    def ChokeOpening(self, value): self.__ChokeOpening = value

    @property
    def DensityIn(self): return self.__DensityIn
    @DensityIn.setter
    def DensityIn(self, value): self.__DensityIn = value

    @property
    def FlowRateIn(self): return self.__FlowRateIn
    @FlowRateIn.setter
    def FlowRateIn(self, value): self.__FlowRateIn = value

    @property
    def TopOfStringVelocity(self): return self.__TopOfStringVelocity
    @TopOfStringVelocity.setter
    def TopOfStringVelocity(self, value): self.__TopOfStringVelocity = value

    @property
    def DesiredROP(self): return self.__DesiredROP
    @DesiredROP.setter
    def DesiredROP(self, value): self.__DesiredROP = value            

    @property
    def SurfaceRPM(self): return self.__SurfaceRPM
    @SurfaceRPM.setter
    def SurfaceRPM(self, value): self.__SurfaceRPM = value

    @property
    def ChokePumpFlowRateIn(self): return self.__ChokePumpFlowRateIn
    @ChokePumpFlowRateIn.setter
    def ChokePumpFlowRateIn(self, value): self.__ChokePumpFlowRateIn = value

    @property
    def BOPChokeOpening(self): return self.__BOPChokeOpening
    @BOPChokeOpening.setter
    def BOPChokeOpening(self, value): self.__BOPChokeOpening = value

    @property
    def ActiveFluidIndex(self): return self.__ActiveFluidIndex
    @ActiveFluidIndex.setter
    def ActiveFluidIndex(self, value): self.__ActiveFluidIndex = value  

def all_setpoints():
    """
    Returns a list of all available/possible setpoints
    Subject to change in the future
    """
    empty_setpoints = [
        "ChokeOpening", "DensityIn", "FlowRateIn", "TopOfStringVelocity",
        "DesiredROP", "SurfaceRPM", "ChokePumpFlowRateIn", "BopChokeOpening",
        "ActiveFluidIndex"
    ]
    return empty_setpoints

def all_results():
    """
    Returns a list of all available/possible results
    Subject to change in the future
    """  
    results_list = [
        "SPP","DownholeECD","FlowRateOut","HookLoad","SurfaceTorque",
        "BitDepth", "TD", "ChokeOpening", "DownholePressure", "ChokePressure",
        "FluidTemperatureOut", "WOB", "InstantaneousROP", "BOPChokeOpening",
        "FlowRateIn", "TopOfStringVelocity", "SurfaceRPM", "ChokePumpFlowRateIn",
        "DrillstringTemperature", "TotalInfluxMass", "CalculatedPressureBottomHole",
        "CuttingsMassFractionTransient", "GasVolumeFraction", "DrillstringBucklingLimit",
        "FluidTemperatureIn", "AnnulusECD", "DrillstringTorqueLimit", "AnnulusTemperature",
        "DrillstringTension", "AnnulusFluidVelocity", "DrillstringFluidVelocity", "CuttingsBedHeight",
        "AnnulusDensity", "DrillstringTorque", "ActivePit", "TotalMudLossMass", "Connection",
        "TopOfStringPosition"
        ]
    return results_list

class resultsClass():
    """
    This is a class property for the results
    """
    def __init__(self):
        self.SPP = dict()
        self.DownholeECD = dict()
        self.FlowRateOut = dict()
        self.HookLoad = dict()
        self.SurfaceTorque = dict()
        self.BitDepth = dict()
        self.TD = dict()
        self.ChokeOpening = dict()
        self.DownholePressure = dict()
        self.ChokePressure = dict()
        self.FluidTemperatureOut = dict()
        self.WOB = dict()
        self.InstantaneousROP = dict()
        self.BOPChokeOpening = dict()
        self.FlowRateIn = dict()
        self.TopOfStringVelocity = dict()
        self.SurfaceRPM = dict()
        self.ChokePumpFlowRateIn = dict()
        self.Connection = dict()
        self.TopOfStringPosition = dict()

        self.DrillstringTemperature = dict()
        self.TotalInfluxMass = dict()
        self.CalculatedPressureBottomHole = dict() #BHP
        self.CuttingsMassFractionTransient = dict()
        self.GasVolumeFraction = dict()
        self.DrillstringBucklingLimit = dict()
        self.DrillstringTorqueLimit = dict()
        self.FluidTemperatureIn = dict()
        self.AnnulusECD = dict()
        self.AnnulusTemperature = dict()
        self.AnnulusDensity = dict()
        self.DrillstringFluidVelocity = dict()
        self.CuttingsBedHeight = dict()
        self.DrillstringTorque = dict()
        self.ActivePit = dict()
        self.TotalMudLossMass = dict()
        self.BopChokePressure = dict()
        self.AnnulusFluidVelocity = dict()
        self.DrillstringTension = dict()

    @property
    def SPP(self): return self._SPP
    @SPP.setter
    def SPP(self, value): self._SPP = value
    
    @property
    def DownholeECD(self): return self._DownholeECD
    @DownholeECD.setter
    def DownholeECD(self, value): self._DownholeECD = value
    
    @property
    def SurfaceTorque(self): return self._SurfaceTorque
    @SurfaceTorque.setter
    def SurfaceTorque(self, value): self._SurfaceTorque = value

    @property
    def TD(self): return self._TD
    @TD.setter
    def TD(self, value): self._TD = value

    @property
    def BitDepth(self): return self._BitDepth
    @BitDepth.setter
    def BitDepth(self, value): self._BitDepth = value
        
    @property
    def DownholePressure(self): return self._DownholePressure
    @DownholePressure.setter
    def DownholePressure(self, value): self._DownholePressure = value

    @property
    def FlowRateOut(self): return self._FlowRateOut
    @FlowRateOut.setter
    def FlowRateOut(self, value): self._FlowRateOut = value

    @property
    def HookLoad(self): return self._HookLoad
    @HookLoad.setter
    def HookLoad(self, value): self._HookLoad = value

    @property
    def ChokePressure(self): return self._ChokePressure
    @ChokePressure.setter
    def ChokePressure(self, value): self._ChokePressure = value

    @property
    def FluidTemperatureOut(self): return self._FluidTemperatureOut
    @FluidTemperatureOut.setter
    def FluidTemperatureOut(self, value): self._FluidTemperatureOut = value

    @property
    def WOB(self): return self._WOB
    @WOB.setter
    def WOB(self, value): self._WOB = value

    @property
    def InstantaneousROP(self): return self._InstantaneousROP
    @InstantaneousROP.setter
    def InstantaneousROP(self, value): self._InstantaneousROP = value

    @property
    def BOPChokeOpening(self): return self._BOPChokeOpening
    @BOPChokeOpening.setter
    def BOPChokeOpening(self, value): self._BOPChokeOpening = value

    @property
    def FlowRateIn(self): return self._FlowRateIn
    @FlowRateIn.setter
    def FlowRateIn(self, value): self._FlowRateIn = value

    @property
    def TopOfStringVelocity(self): return self._TopOfStringVelocity
    @TopOfStringVelocity.setter
    def TopOfStringVelocity(self, value): self._TopOfStringVelocity = value

    @property
    def SurfaceRPM(self): return self._SurfaceRPM
    @SurfaceRPM.setter
    def SurfaceRPM(self, value): self._SurfaceRPM = value

    @property
    def ChokePumpFlowRateIn(self): return self._ChokePumpFlowRateIn
    @ChokePumpFlowRateIn.setter
    def ChokePumpFlowRateIn(self, value): self._ChokePumpFlowRateIn = value

    @property
    def ChokeOpening(self): return self._ChokeOpening
    @ChokeOpening.setter
    def ChokeOpening(self, value): self._ChokeOpening = value


    @property
    def DrillstringTemperature(self): return self._DrillstringTemperature
    @DrillstringTemperature.setter
    def DrillstringTemperature(self, value): self._DrillstringTemperature = value

    @property
    def TotalInfluxMass(self): return self._TotalInfluxMass
    @TotalInfluxMass.setter
    def TotalInfluxMass(self, value): self._TotalInfluxMass = value

    @property
    def CalculatedPressureBottomHole(self): return self._CalculatedPressureBottomHole
    @CalculatedPressureBottomHole.setter
    def CalculatedPressureBottomHole(self, value): self._CalculatedPressureBottomHole = value
    
    @property
    def CuttingsMassFractionTransient(self): return self._CuttingsMassFractionTransient
    @CuttingsMassFractionTransient.setter
    def CuttingsMassFractionTransient(self, value): self._CuttingsMassFractionTransient = value

    @property
    def GasVolumeFraction(self): return self._GasVolumeFraction
    @GasVolumeFraction.setter
    def GasVolumeFraction(self, value): self._GasVolumeFraction = value

    @property
    def DrillstringBucklingLimit(self): return self._DrillstringBucklingLimit
    @DrillstringBucklingLimit.setter
    def DrillstringBucklingLimit(self, value): self._DrillstringBucklingLimit = value

    @property
    def FluidTemperatureIn(self): return self._FluidTemperatureIn
    @FluidTemperatureIn.setter
    def FluidTemperatureIn(self, value): self._FluidTemperatureIn = value

    @property
    def AnnulusECD(self): return self._AnnulusECD
    @AnnulusECD.setter
    def AnnulusECD(self, value): self._AnnulusECD = value

    @property
    def DrillstringTorqueLimit(self): return self._DrillstringTorqueLimit
    @DrillstringTorqueLimit.setter
    def DrillstringTorqueLimit(self, value): self._DrillstringTorqueLimit = value

    @property
    def AnnulusTemperature(self): return self._AnnulusTemperature
    @AnnulusTemperature.setter
    def AnnulusTemperature(self, value): self._AnnulusTemperature = value

    @property
    def DrillstringTension(self): return self._DrillstringTension
    @DrillstringTension.setter
    def DrillstringTension(self, value): self._DrillstringTension = value

    @property
    def AnnulusFluidVelocity(self): return self._AnnulusFluidVelocity
    @AnnulusFluidVelocity.setter
    def AnnulusFluidVelocity(self, value): self._AnnulusFluidVelocity = value

    @property
    def DrillstringFluidVelocity(self): return self._DrillstringFluidVelocity
    @DrillstringFluidVelocity.setter
    def DrillstringFluidVelocity(self, value): self._DrillstringFluidVelocity = value

    @property
    def CuttingsBedHeight(self): return self._CuttingsBedHeight
    @CuttingsBedHeight.setter
    def CuttingsBedHeight(self, value): self._CuttingsBedHeight = value

    @property
    def AnnulusDensity(self): return self._AnnulusDensity
    @AnnulusDensity.setter
    def AnnulusDensity(self, value): self._AnnulusDensity = value

    @property
    def DrillstringTorque(self): return self._DrillstringTorque
    @DrillstringTorque.setter
    def DrillstringTorque(self, value): self._DrillstringTorque = value

    @property
    def ActivePit(self): return self._ActivePit
    @ActivePit.setter
    def ActivePit(self, value): self._ActivePit = value

    @property
    def TotalMudLossMass(self): return self._TotalMudLossMass
    @TotalMudLossMass.setter
    def TotalMudLossMass(self, value): self._TotalMudLossMass = value

    @property
    def Connection(self): return self._Connection
    @Connection.setter
    def Connection(self, value): self._Connection = value

    @property
    def TopOfStringPosition(self): return self._TopOfStringPosition
    @TopOfStringPosition.setter
    def TopOfStringPosition(self, value): self._TopOfStringPosition = value

influx_types = ["ManualInflux", "ManualLoss", "GeoPressureGradient"]

default_manual_influx = {"ComplexReservoirKickOffTime": 30,
            "Id" : "ManualInflux",
            "ManualInfluxLossMd": 2500,
            "ManualInfluxLossMassRate" : 0.83333333,
            "ManualInfluxLossTotalMass": 100,
            "ManualReservoirMode" : True,
            "UseReservoirModel" : True}

default_manual_loss = {"ComplexReservoirKickOffTime": 30,
            "Id" : "ManualLoss",
            "ManualInfluxLossMd": 2500,
            "ManualInfluxLossMassRate" : -1.66666667,
            "ManualInfluxLossTotalMass": 1000,
            "ManualReservoirMode" : True,
            "UseReservoirModel" : True}
            
# technically not default because there are no variable inputs, but want to keep it consistent with the other names
default_geopressure_gradient = {"Id": "GeoPressureGradient", 
            "ManualReservoirMode" : False,
            "UseReservoirModel": True}

#simulation iterable class
class IterSimulation(type):
    def __iter__(cls):
        return iter(cls._registry)

class Simulation(http_client,metaclass=IterSimulation):
    """
    A Simulation class for the OpenLab http_client
    """
    #Things needed to make the simulations iterable
    __metaclass__ = IterSimulation
    _registry = []

    client = None

    def  __init__(self, config_id, sim_id, client):
        self.config_id = config_id
        self.http_client = client 
        self.sim_id = sim_id
        self.setpoints = setpointsClass()
        self.results = resultsClass()
        try:
            self.max_timeStep = client.user_limits()['MaxTimeStep']
        except: self.max_timeStep = None

        self.end_simulation_on_exiting = True
        self.filter_depth_based_results = True #setting true will only get the depth based results for the most recent setpoint
        self.ModelConfiguration = {}
        self._registry.append(self) #add the simulation to the iterable registry 
        self.connecting_previously = False
        self.currently_connecting = False
    
    def __iter__(self):
        return iter(self)

    def get_conf_id(self):
        """
        Returns the configuration id of the simulation instance
        """
        return self.config_id

    def get_sim_id(self):
        """
        Returns the simulation id for the simulation instance
        """
        return self.sim_id

    def whoamiFromSimulation(self):
        return self
    
    def get_status(self):
        """
        Returns the status of the simulation instance 
        """
        return http_client.get_simulation_status(self.http_client,self.sim_id)['Status']

    def last_setpoints(self):
        """
        Returns the last setpoints for the simulation instance
        """
        return http_client.last_setpoint(self.http_client, self.sim_id)

    def current_step(self):
        """
        Returns the current step for the simulation instance
        """
        return http_client.simulation_timestep(self.http_client, self.sim_id)
    
    def current_setpoints(self):
        """
        Returns the simulations instances current setpoints that will be sent to web client when the step method is called
        """
        #empty dictionary for setpoints
        toSet = dict()
        #toSet["TimeStep"] = self.timeStep
        if self.setpoints.ChokeOpening is not None:
            toSet["ChokeOpening"] = self.setpoints.ChokeOpening
        if self.setpoints.TopOfStringVelocity is not None:
            toSet["TopOfStringVelocity"] = self.setpoints.TopOfStringVelocity
        if self.setpoints.FlowRateIn is not None:
            toSet["FlowRateIn"] = self.setpoints.FlowRateIn
        if self.setpoints.SurfaceRPM is not None:
            toSet["SurfaceRPM"] = self.setpoints.SurfaceRPM
        if self.setpoints.ChokePumpFlowRateIn is not None:
            toSet["ChokePumpFlowRateIn"] = self.setpoints.ChokePumpFlowRateIn
        if self.setpoints.DesiredROP is not None:
            toSet["DesiredROP"] = self.setpoints.DesiredROP
        if self.setpoints.DensityIn is not None:
            toSet["DensityIn"] = self.setpoints.DensityIn
        if self.setpoints.BOPChokeOpening is not None:
            toSet["BopChokeOpening"] = self.setpoints.BOPChokeOpening
        if self.setpoints.ActiveFluidIndex is not None:
            toSet["ActiveFluidIndex"] = self.setpoints.ActiveFluidIndex
        return toSet

    def step(self,timeStep):
        """
        Steps the simulation one step forward
        """
        #check if still running
        if self.get_status() != "Running":
            raise Exception("Can not step because simulation is not running")  
    
        # verify the time step is correct
        if timeStep != self.current_step() + 1:
            raise Exception("Trying to set a set a setpoint not at the immediate next timestep")
            
        if timeStep == self.max_timeStep:
            print("Max simulation time of {} steps reached".format(self.max_timeStep))
            self.stop()

        self.timeStep = timeStep

        #get the client to post the setpoints to the web_client 
        http_client.set_setpoints(self.http_client,self.sim_id,self.timeStep, self.current_setpoints())
        
        max_reload_attempts = 50
        i = 0
        for i in range(max_reload_attempts):
            if timeStep == self.current_step(): # setpoints were accepted by web client a step was made
                break
            elif i < max_reload_attempts:
                i = i + 1
                time.sleep(pow(i,0.5)/100) #exponential backoff
            else:
                print("Desired timeStep: {}; Current timestep: {}".format(timeStep, self.current_step()))
                
    def get_results(self,timeStep,tags: list):
        """
        Gets the results for the given timestep
        Pass in openlab.all_results() for all available results
        """
        if timeStep >= 1:
            if "Connection" not in tags:
                tags.append("Connection")
        
            #get the http_client to request simulation results
            res = http_client.get_simulation_results(self.http_client, self.sim_id,timeStep, timeStep, self.filter_depth_based_results, tags)

            if res[timeStep]['Connection'] == 1:
                #check if it just started connecting
                if self.connecting_previously == False:
                    print("Connecting new pipe")
                
                self.connecting_previously = True
                self.currently_connecting = True

            elif self.currently_connecting == True:
                #this will only trigger when res[timeStep]['Connection'] == 0 and flag hasn't been reset
                print("Done Connecting Pipe")
                self.currently_connecting = False

            ##assign each result from the client to its respected result dictionary in simulation class
            for tag in tags:
                if tag in res[timeStep].keys():
                    try:
                        getattr(self.results, tag)[timeStep] = res[timeStep][tag]
                    except TypeError:
                        print("Type Error. Time step: {}; Tag: {}".format(timeStep, tag))
                    except AttributeError:
                        print("Tag '{}' is not a recognized OpenLab result tag".format(tag))
        return
    
    def stop(self):
        """
        Complete the simulation instance
        """
        print("Ending Simulation: {}".format(self.sim_id))
        self.end_simulation(self.http_client,self.sim_id)

    @property
    def end_simulation_on_exiting(self):
        return self._end_simulation_on_exiting
    @end_simulation_on_exiting.setter
    def end_simulation_on_exiting(self, value):
        self._end_simulation_on_exiting = value

def stop_running_simulations():
    """
    Exit code that ends all running simulations
    """
    print("Exiting Code")
    try:
        #loop through all the active simulations
        for simulation in Simulation:
            status = simulation.get_status()
            name = simulation.get_sim_id()
            print("Sim {} is {} ".format(name,status))

            #stop the simulation if it is running, initializing, or created
            if status == "Running" or status == "Initializing" or status == "Created":
                if simulation.end_simulation_on_exiting == True:
                    simulation.stop()
                    time.sleep(0.2) #wait a bit before getting new status
                    print("Sim {} is now {}".format(name,simulation.get_status()))
                else: 
                    print("Sim {} was not ended because end_simulation_on_exiting was set to false".format(name))
    except:
        raise Exception("Could not iterate simulations")

#register the functions to run at exit
atexit.register(stop_running_simulations)
