import numpy as np

class Channel:
    def send(self, signal=np.array([]), receiver=None, noise='normal'):
        if(receiver==None):
            return self.add_noise(signal, noise)
         

    def add_noise(self, signal=np.array([]), noise='normal'):
        if(noise=='normal'):
            return signal+np.random.normal(0,1,size=signal.size)