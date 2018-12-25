# import the pygame module, so you can use it
import pygame
import time
import sys, os


# 音声合成エンジンのpath
# jtalkbin = '/usr/local/open_jtalk-1.10/bin/open_jtalk '
# options = ' -m syn/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /usr/local/open_jtalk-1.10/dic'

jtalkbin = 'open_jtalk '
# options = '-m /usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'
options = '-m ./Voice/mei/mei_happy.htsvoice -ow /tmp/dialogue/out.wav -x /var/lib/mecab/dic/open-jtalk/naist-jdic'
# 音声合成のコマンドを生成 (open jtalk を 使う場合
def mk_jtalk_command(answer):
    jtalk = 'echo "' + answer + '" | ' + jtalkbin + options + ';'
    play = 'play -q /tmp/dialogue/out.wav; rm /tmp/dialogue/out.wav;'
    return jtalk + play

# define a main function
def main():

    pygame.init()
    pygame.display.set_caption("Virtual Girlfriend")
    global screen,backgroundimage,kanojoimage,textboximage,faceimage,buttonimage,dialoguetext,nametext,dialoguefont
    screen = pygame.display.set_mode((800,600))
    backgroundimage = pygame.image.load("GUI/backgrounds/background0.jpg")
    backgroundimage = pygame.transform.scale(backgroundimage,(800,600))
    kanojoimage = pygame.image.load("GUI/tachie.png")
    kanojoimage = pygame.transform.scale(kanojoimage,(600,600))
    textboximage = pygame.image.load("GUI/textbox.png")
    textboximage = pygame.transform.scale(textboximage,(800,200))
    faceimage = pygame.image.load("GUI/faces/face1.png")
    faceimage = pygame.transform.scale(faceimage,(246,246))
    buttonimage = pygame.image.load("GUI/button.png").convert()
    buttonimage = pygame.transform.scale(buttonimage,(300,70))
    buttonimage.set_alpha(128)

    pygame.font.init()
    namefont = pygame.font.Font('GUI/ipag.ttf',40)
    nametext = namefont.render('電子',True,(255,255,255))
    dialoguefont = pygame.font.Font('GUI/ipag.ttf',30)
    dialoguetext = dialoguefont.render('対話',True,(0,0,0))
    global buttonfont,buttontextlist
    buttonfont = pygame.font.Font('GUI/ipag.ttf',30)
    buttontextlist = []

    global background_pos,kanojo_pos,textbox_pos,face_pos,name_pos,dialogue_pos,button_pos_list,button_text_pos_list
    background_pos=(0,0)
    kanojo_pos=(100,0)
    textbox_pos=(0,400)
    face_pos=(280,40)
    name_pos=(80,405)
    dialogue_pos=(80,470)
    button_pos_list=[(50,20),(450,20),(50,120),(450,120),(50,220),(450,220),(50,320),(450,320)]
    button_text_pos_list=[(70,40),(470,40),(70,140),(470,140),(70,240),(470,240),(70,340),(470,340)]

    opening_dialogue = ["僕には密かに片思いしている女の子がいる。","名前は電子ちゃん。同じ学科の女の子だ。","思えばこの学科に入った時から彼女の端麗な容姿と赤く艷やかな髪の毛に一目惚れしていたらしい。","信じられないかもしれないが、僕は今そんな彼女と二人で沖縄に来ている。","たまたまグループ発表で一緒になり、沖縄旅行ペアチケットをゲットしたのだ。","絶対にこの美ら海水族館で告白をして最高のeeicライフを送ってやるぞ！"]
    for j in range (len(opening_dialogue)):
         screen.fill((0,0,0))
         screen.blit(textboximage,textbox_pos)
         dialogue = opening_dialogue[j]

         put_dialogue(dialogue)

         pygame.display.flip()
         time.sleep(3.5)

        # total 21 sec


    global last_input,ending_flag
    last_input = None
    global running
    running = True

    # main loop
    while running:
        input = get_response("response.txt")
        screen.fill((255,255,255))
        update_all(input)
        time.sleep(0.03)

    if ending_flag == "1":
        screen.fill((0,0,0))
        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        faceimage = pygame.image.load("GUI/faces/face7.png")
        faceimage = pygame.transform.scale(faceimage,(246,246))
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)
        dialoguetext = dialoguefont.render("ちょっと考えさせてもらってもいいかな？",True,(0,0,0))
        answer = 'ちょっと考えさせてもらってもいいかな？'
        screen.blit(dialoguetext,dialogue_pos)



        pygame.display.flip()
        os.system(mk_jtalk_command(answer))
        time.sleep(3)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(textboximage,textbox_pos)
        dialogue = "後日彼女からラインでOKをもらった。キラキラ大学生活の始まりだ！"
        put_dialogue(dialogue)
        pygame.display.flip()
        time.sleep(3)

    if ending_flag == "2":
        screen.fill((0,0,0))
        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        faceimage = pygame.image.load("GUI/faces/face3.png")
        faceimage = pygame.transform.scale(faceimage,(246,246))
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)

        dialoguetext = dialoguefont.render("...私でよければ！",True,(0,0,0))
        answer='私でよければ！'

        screen.blit(dialoguetext,dialogue_pos)
        pygame.display.flip()

        os.system(mk_jtalk_command(answer))

        time.sleep(3)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(textboximage,textbox_pos)
        dialogue = "僕達は手を取り合ってその日の便で東京に帰った。最高の沖縄旅行だったな！"
        put_dialogue(dialogue)
        pygame.display.flip()
        time.sleep(3)

    if ending_flag == "3":
        screen.fill((0,0,0))
        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        faceimage = pygame.image.load("GUI/faces/face3.png")
        faceimage = pygame.transform.scale(faceimage,(246,246))
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)
        dialoguetext = dialoguefont.render("私も好き！付きあおう！",True,(0,0,0))
        answer='私も好き！付きあおう！'

        screen.blit(dialoguetext,dialogue_pos)
        pygame.display.flip()
        os.system(mk_jtalk_command(answer))
        time.sleep(3)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(textboximage,textbox_pos)
        dialogue = "季節外れの台風で僕達は延泊することになった。部屋はひとつしか取れなかったけど...。"
        put_dialogue(dialogue)
        pygame.display.flip()
        time.sleep(4

        )

    if ending_flag == "4":
        screen.fill((0,0,0))
        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        faceimage = pygame.image.load("GUI/faces/face4.png")
        faceimage = pygame.transform.scale(faceimage,(246,246))
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)
        dialogue = "君の事は嫌いじゃないんだけど、友達としてしか見れないな...。ごめんね。"
        answer='君の事は嫌いじゃないんだけど、友達としてしか見れないな...。ごめんね。'
        put_dialogue(dialogue)
        pygame.display.flip()

        os.system(mk_jtalk_command(answer))

        time.sleep(4)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(textboximage,textbox_pos)
        dialogue = "彼女の申し訳無さそうな顔が僕の心を締め付けた。僕の片思いは終わった。"
        textx = dialogue_pos[0]
        texty = dialogue_pos[1]
        for c in dialogue:
            char = dialoguefont.render(c,True,(0,0,0))
            if (textx + char.get_rect().w >= 750):
                textx = dialogue_pos[0]
                texty += char.get_rect().h
            screen.blit(char,(textx,texty))
            textx += char.get_rect().w
        pygame.display.flip()
        time.sleep(4)

    if ending_flag == "5":
        screen.fill((0,0,0))
        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        faceimage = pygame.image.load("GUI/faces/face5.png")
        faceimage = pygame.transform.scale(faceimage,(246,246))
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)
        dialogue = "今日のデートで君のこと好きになる人とかいないと思うな。ごめんね。"
        put_dialogue(dialogue)
        pygame.display.flip()

        os.system(mk_jtalk_command(dialogue))

        time.sleep(4)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(textboximage,textbox_pos)
        dialogue = "そう言うと彼女は僕に背中を向けて歩いて行ってしまった。ひとり置いて行かれた僕をマンタが優しく見守っていた。"
        put_dialogue(dialogue)
        pygame.display.flip()
        time.sleep(4)

    if ending_flag == "6":
        screen.fill((0,0,0))
        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        faceimage = pygame.image.load("GUI/faces/face2.png")
        faceimage = pygame.transform.scale(faceimage,(246,246))
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)
        dialogue = "そういうことは鏡見てから言おうね。普通に無理。バイバイ。"
        put_dialogue(dialogue)
        pygame.display.flip()
        os.system(mk_jtalk_command(dialogue))
        time.sleep(4)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(textboximage,textbox_pos)
        dialogue = "彼女の心ない言葉で僕の夢の大学生活はガラガラと音を立てて崩れ去った。"
        put_dialogue(dialogue)
        pygame.display.flip()
        time.sleep(4)

    if ending_flag == "7":
        screen.fill((0,0,0))
        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        faceimage = pygame.image.load("GUI/faces/face2.png")
        faceimage = pygame.transform.scale(faceimage,(246,246))
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)
        dialogue = "私、にんにく臭い人無理だから。ごめんね。"
        put_dialogue(dialogue)
        pygame.display.flip()
        os.system(mk_jtalk_command(dialogue))
        time.sleep(4)
        screen.fill((0,0,0))
        pygame.display.flip()
        time.sleep(1)
        screen.blit(textboximage,textbox_pos)
        dialogue = "あの時二郎系を頼んでいなかったら何か変わっていたのかな...。"
        put_dialogue(dialogue)
        pygame.display.flip()
        time.sleep(4)




def update_kanojo_face(target_index):
    faceimage = pygame.image.load("GUI/faces/face" + target_index +".png")
    faceimage = pygame.transform.scale(faceimage,(246,246))
    return faceimage
def update_dialogue_txt(target_str):
    dialoguefont = pygame.font.Font('GUI/ipag.ttf',30)
    dialoguetext = dialoguefont.render(target_str,False,(0,0,0))
    return dialoguetext
def update_background(target_index):
    backgroundimage = pygame.image.load("GUI/backgrounds/background" + target_index + ".jpg")
    backgroundimage = pygame.transform.scale(backgroundimage,(800,600))
    return backgroundimage
def get_response(path):
    with open(path) as f:
        input = f.readlines()
    input = [x.strip() for x in input]
    return input
def update_button_text_list(str):
    str = str.split('・')
    list = []
    for i in range(len(str)):
        list.append(buttonfont.render(str[i],True,(0,0,0)))
    return list

def check_same_input(input):
    global last_input
    if input == last_input:
        return True
    else:
        return False
def update_all(input):
    global last_input
    if check_same_input(input):
        return
    last_input = input

    if len(input) == 1:
        global ending_flag
        ending_flag = input[0]
        global running
        running = False
        return

    if len(input) == 3:
        backgroundimage = update_background(input[0])
        faceimage = update_kanojo_face(input[1])
        dialogue = input[2]

        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)

        put_dialogue(dialogue)

        pygame.display.flip()

    elif len(input) == 4:
        backgroundimage = update_background(input[0])
        faceimage  = update_kanojo_face(input[1])
        dialogue = input[2]
        buttontextlist = update_button_text_list(input[3])

        screen.blit(backgroundimage,background_pos)
        screen.blit(kanojoimage,kanojo_pos)
        screen.blit(faceimage,face_pos)
        screen.blit(textboximage,textbox_pos)
        screen.blit(nametext,name_pos)

        put_dialogue(dialogue)

        for i in range(len(buttontextlist)):
            screen.blit(buttonimage,button_pos_list[i])
            screen.blit(buttontextlist[i],button_text_pos_list[i])
        pygame.display.flip()

def put_dialogue(str):
    textx = dialogue_pos[0]
    texty = dialogue_pos[1]
    for c in str:
        char = dialoguefont.render(c,True,(0,0,0))
        if(textx + char.get_rect().w>=750):
            textx = dialogue_pos[0]
            texty+=char.get_rect().h
        screen.blit(char,(textx,texty))
        textx+=char.get_rect().w


if __name__=="__main__":
    main()
