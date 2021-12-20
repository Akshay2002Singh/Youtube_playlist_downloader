from tkinter import *
from pytube import YouTube
from time import sleep
from os import listdir
from pytube.contrib.playlist import Playlist
import os

list=[]
temp_status=""
file_size=0
# functions
def clear_url_box():
    URL.set("")
def update_status(temp):
    statusvar.set(temp)
    sbar.update()
def update_percentage_status(temp):
    statusvar.set(f"{temp_status}\nDone : {int(temp*100)}%")
    sbar.update()
def progress(stream,chunk,byte_remaining):
    percent = (file_size-byte_remaining)/file_size
    update_percentage_status(percent)
def download_playlist():
    link=URL.get()
    update_status("Collecting information to download playlist.")
    playlist = Playlist(link)
    temp_title=playlist.title.replace('/','_')
    temp_path=os.path.join(os.getcwd(),temp_title)
    os.mkdir(temp_path)
    cur_path.set(temp_path)
    # print(playlist.length)
    i=1
    trials=0
    for p in playlist:
        print(p)
        download_video(p,i,playlist.length)
        i=i+1
    print(list)
    while not list:
        trials=trials+1
        if trials==10:
            break
        for p in list:
            download_video(p,i,playlist.length)
            i=i+1   
    list.clear()
    
    update_status("Playlist Downloaded.")
    URL.set("")

def download_video(video_link,cur,last):
    global temp_status
    global file_size
    update_status(f"Checking video link {cur} out of {last}")
    if video_link!="":
        try:
            yt=YouTube(video_link,on_progress_callback=progress)
        except:
            list.append(video_link)
            return

        # print(yt)
        try:
            update_status(f"Collecting information to download video {cur} out of {last}")
            video = yt.streams.filter(progressive=True,file_extension='mp4')
            video = video.get_highest_resolution()
        except:
            return
        # print(video)
        try:
            # downloading the video
            file_size=video.filesize
            temp_status=f"Downloading video {cur} out of {last}\nTitle:{video.title}\nSize:{video.filesize/1000000} MB"
            update_percentage_status(0)
            video.download(cur_path.get())
            print(f"done {cur}")
            if video_link in list:
                list.remove(video_link)
        except:
            list.append(video_link)
            return
        delete_list()
    else:
        return
def delete_list():
   mylist.delete(0,END)
   showfiles()
def showfiles():
    for video_file in listdir(cur_path.get()):
        if video_file.endswith(".mp4"):
            mylist.insert(END," "+str(video_file)) 
    

    


# main body
if __name__=="__main__":
    root = Tk()
    # window size
    root.title("Elite Youtube Playlist Downloader")
    root.geometry("1000x600")
    root.minsize(1000,600)
    
    # Variables
    URL = StringVar()
    cur_path = StringVar()
    statusvar = StringVar()
    statusvar.set("Ready to download playlist")
    # code to download a video
    heading1=Label(root,text="ELITE AKSHAY",font="calibre 40 bold",relief=RAISED,background="red",padx=10,pady=9)
    heading1.pack()
    space=Label(root,text="",font="calibre 2 bold")
    space.pack()
    heading2=Label(root,text="YOUTUBE PLAYLIST DOWNLOADER",font="Times 25 bold",relief=RAISED,background="cyan",padx=10,pady=9,)
    heading2.pack()
    f1=Frame(root)
    f1.pack(side=TOP,fill=BOTH,expand=True,pady=10)
    name=Label(f1,text="ENTER URL OF PLAYLIST",font="calibre 20 bold italic",relief=FLAT,padx=8,pady=3)
    name.pack()
    space=Label(f1,text="",font="calibre 2 bold")
    space.pack()
    url_input=Entry(f1,textvariable=URL,font="calibre 25 normal",relief=SUNKEN)
    url_input.pack()

    download_btn=Button(f1,text="Download",command=download_playlist,bd=5,fg="blue",font="calibre 18 bold")
    download_btn.pack(side = LEFT, expand = True, fill = X)
    clear_url_btn=Button(f1,text="CLEAR URL",command=clear_url_box,bd=5,font="calibre 18 bold")
    clear_url_btn.pack(side = LEFT, expand = True, fill = X)

    # show files 
    f2=Frame(root)
    f2.pack(side=TOP,fill=BOTH,expand=True)
    heading_files=Label(f2,text="Downloaded Videos",font="Times 20 bold",relief=RAISED,background="yellow",padx=10,pady=9,)
    heading_files.pack(side=TOP)
    # files 
    mylist = Listbox(f2,height=4)
    mylist.pack(side=LEFT,fill=BOTH,expand=True)
    Scroll =Scrollbar(f2)
    Scroll.pack(side=RIGHT,fill=Y)

    Scroll.config(command=mylist.yview)
    mylist.config(yscrollcommand=Scroll.set)


    
    
    # statusbar
    sbar = Label(root,textvariable=statusvar, relief=SUNKEN, anchor="w",padx=10,pady=7,background="cyan",fg="red",font="calibre 12 bold")
    sbar.pack(side=BOTTOM, fill=X)



    root.mainloop()
