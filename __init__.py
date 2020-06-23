from aqt import mw
from aqt.utils import showWarning
from anki.hooks import addHook
from anki.utils import stripHTMLMedia
import os
import datetime
import urllib
import unicodedata


file_directory = "C:/Audios"
audio_url = "https://www.vocabolaudio.com/audio-it/{}.mp3"

def _normalize_word(word):
    

    nfkd_form = unicodedata.normalize('NFKD', word)
    only_ascii = nfkd_form.encode('ASCII', 'ignore')

    decoded = only_ascii.decode('utf-8')

    return str(decoded)

def get_data(editor):
    ""

    ""

    # get word from current field
    word = stripHTMLMedia(editor.note.fields[editor.currentField])

    clean_word = _normalize_word(word)

    audio_file = save_audio(clean_word)
    if(audio_file == None):
        showWarning('Vocabolaudio: no information found for the word: {}'.format(word))
        return

    editor.addMedia(audio_file)

    for field in editor.note.keys():
        if field == 'Audio' and audio_file != None:
            editor.note[field] = str('[sound:{}.{}]'.format(clean_word, 'mp3'))
            editor.note.flush()
        
    mw.reset()
    
    

def save_audio(word):
    """
    downloads the audio file and saves it to the configured directory
    returns the filepath
    """

    url = str(audio_url).format(word)

    write(url)

    try:
        file_data = urllib.request.urlopen(url)
        if(file_data == None):
            return None
    except:
        return None


    audio = file_data.read()
    if(audio == None):
        return None

    filename = '{0}/{1}.{2}'.format(file_directory, word, 'mp3')
    with open(filename, 'wb') as f:
        f.write(audio)

    return filename

def write(message):
        """
        writes exception-messages in the log.txt file located in the modules base directory
        """

        baseDir = get_base_directory()
        logFile = baseDir + '/log.txt'

        with open(logFile, "a") as log:
            log.write(str('{0} | {1}\n').format(datetime.datetime.now(), message))

def get_base_directory():
        """
        returns the modules base directory
        """

        directory = os.path.dirname(os.path.abspath(__file__))
        results = directory.split('\\')
        tail = results[-1].lower()

        while tail != 'vocabolaudioscraper':
            directory = os.path.dirname(os.path.abspath(directory))
            results = directory.split('\\')
            tail = results[-1].lower()

        return directory

def addEditorButton(buttons, editor):
    """
    creates a new button
    returns new set of buttons
    """

    editor._links['data'] = get_data
    path = get_base_directory()
    icon = path + '/resources/icon.png'

    return buttons + [editor._addButton(icon, 'data', 'get audio')]

addHook('setupEditorButtons', addEditorButton)