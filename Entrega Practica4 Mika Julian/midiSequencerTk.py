
import sys
sys.path.insert(0, "./files")        

import instrument
from tkinter import *
from consts import *
import sounddevice as sd
import numpy as np
import mido
import time 

# Secuenciador MIDI con un solo instrumento (el que se le pase o uno por defecto)

class MidiSequencerTk:
    # análogo a lo anterior
    def __init__(self,tk,instruments=None):
        # si no se pasa un instrumento, se crea uno por defecto
        if instruments == None:            
            self.instruments = [instrument.Instrument(tk,amp=0.2,ratio=3,beta=0.6)]
        else:
            self.instruments = instruments

        # Título de la venta
        frame = LabelFrame(tk, text="Midi Sequencer", bg="#908060")
        frame.pack(side=TOP)

        # Selector de archivo MIDI
        frameFile = Frame(frame, highlightbackground="blue", highlightthickness=6)
        frameFile.pack(side=TOP)
        Label(frameFile,text='Archivo MIDI: ').pack(side=LEFT)

        self.file = Entry(frameFile) #.pack(side=RIGHT)
        self.file.insert(14,"media/pirates.mid")
        self.file.pack(side=LEFT)


        # Ventana para información de eventos MIDI
        self.text = Text(frame,height=6,width=23)
        self.text.pack(side=RIGHT)

        # Botones de control play/stop
        playBut = Button(frame,text="Play", command=self.play)
        playBut.pack(side=TOP)
        stopBut = Button(frame,text="Stop", command=self.stop)
        stopBut.pack(side=BOTTOM)

        # para transponer la partitura, si se quiere
        self.transport = 0

        # tiempo entre eventos MIDI (en ms) para el loop de reproducción: "precision del reloj de secuenciación"
        # puede utilizarse para alterar la velocidad de reproducción (tempo) escalando este valor
        self.tick = 1 

        # y estado del secuenciador
        self.state = 'off'

    # obtención de la secuencia midi (noteOn/Off) con tiempos acumulados, relativos al inicio
    def getSeq(self,midiEvents):
        seq = []
        accTime = 0
        for m in midiEvents:
            accTime += m.time
            if m.type=='note_on':
                if m.velocity==0: seq.append((accTime,'noteOff',m.note+self.transport,m.channel))
                else: seq.append((accTime,'noteOn',m.note+self.transport,m.channel))    
            elif m.type=='note_off':
                seq.append((accTime,'noteOff',m.note+self.transport,m.channel))
        return seq


    # reproducción de la secuencia MIDI: prepara la secuencia y lanza el loop de reproducción playLoop
    def play(self):
        events = mido.MidiFile(self.file.get())
        seq = self.getSeq(events)
        print(seq)

        self.state = 'on'
        self.playLoop(seq)

    # método principal de reproducción: se llama a sí mismo cada tick ms para procesar los eventos MIDI que correspondan al tiempo acumulado accTime
    def playLoop(self,seq,item=0,accTime=0):   
        # final de la secuencia -> fin de la recursión
        if item>=len(seq) or self.state =='off':
            return

        # hay que procesar TODOS los ítems cuyo tiempo supere el crono accTime    
        while item<len(seq) and accTime>=seq[item][0]:
            (_,msg,midiNote,chan) = seq[item]  # (time,'noteOff',midNote,channel)

            # mostramos el evento MIDI en la ventana de texto
            self.text.insert('6.0',  f'{msg} {midiNote}\n') 

            # activamos/apagamos nota
            if msg=='noteOn':  
                self.instruments[chan].noteOn(midiNote)                   
            else: # msg noteOff   
                self.instruments[chan].noteOff(midiNote)                   

            # y avanzmos ítem
            item += 1 


        # avanzammos crono con un factor de escalado
        accTime += self.tick/1000

        self.text.after(self.tick,lambda: self.playLoop(seq,item,accTime)) 


    def stop(self):
        for i in range(0, len(self.instruments)):
            self.instruments[i].stop()
        self.state = 'off'   
