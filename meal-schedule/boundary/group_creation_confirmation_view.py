from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# ==========================================
# テスト用のダミー（本来は既存のControl/Entityを使用）
# ==========================================
class DummyUser:
    def __init__(self, account_id):
        self.account_id = 123  # ダミーのアカウントID

class DummyGroup:
    def __init__(self, group_id, group_name):
        self.group_id = group_id
        self.group_name = group_name

class DummyAccountManager:
    def get_current_user(self):
        # テスト用（Noneにするとユーザー情報取得エラーのテストができます）
        return DummyUser(account_id=123)

class DummyGroupManager:
    def create_group(self, account_id: int, group_name: str):
        # バリデーションテスト用（空文字や特定の名前でエラーを起こしたい場合）
        if group_name == "エラーテスト":
            raise ValueError("このグループ名はすでに使用されています")
        
        # 正常系：ダミーのグループIDを生成してGroupエンティティ風オブジェクトを返す
        return DummyGroup(group_id="G_9999", group_name=group_name)

# マネージャーのインスタンス化
account_manager = DummyAccountManager()
group_manager = DummyGroupManager()


# ==========================================
# 境界層（HTMLテンプレート定義）
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>グループ作成確認</title>
    <style>
        body { font-family: 'Yu Gothic', sans-serif; text-align: center; padding: 20px; background-color: #f0f2f5; color: #333; }
        .container { background: white; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h3 { font-size: 16px; color: #666; margin-bottom: 10px; }
        .group-name-display { font-size: 22px; font-weight: bold; color: #007bff; background-color: #e7f1ff; padding: 15px; border-radius: 5px; margin: 20px 0; border: 1px solid #b6d4fe; }
        .error-msg { color: #f44336; font-weight: bold; font-size: 14px; margin-bottom: 15px; text-align: left; }
        .btn-group { display: flex; justify-content: space-around; margin-top: 25px; }
        .btn { width: 45%; padding: 12px; border: none; border-radius: 5px; font-size: 16px; font-weight: bold; cursor: pointer; text-decoration: none; color: white; }
        .btn-submit { background-color: #007bff; }
        .btn-submit:hover { background-color: #0056b3; }
        .btn-back { background-color: #6c757d; line-height: 24px; }
        .btn-back:hover { background-color: #545b62; }
    </style>
</head>
<body>
    <div class="container">
        <h3>以下の内容でグループを作成しますか？</h3>
        
        <div class="group-name-display">
            グループ名：{{ group_name }}
        </div>
        
        {% if error_msg %}
            <div class="error-msg">⚠️ {{ error_msg }}</div>
        {% endif %}
        
        <form action="/group-creation-confirmation" method="POST">
            <input type="hidden" name="group_name" value="{{ group_name }}">
            
            <div class="btn-group">
                <input type="submit" class="btn btn-submit" value="登録する">
                <a href="/group-creation-placeholder" class="btn btn-back">戻る</a>
            </div>
        </form>
    </div>
</body>
</html>
"""


# ==========================================
# ルーティング（確認と登録処理）
# ==========================================
@app.route('/group-creation-confirmation', methods=['GET', 'POST'])
def group_creation_confirmation_view():
    # 前の画面（group_creation_view）から引き継いだ想定のデータ（テスト用デフォルト値）
    group_name = request.args.get('group_name', request.form.get('group_name', '大坪家・三根家'))
    error_msg = None

    # --- 「登録する」ボタンが押されたときの処理 (Tkinterの register_group に対応) ---
    if request.method == 'POST':
        user = account_manager.get_current_user()

        # 1. ユーザー情報取得チェック
        if user is None:
            error_msg = "ユーザー情報が取得できません"
            return render_template_string(HTML_TEMPLATE, group_name=group_name, error_msg=error_msg)

        try:
            # 2. グループ作成処理の実行
            group = group_manager.create_group(user.account_id, group_name)
            
            # 登録成功時は生成されたgroup_idとgroup_nameを完了画面に渡して遷移
            return redirect(url_for('success_page', group_id=group.group_id, group_name=group.group_name))

        # 3. マネージャー層からのValueErrorをキャッチして画面に表示
        except ValueError as e:
            error_msg = str(e)
            return render_template_string(HTML_TEMPLATE, group_name=group_name, error_msg=error_msg)

    # --- 画面を初めて開いたときの処理 (Tkinterの display に対応) ---
    return render_template_string(HTML_TEMPLATE, group_name=group_name, error_msg=error_msg)


@app.route('/success')
def success_page():
    group_id = request.args.get('group_id', '')
    group_name = request.args.get('group_name', '')
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif; line-height: 1.8;">
        <h1>🎉 登録完了</h1>
        <p style="font-size: 18px;">グループを作成しました。</p>
        <div style="background-color: #f8f9fa; display: inline-block; padding: 20px; border-radius: 8px; border: 1px solid #ddd; text-align: left; margin: 15px 0;">
            <strong>🆔 グループID：</strong> {group_id} <br>
            <strong>📁 グループ名：</strong> {group_name}
        </div>
        <br>
        <a href="/group-creation-confirmation" style="font-size: 16px; color: #007bff;">戻る</a>
    </div>
    """

@app.route('/group-creation-placeholder')
def group_creation_placeholder():
    return "<h3>（ここは group_creation_view 画面のダミーです）</h3><a href='/group-creation-confirmation'>作成確認画面へ</a>"


# ==========================================
# アプリケーションの起動
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)