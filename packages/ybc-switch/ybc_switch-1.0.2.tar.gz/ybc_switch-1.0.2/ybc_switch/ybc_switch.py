from pydub import AudioSegment
import ybc_speech as speech

def analysis(filename):
    sound = AudioSegment.from_mp3(filename).set_frame_rate(16000)
    sound.export('tmp.wav', format = "wav")
    text = speech.voice2text('tmp.wav')
    return text
