length = int(length * rate)
factor = float(frequency) * (pi * 2) / rate
waveform = np.sin(np.arange(length) * factor)


waveform2 = np.power(waveform, 3)
waveform3 = np.power(waveform, 4)
rounded_waveform = np.round(waveform3, 0)

# return np.add(np.add(waveform, waveform2), np.add(rounded_waveform, waveform3))

return waveform


#
# length = math.floor(self.rate/frequency)
# diff = self.rate - length * frequency
# error = diff/length
# frequency += error
# factor = float(frequency) * (pi * 2) / self.rate
# waveform = np.sin(np.arange(length) * factor)
