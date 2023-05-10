import os
import azure.cognitiveservices.speech as speechsdk
import csv


SPEECH_KEY=""
SPEECH_REGION="eastus"



# 1.目錄底下要放total.csv
# 2.可以調整語速
# 3.可以定義動物使用的人聲
# 4.csv抓取的語言欄位可透過text_language調整，如zh-TW
# 執行後就會抓取檔名和台詞，生成xml檔案後，根據xml檔案生成wav檔案

# 目錄底下的csv名稱
csv_name = 'total.csv'

# 是否要順便產生wav
create_wav = 1

#英文語系說話速度
en_rate = 0.6
#中文語系說話速度
ch_rate = 1

# CSV要抓取的語言欄位
text_language = "zh-TW"

#修改動物使用的聲音，前面放對應的語言如中文或日文，後面主要是英文
voice = {'Alpaca':['zh-TW-HsiaoChenNeural','en-US-JennyNeural'],
         'Sheep_Baby':['zh-TW-HsiaoChenNeural','en-US-JennyNeural'],
         'Black_Boar':['zh-TW-YunJheNeural','en-US-RogerNeural'],
         }



# ________________________________________________________________________




# 把檔案名稱和zh-TW的台詞抓出來
def get_csv_list(csvfile,text_language):
    with open('total.csv', newline='',encoding='utf-8') as csvfile:
        rows = csv.reader(csvfile)
        filename_text_list = [] #放檔名和文字內容
        first = 0
        for  row in rows:
            

            if len(row) == 0:continue
            if row[0] == 'OutgoingLinks':break

            if row[0] == 'entrytag':
                first = 1
                zh_tw=row.index(text_language)
            
            if first:
                filename_text_list.append([row[0],row[zh_tw]])

    return filename_text_list

#產生xml檔案
def make_xml(filename_text_list,voice,en_rate,ch_rate,text_language):
    # 開啟 CSV 檔案
    output_filename = []
    for filename,text in filename_text_list:
        if text.strip() == "": continue
        speak_tag = f'<speak version="1.0" xmlns="https://www.w3.org/2001/10/synthesis" xml:lang="zh-TW">'
        voice_tag = ''
        voice_master=''
        prosody_tag = ''
        for name in voice.keys():
            if name in filename:
                voice_master = name
                break
        
        if voice_master == '' : continue

        en_ch_list = ch_en_check(text)
        for t in en_ch_list:
            rate = ch_rate
            voice_tag = voice[voice_master][0]
            if ord(t[0]) < 256:
                rate = en_rate
                voice_tag = voice[voice_master][1]
            prosody_tag += f'<voice name="{voice_tag}"> <prosody rate="{rate}">{t}</prosody></voice>\n'
        new_filename = f'{filename}_{text_language}.xml'
        with open(new_filename, 'w' , encoding='utf-8') as f:
            f.write(f'{speak_tag}\n{prosody_tag}\n</speak>\n')
        output_filename.append(f'{filename}_{text_language}')
    return output_filename
def ch_en_check(text):
    en = ''
    ch = ''
    en_ch_list = []
    # special_text =['!','?','"','！','？']
    for t in text:
        if ord(t) < 256 :
            en+=t
        elif en != '':
            en_ch_list.append(en)
            en = ''

        if not ord(t) < 256 :
            ch+=t
        elif ch != '':
            en_ch_list.append(ch)
            ch = ''
        
    if en != '':
        en_ch_list.append(en)
        en = ''
    if ch != '':
        en_ch_list.append(ch)
        ch = ''
    print(en_ch_list)
    return en_ch_list



def make_wav(file_name):
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    print(file_name + '.xml')
    ssml_string = open(file_name + '.xml', "r", encoding='utf-8').read()
    result = synthesizer.speak_ssml_async(ssml_string).get()

    stream = speechsdk.AudioDataStream(result)
    stream.save_to_wav_file(file_name + ".wav")


output_filename =  make_xml(get_csv_list(csv_name,text_language),voice,en_rate,ch_rate,text_language)

if create_wav :
    for file in output_filename:
        make_wav(file)

# 單一檔案輸出
# make_wav('Alpaca_2_2_zh-TW')