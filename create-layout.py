import tkinter.ttk as ttk  #ktinter대형도서관의 ttk라는 소형도서관을 사용하겠다.
from tkinter import *
import tkinter.messagebox as msgbox
from tkinter import *
from tkinter import filedialog
from PIL import Image
import os


root = Tk()
root.title("Merge Images")

#파일추가
def add_file():
    files = filedialog.askopenfilenames(title="합칠 이미지 파일들을 선택하시오", \
        filetypes=(("PNG 파일", "*.png"), ("모든파일", "*")), \
            initialdir=r"/Users/kis")
    #사용자가 선택한 파일목록
    for file in files:
        list_file.insert(END, file)

#선택삭제
def del_file():
    #print(list_file.curselection())
    for index in reversed(list_file.curselection()):
        list_file.delete(index)

#저장경로(폴더)
def browse_dest_path():
    folder_selected = filedialog.askdirectory()
    if folder_selected is None: #사용자가 X를 누르거나 취소를 누를 때
        return
    #print(folder_selected)
    txt_dest_path.delete(0, END)
    txt_dest_path.insert(0, folder_selected)

#시작
def start():
    #각 옵션들의 값을 확인
    print("가로넓이:", cmb_width.get())
    print("간격:", cmb_space.get())
    print("포맷:", cmb_format.get())

    #파일목록 확인 경고 메세지
    if list_file.size() == 0:
        msgbox.showwarning("경고", "이미지 파일을 추가하세요")
        return

    #저장경로 확인 경고메세지
    if len(txt_dest_path.get()) ==0:
        msgbox.showwarning("경고", "저장경로를 선택하세요")
        return

    #이미지 합치기
    merge_image()

def merge_image():
    # print(list_file.get(0, END)) #모든 파일 목록을 가져오기
    images = [Image.open(file) for file in list_file.get(0,END)]
    print(images)

    widths, heights = zip(*(image.size for image in images))
    print(widths, heights)

    max_width, total_height = max(widths), sum(heights)

    #스케치북 준비
    result_img = Image.new("RGB", (max_width, total_height, total_height), (255,255,255)) #배경흰색
    y_offset = 0 #y위치

    for idx, img in enumerate(images):
        result_img.paste(img, (0,y_offset))
        y_offset += img.size[1]

        #실제 percent 정보를 계산
        progress = (idx+1) / len(images) * 100
        p_var.set(progress)
        progress_bar.update()

    dest_path = os.path.join(txt_dest_path.get())
    result_img.save(dest_path)
    msgbox.showinfo("알림", "작업이 완료되었습니다")




#파일프레임
file_frame = Frame(root)
file_frame.pack(fil = "x", padx=5, pady=5) #간격띄우기


#가로넓이 확보
btn_add_file = Button(file_frame, padx=5, pady=5, width=12, text="파일추가", command=add_file)
btn_add_file.pack(side="left")

btn_del_file = Button(file_frame, padx=5, pady=5, width=12, text="선택삭제", command=del_file)
btn_del_file.pack(side="right")


#list frame
list_frame = Frame(root)
list_frame.pack(fill="both", padx=5, pady=5)

scrollbar = Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")

list_file = Listbox(list_frame, selectmode = "extence", height=15, yscrollcommand = scrollbar.set)
list_file.pack(side="left", fill="both", expand=True)
scrollbar.config(command=list_file.yview)


#저장경로 프레임
path_frame = LabelFrame(root, text="저장경로")
path_frame.pack(fill="x", padx=5, pady=5, ipady=5)

txt_dest_path = Entry(path_frame)
txt_dest_path.pack(side="left", fill="x", expand=True, padx=5, pady=5, ipady=4) #높이변경

#찾아보기 버튼
btn_dest_path = Button(path_frame, text = "찾아보기", width = 7, command=browse_dest_path)
btn_dest_path.pack(side="right", padx=5, pady=5)



#option frame
frame_option = LabelFrame(root, text="옵션")
frame_option.pack(padx=5, pady=5, ipady=5)


#1.가로넓이 옵션
#가로넓이 레이블
lbl_with = Label(frame_option, text="가로넓이", width=5)
lbl_with.pack(side="left", padx=5, pady=5)

#가로넓이 콤보
opt_width = ["원본유지", "1024", "800", "640"]
cmb_width = ttk.Combobox(frame_option, state="readonly", values=opt_width, width=10)
cmb_width.current(0) #콤보박스에서 가장 먼저 나타낼 값의 인덱스 위치
cmb_width.pack(side="left", padx=5, pady=5)


#2. 간격옵션
#간격옵션 레이블
lbl_space = Label(frame_option, text="간격", width=5)
lbl_space.pack(side="left", padx=5, pady=5)

#간격 옵션 콤보
opt_space = ["없음", "좁게", "보통", "넓게"]
cmb_space = ttk.Combobox(frame_option, state="readonly", values=opt_space, width=10)
cmb_space.current(0) #콤보박스에서 가장 먼저 나타낼 값의 인덱스 위치
cmb_space.pack(side="left", padx=5, pady=5)


#3.파일 포맷옵션
#파일 포맷 레이블
lbl_format = Label(frame_option, text="포맷", width=5)
lbl_format.pack(side="left", padx=5, pady=5)

#파일 포맷 옵션 콤보
opt_format = ["PNG", "JPG", "BMP"]
cmb_format = ttk.Combobox(frame_option, state="readonly", values=opt_format, width=10)
cmb_format.current(0)
cmb_format.pack(side="left", padx=5, pady=5)

#진행상황 progress bar
frame_progress = LabelFrame(root, text="진행상황")
frame_progress.pack(fill="x", padx=5, pady=5, ipady=5)

p_var= DoubleVar()
progress_bar = ttk.Progressbar(frame_progress, maximum=100, variable=p_var)
progress_bar.pack(fill="x", padx=5, pady=5)

#실핼프레임
frame_run = Frame(root)
frame_run.pack(fill="x", padx=5, pady=5)

btn_close = Button(frame_run, padx=5, pady=5, text="닫기", width=12, command=root.quit)
btn_close.pack(side="right", padx=5, pady=5)

btn_start = Button(frame_run, padx=5, pady=5, text="시작", width=12, command=start)
btn_start.pack(side="right", padx=5, pady=5)

root.resizable(False, False)
root.mainloop()