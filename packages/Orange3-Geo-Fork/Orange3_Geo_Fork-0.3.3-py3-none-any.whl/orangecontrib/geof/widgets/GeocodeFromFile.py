#widget to suppoprt geocoding from a file

import io
import tkinter as tk
from tkinter import filedialog
from os import path

import pandas as pd
import numpy as np
from AnyQt.QtCore import Qt
from AnyQt.QtWidgets import QComboBox, QItemEditorFactory, QLineEdit, \
    QCompleter, QHeaderView
from Orange.data import Table, Domain, StringVariable, DiscreteVariable, ContinuousVariable
from Orange.widgets import gui, widget, settings
from Orange.widgets.utils.itemmodels import DomainModel, PyTableModel
from Orange.widgets.widget import Input, Output

class GeoCodeFromFile(widget.OWWidget):
    name = 'Geocode File'
    description = 'Encode region names into geographical coordinates from a custom file of coordinates - output this widget to an orange data table'
    icon = "icons/Geocoding.svg"
    priority = 40

    class Inputs:
        None

    class Outputs:
        coded_data = Output("Coded Data", Table, default=True)
    
    settingsHandler = settings.DomainContextHandler()
    resizing_enabled = False

    #the initialisation function for the widget
    def __init__(self):
        super().__init__()
        self.data = None
        self.domainmodels = []
        self.unmatched = []
        top = self.controlArea

        box = gui.vBox(self.controlArea, "Geocode A File")
        fpbox = gui.vBox(self.controlArea, "Selected File")

        gui.button(
            box, 
            self, 
            label='Pick File', 
            callback= lambda: pick_file()
        )
        
        gui.button(
            box, 
            self, 
            label='Resolve Coordinates', 
            callback= lambda: resolve_coords()
        )

        #function to remove the old label and update it
        def refresh_label(path):
            nonlocal fpbox
            fpbox.hide()
            fpbox = None
            fpbox = gui.vBox(self.controlArea, "Selected File")
            if (not path.endswith('xlsx')):
                path = "SELECT AN XLSX FILE"
            gui.label(fpbox, self, path)

        #function to pick a file to geocode - save the path to disk
        def pick_file():
            root = tk.Tk()
            root.withdraw()
            file_path = filedialog.askopenfilename()
            pathwriter = open("xlfp.txt", "w")
            pathwriter.write(file_path)
            pathwriter.close()
            refresh_label(file_path)

        def getd(district, coords):
            try:
                for i in range(len(coords['lat'])):
                    if (coords['city_ascii'][i] == district):
                        #get the index for the coords
                        return i
            except:
                print('Invalid District: ' + district)
                exit()
            
        #function to resolve coordinates
        def resolve_coords():
            data = None
            try:
                fp = open("xlfp.txt", "r")
                _path = fp.readline()
                df = pd.read_excel(_path)
                #mark empty fields in lat and long with a 0
                df.fillna({'Lat':0, 'Long':0}, inplace=True)
                data = df
            except:
                print("Invalid file or Broken Path")
            #read the coordinate file
            try:
                csvPath = path.join(path.dirname(path.dirname(__file__)), 'worldcities.csv')
                df = pd.read_csv(csvPath)
                coordfile = df.to_dict()
            except:
                print("could not find coordinate file worldcities.csv in main Orange folder")

            #search and update the data
            rindex = 0
            for row in data.itertuples(index=True):
                if (row.Lat == 0.0):
                    indx = getd(row.District, coordfile)
                    
                    #if index is valid then set coords
                    if (indx != None):
                        data.at[rindex, 'Lat'] = coordfile['lat'][indx]
                        data.at[rindex, 'Long'] = coordfile['lng'][indx]
                    if (data.at[rindex, 'Lat'] == 0.0 or data.at[rindex, 'Long'] == 0.0):
                        data.at[rindex, 'Lat'] = np.nan
                        data.at[rindex, 'Long'] = np.nan
                rindex+=1
            try:
                writer = pd.ExcelWriter('output.xlsx')
                data.to_excel(writer, 'Sheet1')
                writer.save()
                output = Table.from_file('output.xlsx')
                self.Outputs.coded_data.send(output)
            except:
                print("Unable to write excel file")

#the main function
def main():
    from AnyQt.QtWidgets import QApplication
    a = QApplication([])
    ow = GeoCodeFromFile()
    ow.show()
    ow.raise_()
    a.exec()
    ow.saveSettings()

if __name__ == "__main__":
    main()