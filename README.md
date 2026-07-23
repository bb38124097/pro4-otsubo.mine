家族向け食事スケジュール管理アプリケーション

家族間での「今日のご飯いる？」「何時に帰ってくる？」といった連絡や確認の手間を減らし、食事予定や帰宅時間、メッセージを円滑に共有するためのアプリケーションです。

## 1. ソースコードの構成（フォルダ構成など）

本システムは、演習の設計方針である **Entity-Control-Boundary（ECB）の三層アーキテクチャ** に基づき、ディレクトリごとに役割を明確に分離して実装しています。

```text
meal-schedule/
├── boundary/            
│   ├── account_registration_view.py
│   ├── add_member_view.py
│   ├── date_detail_view.py
│   ├── delete_account_view.py
│   ├── group_creation_confirmation_view.py
│   ├── group_creation_view.py
│   ├── leave_group_view.py
│   ├── main_view.py
│   ├── meal_input_view.py
│   ├── message_input_view.py
│   └── return_time_input_view.py
├── control/              
│   ├── account_manager.py
│   ├── group_manager.py
│   └── meal_schedule_manager.py
├── entity/              
│   ├── group_calendar.py
│   ├── group.py
│   ├── meal_schedule.py
│   ├── user_calendar.py
│   └── user.py
├── static/               
│   └── style.css         
├── templates/            
│   ├── account.html
│   ├── add_member.html
│   ├── group_create.html
│   ├── index.html
│   ├── leave_group.html
│   ├── login.html
│   ├── main.html
│   ├── meal_detail.html
│   ├── meal.html
│   └── register.html
├── app.py                # Webアプリケーション（Flask）メイン起動スクリプト
├── meal_schedule.db      # SQLiteデータベースファイル
├── requirements.txt      # 依存パッケージリスト
├── README.md             # 本ドキュメント
└── video.mp4             # アプリ紹介・デモ動画

