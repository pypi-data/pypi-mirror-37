# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 13:20:01 2018

@author: samantha
"""

import os
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import click

def look_in_csv(city, csv_path):
    lon_lat = []
    city = city.lower() # lower case all letters
    city = city.capitalize() # capitalises
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        try:
            for row in reader:
                if row[0] == city:
                    lon_lat = [float(row[2]), float(row[1])]
        except IndexError:
            print("Location not in database...")
    return lon_lat

def plot_map(lon, lat, city):  
    red_patch = mpatches.Patch(color='#c20000', label='< 5') 
    orange_patch = mpatches.Patch(color='#ff8c57', label='5-6') 
    lorange_patch = mpatches.Patch(color='#ffab57', label='6-6.5') # lighter orange
    yellow_patch = mpatches.Patch(color='#ffea8f', label='6.5-7.2')
    green_patch = mpatches.Patch(color='#c9cf99', label='7.2-7.5')
    lblue_patch = mpatches.Patch(color='#768094', label='7.5-8') # lighter blue
    blue_patch = mpatches.Patch(color='#000280', label='> 8')
            
    city = city.lower()
    m = plt.imread(os.path.dirname(__file__)+"/input/ukphsoil.png")
    plt.imshow(m, extent=[-9,2,50,59])
    plt.axis([-9,2,50,59])
    plt.plot(lon, lat, marker='o', markersize='15', color='white', mfc="none")
    plt.axvline(x=lon, linewidth=2, color="white", alpha=96)
    plt.axhline(y=lat, linewidth=2, color="white", alpha=96)

    plt.title("Soil pH plot of location: %s" % (city.capitalize()))

    plt.legend(loc=3, title="pH",
        handles=[red_patch, orange_patch, lorange_patch, yellow_patch, green_patch, lblue_patch, blue_patch]) 
    plt.savefig('soil-ph_%s.png' % (city))


@click.command()
@click.option('--city', default='Aberystwyth', help='Enter city.')  
def main(city):
    print("Please note: due to the fact that the Earth is spherical and maps are 2-dimensional, there will be some distortion when plotting locations.")
    path = os.path.dirname(__file__)+"/input/latlon.csv"
    lon_lat = look_in_csv(city, path)
    
    plt.figure(1) 
    try:
        plot_map(lon_lat[0], lon_lat[1], city)
    except IndexError:
        print("Location not in database or spelt incorrectly!")
    
##############################

if __name__ == "__main__":   
    main()
