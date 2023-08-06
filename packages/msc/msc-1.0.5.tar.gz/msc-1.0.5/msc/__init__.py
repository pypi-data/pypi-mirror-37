import os,sys,inspect
from kafka import KafkaConsumer
from kafka import KafkaProducer
import _thread
import json,datetime
from pymongo import MongoClient
import base64,pprint,time
from colorama import init, Fore, Back, Style
import copy

class DictConvert(object):
    """Object view of a dict, updating the passed in dict when values are set
    or deleted. "Dictate" the contents of a dict...: """

    def __init__(self, d = {}):
        # since __setattr__ is overridden, self.__dict = d doesn't work
        object.__setattr__(self, '_DictConvert__dict', d)
        
    # Dictionary-like access / updates
    def __getitem__(self, name):
        value = self.__dict[name]
        if isinstance(value, dict):  # recursively view sub-dicts as objects
            value = DictConvert(value)
        return value

    def __setitem__(self, name, value):
        self.__dict[name] = value
    def __delitem__(self, name):
        del self.__dict[name]

    # Object-like access / updates
    def __getattr__(self, name):
        try:
            return self[name]
        except:
            return None

    def __setattr__(self, name, value):
        self[name] = value
    def __delattr__(self, name):
        del self[name]

    def __repr__(self):
        return "%s(%r)" % (type(self).__name__, self.__dict)
    def __str__(self):
        return str(self.__dict)


    def toJson(self):
        return dict(
            (key, value)
            for (key, value) in self.__dict__.items()
        )["_DictConvert__dict"]

class db():
    __mongo_uri = ""

    def __init__(self,mongo_uri = ""):
        self.__mongo_uri = mongo_uri
        
    def conexion(self):
        print("conexion a mongo")
        conexion = None
        try:        
            conexion = MongoClient(self.__mongo_uri)
            return conexion
        except:
            return None

class microservice(db):

    variable_entorno = "MQ"
    _debug = False
    service_app = ""
    service_name = ""
    service_topic_name = ""
    service_version = ""
    server_cola_mensajeria = ""
    servers_mensajeria = []
    service_es_worker = None
    __producer = None
    __consumer = None
    __flujo = []
    __metadataBifurcacion = []
    __functionWorkerCambiarData = None
    __errores = {}
    __config_serv = {}
    __respuesta_asincronos = []

    def __init__(self,configuracion):
        self._debug  = configuracion["_debug"]

        self.service_app = configuracion["_appName"]
        self.service_name = configuracion["_actionName"]
        self.service_es_worker = True if configuracion["_type"].upper() == "WORKER" else False
        if configuracion["_appName"] == "appcoppel" and configuracion["_versionName"] == "v1":
            self.service_topic_name = configuracion["_actionName"]
        else:
            self.service_topic_name = configuracion["_appName"]+"_"+configuracion["_versionName"]+"_"+configuracion["_actionName"]
        self.service_version = configuracion["_versionName"]

        #Reviso que existan las variables de entorno
        f = self.obtener_vars_entorno()
        if not f:
            if configuracion["_zookeeperServer"] != "":
                self.server_cola_mensajeria = configuracion["_zookeeperServer"]
                self.servers_m_q()
            else:
                print("No se definio el servidor de messagequeue")
                sys.exit(0)
        else:
            self.servers_m_q()

    def servers_m_q(self):
        var = self.server_cola_mensajeria.split(",")
        arr = []
        for item in var:
            if item[len(item)-4:len(item)] == "2181":
                modif = item[0:len(item)-4] + "9092"
                arr.append(modif)
            else:
                arr.append(item)
        self.servers_mensajeria = arr

    def obtener_vars_entorno(self):
        self.server_cola_mensajeria = os.environ.get(self.variable_entorno)
        return True if self.server_cola_mensajeria else False

    def setType(self, tipo):
        self.service_es_worker = True if tipo.upper() == "WORKER" else False
    
    def serErrors(self,obj):
        self.__errores = obj

    def start(self,function = object,flujo=[]):
        if self.service_es_worker == None:
            print("No se ha definido tipo de microservicio")
            sys.exit(0)
        else:
            if self.service_es_worker:
                print("start Worker")
                self.__config_serv = flujo
                self.funcion_worker(function,flujo)
            else:
                print("start Bifurcacion")
                flujito = self.modificarFlujo(flujo)

                self.funcion_bifurcacion(function,flujito)
            
    def modificarFlujo(self,flujo):

        reconstruido = []    
        modificado = []
        if len(flujo) > 0:
            modificado.append({
                "appName":self.service_app,
                "name":self.service_name,
                "version":self.service_version
            })
            
            for item3 in flujo:
                modificado.append(item3)


            objetos = len(modificado)
            count = 0

            for item in modificado:
                objeto = {}
                objInsertar = []
                if type(item) is dict:
                    # ! Owner_Conf
                    if count == 0:
                        objeto["grabar_metadata"] = True
                        if item["version"] == "v1" and item["appName"] == "appcoppel":
                            objeto["owner_conf"] = item["name"]
                        else:
                            objeto["owner_conf"] = item["appName"]+"_"+item["version"]+"_"+item["name"]
                    else:

                        if modificado[count]["appName"] == "appcoppel" and modificado[count]["version"] == "v1":
                            objeto["owner_conf"] = modificado[count]["name"]
                        else:
                            objeto["owner_conf"] =  modificado[count]["appName"]+"_"+ modificado[count]["version"]+"_"+ modificado[count]["name"]
                    
                    # ! Worker_Conf
                    if (count + 1) < objetos:
                        if type(modificado[count+1]) is list:
                            worker_conf = ""
                            total = len(modificado[count+1])
                            for item2 in modificado[count+1]:
                                worker_conf += item2["appName"]+"_"+item2["version"]+"_"+item2["name"] + ","
                                try:
                                    objInsertar.append({
                                        "end": False,
                                        "async":True,
                                        "paralelos":total,
                                        "owner_conf": item2["appName"]+"_"+item2["version"]+"_"+item2["name"],
                                        "worker_conf": modificado[count + 2]["appName"]+"_"+modificado[count + 2]["version"]+"_"+modificado[count + 2]["name"]
                                    })
                                except:
                                    objInsertar.append({
                                        "end": True,
                                        "async":True,
                                        "paralelos":total,
                                        "owner_conf": item2["appName"]+"_"+item2["version"]+"_"+item2["name"],
                                        "worker_conf": ""
                                    })

                            worker_conf = worker_conf[:len(worker_conf) - 1]
                           
                            objeto["worker_conf"] = worker_conf
                        else:
                            if  modificado[count+1]["appName"] == "appcoppel" and  modificado[count+1]["version"] == "v1":
                                objeto["worker_conf"] = modificado[count+1]["name"]
                            else:
                                objeto["worker_conf"] = modificado[count+1]["appName"]+"_"+modificado[count+1]["version"]+"_"+modificado[count+1]["name"]
                    else:
                        objeto["worker_conf"] = ""
                        
                    # ! End
                    if (count + 1) < objetos :
                        objeto["end"] = False
                    else:
                        objeto["end"] = True

                    reconstruido.append(objeto)
                    if len(objInsertar) > 0:
                        for objetito in objInsertar:
                            reconstruido.append(objetito)
                

                count = count + 1
                
        else:
            print("no tiene flujo")

        print(json.dumps(reconstruido,sort_keys=True,indent=4)) if self._debug else self._debug
        return reconstruido

    def funcion_bifurcacion(self,function,flujo):
        self.__functionWorkerCambiarData = function
        if len(inspect.getargspec(function).args) == 0:
            print("")
            print("")
            print("La funcion (startBifurcacion) recibe un objeto funcion")# debera recibir 2 argumentos no : "+str(countArgs))
            print("*****************************************************************************")
        else:
            countArgs = len(inspect.getargspec(function).args)
            if countArgs != 5:
                print("*****************************************************************************")
                print("la funcion de entrada debera recibir 5 argumentos no : "+str(countArgs))
                print("funcionalidad de la funcion : modificar la data de entrada del siguiente worker")
                print("Argumentos:")
                print("    1 argumento  = para recibir Nombre del worker que respondio")
                print("    2 argumento  = para recibir Id_transaction")
                print("    3 argumento  = para recibir Configuracion general del Microservicio")
                print("    4 argumento  = para recibir Data inicial de la transaccion")
                print("    5 argumento  = para recibir Respuesta del Worker anterior")
                print("*****************************************************************************")
            else:
                if len(flujo) == 0:
                    print("****************************************")
                    print("No se recibio el flujo del a bifurcacion")
                    print("****************************************")
                else:
                    self.__flujo = flujo
                    self.startConsumer(self.__functionBifurcacion)

    def funcion_worker(self,function,config={}):
        if len(inspect.getargspec(function).args) == 0:
            print("")
            print("")
            print("La funcion (del worker) recibe un objeto funcion")# debera recibir 2 argumentos no : "+str(countArgs))
            print("*****************************************************************************")
        else:
            try:
                countArgs = len(inspect.getargspec(function).args)
                if countArgs == 3:
                    self.startConsumer(function,config)
                else:
                    print("*****************************************************************************")
                    print("la funcion de entrada debera recibir 3 argumentos no : "+str(countArgs))
                    print("Argumentos:")
                    print("    1 argumento  = para recibir los datos de configuracion del microservicio")
                    print("    2 argumento  = para recibir los datos de entrada al servicio")
                    print("    3 argumento  = para recibir funcion escribirWorkerAsincrono")
                    print("La funcion  debe retornar una tupla ejemplo :  (0 =int,{} =json)")
                    print("*****************************************************************************")
            except Exception as e:
                print(e)
                print("la funcion debe retornar una tupla ejm.: return (0,{})")
        
    def conecctMQ(self):
        ret = False
        try:
            self.__producer = KafkaProducer(bootstrap_servers=self.servers_mensajeria)
            self.__consumer = KafkaConsumer(self.service_topic_name,bootstrap_servers=self.servers_mensajeria,group_id=str(self.service_topic_name))
            ret = True
        except:
            ret = False
        return ret
    
    def __json_to_b64(self,json_in):
        return base64.b64encode(str.encode(json.dumps(json_in)))

    def __b64_to_json(self,encoded):
        decoded = base64.b64decode(encoded)
        return json.loads(decoded.decode('utf-8'))

    def startConsumer(self,function,config={}):
        if self.conecctMQ() == True:
            print("startConsumer")
            print(" * Running Daemon on : " + str(self.servers_mensajeria) + " servicio: " + self.service_topic_name)
            try:
                for message in self.__consumer:
                    try:
                        objeto = self.__b64_to_json(message.value)
                        _thread.start_new_thread(self.__functionBridge,(function,config,objeto,self.llamar_worker_asincrono,))
                    except Exception as e:
                        print(e)
                        pass
            finally:
                print("se desconecto la cola de mensajeria (reconectar)")
                self.startConsumer(function)

        else:
	        print("Error:\n############################\nNo esta activo el Message Queue\n############################\n")

    def __functionBridge(self,function,*args):
        if "data" in args[1] and ("smoketest" in args[1]["data"] 
            or ("configuraciones" in args[1]["data"] and args[1]["data"]["configuraciones"] == True)
            or ("reload" in args[1]["data"])):

            metadata = args[1]["metadata"]
            data = args[1]["data"]
            headers = args[1]["headers"]
            respuesta = {}
            respuesta["meta"] = {}
            respuesta["data"] = {}
            respuesta["meta"]["id_transaction"] = ""
            respuesta["meta"]["status"] = "SUCCESS"
            if "smoketest" in args[1]["data"]:
                respuesta["data"]["response"] = {
                    "errorCode":"0",
                    "userMessage":"smoketest ok"
                }
            else:
                if "reload" in args[1]["data"]:
                    print("RECARGAR ")
                    self.__metadataBifurcacion = []
                    respuesta["data"]["response"] = self.__config_serv
                else:
                    self.__config_serv["container_id"] = os.environ.get("HOSTNAME")
                    respuesta["data"]["response"] = self.__config_serv

            respuestax = {}                                                                                                                                                                                                                                                  																																																														
            respuestax["metadata"] = metadata                                                                                                                                                                                                                                            
            respuestax["headers"] = headers                                                                                                                                                                                                                                              
            respuestax["data"] = data     
            respuestax["response"] = respuesta
            respuestax["metadata"]["time"] = str(datetime.datetime.now())                                                                                                                                                                                                                
            respuestax["metadata"]["worker"]  = respuestax["metadata"]["owner"]                                                                                                                                                                                                           
            respuestax["metadata"]["owner"]  = self.service_name
            respuestax["metadata"]["mtype"] = "output"                                                                                                                                                                                                                                   
            if("uowner" in respuestax["metadata"]):                                                                                                                                                                                                                                      
                uowner = respuestax["metadata"]["uowner"]                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                        
            if("uworker" in respuestax["metadata"]):                                                                                                                                                                                                                                     
                uworker = respuestax["metadata"]["uworker"]                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                        
            respuestax["metadata"]["uworker"] = uowner                                                                                                                                                                                                                                   
            respuestax["metadata"]["uowner"] = uworker 


            if(metadata["bifurcacion"] == True):                                                                                                                                                                                                                                        
                metadata["bifurcacion"] = False                                                                                                                                                                                                                                     
                TOPICO = respuestax["metadata"]["callback"]
                self.__escribirColaMensajeria(TOPICO,respuestax,metadata["id_transaction"])
            else:
                TOPICO = "respuesta_"+metadata["owner"]
                respuesta2 = {"_id":respuestax["metadata"]["id_transaction"],"response":respuestax["response"],"metadata":respuestax["metadata"]}
                self.__escribirColaMensajeria(TOPICO,respuesta2,metadata["id_transaction"])
        else:
            if self.service_es_worker == True:
                
                configuracion_entrada = args[0]
                mensaje_entrada = args[1]
                funcion_entrada = args[2]
                code = 0
                datax = {}
                try:
                    code,dataxx = function(configuracion_entrada,mensaje_entrada,funcion_entrada)
                    try:
                        datax = dataxx.toJson()
                    except:
                        datax = dataxx
                except Exception as e:
                    code,datax  = -99,{}
                    error = {"_id":args[1]["metadata"]["id_transaction"],"servicio":self.service_topic_name,"error":str(e)}
                    # TODO Escribir en cola de mensajeria

                metadata = mensaje_entrada["metadata"]
                data = mensaje_entrada["data"]
                headers = mensaje_entrada["headers"]
                if "headers" not in   mensaje_entrada or "data" not in   mensaje_entrada or "metadata" not in   mensaje_entrada:
                    print("No contiene datos correctos")
                else:
                    respuesta = self.__response(code,datax,metadata)
                    respuestax = {}                                                                                                                                                                                                                                                              																																																														
                    respuestax["metadata"] = metadata                                                                                                                                                                                                                                            
                    respuestax["headers"] = headers                                                                                                                                                                                                                                              
                    respuestax["data"] = data                                                                                                                                                                                                                                              
                    respuestax["response"] = respuesta                                                                                                                                                                                                                                      
                    respuestax["metadata"]["time"] = str(datetime.datetime.now())                                                                                                                                                                                                                
                    respuestax["metadata"]["worker"]  = respuestax["metadata"]["owner"]                                                                                                                                                                                                           
                    respuestax["metadata"]["owner"]  = self.service_topic_name
                    respuestax["metadata"]["mtype"] = "output"                                                                                                                                                                                                                        
                    if("uowner" in respuestax["metadata"]):                                                                                                                                                                                                                                      
                        uowner = respuestax["metadata"]["uowner"]                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                                                                
                    if("uworker" in respuestax["metadata"]):                                                                                                                                                                                                                                     
                        uworker = respuestax["metadata"]["uworker"]                                                                                                                                                                                                                          
                                                                                                                                                                                                                                                                                                
                    respuestax["metadata"]["uworker"] = uowner                                                                                                                                                                                                                                   
                    respuestax["metadata"]["uowner"] = uworker    

                    if(metadata["bifurcacion"] == True):                                                                                                                                                                                                                                        
                        metadata["bifurcacion"] = False                                                                                                                                                                                                                                     
                        TOPICO = respuestax["metadata"]["callback"]
                        self.__escribirColaMensajeria(TOPICO,respuestax,respuestax["metadata"]["id_transaction"])
                    else:
                        TOPICO = "respuesta_"+metadata["owner"]                                                                                                                                                                                                                             
                        respuesta2 = {"_id":respuestax["metadata"]["id_transaction"],"response":respuestax["response"],"metadata":respuestax["metadata"]}                                                                                                                                                                                                                                                                                                                             
                        self.__escribirColaMensajeria(TOPICO,respuesta2,respuestax["metadata"]["id_transaction"])

            else:
                TOPICO,respuesta = function(args[0],args[1])
                if TOPICO != "":
                    self.__escribirColaMensajeria(TOPICO,respuesta,args[1]["metadata"]["id_transaction"])


    def llamar_worker_asincrono(self,topico,respuesta,id_transaction = ""):
        _thread.start_new_thread(self.escribir,(topico,respuesta,id_transaction,))

    def escribir(self,topico,respuesta,idTransaction):
        if respuesta != {}:
            msj = self.__json_to_b64(respuesta)
            self.__producer.send(topico,key=str.encode(str(idTransaction)),value=msj)
            self.__producer.flush()
            
            if topico[:9] == "respuesta":
                print(Fore.RED+"*****************   SALIDA FINAL  *****************"+Fore.WHITE) if self._debug else self._debug
                print(Fore.YELLOW+"[ "+idTransaction+" ] -  SALIDA - ["+topico+"]") if self._debug else self._debug
                print(json.dumps(respuesta["response"],sort_keys=True,indent=4)) if self._debug else self._debug
                print(" "+Fore.WHITE) if self._debug else self._debug
            else:
                print(Fore.RED+"********************   SALIDA   *******************"+Fore.WHITE) if self._debug else self._debug
                #print("[ "+idTransaction+" ] -  SALIDA - ["+topico+"]\n"+str(respuesta)) if self._debug else self._debug
                print("[ "+idTransaction+" ] -  output - ["+topico+"]\n"+"Headers      : "+str(respuesta["headers"])+"\nData        : "+str(respuesta["data"])) if self._debug else self._debug
    
    def __escribirColaMensajeria(self,topico,respuesta,idTransaction = ""):
        self.escribir(topico,respuesta,idTransaction)

    def __response(self,code,data = None,metadata = None):
        response = {}
        response["meta"] = {}
        response["data"] = {}

        response["meta"]["id_transaction"] = metadata["id_transaction"]
        
        if code == 0:
            response["meta"]["status"] = "SUCCESS"    
            response["data"]["response"] = data
        else:
            response["meta"]["status"] = "ERROR"
            response["data"]["response"] = {
                "errorCode":str(code),
                "userMessage":self.__buscarMensaje(str(code))
            }
        return response

    def __buscarMensaje(self,id):
        res = ""
        if str(id) in self.__errores:
            res = self.__errores[str(id)]

        else:
            if str(id) == "-99":
                res = "Ocurrio algo inesperado, favor de intentarlo de nuevo."
            else:
                res = "Error No Definido"
        return res

    def __borrarAsincrono(self,id_trans):
        index = 0
        for item in self.__respuesta_asincronos:
            if item["id_transaction"] == id_trans:
                self.__respuesta_asincronos.pop(index)
            index += 1

    def __functionBifurcacion(self,configService,jsonArguments):
        log = print
        if jsonArguments == {}:
            return "",{}
        else:
            """Retorna topico a responder y json a escribir"""
            metadata = jsonArguments["metadata"]
            data = jsonArguments["data"]
            headers = jsonArguments["headers"]
            response = {}
            if "response" in jsonArguments:
                response = jsonArguments["response"]
            OWNER = metadata["owner"]
            ID_TRANSACCION = metadata["id_transaction"]
            try:
                print(Fore.GREEN+"********************   ENTRADA  ********************"+Fore.WHITE) if self._debug else self._debug
                log("[ "+ID_TRANSACCION + " ] - ENTRADA - ["+metadata["owner"]+"] \nHeaders : "+str(headers) +"\nData : "+ str(data) +"\nResponse : "+ str(response)) if self._debug else self._debug
                metadata["mtype"] = "input"
                metadata["time"] = str(datetime.datetime.now())
                metadata["bifurcacion"] = True
                
                cursor_conf = self.__buscar(metadata["owner"])
                asyncronos = cursor_conf["worker_conf"].split(",")
                worker_conf = ""

                if "async" in cursor_conf:
                    print("Respondio asyncrono :",metadata["owner"]) if self._debug else self._debug
                    self.__respuesta_asincronos.append({
                        "id_transaction" : metadata["id_transaction"],
                        "worker":metadata["owner"],
                        "response":jsonArguments["response"]
                    })
                    #data_inicial,metadata_inicial = self.__obtenerMetadataInicial(metadata["id_transaction"])
                    data_inicial,metadata_inicial = jsonArguments["metadata"]["inicial_bifurcacion"]["data"],jsonArguments["metadata"]["inicial_bifurcacion"]["metadata"]
                    if jsonArguments["response"]["meta"]["status"] == "SUCCESS":
                        count_respuestas = 0
                        respuestas_pegadas = {}
                        for iteracion in self.__respuesta_asincronos:
                            if iteracion["id_transaction"] == metadata["id_transaction"]:
                                respuestas_pegadas[str(iteracion["worker"])] = iteracion["response"]["data"]["response"]
                                count_respuestas += 1

                            if count_respuestas == 3:
                                break                        
                        if count_respuestas == cursor_conf["paralelos"]:
                            if cursor_conf["end"] == False:
                                self.__borrarAsincrono(metadata["id_transaction"])
                                worker_conf = cursor_conf["worker_conf"]
                                log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" NO ES SERVICIO FINAL") if self._debug else self._debug
                                uWorker_async = metadata["uworker"]
                                string = str(time.time()).replace('.', '')
                                jsonArguments["metadata"]["id_operacion"] = int(string)
                                jsonArguments["metadata"]["uowner"] = uWorker_async
                                jsonArguments["metadata"]["worker"] = worker_conf
                                jsonArguments["metadata"]["uworker"] = metadata["worker"]+"_"+str(metadata["id_operacion"])
                                jsonArguments["metadata"]["owner"] = self.service_topic_name
                                responseAnterior = {}
                                if "data" in jsonArguments["response"]:
                                    jsonArguments["response"]["data"]["response"] = respuestas_pegadas
                                    responseAnterior = jsonArguments["response"]["data"]["response"]
                                else:
                                    responseAnterior = jsonArguments["data"]
                                data_mod = self.__functionWorkerCambiarData(OWNER,ID_TRANSACCION,{},data_inicial,responseAnterior)
                                
                                if data_mod != {}:
                                    jsonArguments["data"] = data_mod
                                jsonArguments["response"] = {}
                                return jsonArguments["metadata"]["worker"],jsonArguments
                            else:
                                self.__borrarAsincrono(metadata["id_transaction"])
                                log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" ES SERVICIO FINAL") if self._debug else self._debug
                                JSON_RESPUESTA_FIN = {}
                                if JSON_RESPUESTA_FIN == {}:
                                    jsonArguments["response"]["data"]["response"] = respuestas_pegadas
                                    JSON_RESPUESTA_FIN = jsonArguments["response"]
                                
                                #self.borrarMetadata(metadata["id_transaction"])

                                msj = {"_id":metadata["id_transaction"],"response":JSON_RESPUESTA_FIN,"metadata":metadata_inicial}
                                
                                return "respuesta_"+metadata["callback"],msj
                        else:
                            return "",{}
                    else:
                        self.__borrarAsincrono(metadata["id_transaction"])
                        log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" ES SERVICIO FINAL") if self._debug else self._debug
                        JSON_RESPUESTA_FIN = {}
                        if JSON_RESPUESTA_FIN == {}:
                            JSON_RESPUESTA_FIN = jsonArguments["response"]
                        #self.borrarMetadata(metadata["id_transaction"])
                        msj = {"_id":metadata["id_transaction"],"response":JSON_RESPUESTA_FIN,"metadata":metadata_inicial}
                        return "respuesta_"+metadata["callback"],msj
                    
                else:
                    # ? validar si es llamado a workers asincronos
                    if len(asyncronos) <=  1:
                        worker_conf = cursor_conf["worker_conf"]
                        if "grabar_metadata" in cursor_conf:
                            #self.__guardarMetadata("metadata_"+metadata["owner"],{"_id":jsonArguments["metadata"]["id_transaction"],"metadata":jsonArguments["metadata"],"data":jsonArguments["data"]})
                            # ? gurdo la metadata y data inicial para cuando la necesite
                            inicial = {}
                            inicial["data"] = copy.copy(jsonArguments["data"])
                            inicial["metadata"] = copy.copy(jsonArguments["metadata"])


                            #jsonArguments["metadata"]["inicial"] = inicial
                            jsonArguments["metadata"]["inicial_bifurcacion"] = inicial
                            uWorker_async = metadata["uworker"]
                            string = str(time.time()).replace('.', '')
                            jsonArguments["metadata"]["id_operacion"] = int(string)
                            jsonArguments["metadata"]["uowner"] = uWorker_async
                            jsonArguments["metadata"]["worker"] = worker_conf
                            jsonArguments["metadata"]["uworker"] = metadata["worker"]+"_"+str(metadata["id_operacion"])
                            jsonArguments["metadata"]["owner"] = self.service_topic_name
                            data_mod = self.__functionWorkerCambiarData(OWNER,ID_TRANSACCION,{},jsonArguments["data"],jsonArguments["data"])
                            if data_mod != {}:
                                jsonArguments["data"] = data_mod
                            jsonArguments["response"] = {}
                            return jsonArguments["metadata"]["worker"],jsonArguments
                        else:
                            #data_inicial,metadata_inicial = self.__obtenerMetadataInicial(metadata["id_transaction"])
                            data_inicial,metadata_inicial = jsonArguments["metadata"]["inicial_bifurcacion"]["data"],jsonArguments["metadata"]["inicial_bifurcacion"]["metadata"]
                            success =True

                            #Reviso la respuesta del servicio entrante
                            if "response" in jsonArguments and jsonArguments["response"]["meta"]["status"] == "ERROR":
                                success = False
                            
                            # si success y  servicio es fin y  envio al servicio que sigue
                            if success == True:
                                log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" SUCCESS") if self._debug else self._debug
                                if cursor_conf["end"] == False:
                                    log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" NO ES SERVICIO FINAL") if self._debug else self._debug
                                    uWorker_async = metadata["uworker"]
                                    string = str(time.time()).replace('.', '')
                                    jsonArguments["metadata"]["id_operacion"] = int(string)
                                    jsonArguments["metadata"]["uowner"] = uWorker_async
                                    jsonArguments["metadata"]["worker"] = worker_conf
                                    jsonArguments["metadata"]["uworker"] = metadata["worker"]+"_"+str(metadata["id_operacion"])
                                    jsonArguments["metadata"]["owner"] = self.service_topic_name
                                    responseAnterior = {}
                                    if "data" in jsonArguments["response"]:
                                        responseAnterior = jsonArguments["response"]["data"]["response"]
                                    else:
                                        responseAnterior = jsonArguments["data"]
                                    data_mod = self.__functionWorkerCambiarData(OWNER,ID_TRANSACCION,{},data_inicial,responseAnterior)
                                    
                                    if data_mod != {}:
                                        jsonArguments["data"] = data_mod
                                    jsonArguments["response"] = {}
                                    if "worker_tmp" in data_mod:
                                        return data_mod["worker_tmp"],jsonArguments
                                    else:
                                        return jsonArguments["metadata"]["worker"],jsonArguments
                                else:
                                    log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" ES SERVICIO FINAL") if self._debug else self._debug
                                    JSON_RESPUESTA_FIN = {}
                                    if JSON_RESPUESTA_FIN == {}:
                                        JSON_RESPUESTA_FIN = jsonArguments["response"]

                                    #self.borrarMetadata(metadata["id_transaction"])
                                    msj = {"_id":metadata["id_transaction"],"response":JSON_RESPUESTA_FIN,"metadata":metadata_inicial}
                                    return "respuesta_"+metadata["callback"],msj
                            else:
                                log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" ERROR") if self._debug else self._debug
                                msj = {"_id":metadata["id_transaction"],"response":jsonArguments["response"],"metadata":metadata_inicial}
                                #self.borrarMetadata(metadata["id_transaction"])
                                return "respuesta_"+metadata["callback"],msj
                    else:
                        #data_inicial,metadata_inicial = self.__obtenerMetadataInicial(metadata["id_transaction"])
                        data_inicial,metadata_inicial = jsonArguments["metadata"]["inicial_bifurcacion"]["data"],jsonArguments["metadata"]["inicial_bifurcacion"]["metadata"]
                        success =True

                        #Reviso la respuesta del servicio entrante
                        if "response" in jsonArguments and jsonArguments["response"]["meta"]["status"] == "ERROR":
                            success = False
                        
                        if success == True:
                            for work in asyncronos:
                                # si success y  servicio es fin y  envio al servicio que sigue
                                log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" SUCCESS") if self._debug else self._debug
                                log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" NO ES SERVICIO FINAL") if self._debug else self._debug
                                uWorker_async = metadata["uworker"]
                                string = str(time.time()).replace('.', '')
                                jsonArguments["metadata"]["id_operacion"] = int(string)
                                jsonArguments["metadata"]["uowner"] = uWorker_async
                                jsonArguments["metadata"]["worker"] = work
                                jsonArguments["metadata"]["uworker"] = metadata["worker"]+"_"+str(metadata["id_operacion"])
                                jsonArguments["metadata"]["owner"] = self.service_topic_name
                                responseAnterior = {}
                                if "data" in jsonArguments["response"]:
                                    responseAnterior = jsonArguments["response"]["data"]["response"]
                                else:
                                    responseAnterior = jsonArguments["data"]
                                data_mod = self.__functionWorkerCambiarData(OWNER,ID_TRANSACCION,{},data_inicial,responseAnterior)
                                
                                if data_mod != {}:
                                    jsonArguments["data"] = data_mod
                                jsonArguments["response"] = {}
                                self.__escribirColaMensajeria(jsonArguments["metadata"]["worker"],jsonArguments,jsonArguments["metadata"]["id_transaction"])
                        else:
                            log("[ "+ID_TRANSACCION + " ] - "+metadata["owner"] +" ERROR") if self._debug else self._debug
                            msj = {"_id":metadata["id_transaction"],"response":jsonArguments["response"],"metadata":metadata_inicial}
                            #self.borrarMetadata(metadata["id_transaction"])
                            return "respuesta_"+metadata["callback"],msj

            except Exception as e:            
                error = {"_id":jsonArguments["metadata"]["id_transaction"],"servicio":self.service_topic_name,"error":str(e)}
                #self.borrarMetadata(jsonArguments["metadata"]["id_transaction"])
                self.__escribirColaMensajeria("Errores_criticos",error,jsonArguments["metadata"]["id_transaction"])

            return self.service_topic_name,{}

    def __buscar(self,microservicio):
        ret = { "end":True,"worker_conf":""}
        for item in self.__flujo:
            if item["owner_conf"] == microservicio:
                ret = item
                break
        return ret