import hjson
from src.controller import Controller
from src.speech_to_text import SpeechToText
from src.profile_loader_interface import ProfileLoaderInterface
import src.modules
from src.modules.module_interface import ModuleInterface


class ProfileLoader(ProfileLoaderInterface):
    VERSION_MAJOR: int = 1
    VERSION_MINOR: int = 0

    def __init__(self, controller: Controller, speechToText: SpeechToText):
        self.controller = controller
        self.speechToText = speechToText

    def load_profile(self, filename: str):
        self.controller.clear_pipeline()
        print("load profile: ", filename)
        with open(filename) as jsonFile:
            jsonObject = hjson.load(jsonFile)
            jsonFile.close()
        try:
            if jsonObject["version"][0] < Controller.VERSION_MAJOR:
                print("Profile in wrong version")
                return False
            # Speech to Text Module
            speechModule = jsonObject["speech-to-text"]
            api_key = speechModule.get("api-key", None)
            phrase_time_limit = speechModule.get("phrase_time_limit",5)
            non_speaking_duration = speechModule.get("non_speaking_duration",0.5)
            self.speechToText.phrase_time_limit = phrase_time_limit
            self.speechToText.non_speaking_duration = non_speaking_duration
            self.speechToText.pause_threshold = speechModule.get("pause_threshold",0.8)
            self.speechToText.phrase_threshold = speechModule.get("phrase_threshold",0.3)
            input_language = speechModule["input-language"]
            error_output = speechModule["error-output"]
            technology: str = speechModule["api"]
            mainModule = jsonObject["main-module"]
            sytem_name = mainModule["system-name"]
            system_language = mainModule["system-language"]
            ignore_input = mainModule.get("ignore-input",[])
            debug_output = mainModule["debug-output"]
            ro = mainModule["read-only"]
            sleeping = mainModule.get("start-sleeping", False)
            modules_cache = []
            # Pipeline
            pipeline = jsonObject["pipeline"]["modules"]
            for moduleConfig in pipeline:
                name: str = moduleConfig["name"]

                settings = moduleConfig["settings"]
                activated: bool = moduleConfig["activated"]
                if name in src.modules.module_name_to_class:
                    module = src.modules.module_name_to_class[name](activated, settings)
                    if "id" in moduleConfig:
                        module.identifier = moduleConfig["id"]
                    if issubclass(src.modules.module_name_to_class[name], ModuleInterface):
                        modules_cache.append(module)
                        print("Info: Append Module ", module.__class__.__name__)
                    else:
                        print("Error: Add something to the pipeline which is not a module. Possible modules are: ",
                              src.modules.module_name_to_class.keys())
                        return False
                else:
                    print("Error: Module not found: '", name, "'")
                    return False

            # Atomic change if no errors
            # Do not override key if not given
            if api_key is not None:
                self.speechToText.args.key = api_key
            self.speechToText.input_language = input_language
            self.speechToText.print_errors = error_output

            # Main Module
            self.controller.set_subject_name(sytem_name)
            self.controller.system_language = system_language
            self.controller.debug_output = debug_output
            self.controller._ignore_input = ignore_input
            #self.controller.profile_is_read_only = ro
            if sleeping:
                self.controller._mode = Controller.Mode.SLEEPING
            else:
                self.controller._mode = Controller.Mode.AWAKE
            #print(len(modules_cache))
            for moduleConfig in modules_cache:
                self.controller.append_module(moduleConfig)
            print("INFO: Profile loaded")
            return True
        except KeyError as err:
            print("Profile load entry is missing: ", err)
            return False
        except OSError as e:
            print(e)
            return False
