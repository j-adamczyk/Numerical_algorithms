from file_manager import load_article_text
from flask import Flask, render_template, request, redirect
from search_engine import query_search


app = Flask(__name__)

query = ""
search_results = []


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    query = request.form["query"]
    global search_results
    try:
        search_results = query_search(query)
    except:
        search_results = []
    return redirect("/search_results")


@app.route("/search_results")
def search_results():
    titles = [result[0] for result in search_results]
    return render_template("after_search.html", search_results=titles)


@app.route("/article", methods=["GET", "POST"])
def article():
    title = request.args.to_dict()["title"]
    article_text = load_article_text(title)
    article_text = article_text.replace("\n", "<br>")
    return render_template("article.html", title=title, text=article_text)


if __name__ == "__main__":
    app.run()
