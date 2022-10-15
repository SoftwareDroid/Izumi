# Import all usable modules
from src.modules.dictation.dictation_module import DictationModule
from src.modules.print.print_module import PrintModule
from src.modules.punctuation_marks_replacer.punctuation_marks_replacer import PunctuationMarksReplacer
# from src.modules.offline_translator.offline_translator_module import OfflineTranslatorModule
# from src.modules.deepl_translator.deepl_translator_module import DeeplTranslatorModule
# from src.modules.japanese_learning.japanese_char_transformer_module import JapaneseCharTransformerModule
from src.modules.file_writer.file_writer_module import FileWriterModule
from src.modules.text_to_speech.text_to_speech_module import TextToSpeechModule

module_name_to_class = {PrintModule.__name__: PrintModule, DictationModule.__name__: DictationModule,
                        PunctuationMarksReplacer.__name__: PunctuationMarksReplacer,
                        # OfflineTranslatorModule.__name__: OfflineTranslatorModule,
                        # DeeplTranslatorModule.__name__: DeeplTranslatorModule,
                        FileWriterModule.__name__: FileWriterModule,
                        # JapaneseCharTransformerModule.__name__:JapaneseCharTransformerModule,
                        TextToSpeechModule.__name__: TextToSpeechModule}

