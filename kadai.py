import tkinter as tk
import random
index=0 #ゲームの進行状況を管理
timer=0 #ゲームオーバー時に時間に5秒止める処理に使う
score=0 #点数を管理
hisc=1000 #ハイスコア
difficulty=0 #難易度
tsugi=0 #次に出てくるネコの番号
cursor_x = 0
cursor_y = 0
mouse_x = 0
mouse_y = 0
mouse_c = 0
def mouse_move(e):
	global mouse_x, mouse_y
	mouse_x = e.x
	mouse_y = e.y
	
def mouse_press(e):
		global mouse_c
		mouse_c = 1
neko = []
check = []
for i in range(10):
	neko.append([0, 0, 0, 0, 0, 0, 0, 0])
	check.append([0, 0, 0, 0, 0, 0, 0, 0])
def draw_neko():
	cvs.delete("NEKO")
	for y in range(10):
		for x in range(8):
			if neko[y][x] > 0:
				cvs.create_image(x*72+60, y*72+60, image=img_neko[neko[y][x]], tag="NEKO")
def check_neko():
	#盤面のコピー
	for y in range(10):
		for x in range(8):
			check[y][x] = neko[y][x]
	#縦方向3並びチェック
	for y in range(1,9):
		for x in range(8):
			if check[y][x] > 0:
				if check[y-1][x] == check[y][x] == check[y+1][x]:
					neko[y-1][x] = neko[y][x] = neko[y+1][x] = 7
	#横方向3並びチェック
	for y in range(10):
		for x in range(1,7):
			if check[y][x] > 0:
				if check[y][x-1] == check[y][x] == check[y][x+1]:
					neko[y][x-1] = neko[y][x] = neko[y][x+1] = 7
	#ななめ方向3並びチェック
	for y in range(1,9):
		for x in range(1,7):
			if check[y][x] > 0:
				if check[y-1][x-1] == check[y][x] == check[y+1][x+1]:					neko[y-1][x-1] = neko[y][x] = neko[y+1][x+1] = 7
				if check[y-1][x+1] == check[y][x] == check[y+1][x-1]:
					neko[y-1][x+1] = neko[y][x] = neko[y+1][x-1] = 7
# 揃ったマスを空白にし、揃ったマスの個数を返す
def sweep_neko():
	num = 0
	for y in range(10):
		for x in range(8):
			if neko[y][x] == 7:
				neko[y][x] = 0
				num += 1
	return num
# すべてのマスに対して下に１個移動できるかをチェックし、
# 移動できた場合は下に移動する。
# 移動できた場合はTrueを返す
def drop_neko():
	flg = False
	for y in range(8,-1,-1):
		for x in range(8):
			if neko[y][x] != 0 and neko[y+1][x] == 0:
				neko[y+1][x] = neko[y][x]
				neko[y][x]=0
				flg = True
	return flg
# 最上段にネコマスがあったらTrueを返す
def over_neko():
	for x in range(8):
		if neko[0][x] > 0:
			return True
	return False
# 最上段にランダムでネコをセットする(0は空欄)
def set_neko():
	for x in range(8):
		#neko[0][x] = random.randint(0,6)
		neko[0][x] = random.randint(0,difficulty)
# 文言を表示する
def draw_txt(txt,x,y,size,color,tg):
	fnt = ("HGS創英角ﾎﾟｯﾌﾟ体 標準" ,size,"bold")
	#2ピクセルずらして影を描画
	cvs.create_text(x+5,y+5,text=txt,fill="black",font=fnt,tag=tg)
	cvs.create_text(x,y,text=txt,fill=color,font=fnt,tag=tg)
def game_main():
	#global index,timer,score,tsugi
	global index,timer,score,tsugi,hisc,difficulty
	global cursor_x,cursor_y,mouse_c
	if index == 0: # タイトルロゴ
		draw_txt("リアぷよ",312,240,100,"white","TITLE")
		cvs.create_rectangle(168, 384, 456, 456, fill="yellow", width=0, tag="TITLE")
		draw_txt("甘口", 312, 420, 40, "white", "TITLE")
		cvs.create_rectangle(168, 528, 456, 600, fill="orange", width=0, tag="TITLE")
		draw_txt("中辛", 312, 564, 40, "white", "TITLE")
		cvs.create_rectangle(168, 672, 456, 744, fill="red", width=0, tag="TITLE")
		draw_txt("辛口", 312, 708, 40, "white", "TITLE")
		index = 1
		mouse_c =0
	elif index == 1: # タイトル画面 スタート待
		difficulty = 0
		if mouse_c == 1:
			if 168 < mouse_x < 456 and 384 < mouse_y < 456:
				difficulty = 4
			if 168 < mouse_x < 456 and 528 < mouse_y < 600:
				difficulty = 5
			if 168 < mouse_x < 456 and 672 < mouse_y < 744:
				difficulty = 6
		if difficulty > 0:
			#盤面初期化
			for y in range(10):
				for x in range(8):
					neko[y][x] = 0
			mouse_c = 0
			score = 0
			tsugi=0
			cursor_x = 0
			cursor_y = 0
			set_neko()
			draw_neko()
			cvs.delete("TITLE")
			index=2
	elif index == 2: #落下
		if drop_neko() == False:
			index = 3
		draw_neko()
	elif index == 3: # 揃ったか
		check_neko()
		draw_neko()
		index = 4
	elif index == 4: #揃ったネコがあれば消す
		sc = sweep_neko()
		#score = score + sc*10
		score = score + sc*difficulty*2
		if score > hisc:
			hisc = score
		if sc > 0:
			index = 2
		else:
			if over_neko() == False:
				#tsugi = random.randint(1,6)
				tsugi = random.randint(1,difficulty)
				index=5
			else:
				index = 6
				timer = 0
		draw_neko()
	elif index == 5: # マウス入力を待つ
		if 24 <= mouse_x < 24+72*8 and 24 <= mouse_y <24+72*10:
			cursor_x = int((mouse_x-24)/72)
			cursor_y = int((mouse_y-24)/72)
			if mouse_c == 1:
				mouse_c =0
				set_neko()
				neko[cursor_y][cursor_x] = tsugi
				tsugi = 0
				index = 2
		cvs.delete("CURSOR")
		cvs.create_image(cursor_x*72+60,cursor_y*72+60,image=cursor,tag="CURSOR")
		draw_neko()
	elif index == 6: #ゲームオーバー
		timer += 1
		if timer== 1:
			draw_txt("ばたんきゅ～",312,348,60,"white","OVER")
		if timer == 50:
			cvs.delete("OVER")
			index=0
	cvs.delete("INFO")
	draw_txt(f"得点{score}",763,690,32,"white","INFO")
	draw_txt(f"最高得点{hisc}",752,740,32,"white","INFO")
	if tsugi > 0:
		cvs.create_image(768,150,image=img_neko[tsugi],tag="INFO")
	root.after(100,game_main)
root = tk.Tk()
root.title("リアぷよ ~ちょっとリアルなぷよぷよ~")
root.resizable(False, False)
root.bind("<Motion>", mouse_move)
root.bind("<ButtonPress>", mouse_press)
cvs = tk.Canvas(root, width=912, height=768)
cvs.pack()
bg = tk.PhotoImage(file="u.png")
cursor = tk.PhotoImage(file="c2.png")
img_neko = [
	None,
	tk.PhotoImage(file="g.png"),
	tk.PhotoImage(file="r.png"),
	tk.PhotoImage(file="y.png"),
	tk.PhotoImage(file="b.png"),
	tk.PhotoImage(file="p.png"),
    tk.PhotoImage(file="s.png"),
	tk.PhotoImage(file="k4.png")
]
cvs.create_image(456, 384, image=bg)
#2行削除
game_main()
root.mainloop()
