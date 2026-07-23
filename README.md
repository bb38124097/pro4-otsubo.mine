# 家族向け食事スケジュール管理アプリケーション

家族間での「今日のご飯いる？」「何時に帰ってくる？」といった連絡や確認の手間を減らし、食事予定や帰宅時間、メッセージを円滑に共有するためのアプリケーションです。

## 1. ソースコードの構成（フォルダ構成など）

本システムは、演習の設計方針である **Entity-Control-Boundary（ECB）の三層アーキテクチャ** に基づき、ディレクトリごとに役割を明確に分離して実装しています。

```text
meal-schedule/
├── boundary/             # 【Boundary層】画面表示・ユーザー入力を担うUI処理
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
├── control/              # 【Control層】ビジネスロジック・ユースケース制御
│   ├── account_manager.py
│   ├── group_manager.py
│   └── meal_schedule_manager.py
├── entity/               # 【Entity層】システムが扱うデータ構造（モデル）
│   ├── group_calendar.py
│   ├── group.py
│   ├── meal_schedule.py
│   ├── user_calendar.py
│   └── user.py
├── templates/            # HTMLテンプレートファイル（Web画面用）
├── static/               # CSS等の静的ファイル
├── app.py                # Webアプリケーション（Flask）メイン起動スクリプト
└── README.md             # 本ドキュメント