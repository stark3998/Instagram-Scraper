from tkinter import *
master = Tk()
ft="Times 30 bold"
w, h = master.winfo_screenwidth(), master.winfo_screenheight()

master.geometry("%dx%d+0+0" % (w, h))
master.title("Instagram Scraper : Jatin Madan")

background_image= PhotoImage("C:\\Users\\jatin\\Desktop\\Stark\\Wallpaper.jpg")
background_label = Label(master, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


Label(master, text='Username',font=ft).place(x=560,y=340)
Label(master, text='Password',font=ft).place(x=565,y=420) 
e1 = Entry(master,font=ft) 
e2 = Entry(master,font=ft) 
e1.place(x=900,y=340)
e2.place(x=900, y=420)
Button(text="Sign In", font=ft).place(x=1150,y=500)
mainloop() 
