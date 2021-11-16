from tkinter import filedialog as fd
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from PIL.ExifTags import TAGS
from exif import Image as imk
from selenium import webdriver
from selenium.webdriver.common.by import By



class App:
    def __init__(self) -> None:
        self.root = Tk()
        self.root.geometry("700x420+500+200")
        self.root.title("Place Finder")
        self.index = []
        self.count = 0
      
        self.image_label = Label(self.root,text="Image must be click by phone.")
        self.image_label.place(x=250,y=170)
        
        self.btn_lb = Label(self.root,bg='gray',width=500,height=30)
        self.btn_lb.place(x=0,y=370)
        self.select_btn = Button(self.root,cursor='hand2',text="Select Image",relief=GROOVE,command=self.file_reader)
        self.select_btn.place(x=300,y=380)

    def file_reader(self):
        try:
            del self.index
            self.f1.destroy()
            self.f2.destroy()
        except:pass
        self.index = []
        f_types = [('Jpg Files', '*.jpg')]
        filename = fd.askopenfilename(filetypes=f_types)
        if filename!=None:
            
            self.img = Image.open(filename)
            
            exifdata = self.img.getexif()
            exifdata1 = filename

            self.img = self.img.resize((260,250))
            self.img = ImageTk.PhotoImage(self.img)
            self.sk=Frame(self.root,bg='black',width=700,height=30)
            self.sk.place(x=0,y=0)

            Label(self.sk,text="Image Details",bg='black',fg='white',font=("",10)).place(x=55,y=5)
            Label(self.sk,text="Selected Image",bg='black',fg='white',font=("",10)).place(x=510,y=5)
            
            self.f1 = Frame(self.root,width=200,height=500)
            self.f1.place(x=0,y=35)
            self.f2 = Frame(self.root,width=200,height=500)
            self.f2.place(x=215,y=35)
            self.image_label.config(image=self.img)
            self.image_label.place(x=430,y=35)
            
            self.find_btn = Button(self.btn_lb,text=" Find ",cursor='hand2',relief=RAISED,command=lambda:[self.get_info(exifdata1)])
            self.find_btn.place(x=630,y=10)
            
            for tag_id in exifdata:
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                if isinstance(data, bytes):
                    data = data.decode()
                if self.count !=9:
                    self.index.append(Label(self.f1,text=f"{tag:25}: {data}",fg='blue'))
                    self.index[self.count].pack(pady=2, side= TOP, anchor="w")
                else:
                    self.index.append(Label(self.f2,text=f"{tag:25}: {data}",fg='blue'))
                    self.index[self.count].pack(pady=2, side= TOP, anchor="w")
                self.count+=1
            
            with open(exifdata1, "rb") as src:
                img = imk(src)
            if img.has_exif:
                try: 
                    img.gps_latitude,img.gps_latitude_ref,img.gps_longitude,img.gps_longitude_ref
                    Label(self.root,text="avaliable").place(x=520,y=300)
                except:
                    Label(self.root,text="unavaliable").place(x=520,y=300)   
            self.count=0
            
    def get_info(self,exifdata):
        
        with open(exifdata, "rb") as src:
            img = imk(src)
        if img.has_exif:
            try: 
                self.automate_brow(self.remove_sm([img.gps_latitude,img.gps_longitude],[img.gps_latitude_ref,img.gps_longitude_ref]))
                Button(self.root,text="Exit Browser",cursor='hand2',command=self.driver.quit).place(x=10,y=380)
            except:
                  messagebox.showerror(title="Error",message="Location cannot find ?")    
        else:
            messagebox.showerror(title="Error",message="it's has not metadata")
    

    def remove_sm(self,item,ref):
        li = []
        for i in item:
            i=str(i)
            a = i.translate({ord('('): None,ord(')'): None,ord(','): None})
            a = a.split(" ")
            a[0] = str(int(float(a[0]))) +"°"
            a[1] = str(int(float(a[1]))) +"'"
            a[2] = a[2] +"""" """
            li.append(a[0]+a[1]+a[2])
        li[0] = li[0] + ref[0]
        li[1] = li[1] + ref[1]
        return li[0]+" "+li[1]

    def automate_brow(self,value):
        self.driver = webdriver.Chrome("chromedriver.exe") # Enter whole Address of chromeWebDriver 
        self.driver.maximize_window()
        self.driver.get("https://www.google.com/maps/@20.9880135,82.7525294,5z")

        self.driver.find_element(By.XPATH,"//*[@id='searchboxinput']").send_keys(value)
        self.driver.find_element_by_id("searchbox-searchbutton").click()


app = App()
app.root.mainloop()
# Ready to use it
