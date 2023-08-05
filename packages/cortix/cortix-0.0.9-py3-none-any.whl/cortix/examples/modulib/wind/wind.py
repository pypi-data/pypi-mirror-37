# -*- coding: utf-8 -*-
# This file is part of the Cortix toolkit evironment
# https://github.com/dpploy/cortix
#
# All rights reserved, see COPYRIGHT for full restrictions.
# https://github.com/dpploy/COPYRIGHT....
#
# Licensed under the GNU General Public License v. 3, please see LICENSE file.
# https://www.gnu.org/licenses/gpl-3.0.txt
'''
Wind module example in Cortix.
'''
#*********************************************************************************
import os, sys, io, time
import logging
from collections             import namedtuple

from cortix.support.quantity import Quantity
from cortix.support.specie   import Specie
from cortix.support.phase    import Phase
#*********************************************************************************

class Wind():
 r'''
  Wind module used example in Cortix.
 '''

 def __init__( self,
               slot_id,
               input_full_path_file_name,
               work_dir,
               ports = list(),
               cortix_start_time = 0.0,
               cortix_final_time = 0.0,
               cortix_time_step = 0.0,
               cortix_time_unit=None
             ):

#.................................................................................
# Sanity test

  assert isinstance(slot_id, int), '-> slot_id type %r is invalid.' % type(slot_id)
  assert isinstance(ports, list), '-> ports type %r is invalid.'  % type(ports)
  assert len(ports) > 0
  assert isinstance(cortix_start_time,float), '-> time type %r is invalid.' % \
         type(cortix_start_time)
  assert isinstance(cortix_final_time, float), '-> time type %r is invalid.' % \
         type(cortix_final_time)
  assert isinstance(cortix_time_step, float), '-> time step type %r is invalid.' % \
         type(cortix_time_step)
  assert isinstance(cortix_time_unit, str), '-> time unit type %r is invalid.' % \
         type(cortix_time_unit)

  # Logging
  self.__log = logging.getLogger('launcher-wind'+str(slot_id)+'.cortix_driver.wind')
  self.__log.info('initializing an object of Wind()')

#.................................................................................
# Member data 

  self.__slot_id = slot_id
  self.__ports   = ports

  # Convert Cortix's time unit to Wind's internal time unit
  if cortix_time_unit == 'minute':
     self.__time_unit_scale = 60.0
  elif cortix_time_unit == 'second': 
     self.__time_unit_scale = 1.0
  elif cortix_time_unit == 'hour': 
     self.__time_unit_scale = 60.0*60.0
  else:
     assert False, 'Cortix time_unit: %r not acceptable.' % time_unit

  self.__cortix_time_unit = cortix_time_unit

  self.__start_time = cortix_start_time * self.__time_unit_scale # Wind time unit
  self.__final_time = cortix_final_time * self.__time_unit_scale # Wind time unit

  if work_dir[-1] != '/': work_dir = work_dir + '/'
  self.__wrkDir = work_dir

  # Signal to start operation
  self.__goSignal = True     # start operation immediately
  for port in self.__ports:  # if there is a signal port, start operation accordingly
      (port_name, port_type, this_port_file) = port
      if port_name == 'go-signal' and port_type == 'use': self.__go_signal = False

  self.__setup_time = 60.0  # time unit; a delay time before starting to run

#.................................................................................
# Input ports
# Read input information if any

  #fin = open(input_full_path_file_name,'r')

# Configuration member data   

  self.__pyplot_scale = 'linear'
#  self.__ode_integrator = 'scikits.odes' # or 'scipy.integrate' 
  self.__ode_integrator = 'scipy.integrate' 

# Domain specific member data 

  shear_coeff = 0.4  # dimensionless
  Params = namedtuple('Params',['shear_coeff'])
  self.__params = Params( shear_coeff ) 

  # Setup the material phase as a gas
  species = list()

  air = Specie( name='air', formulaName='Air', phase='gas' )
  air.massCCUnit = 'g/cc'
  air.molarCCUnit = 'mole/cc'

  species.append(air)

  quantities = list()

  # altitude
  altitude = Quantity( name='altitude', formalName='Altitude', unit='m' )
  quantities.append( altitude )
  # velocity
  velocity = Quantity( name='velocity', formalName='Velocity', unit='m/s' )
  quantities.append( velocity )

  self.__gas_phase = Phase( self.__start_time, species=species, quantities=quantities)

  # Initialize phase
  air_mass_cc = 0.1 # [g/cc]
  self.__gas_phase.SetValue( 'water', water_mass_cc, self.__start_time )

  x_0 = 1000.0  # initial altitude [m] above ground at 0
  self.__gas_phase.SetValue( 'altitude', x_0, self.__start_time )

  v_0 = np.array([0.0,0.0,0.0])   # initial wind velocity [m/s]
  self.__gas_phase.SetValue( 'velocity', v_0, self.__start_time )

#---------------------- end def __init__():---------------------------------------

 def call_ports( self, cortix_time=0.0 ):
  '''
  Transfer data at cortix_time
  '''

  cortix_time *= self.__time_unit_scale  # convert to Wind time unit

  # provide data to all provide ports 
  self.__provide_data( provide_port_name='output', at_time=cortix_time )
  self.__provide_data( provide_port_name='state',  at_time=cortix_time )

  # use data using the 'use-port-name' of the module
  self.__use_data( use_port_name='spatial-position', at_time=cortix_time )

  return
#---------------------- end def call_ports():---------------------------------------

 def execute( self, cortix_time=0.0, cortix_time_step=0.0 ):
  '''
  Evolve system from cortix_time to cortix_time + cortix_time_step
  '''

  cortix_time      *= self.__time_unit_scale  # convert to Wind time unit
  cortix_time_step *= self.__time_unit_scale  # convert to Wind time unit

  s = 'execute('+str(round(cortix_time,2))+'[min]): '
  self.__log.debug(s)

  self.__evolve( cortix_time, cortix_time_step )

  return
#---------------------- end def execute():----------------------------------------

#*********************************************************************************
# Private helper functions (internal use: __)

 def __provide_data( self, provide_port_name=None, at_time=0.0 ):

# Access the port file
  port_file = self.__get_port_file( provide_port_name = provide_port_name )

# Provide data to port files
  if provide_port_name == 'output' and port_file is not None: 
   self.__provide_persistent_output( port_file, at_time )

  if provide_port_name == 'state' and port_file is not None: 
   self.__provide_state( port_file, at_time )

  if provide_port_name == 'wind_velocity' and port_file is not None: 
   self.__provide_wind_velocity( port_file, at_time )

  return
#---------------------- end def __provide_data():---------------------------------

 def __use_data( self, use_port_name=None, at_time=0.0 ):

# Access the port file
  port_file = self.__get_port_file( use_port_name = use_port_name )
 
# Use data from port file
  if use_port_name == 'altitude' and port_file is not None:  
     self.__use_altitude( port_file, at_time )

  return
#---------------------- end def __use_data():-------------------------------------

 def __get_port_file( self, use_port_name=None, provide_port_name=None ):
   '''
   This may return a None port_file
   '''

   port_file = None

   #..........
   # Use ports
   #..........
   if use_port_name is not None:
 
     assert provide_port_name is None
 
     for port in self.__ports:

       (port_name,port_type,this_port_file) = port

       if port_name == use_port_name and port_type == 'use': 
          port_file = this_port_file

     if port_file is None: 
        return None
 
     max_n_trials = 50
     n_trials     = 0
     while os.path.isfile(port_file) is False and n_trials <= max_n_trials:
       n_trials += 1
       time.sleep(0.1)
 
     if n_trials > max_n_trials:
         s = '__get_port_file(): waited ' + str(n_trials) + ' trials for port: ' +\
             port_file
         self.__log.warn(s)
 
     assert os.path.isfile(port_file) is True, \
            'port_file %r not available; stop.' % port_file

   #..............
   # Provide ports
   #..............
   if provide_port_name is not None:
 
     assert use_port_name is None

     for port in self.__ports:
       (port_name,port_type,this_port_file) = port
       if port_name == provide_port_name and port_type == 'provide': port_file = this_port_file
 
   return port_file
#---------------------- end def __get_port_file():--------------------------------

 def __provide_persistent_output( self, port_file, at_time ):
   '''
   Provide data that will remain in disk after the simulation ends.
   '''
   import datetime

   # if the first time step, write the header of a table data file
   if at_time == self.__start_time:

     assert os.path.isfile(port_file) is False, 'port_file %r exists; stop.' % port_file
     fout = open(port_file,'w')

     fout.write('# name:   '+'wind_'+str(self.__slot_id)); fout.write('\n')
     fout.write('# author: '+'cortix.examples.modulib.wind'); fout.write('\n')
     fout.write('# version:'+'0.1'); fout.write('\n')
     today = datetime.datetime.today()
     fout.write('# today:  '+str(today)); fout.write('\n')
     fout.write('#')
# write file header
     fout.write('%17s'%('Time[sec]'))
     # mass density   
     for specie in self.__gas_phase.GetSpecies():
       fout.write('%18s'%(specie.formulaName+'['+specie.massCCUnit+']'))
     # quantities     
     for quant in self.__gas_phase.GetQuantities():
       fout.write('%18s'%(quant.formalName+'['+quant.unit+']'))

     fout.write('\n')
     fout.close()

   # write history data

   fout = open(port_file,'a')

   # Wind time 
   fout.write('%18.6e' % (at_time))

   # mass density   
   for specie in self.__gas_phase.GetSpecies():
     rho = self.__gas_phase.GetValue(specie.name, at_time)
     fout.write('%18.6e'%(rho))
     # quantities     
   for quant in self.__gas_phase.GetQuantities():
     val = self.__gas_phase.GetValue(quant.name, at_time)
     fout.write('%18.6e'%(val))

   fout.write('\n')
   fout.close()

   return
#---------------------- end def __provide_persistent_output():--------------------
 def __provide_state( self, port_file, at_time ):
   '''
   Provide the internal state of the module. This is typically used by another
   module such as '.cortix.modulib.pyplot'; this XML file type is now deprecated.
   However to have a dynamic plotting option, create this history file in the
   time unit of Cortix; that is, undo the time scaling.
   '''
   import datetime
   import xml.etree.ElementTree as ElementTree
   from threading import Lock

   n_digits_precision = 8

   # write header
   if at_time == self.__start_time:

    assert os.path.isfile(port_file) is False, 'port_file %r exists; stop.' % port_file

    tree = ElementTree.ElementTree()
    root_node = tree.getroot()

    a = ElementTree.Element('time-sequence')
    a.set('name','wind_'+str(self.__slot_id)+'-state')

    b = ElementTree.SubElement(a,'comment')
    today = datetime.datetime.today()
    b.set('author','cortix.examples.modulib.wind')
    b.set('version','0.1')

    b = ElementTree.SubElement(a,'comment')
    today = datetime.datetime.today()
    b.set('today',str(today))

    b = ElementTree.SubElement(a,'time')
    b.set('unit',self.__cortix_time_unit)

    # setup the headers
    for specie in self.__gas_phase.species:
        b = ElementTree.SubElement(a,'var')
        formula_name = specie.formulaName
        b.set('name',formula_name)
        unit = specie.massCCUnit
        b.set('unit',unit)
        b.set('legend','Wind_'+str(self.__slot_id)+'-state')
        b.set('scale',self.__pyplot_scale)

    for quant in self.__gas_phase.quantities:
        b = ElementTree.SubElement(a,'var')
        formal_name = quant.formalName 
        b.set('name',formal_name)
        unit = quant.unit
        b.set('unit',unit)
        b.set('legend','Wind_'+str(self.__slot_id)+'-state')
        b.set('scale',self.__pyplot_scale)

    # write values for all variables
    b = ElementTree.SubElement(a,'timeStamp')
    b.set('value',str(round(at_time/self.__time_unit_scale,n_digits_precision)))

    values = list()

    for specie in self.__gas_phase.species:
        val = self.__gas_phase.GetValue( specie.name, at_time )
        values.append( val )

    for quant in self.__gas_phase.quantities:
        val = self.__gas_phase.GetValue( quant.name, at_time )
        values.append( val )

    # flush out data
    text = str()
    for value in values:
        text += str(round(value,n_digits_precision)) + ',' 

    text = text[:-1]

    b.text = text 

    tree = ElementTree.ElementTree(a)

    tree.write( port_file, xml_declaration=True, encoding="unicode", method="xml" )

  #-------------------------------------------------------------------------------
  # if not the first time step then parse the existing history file and append
   else:

    mutex = Lock()
    mutex.acquire()

    tree = ElementTree.parse( port_file )
    root_node = tree.getroot()

    a = ElementTree.Element('timeStamp')
    a.set('value',str(round(at_time/self.__time_unit_scale,n_digits_precision)))

    # all variables values
    values = list()

    for specie in self.__gas_phase.species:
        val = self.__gas_phase.GetValue( specie.name, at_time )
        values.append( val )
    for quant in self.__gas_phase.quantities:
        val = self.__gas_phase.GetValue( quant.name, at_time )
        values.append( val )

    # flush out data
    text = str()
    for value in values:
        text += str(round(value,n_digits_precision)) + ',' 

    text = text[:-1]

    a.text = text 

    root_node.append(a)

    tree.write( port_file, xml_declaration=True, encoding="unicode", method="xml" )

    mutex.release()

   return 

#---------------------- end def __provide_state():--------------------------------

 def __evolve( self, cortix_time=0.0, cortix_time_step=0.0 ):
  r'''
  .. math::
  ODE IVP problem:
  Given the initial data at $t=0$, $u_1(0) = x_0$, $u_2(0) = v_0 = \dot{u}_1(0)$
  solve $\frac{\mathtext{d}u}{\mathtext{d}t} = f(u)%
  ''' 
  import numpy as np

  if self.__ode_integrator == 'scikits.odes':
     from scikits.odes import ode        # this requires the SUNDIALS ODE package 
  elif self.__ode_integrator == 'scipy.integrate':
     from scipy.integrate import odeint  # this ships with scipy 
  else:
     assert False, 'Fatal: invalid ode integrator config. %r'%self.__ode_integrator

  x_0 =   self.__gas_phase.GetValue( 'altitude', cortix_time )
  v_0 = - self.__gas_phase.GetValue( 'speed', cortix_time )

  u_vec_0 = [x_0, v_0]

  # rhs function
  if self.__ode_integrator == 'scikits.odes':
    def rhs_fn(t, u_vec, dt_u_vec, params):
      dt_u_vec[0] = u_vec[1]              #  d_t u_1 = u_2
      dt_u_vec[1] = - params.gravity      #  d_t u_2 = -g
      return
  elif self.__ode_integrator == 'scipy.integrate':
    def rhs_fn(u_vec, t, gravity):
      dt_u_0 = u_vec[1]              #  d_t u_1 = u_2
      dt_u_1 = - gravity             #  d_t u_2 = -g
      return [dt_u_0, dt_u_1]
  else:
     assert False, 'Fatal: invalid ode integrator config. %r'%self.__ode_integrator

  t_interval_sec = np.linspace(0.0, cortix_time_step, num=2)

  if self.__ode_integrator == 'scikits.odes':
     cvode = ode('cvode', rhs_fn, user_data=self.__params, old_api=False)
     solution = cvode.solve( t_interval_sec, u_vec_0 )  # solve for time interval 

     results = solution.values
     message = solution.message

     assert solution.message == 'Successful function return.'
     assert solution.errors.t is None, 'errors.t = %r'%solution.errors.t
     assert solution.errors.y is None, 'errors.y = %r'%solution.errors.y

     u_vec = results.y[1,:] # solution vector at final time step

  elif self.__ode_integrator == 'scipy.integrate':
     u_vec_hist, info_dict = odeint( rhs_fn,
                                     u_vec_0, t_interval_sec,
                                     args=( self.__params.gravity, ), full_output=True
                                   )

     assert info_dict['message']=='Integration successful.',\
            'Fatal: scipy.integrate.odeint failed %r'%info_dict['message']

     u_vec = u_vec_hist[1,:]  # solution vector at final time step
  else:
     assert False, 'Fatal: invalid ode integrator config. %r'%self.__ode_integrator

  values = self.__gas_phase.GetRow( cortix_time ) # values at previous time

  at_time = cortix_time + cortix_time_step  

  self.__gas_phase.AddRow( at_time, values ) # repeat values for current time

  if u_vec[0] <= 0.0: # ground impact sets result to zero
   u_vec[0] = 0.0
   u_vec[1] = 0.0

  self.__gas_phase.SetValue( 'altitude', u_vec[0], at_time )      # update current values
  self.__gas_phase.SetValue( 'speed',  abs(u_vec[1]), at_time ) # update current values

#  print('u(t=',at_time*60,'[s]) = ',u_1)
  
#---------------------- end def __evolve():---------------------------------------


#======================= end class Wind: =========================================
