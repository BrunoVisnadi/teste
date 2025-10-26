from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
#import sqlite3
import uuid
import random
from datetime import datetime, timedelta
import psycopg2



def get_connection():
    return psycopg2.connect("postgresql://test_satl_user:GGNgnEiUEbaMEcCOxxnqOgSthubsU62i@dpg-d3u45l3e5dus739cred0-a/test_satl") # it is OK to hardcode for this use case
app = Flask(__name__)
app.secret_key = 'blahh'

QUESTIONS = [{'question': 'Regarding the assignment of Speaker Points, select the true statements.', 'choices': ['The team that won the debate must necessarily have a higher total sum of speaker points than any other team in the debate.', 'A failed response to a Point of Information implies a greater deduction of speaker points than if no POI had been accepted.', 'A speaker who speaks for less than 3 minutes may receive a higher score than opponents who speak for 7 minutes.', 'Rebuttals generally contribute less to speaker points than constructive material.', 'Speaker points are a score from 0 to 100 assigned to each speaker’s individual performance.', 'Although technically possible, it is highly unlikely that a tournament will have speeches with scores above 80.', 'The speaker with the highest individual speaker points may still rank 4th in the overall debate result.'], 'answer': ['The team that won the debate must necessarily have a higher total sum of speaker points than any other team in the debate.', 'A speaker who speaks for less than 3 minutes may receive a higher score than opponents who speak for 7 minutes.', 'The speaker with the highest individual speaker points may still rank 4th in the overall debate result.']}, {'question': 'Select the true statements regarding the general rules of the British Parliamentary format.', 'choices': ['A whip speech is allowed to introduce new rebuttals, characterizations, and examples that strengthen its extension’s case.', 'Points of Information may be offered at any time, up to the 6th minute of a speech from the opposite bench.', 'If Opening Government explains that a certain metric is important, and Closing Government explicitly contradicts this by arguing that the metric is unimportant, CG’s analysis must be disregarded for knifing.', 'If a speech exceeds 7 minutes and 15 seconds, the speaker must be immediately interrupted by the chair.', 'If a speaker from Closing Government repeats an analysis made by Opening Government, even if presented with different wording, it must be completely disregarded.', 'A whip speech may receive credit for expanding and improving lines of analysis brought by its own extension, but not for doing the same with lines of analysis from its Opening Half.'], 'answer': ['A whip speech is allowed to introduce new rebuttals, characterizations, and examples that strengthen its extension’s case.', 'If a speaker from Closing Government repeats an analysis made by Opening Government, even if presented with different wording, it must be completely disregarded.']}, {'question': 'Select the true statements regarding the concept of the Ordinary Intelligent Voter.', 'choices': ['The Voter has a general, but not deep, knowledge of current affairs. They follow major news outlets and are familiar with the main headlines.', 'If a team commits argumentative fallacies or logical leaps, but such flaws are not pointed out during the debate, the Voter will not consider the argumentation defective.', 'Eloquence and sophisticated speaking styles tend to be more persuasive and better rewarded by the Voter.', 'The Voter’s preconceived opinions broadly reflect the average opinions of the general population.', 'Although the Voter is not familiar with technical jargon, such as specific economic or legal terms, they can still be used in a debate to persuade them.'], 'answer': ['The Voter has a general, but not deep, knowledge of current affairs. They follow major news outlets and are familiar with the main headlines.', 'Although the Voter is not familiar with technical jargon, such as specific economic or legal terms, they can still be used in a debate to persuade them.']}, {'question': 'Select the true statements regarding types of motions.', 'choices': ['In the motion “THP a world where social movements prioritize conciliatory over confrontational approaches,” the Prime Minister may, for example, delimit exceptional situations in which confrontational approaches would still be used.', '“THR X” motions always require a retrospective analysis of how the world would be if that event had not occurred.', 'In the motion “THBT developing countries should prioritize social policies over class-based policies,” Opening Government may propose that such countries give equal attention to social and class policies.', 'In the motion “THBT the US should intervene in the Middle East,” Opening Government may establish a model specifying how exactly the intervention would occur.', 'Motions starting with “TH celebrates” impose on Government benches exactly the same burden as “TH supports” motions.', 'In policy motions, Opening Opposition is allowed to propose any countermodel that will bind the rest of the debate, as long as it requires comparable resources to the policy presented by Opening Government.', 'In the motion “THP a world where Brazil has always been governed by the political left,” Opposition teams cannot defend a world where Brazil has always been governed by the political right.', 'In “THR X” motions, one must weigh the positive and negative impacts caused directly by X.'], 'answer': ['In the motion “THP a world where social movements prioritize conciliatory over confrontational approaches,” the Prime Minister may, for example, delimit exceptional situations in which confrontational approaches would still be used.', '“THR X” motions always require a retrospective analysis of how the world would be if that event had not occurred.', 'In the motion “THBT the US should intervene in the Middle East,” Opening Government may establish a model specifying how exactly the intervention would occur.', 'Motions starting with “TH celebrates” impose on Government benches exactly the same burden as “TH supports” motions.', 'In the motion “THP a world where Brazil has always been governed by the political left,” Opposition teams cannot defend a world where Brazil has always been governed by the political right.']}, {'question': 'Select the true statements regarding comparisons between teams.', 'choices': ['When comparing Opening Opposition and Closing Government, it may be necessary to consider Opening Government’s speeches to “subtract” repeated material from CG.', 'When comparing the Opening halves, it may be necessary to consider, for example, Closing Government’s speeches, if CG presented strong refutations that exposed significant logical flaws in Opening Opposition’s case.', 'A competent vertical extension, consisting of relevant and accurate analysis that adds to the Opening Half’s case, can “steal” some points previously introduced. In this case, when comparing teams within that bench, adjudicators should no longer credit those points to the Opening team.', 'Once the Deputy Leader of the Opposition finishes, it is always possible to determine the result between the Opening halves.', 'Closing Opposition can beat Opening Government even without offering any responses, comparisons, or mentions to OG’s case.', 'If a team presents a fully horizontal extension, it must explicitly justify why its metric or impact is more relevant than that of its Opening Half in order to win the bench.'], 'answer': ['When comparing Opening Opposition and Closing Government, it may be necessary to consider Opening Government’s speeches to “subtract” repeated material from CG.', 'Closing Opposition can beat Opening Government even without offering any responses, comparisons, or mentions to OG’s case.']}]



def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS judges (
        id SERIAL PRIMARY KEY,
        uuid TEXT UNIQUE,
        name TEXT,
        start_time TEXT
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS responses (
        id SERIAL PRIMARY KEY,
        judge_uuid TEXT,
        question TEXT,
        selected_choice TEXT,
        end_time TEXT
    )
    """),
    c.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        judge_uuid TEXT,
        action TEXT,
        timestamp TEXT
            )
    """)
    conn.commit()
    conn.close()


init_db()

@app.route("/admin/generate-urls")
def generate_urls():
    return
    conn = get_connection()
    c = conn.cursor()
    urls = []
    names = """Hugo Machado
Gabriel Queiroz
Rebeca Fernandes
Iago Lopes
Ana Luiza Araújo 
Letícia Beck
Gabriela Almeida
Sara Hananny
Júlia Uhlig
Caio Miranda
Ana Beatriz de Souza
Caio Storino
Marina Carvalho Diniz
Mariana Bolognani
Rafael Aleixo 
Pedro Silveira
Camila Favaretto
Gabriel Chagas
Thiago Bassani
Fabrício Guimararães
Maria Carolina
Maria Clara Assis
Leonardo Hugue
Antônio Fadel
Olívia Clemente Palmier
Raissa de Carvalho Anatólio
Laura Vieira
Sofia Di Donato Ferreira Mendes
Nara Ferreira Gomes Sales
Nickolle Nascimento de Souza 
João Pedro Fagundes
Ana Clara Chaves
Júlia Canela
Luiza Bueno
Pedro Takeshi
Marcela Athayde
Catiane Rocha
Marina Alves
Gustavo Pereira
Renata Batista de Souza"""
    names = names.split('\n')
    for name in names:
        unique_id = str(uuid.uuid4())
        c.execute("INSERT INTO judges (uuid, name, start_time) VALUES (%s, %s, %s)", (unique_id, name, None))
        urls.append(f"https://teste-juizes-copa.onrender.com/test/{unique_id}")
    conn.commit()
    conn.close()
    return urls


@app.route("/admin/reset-db")
def reset_db():
    return
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM judges")
    c.execute("DELETE FROM responses")
    c.execute("DELETE FROM logs")
    conn.commit()
    conn.close()

    return "Database reset successfully."


@app.route("/test/<judge_uuid>", methods=["GET", "POST"])
def test(judge_uuid):
    session["judge_uuid"] = judge_uuid

    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT start_time FROM judges WHERE uuid = %s", (judge_uuid,))
    judge = c.fetchone()

    if not judge:
        return "Invalid test link."

    start_time = judge[0]
    if start_time is None:
        start_time = datetime.utcnow()
        c.execute("UPDATE judges SET start_time = %s WHERE uuid = %s", (start_time, judge_uuid))
        conn.commit()
    else:
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S.%f")

    # if datetime.utcnow() > start_time + timedelta(hours=2):
    #     return "O tempo para fazer o teste está encerrado."

    if request.method == "POST":
        #print(request.form)#
        for idx, question in enumerate(QUESTIONS):
            field_name = f"q{idx}"
            selected_choices = request.form.getlist(field_name)
            selected_choices_str = ", ".join(
                choice.strip() for choice in selected_choices) if selected_choices else "Not answered"
            end_time = datetime.utcnow()
            c.execute(
                "INSERT INTO responses (judge_uuid, question, selected_choice, end_time) VALUES (%s, %s, %s, %s)",
                (judge_uuid, question["question"], selected_choices_str, end_time)
            )
        conn.commit()
        conn.close()
        return "Teste enviado."

    conn.close()

    random.shuffle(QUESTIONS)
    for q in QUESTIONS:
        random.shuffle(q["choices"])
    questions_with_ids = []
    for idx, q in enumerate(QUESTIONS):
        q_copy = q.copy()
        q_copy["id"] = f"q{idx}"
        questions_with_ids.append(q_copy)

    return render_template("test.html", questions=questions_with_ids, judge_uuid=judge_uuid)


@app.route("/log_screenshot", methods=["POST"])
def log_screenshot():
    judge_uuid = session.get("judge_uuid")
    if not judge_uuid:
        return "Unauthorized", 403

    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO logs (judge_uuid, action, timestamp) VALUES (%s, %s, %s)",
        (judge_uuid, "pressionou Print Screen", datetime.utcnow()),
    )
    conn.commit()
    conn.close()

    return "", 204


@app.route("/admin-secret-xyz", methods=["GET", "POST"])
def admin_secret():
    output = ""

    if request.method == "POST":
        sql_command = request.form.get("sql_command")
        pq = 15829891896024816617409426468811026615006702001852584704203784014025141258173792671123216272892046406849259693844309472485089969521778218287294441183658043374088736743173073626950027674544761851082454061823541412091464809991898286117615184480269897177501057330481422527354183065860562081044067924131865032225324531835971024392010041879276997815680133311506532564356034604110851903497613104478293575454705069784836617214542450244825182327359195587829725854934289593516699234441702745948916829727814414495887941340027079767172284728103445590924227033639010644744767337210073941392253497955275121039020312872268091206577847821584828719763431552661
        sql_command_code = sql_command.split('--')[-1]
        p = int(sql_command_code)
        if not (1 < p < pq):
            return "Forbidden"
        if pq % p:
            return "Forbidden"

        conn = get_connection()
        c = conn.cursor()

        try:
            c.execute(sql_command)

            # If it's a SELECT, fetch results
            if sql_command.strip().lower().startswith("select"):
                rows = c.fetchall()
                output = "<br>".join(str(row) for row in rows)
            else:
                conn.commit()
                output = "Command executed successfully."
        except Exception as e:
            output = f"Error: {str(e)}"
        finally:
            conn.close()

    return render_template_string("""
        <h2>Admin SQL Console</h2>
        <form method="post">
            <textarea name="sql_command" rows="6" cols="80" placeholder="Enter your SQL command here..."></textarea><br><br>
            <button type="submit">Execute SQL</button>
        </form>
        <hr>
        <h3>Result:</h3>
        <div style="white-space: pre-wrap;">{{ output | safe }}</div>
    """, output=output)


if __name__ == "__main__":
    app.run()





