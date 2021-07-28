import librosa
from spectrogram import *

def analyze_spec(spectrogram, freqs, times, sampling_rate=44100.00, threshold_percentile=99):
    '''
    Parameters
    ----------
    spectrogram : numpy.ndarray
        A 2d-array of Fourier coefficients organized by frequencies (rows) and times (columns).

    Returns
    -------
    time_tuples : List[tuple]
        Each tuple contains (time, freqs = []) where freqs is a list of frequencies being played
        at that specified time

    '''
    
    amp_threshold = np.percentile(spectrogram, threshold_percentile)
    print(amp_threshold)
    
    time_freq_tuples = []

    for col_ind in range(0,len(spectrogram[0]), 20):
        myfreqs = []
        amps = []
        for row_ind in range(5, len(spectrogram)):
            amp = spectrogram[row_ind, col_ind]
            if amp > amp_threshold:
                
                if len(amps) == 0:
                    myfreqs.append(freqs[row_ind])
                    amps.append(amp)
                else:
                    for index, a in enumerate(amps):
                        if amp < a:
                            continue
                        else:
                            amps.insert(index, amp)
                            myfreqs.insert(index, freqs[row_ind])
                            break
            '''
                if len(myfreqs) > 4:
                    if amp > min(amps):
                        index = amps.index(min(amps))
                        amps[index] = amp
                        myfreqs[index] = freqs[row_ind]
                else:
                    myfreqs.append(freqs[row_ind])
                    amps.append(amp)
            '''
                  
        myfreqs = myfreqs[:4]            
        time_freq_tuples.append( (times[col_ind], myfreqs) )
    
   # print("time_freq_tuples: " + str(time_freq_tuples))
    return time_freq_tuples

def get_notes(time_freq_tuples):
    '''
    Parameters
    ----------
    time_tuples :
    
    Returns
    -------
    
    '''
    time_note_tuples = []
    for time, freqs in time_freq_tuples:
        notes = []
        for f in freqs:
            n = freq_to_note(f)
            notes.append(n)
        time_note_tuples.append( (time, notes) )
    
  #  print("time_note_tuple: " + str(time_note_tuples))
    return time_note_tuples

def freq_to_note(freq):
    '''
    Determines the closet note based on an input frequency.

    Parameters
    ----------
    freq : float

    Returns
    -------
    note_name : String
    '''

    #TODO finish populating notes
    #notes = { 130.81 : "C3", 138.59 : "C#3/Db3", 146.83 : "D3", 155.56 : "D#3/Eb3", 220.00 : "A3", 261.63 : "C4", 440.00 : "A4",  523.25 : "C5", 880.00 : "A5", 1046.50 : "C6", 1760.00 : "A6"}
    
    notes = populate_notes()
    
    note_dis = abs(440-freq)
    note_name = "A4"
    
    for f in notes.keys():
        new_dis = abs(freq - f)
        if (new_dis < note_dis):
            note_dis = new_dis
            note_name = notes[f]
    
    return note_name

def display_notes(time_note_tuples, listen_time):
    '''
    takes the notes and the times they are played and prints out a how long and 
    which notes to play
    '''
    print("I am at display_notes")
    
    for index in range(len(time_note_tuples) - 1):
        time, notes = time_note_tuples[index]
        next_time, next_notes = time_note_tuples[index + 1]
        
        if (len(notes) > 0 and len(next_notes) > 0 and (notes[0] == next_notes[0] or notes[0] == next_notes[1])):
            time_note_tuples[index + 1] = time, notes
        else:
            print("play " + str(notes) + " for " + str(round(next_time - time, 1)) + " seconds.")
        
    time, notes = time_note_tuples[len(time_note_tuples) - 1]
    print("play " + str(notes) + " for " + str(round(listen_time - time, 1)) + " seconds.")
            
def populate_notes():
    
    note_vals = {32.70 : "1", 65.41 : "2", 130.81: "3", 261.63: "4", 523.25 : "5", 1046.50 : "6"}
    
    note_letters = ["C", "C#/Db", "D", "D#/Eb", "E", "F", "F#/Gb", "G", "G#/Ab", "A", "A#/Bb", "B"]
    
    notes = {}
    
    for letter_index, letter in enumerate(note_letters):
        for start_freq in note_vals:
            end_freq = start_freq * (2.00 ** (letter_index / 12))
            notes.update( {end_freq: letter + note_vals[start_freq]} )
     
    notes.update({2073.00 : "Overtone"})
    return notes


def transcribe_audio(spectrogram, freqs, times):
    listen_time = 1
    time_freq_tuples = analyze_spec(spectrogram, freqs, times)
    time_note_tuples = get_notes(time_freq_tuples)
    display_notes(time_note_tuples, listen_time)

def pitch_shift(recorded_audio, sampling_rate, target_freq):
    S, freqs, times = get_spectogram(recorded_audio)
    old = 1108.7305 
    steps = 12*np.log(target_freq/old)/np.log(2)
    shifted_audio = librosa.effects.pitch_shift(recorded_audio, sampling_rate, n_steps=steps)
    return shifted_audio, sampling_rate

def speed_shift():
    """
    """

