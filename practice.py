import pathlib
from pydub import AudioSegment
from pydub.playback import play

pathname = str(pathlib.Path(__file__).parent.resolve())
filename = "\\\\explosion_03.wav"

song = AudioSegment.from_file(pathname + filename)

play(song)
