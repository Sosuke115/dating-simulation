
#!/bin/bash
#!/usr/bin/python3
#
# 音声対話システムデモ（bash 版）


chmod u+x question.py
chmod u+x question2.py
chmod u+x happyend1.py
chmod u+x badend1.py
chmod u+x GUI/GUI.py

## dialogue directory ##
tmpdirname=/tmp/dialogue

#前回の好感度
pre_favorability=0
#好感度
favorability=0
file_number=1
#時間
time=10
endflag=0
#背景(for GUI)
background=0
#表情(for GUI)　0がNormal　1がangry 2がhappy
face=0
#満腹度
full=0
#file_number計算処理を1のときskip
skip=0
#決定的な選択(二郎など)
badconditions=0




# gnome-terminal -- GUI/GUI.py
python3 GUI/GUI.py &
sleep 21
# もしディレクトリが存在しなければ作成
if [ ! -e $tmpdirname ];then
	mkdir ${tmpdirname}
fi

echo "0" > badconditions.txt

while true; do
	clear
	# echo "$endflag"
	# 21時になったら終了(gameover)
	if [ $time = 21 ]; then
		endflag=5
		echo "$endflag" > response.txt
		sleep 1
	fi


	echo "好感度：$favorability"
	#もし時間が一定以上たつもしくはendflag1なら、帰るか告白を選択
	#好感度、副好感度によってED分岐
	echo "$time時"


	face=0
	if [ $file_number = 5  ] || [ $file_number = 9  ]; then
		echo "$file_number" > response1.txt
		# echo "$file_number" > response.txt
	else
		echo "0" > response1.txt
		# echo "0" > response.txt
	fi



	echo "$face" >> response1.txt

	# echo "$face" >> response.txt

	#最初の質問+選択肢
	echo "####$file_number"
  cp response1.txt response.txt
	./question.py dialogue/aquarium/dialogue${file_number}.conf 1
	cp response1.txt response.txt

  # rm reponse.txt



	# sleep 1 #4へ変更
	if [ $file_number = 5  ] || [ $file_number = 9  ]; then
		echo "$file_number" > response1.txt
		# echo "$file_number" > response.txt
	else
		echo "0" > response1.txt

		# echo "0" > response.txt
	fi

	echo "$face" >> response1.txt

	# echo "$face" >> response.txt

	echo "（どうしようか・・・・）" >> response1.txt

	# echo "（どうしようか・・・・）" >> response.txt

	cp response1.txt response.txt
	./question2.py dialogue/aquarium/dialogue${file_number}.conf 1
	cp response1.txt response.txt




	# adinrec による録音
	filename=${tmpdirname}/input.wav
	adinrec $filename > /dev/null
	# echo "キーボードから文字をにゅうりょくしてください"
	# read DATA
	#Ctrl-C で抜けるための処理
	if [ ! -e $filename ];then
		rmdir $tmpdirname
		exit;
	fi

	# 話者認識
	sidfile=${tmpdirname}/spkid.txt

	#cd sid;
	bash sid/test.sh $filename $sidfile;
	#cd ..

	# 現在の話者番号を格納（使ってない）
	# もし前の状態を保存しておきたければ別変数/別ファイルを用意する
 	sidnum=$(cat $sidfile)

	# echo "$sidnum"



	# 音声認識
	asrresult=${tmpdirname}/asrresult.txt


	echo $filename > ${tmpdirname}/list.txt


	# 音声認識をして結果をファイルに保存
	# もし前の状態を保存しておきたければ別変数/別ファイルを用意する

	julius -C asr/grammar.jconf -filelist ${tmpdirname}/list.txt 2> /dev/null | grep "^sentence1: " | sed -e 's/sentence1://' -e 's/silB//' -e 's/silE//' -e 's/ //g' > ${asrresult}
  # cp $DATA $asrresult

	# sleep 1

	# ${tmpdirname}/list.txt 2> /dev/null | grep "^sentence1: " | sed -e 's/sentence1://' -e 's/silB//' -e 's/silE//' -e 's/ //g' > ${asrresult2}
	rm ${tmpdirname}/list.txt



	# 話者認識/音声認識結果を応答を生成する
	# 状態/履歴への依存性を持たせたければこのプログラムを適宜修正（引数変更等）

  # rm response.txt
	cp $asrresult data.txt
 	Test=$(<data.txt) #音声入力に戻すときはここをもどす
	#echo "入力してください"
	#read Test

	if [ $Test = '二郎系ラーメン' ]; then
		echo "1" > badconditions.txt
	fi

	#badword.txtから一行ずつwhileで読み込み、一致するものがあれば笑顔
	while IFS= read -r line; do
		# echo "$line"
		if [ $line = $Test ]; then
			face=1
		fi
	done < dialogue/aquarium/badword.txt

	#goodword.txtから一行ずつwhileで読み込み、一致するものがあれば嫌な顔
	while IFS= read -r line; do
		# echo "$line"
		if [ $line = $Test ]; then
			face=2
		fi
	done < dialogue/aquarium/goodword.txt





	if [ $file_number = 5  ] || [ $file_number = 9  ]; then
		echo "$file_number" > response1.txt
		# echo "$file_number" > response.txt
	else
		echo "0" > response1.txt
		# echo "0" > response.txt
	fi

	echo "$face" >> response1.txt

	# echo "$face" >> response.txt

　#入力音声に対する応答
  cp response1.txt response.txt
	./response.py dialogue/aquarium/dialogue${file_number}.conf $sidnum $asrresult
	cp response1.txt response.txt

	while IFS= read -r line; do
		# echo "$line"
		if [ $line = 'え？もう１回言って' ]; then
			skip=1
		fi
	done < response.txt

	#response.txtを読み込んで”え？もう一回いって"があればdialogue維持

	# sleep 1


	# 事後処理
	# rm $filename $

	rm $filename $sidfile $asrresultt

	#入力された音声をTestに保存


	# echo "$Test"
	count=1

	#calculate file_number

	if [ $file_number = 6 ] && [ $Test = "レクチャー" ]; then
		file_number=22
		skip=1
	elif [ $file_number = 6 ] && [ $Test = "工作" ]; then
		file_number=23
		skip=1
	fi

	if [ $file_number = 9 ] && [ $Test = "美ら海に生きる" ]; then
		if [ $time = 9  ] || [ $time = 12 ] || [ $time = 16 ]; then
			file_number=17
		else
			file_number=16
		fi
		skip=1
	fi

	if [ $file_number = 9 ] && [ $Test = "沖縄黒潮の海" ]; then
		if [ $time = 10  ] || [ $time = 13 ] || [ $time = 17 ]; then
			file_number=19
		else
			file_number=18
		fi
		skip=1
	fi

	if [ $file_number = 9 ] && [ $Test = "沖縄サンゴ礁の海" ]; then
		if [ $time = 11  ] || [ $time = 14 ] || [ $time = 18 ]; then
			file_number=21
		else
			file_number=20
		fi
		skip=1
  fi

	if [ $file_number = 10 ] && [ $Test = "ホオジロザメの標本" ]; then
		file_number=24
		skip=1
	elif [ $file_number = 10 ] && [ $Test = "サメの肌の標本" ]; then
		file_number=25
		skip=1
	elif [ $file_number = 10 ] && [ $Test = "水槽" ]; then
		file_number=25
		skip=1
	fi

	if [ $file_number = 27 ] && [ $Test = "レストラン" ]; then
		file_number=28
		skip=1
	elif [ $file_number = 27 ] && [ $Test = "モニュメント" ]; then
		file_number=29
		skip=1
	elif [ $file_number = 27 ] && [ $Test = "水槽" ]; then
		file_number=30
		skip=1
	fi


　#bunki.txtのワードに従って分岐
	if [ $skip = 0 ]; then

		while IFS= read -r line; do
			# echo "$line"
			# echo "$count"
			if [ $line = $Test ]; then
				file_number=$count
			fi
			count=$((count+1))
			#時間帯処理もここでいいのでは
		done < dialogue/aquarium/bunki.txt

	fi
	if [ $skip = 0 ]; then

		if [ $file_number -gt 36 ]; then
			file_number=7
			skip=1
		fi
	fi

	#入力された音声によって分岐

	#badword.txtから一行ずつwhileで読み込み、一致するものがあれば評価-1
	while IFS= read -r line; do
		# echo "$line"
		if [ $line = $Test ]; then
			favorability=$((favorability-1))
		fi
	done < dialogue/aquarium/badword.txt

	#goodword.txtから一行ずつwhileで読み込み、一致するものがあれば評価+1
	while IFS= read -r line; do
		# echo "$line"
		if [ $line = $Test ]; then
			favorability=$((favorability+1))
		fi
	done < dialogue/aquarium/goodword.txt

	# #endword判定
	if [ $Test = "帰る" ]; then
		endflag=5
		echo "$endflag" > response.txt
		sleep 1
		exit
	fi

	while IFS= read -r line; do
		# echo "$line"
		if [ $line = "1" ]; then
			badconditions=1
		fi
	done < badconditions.txt

	echo "二郎：$badconditions"

	#告白によるEnding分岐
	if [ $Test = "告白" ]; then
		if [ $badconditions == 1 ]; then
			endflag=7
		elif [ $favorability -gt 5 ]; then
			endflag=3
		elif [ $favorability -gt 3  ]; then
			endflag=2
		elif [ $favorability -gt 1  ]; then
		  endflag=1
		elif [ $favorability -gt 0  ]; then
			endflag=4
		elif [ $favorability -gt -2  ]; then
			endflag=5
		else
			endflag=6
		fi
		echo "$endflag" > response.txt
		exit;
		sleep 1
	fi

	#time進行条件はdialogue7を見たら
	if [ $file_number = 7 ]; then
		time=$((time+1))
	fi



	pre_favorability=favorability

	skip=0





done
# ここは実行されないはず
rmdir $tmpdirname
