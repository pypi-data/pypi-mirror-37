import logging

#User Settings - Change These
email = "a.holsaeter@gmail.com"
api_key = "ABF17DFB6AB178674A95F60DDB276EDF855362B58D9CD498E1B2CB21E62B56A5"
# api_key = "E5075A87EA0A3B5029522993FA0BAC379A409DB1EE1EE829FC21A8F509CF3861" #prod

#Advanced Settings
log = False #whether or not to log respective to below level
log_level = logging.INFO # Critical, Error, Warning, Info, Debug, Notset
network_proxies = {}
verify = True #True/False (Strongly advice against setting this to False) or path to CA_BUNDLE file or directory.
#Note from requests library: If directory, it must be processed using the c_rehas utility supplied with OpenSSL

#Don't need to change these 
client_id = 'OpenLab'
# OPENLAB_URL= 'https://openlab.iris.no'
OPENLAB_URL= 'https://dev.openlab.iris.no'
# OPENLAB_URL= 'https://build.openlab.iris.no'
#OPENLAB_URL= 'http://localhost:8888'

#NOTE when changing any of the above after installation, an uninstall/reinstall might be necessary
