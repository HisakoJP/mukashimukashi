# -*- coding: utf-8 -*-
import boto3
import requests
import os

# Pollyクライアント作成
polly = boto3.client('polly', region_name='ap-northeast-1')

# ファイルリスト取得
FILELIST_URL = "https://raw.githubusercontent.com/HisakoJP/mukashimukashi/main/filelist.txt"

print("ファイルリストを取得中...")
response = requests.get(FILELIST_URL)
files = [line.strip() for line in response.text.split('\n') if line.strip()]
print(f"✓ {len(files)}個のタイトルを取得しました\n")

# 出力ディレクトリ作成
os.makedirs('titles', exist_ok=True)

# 一括生成（m4aに変更）
for i, filename in enumerate(files):
    title = filename.replace('.m4a', '')
    output_path = f'titles/{title}.m4a'  # ← .mp3 から .m4a に変更
    
    # すでに存在する場合はスキップ
    if os.path.exists(output_path):
        print(f"[{i+1}/{len(files)}] スキップ: {title}")
        continue
    
    print(f"[{i+1}/{len(files)}] 生成中: {title}")
    
    try:
        # Pollyで音声生成（mp4に変更）
        response = polly.synthesize_speech(
            Text=title,
            OutputFormat='mp4',  # ← mp3 から mp4 (=m4a) に変更
            VoiceId='Takumi',
            Engine='neural'
        )
        
        # ファイルに保存
        with open(output_path, 'wb') as f:
            f.write(response['AudioStream'].read())
            
    except Exception as e:
        print(f"  ⚠️ エラー: {e}")

print("\n完了！titlesフォルダをRaspberry Piに転送してください")