
from flask import Flask, request, jsonify, render_template_string
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Atlas</title>
<style>
body {
background:#0b0b0b;
color:white;
font-family:Arial;
padding:40px;
max-width:900px;
margin:auto;
}
textarea {
width:100%;
height:120px;
background:#111827;
color:white;
border-radius:10px;
padding:15px;
border:1px solid #333;
}
button {
margin-top:15px;
padding:12px 18px;
border:none;
border-radius:8px;
font-weight:bold;
cursor:pointer;
}
.output {
margin-top:20px;
background:#111827;
padding:20px;
border-radius:10px;
white-space:pre-wrap;
}
</style>
</head>
<body>
<h1>Atlas</h1>
<p>AI-native Mathematical Discovery System</p>

<textarea id="q"></textarea><br>
<button onclick="ask()">Analyze</button>

<div class="output" id="out">
Try:
integrate x^2
derive sin(x)*x^2
solve x^2 - 5*x + 6
factor x^2 - 9
</div>

<script>
async function ask() {
 const q = document.getElementById("q").value;

 const res = await fetch("/ask", {
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({question:q})
 });

 const data = await res.json();
 document.getElementById("out").innerText = data.answer;
}
</script>
</body>
</html>
"""

THEOREMS = {
"pythagorean theorem":"a^2 + b^2 = c^2",
"bayes theorem":"P(A|B)=P(B|A)P(A)/P(B)",
"euler formula":"e^(ix)=cos(x)+i*sin(x)"
}

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/ask", methods=["POST"])
def ask():
    q = request.json.get("question","").lower().strip()
    x = sp.symbols("x")

    try:
        if q.startswith("integrate "):
            expr = parse_expr(q.replace("integrate ",""))
            return jsonify({"answer":str(sp.integrate(expr, x))})

        elif q.startswith("derive "):
            expr = parse_expr(q.replace("derive ",""))
            return jsonify({"answer":str(sp.diff(expr, x))})

        elif q.startswith("solve "):
            expr = parse_expr(q.replace("solve ",""))
            return jsonify({"answer":str(sp.solve(expr, x))})

        elif q.startswith("expand "):
            expr = parse_expr(q.replace("expand ",""))
            return jsonify({"answer":str(sp.expand(expr))})

        elif q.startswith("factor "):
            expr = parse_expr(q.replace("factor ",""))
            return jsonify({"answer":str(sp.factor(expr))})

        elif q.startswith("theorem "):
            t = q.replace("theorem ","")
            return jsonify({"answer":THEOREMS.get(t, "Unknown theorem")})

        return jsonify({
            "answer":"Unknown query. Use integrate / derive / solve / factor / theorem"
        })

    except Exception as e:
        return jsonify({"answer":f"Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
