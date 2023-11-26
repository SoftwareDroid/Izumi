from setuptools import setup, find_packages

setup(
    name='Izumi',
    version='1.0.0',
    packages=find_packages(include=[]),
    install_requires=[
        'pygame',
        'SpeechRecognition',
        'pyaudio',
        'hjson',
        'pyautogui',
        'pydub',
        'gtts',
        'ffmpeg',
        'pyinstaller'
    ],
    extras_require={
        # 'interactive': ['matplotlib>=2.2.0', 'jupyter'],
    }
)
