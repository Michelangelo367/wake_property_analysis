from tkinter import *
import real_estate as re 

def analyze_command():
    if city_text.get():
        re.propAnalysis_city(city_text.get())
    if zip_text.get():
        re.propAnalysis_zip(zip_text.get())
    if street_text.get():
        re.propAnalysis_street(street_text.get())

window=Tk()

l1=Label(window, text="City:")
l1.grid(row=0, column=0)

l2=Label(window, text="Zip Code:")
l2.grid(row=1, column=0)

l3=Label(window, text="Street: (No Dr., Rd., Ln., etc.)")
l3.grid(row=2, column=0)

city_text=StringVar()
e1=Entry(window, textvariable=city_text)
e1.grid(row=0,column=1)

zip_text=StringVar()
e2=Entry(window, textvariable=zip_text)
e2.grid(row=1, column=1)

street_text=StringVar()
e3=Entry(window, textvariable=street_text)
e3.grid(row=2, column=1)

b1=Button(window, text="Analyze", command=analyze_command)
b1.grid(row=3,column=1)

window.mainloop()

