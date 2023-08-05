from .cary5000_file_reader import  Cary5000FileReader
from plotly.offline import init_notebook_mode, iplot, plot
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy import constants as sc


class Cary5000:

    def __init__(self, filename=None,gridfs=None,johan_version=False,absorption=False,**kwargs):
        self.filename = filename
        if johan_version:
            self.version = 'johan'
            self.data = Cary5000FileReader.read_data_from_file(filename)
            print(self.data)
        elif filename:
            self.version = 'cool'
            self.absorption = absorption
            self.data = Cary5000FileReader.read_data(filename=self.filename,**kwargs)
        elif gridfs:
            self.version = 'johan'
            self.data = Cary5000FileReader.read_data_from_gridfs(gridfs)

    def get_wavelength(self, sample):
        if self.version == 'johan':
            return self.data['acquired data'][sample]['Wavelength (nm)']
        return self.data[sample].wavelength

    def get_transmission(self, sample):
        if self.version == 'johan':
            return self.data['acquired data'][sample]['%T']
        return self.data[sample].transmission

    def get_energy(self,sample):
        if self.version == 'johan':
            return 'wir müssen die Versionen wieder abschaffen'
        if self.data[sample].energy is None:
            self.data[sample].energy=self._convert_wavelength_to_energy(self.get_wavelength(sample))

        return self.data[sample].energy

    def is_absorption(self):
        return self.absorption

    def get_samples(self):
        if self.version == 'johan':
            return self.data['sample names']
        else:
            return self.data.keys()

    def get_area_under_curve(self,sample,interval):
        transmi = 100 - self.get_transmission(sample)
        wavelength = self.get_wavelength(sample)
        _, start_idx = self._find_nearest(wavelength, interval[1])
        _, end_idx = self._find_nearest(wavelength, interval[0])
        return np.trapz(transmi[start_idx:end_idx], wavelength[start_idx:end_idx])

    def get_weird_energy_like_stuff_under(self,sample,energy_interval):
        if self.version == 'johan':
            return 'das mit den verschiedenen Versionen ist irgendwie blöd'
        transmi = 100-self.get_transmission(sample)
        energy_axis = self.get_energy(sample)
        _, start_idx = self._find_nearest(energy_axis, energy_interval[0])
        _, end_idx = self._find_nearest(energy_axis, energy_interval[1])
        return np.sum(np.multiply(transmi[start_idx:end_idx], energy_axis[start_idx:end_idx]))


    def correct_step(self,find_step_range=[200,1200], slope_correction=False):
        samples = self.get_samples()

        for sample in samples:
            if sample == 'Baseline 100%T':
                continue

            wave = self.get_wavelength(sample=sample)

            trans = Cary5000._correct_step(wavelength=wave,transmission=self.get_transmission(sample=sample), find_step_range=find_step_range)

            if slope_correction is True:
                trans = Cary5000._correct_slope(wave, trans)
            self.data[sample].transmission = trans

        return

    def plotly_all(self, title='', mode='transmission'):
        init_notebook_mode(connected=True)
        data = []
        for sample in self.get_samples():
            if sample == 'Baseline':
                continue
            x = self.data[sample].wavelength
            y = self.data[sample].transmission
            if mode=='Arturo':
                trace = Cary5000._create_x_y_trace(x, 100-y, sample)
            else:
                trace = Cary5000._create_x_y_trace(x, y, sample)
            data.append(trace)
        layout = Cary5000._get_plotly_layout(title, mode=mode)
        fig = go.Figure(data=data, layout=layout)
        return iplot(fig)

    def plot_sample(self,sample,ax=None, label=None):
        if ax is None:
            ax = plt.axes()
        if label is None:
            ax.plot(self.get_wavelength(sample),self.get_transmission(sample),label=sample)
        else:
            ax.plot(self.get_wavelength(sample),self.get_transmission(sample),label=label)
        return ax

    def find_peak(self,sample):
        transmission = self.get_transmission(sample)
        wavelength = self.get_wavelength(sample)
        index_of_min = np.argmin(transmission)
        return wavelength[index_of_min], transmission[index_of_min], index_of_min

    @staticmethod
    def _find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx

    @staticmethod
    def _correct_step(wavelength, transmission,find_step_range):

        start = find_step_range[1]
        end = find_step_range[0]

        start, start_idx= Cary5000._find_nearest(wavelength,start)
        end, end_idx= Cary5000._find_nearest(wavelength,end)

        grad = np.gradient(transmission, wavelength)
        gmid = np.argmax(abs(grad[start_idx:end_idx]))  + start_idx

        delta1 = transmission[gmid - 1] - transmission[gmid]
        delta2 = transmission[gmid] - transmission[gmid + 1]

        if abs(delta1) > abs(delta2):
            delta = delta1
            for i, t in enumerate(transmission):
                if i < gmid:
                    transmission[i] = transmission[i] - delta
        else:
            delta = delta2
            for i, t in enumerate(transmission):
                if i <= gmid:
                    transmission[i] = transmission[i] - delta

        return transmission

    @staticmethod
    def _correct_slope(wavelength, transmission):
        x = [wavelength[0], wavelength[-1]]
        y = [transmission[0], transmission[-1]]
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        y_delta = intercept - 100 + slope * wavelength
        return transmission - y_delta

    @staticmethod
    def _convert_wavelength_to_energy(wavelength):
        return (sc.h * sc.c / (wavelength*1e-9 * sc.e)) # in eV

    @staticmethod
    def _create_x_y_trace(x, y, name):
        if name == 'Baseline 100%T':
            return go.Scatter(x=x, y=y, name=name, visible='legendonly')
        else:
            return go.Scatter(x=x, y=y, name=name)

    @staticmethod
    def _get_plotly_layout(title='', mode='transmission'):
        if mode=='transmission':
            return go.Layout(
                title = title,
                xaxis=dict(
                    title='Wavelength [nm]'
                ),
                yaxis=dict(
                    title='%T'
                )
            )
        else:
            return go.Layout(
                title=title,
                xaxis=dict(
                    title='Wavelength [nm]'
                ),
                yaxis=dict(
                    title='extinction'
                )
            )

