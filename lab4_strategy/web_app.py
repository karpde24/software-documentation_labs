from flask import Flask, render_template_string, request

from main import run_strategy


app = Flask(__name__)


HTML_PAGE = """
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Lab 4 Strategy Pattern</title>
</head>
<body>
    <h1>Lab 4: GoF Strategy Pattern</h1>

    <p>
        Цей веб-інтерфейс дозволяє запускати різні стратегії виводу даних
        без зміни основного коду програми.
    </p>

    <form method="post">
        <label>Оберіть стратегію:</label>
        <select name="strategy">
            <option value="console">Console</option>
            <option value="file">File</option>
            <option value="firebase">Firebase</option>
            <option value="redis">Redis</option>
            <option value="kafka">Kafka</option>
        </select>

        <button type="submit">Запустити</button>
    </form>

    {% if result %}
        <hr>
        <h2>Результат виконання</h2>
        <p><strong>Стратегія:</strong> {{ result.strategy }}</p>
        <p><strong>Кількість записів:</strong> {{ result.records_count }}</p>
        <p><strong>Повідомлення:</strong> {{ result.result }}</p>
    {% endif %}

    {% if error %}
        <hr>
        <h2>Помилка</h2>
        <p style="color:red;">{{ error }}</p>
    {% endif %}

    <script type="module">
      import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js";
      import { getAnalytics, logEvent } from "https://www.gstatic.com/firebasejs/10.12.5/firebase-analytics.js";

      const firebaseConfig = {
        apiKey: "AIzaSyDwh-ypUg7MsksVFBtUTgbX3MSRkOAJocA",
        authDomain: "lab4-strategy-15df3.firebaseapp.com",
        projectId: "lab4-strategy-15df3",
        storageBucket: "lab4-strategy-15df3.firebasestorage.app",
        messagingSenderId: "221457679547",
        appId: "1:221457679547:web:7f9e712ccee47f95e5d59e",
        measurementId: "G-FMDM31DZRF"
      };

      const app = initializeApp(firebaseConfig);
      const analytics = getAnalytics(app);

      const form = document.querySelector("form");

      if (form) {
        form.addEventListener("submit", function () {
          const strategy = document.querySelector("select[name='strategy']").value;

          logEvent(analytics, "strategy_selected", {
            strategy_name: strategy
          });
        });
      }
    </script>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        strategy = request.form.get("strategy")

        try:
            result = run_strategy(strategy)
        except Exception as exception:
            error = str(exception)

    return render_template_string(
        HTML_PAGE,
        result=result,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True, port=5001)