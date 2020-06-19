#Kupujem prodajem - Polovni racunari

# class adPrice - cena
# class adName - ime
# class locationSec - mesto
import bs4
import requests
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from tkinter import *
from functools import partial
import time

karakteri = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMčČćĆšŠđĐžŽ- . ,0123456789,€dinKontakt Kupujem Pozvati Novo"

class Predmet:
    def __init__(self, imeKlase, karakteriZaFilter,brojStrana):
        self.imeKlase = imeKlase
        self.karakteriZaFilter = karakteriZaFilter
        self.brojStrana = brojStrana
     

    def Lista(self,brojStrana):#vraca listu (ime,cena,lokacija....)
        lista = []
        listaFinal =[]
        for i in range(1,brojStrana):
            url = "https://www.kupujemprodajem.com/Kompjuteri-Desktop/Polovni-kompjuteri/10-98-" + str(i)+"-grupa.htm"
            res = requests.get(url)
            soup = bs4.BeautifulSoup(res.text , "lxml")
            for i in soup.select("."+self.imeKlase):
                podatak = i.text
                lista.append(str(podatak))
                
            for j in lista:
                if(j != "Mesto/Grad"):
                    listaFinal.append(''.join(c for c in j if c in self.karakteriZaFilter))
        return listaFinal

def FilterCena(cenaLista):#bez decimalnih vrednosti samo cena i valuta
    cenaFilter=[]
    for i in cenaLista:
        string = ""
        prekidac = True
        for j in i:
            if (j != "," and prekidac == True):
                string += j
            elif(j == ","):
                prekidac = False
                
        if("€" in i):
            string += "€"
            
        cenaFilter.append(string)
    return cenaFilter
    

#Slanje mejla sa attachment-om (text + fajl)

def slanjeMejla(posaljioc,lozinka,primaoc,imeFajla):
    
    salje = posaljioc.get()
    lozinka = lozinka.get()
    prima = primaoc.get()
    subject = "Python!"
    nazivFajla = imeFajla.get()


    msg = MIMEMultipart()
    msg['From'] = salje
    msg['To'] = prima
    msg['Subject'] = subject

    teloPoruke = "Ovaj mejl je poslat preko pythona!"#tekstualni deo mejla
    msg.attach(MIMEText(teloPoruke,'plain'))

    fajl = nazivFajla
    attachment = open(fajl, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= " + fajl)

    msg.attach(part)
    text = msg.as_string()

    server = smtplib.SMTP('smtp.gmail.com' , 587)
    server.starttls()
    server.login(salje,lozinka)
    server.sendmail(salje,prima,text)
    server.quit()
    print("Uspesno ste poslali mejl korisniku : " + str(prima))

#skidanje podataka sa neta i upisivanje u PDF
    
    
def PDF(SacuvajKao , brStrana):
    
    brojStrana = int(brStrana.get())
    sacuvajKao = SacuvajKao.get()

    p1 = Predmet("adName" , karakteri, brojStrana)
    p2 = Predmet("adPrice" , karakteri, brojStrana)
    p3 = Predmet("locationSec" , karakteri, brojStrana)

    ime = p1.Lista(brojStrana)
    cena = p2.Lista(brojStrana)
    mesto = p3.Lista(brojStrana)
    print("Skinuti su podaci sa sajta...")
    
    pdf = canvas.Canvas(sacuvajKao+".pdf")
    pdf.setTitle("KupujemProdajem - Racunari")
    pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))#Registrovanje fonta
    pdf.setFont('Vera', 12)

    y = 810
    for i in range(1,len(ime)):
        string = str(str(i)+"."+ime[i-1]+"   ||   "+cena[i-1]+"   ||   "+mesto[i-1])
        pdf.drawString(0,y,string)    
        y -= 20
        if(y <= 0):
            y = 810            
            pdf.showPage()#prelazak na novu stranu
            pdf.setFont('Vera', 12)    
    pdf.save()
    time.sleep(5)
    print("PDF je kreiran i sacuvan pod nazivom 'Racunari.pdf'")
    time.sleep(1)
########################################################################################################################
    
#window
tkWindow = Tk()  
tkWindow.geometry('400x150')  
tkWindow.title('Uros Jevtic - Namenski racunarski sistemi - Projekat 2')
tkWindow.configure(bg='#02022d')

##0290f0
#From - mejl osobe koja salje fajl
posaljiocLabel = Label(tkWindow, text="Posaljioc",bg='#02022d',fg='white').grid(row=0, column=0)
posaljioc = StringVar()
posaljiocEntry = Entry(tkWindow, textvariable=posaljioc,bg='#0290f0',fg='white').grid(row=0, column=1)


#password - lozinka osobe koja salje fajl 
lozinkaLabel = Label(tkWindow,text="Lozinka",bg='#02022d',fg='white').grid(row=1, column=0)  
lozinka = StringVar()
lozinkaEntry = Entry(tkWindow, textvariable=lozinka, show='*',bg='#0290f0',fg='white').grid(row=1, column=1)  

#To - mejl osobe kojoj se salje fajl (primaoc)
primaocLabel = Label(tkWindow, text="Primaoc",bg='#02022d',fg='white').grid(row=2, column=0)
primaoc = StringVar()
primaocEntry = Entry(tkWindow, textvariable=primaoc,bg='#0290f0',fg='white').grid(row=2, column=1)

#FileName - naziv fajla koji saljemo
nazivFajlalaLabel = Label(tkWindow, text="Naziv fajla",bg='#02022d',fg='white').grid(row=3, column=0)
nazivFajla = StringVar()
nazivFajlaEntry = Entry(tkWindow, textvariable=nazivFajla,bg='#0290f0',fg='white').grid(row=3, column=1)


#SaveAs - ime pdf fajla kojeg cemo kreirati
sacuvajKaoLabel = Label(tkWindow, text="Sacuvaj kao",bg='#02022d',fg='white').grid(row=0, column=4)
sacuvajKao = StringVar()
sacuvajKaoEntry = Entry(tkWindow, textvariable=sacuvajKao,bg='#0290f0',fg='white').grid(row=0, column=5)

#Pages - koliko strana sa sajta skidamo
brStranaLabel = Label(tkWindow, text="Broj strana",bg='#02022d',fg='white').grid(row=2, column=4)
brStrana = StringVar()
brStranaEntry = Entry(tkWindow, textvariable=brStrana,bg='#0290f0',fg='white').grid(row=2, column=5) 

 
slanjeMejla = partial(slanjeMejla, posaljioc, lozinka,primaoc,nazivFajla)
PDF = partial(PDF, sacuvajKao, brStrana)

#dugme za slanje
slanjeDugme = Button(tkWindow, text="Posalji mejl", command=slanjeMejla).grid(row=6, column=1)

#dugme za pdf fajl
PDFDugme = Button(tkWindow, text="Napravi PDF fajl", command=PDF).grid(row=6, column=5)  

tkWindow.mainloop()


