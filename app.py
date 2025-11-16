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

QUESTIONS = [{'question': 'Selecione as alternativas verdadeiras referentes ao momento de deliberação.', 'choices': ['O chair é obrigado a conduzir a deliberação em ordem cronológica, sempre iniciando da comparativa, 1G frente à 1O.', 'Em casos de Split onde o chair está na minoria, um dos wings deve ser responsável pela call oral.', 'Durante a deliberação, o chair sempre deve revelar sua call por último.', 'As normas de decoro de uma deliberação incluem escutar o contributo de seus wings e trainees até eles sentirem que contribuíram de maneira suficiente.', 'Os juízes têm o dever de avaliar quais equipes foram mais persuasivas na defesa dos argumentos que o seu lado do debate precisa provar.'], 'answer': ['Em casos de Split onde o chair está na minoria, um dos wings deve ser responsável pela call oral.', 'Durante a deliberação, o chair sempre deve revelar sua call por último.', 'Os juízes têm o dever de avaliar quais equipes foram mais persuasivas na defesa dos argumentos que o seu lado do debate precisa provar.']}, {'question': 'Selecione as alternativas verdadeiras referentes a comparativas entre duplas.', 'choices': ['Se 2O não tiver trazido respostas diretas ao caso de 1G, 1G deve vencer na comparativa tendo em vista que seu caso não foi respondido.', 'Caso 1G construa uma definição desconectada da realidade, ainda assim 2G não pode trazer uma definição alternativa que contradiz o material trazido pela primeira bancada, sob pena de ser considerado esfaqueamento.', 'O adjunto de Oposição sempre carrega um ônus responsivo maior em relação ao adjunto de Governo do que o próprio adjunto de Governo tem em responder à 1O. ', 'Caso 1G tenha trazido uma métrica que não foi respondida ou trabalhada pelas demais duplas no debate, 1G deve ficar em quarto lugar por não ter sido considerado relevante o suficiente. ', 'Uma extensão que segue a mesma lógica argumentativa da sua casa alta, mas aprofunda os argumentos de modo estratégico, não é derivativa, e os argumentos da bancada alta passam a ser creditados exclusivamente à bancada baixa.', 'Embora recomendado, não é um fardo específico da função de um adjunto fazer comparativas.'], 'answer': ['O adjunto de Oposição sempre carrega um ônus responsivo maior em relação ao adjunto de Governo do que o próprio adjunto de Governo tem em responder à 1O. ', 'Embora recomendado, não é um fardo específico da função de um adjunto fazer comparativas.']}, {'question': 'Selecione as alternativas verdadeiras referentes a tipos de moção.', 'choices': ['Moções “EC lamenta X” sempre exigem uma análise retrospectiva de como seria o mundo se determinado fenômeno não tivesse ocorrido.', 'Na moção “EC prefere um mundo em que a proximidade religiosa seja dominante, em detrimento de um mundo em que o distanciamento religioso seja dominante”, não é necessário que nenhuma das bancadas defenda o status quo.', 'Na moção “ECAQ os o governo dos EUA deveria intervir na Tailândia”, 1G pode estabelecer um modelo de como exatamente a intervenção será realizada, desde que limitado àquelas medidas que o agente tem poder de realizar.”.', 'Moções “EC apoia X” são analiticamente equivalentes à moções como “EC acredita que X faz mais bem do que mal.” ', 'Em moções de “EC prefere um mundo” argumentos sobre transições entre o status quo e o mundo alternativo são permitidos.', 'Em moções de "EC, enquanto A, faria X", deve ser avaliado o que um agente deveria fazer e não somente o que ele provavelmente faria.', 'Em moções de agente, quando as crenças existentes de um agente são desafiadas, os juízes devem considerar se o agente, após reflexão racional, continuaria a manter essas crenças diante dos argumentos apresentados pelas duplas.', 'Na moção "EC implementaria um sistema nacional de avaliação seriada, nos moldes do PAS, em substituição ao ENEM", a LO pode propor reformas estruturais no ENEM e está seria uma contraproposta válida dentro do debate porque é mutuamente exclusiva.'], 'answer': ['Moções “EC lamenta X” sempre exigem uma análise retrospectiva de como seria o mundo se determinado fenômeno não tivesse ocorrido.', 'Na moção “EC prefere um mundo em que a proximidade religiosa seja dominante, em detrimento de um mundo em que o distanciamento religioso seja dominante”, não é necessário que nenhuma das bancadas defenda o status quo.', 'Na moção “ECAQ os o governo dos EUA deveria intervir na Tailândia”, 1G pode estabelecer um modelo de como exatamente a intervenção será realizada, desde que limitado àquelas medidas que o agente tem poder de realizar.”.', 'Moções “EC apoia X” são analiticamente equivalentes à moções como “EC acredita que X faz mais bem do que mal.” ', 'Em moções de "EC, enquanto A, faria X", deve ser avaliado o que um agente deveria fazer e não somente o que ele provavelmente faria.', 'Em moções de agente, quando as crenças existentes de um agente são desafiadas, os juízes devem considerar se o agente, após reflexão racional, continuaria a manter essas crenças diante dos argumentos apresentados pelas duplas.', 'Na moção "EC implementaria um sistema nacional de avaliação seriada, nos moldes do PAS, em substituição ao ENEM", a LO pode propor reformas estruturais no ENEM e está seria uma contraproposta válida dentro do debate porque é mutuamente exclusiva.']}, {'question': 'Selecione as alternativas verdadeiras referentes às regras gerais do modelo Parlamento Britânico.', 'choices': ['Para vencer um debate, é necessário fornecer respostas para todos os argumentos das demais duplas.', 'Os juízes devem levar em consideração o fato de acreditarem que ocorreu uma violação da equidade ao avaliar quem venceu um debate ou quantos speaker points atribuir.', 'Materiais trazidos pelo whip que não alteram significativamente a direção do caso da extensão, como sopesamentos e caracterizações, podem ser creditados como uma forma de extensão à sua casa alta.', 'Se o primeiro ministro faz uma definição que o líder de oposição contesta como restritiva, o juíz deve adotar a justificativa de 1O meramente pelo mérito dela ser mais abrangente.', 'Se 2O contesta uma definição injusta que foi feita pela pelo PM e aceita no debate, o juiz deve considerar a contestação de 2O.', 'Na moção “Esta Casa se opõe à candidatura de Jones Emanuel como principal nome da esquerda em 2026”, se  1G argumentar que a candidatura de Jones Emanuel é ruim porque aumenta as chances de a esquerda perder a eleição, e 1O conceder que Jones Emanuel provavelmente perderia, mas que isso é bom porque a esquerda é ruim, então a 2O não pode contestar que Jones Emanuel provavelmente perderá nem que a vitória de um candidato de esquerda é algo ruim.”', 'As opiniões pré-concebidas pelo Eleitor Bem Informado e Inteligente são, a grosso modo, as opiniões médias da população geral.', 'Caso 1O não tenha trazido uma contraproposta em uma moção de política, 2O deve suprir esse ônus argumentativo de oposições, apresentando uma contraproposta na extensão.', 'Realizar um discurso ofensivo geralmente não é persuasivo para o eleitor bem informado e inteligente comum.'], 'answer': ['Materiais trazidos pelo whip que não alteram significativamente a direção do caso da extensão, como sopesamentos e caracterizações, podem ser creditados como uma forma de extensão à sua casa alta.', 'Se 2O contesta uma definição injusta que foi feita pela pelo PM e aceita no debate, o juiz deve considerar a contestação de 2O.', 'Na moção “Esta Casa se opõe à candidatura de Jones Emanuel como principal nome da esquerda em 2026”, se  1G argumentar que a candidatura de Jones Emanuel é ruim porque aumenta as chances de a esquerda perder a eleição, e 1O conceder que Jones Emanuel provavelmente perderia, mas que isso é bom porque a esquerda é ruim, então a 2O não pode contestar que Jones Emanuel provavelmente perderá nem que a vitória de um candidato de esquerda é algo ruim.”', 'Realizar um discurso ofensivo geralmente não é persuasivo para o eleitor bem informado e inteligente comum.']}, {'question': 'Em relação a atribuição de Speaker Points, selecione as alternativas verdadeiras.', 'choices': ['Cada orador deve aceitar pelo menos um POI ou será penalizado por ausência de engajamento.', 'Os juízes devem reduzir os speaker points dos debatedores que não aceitaram POIs para refletir o seu baixo engajamento.', 'É improvável que uma sala com dificuldade baixa contenha discursos com notas superiores a 75.', 'Se o POI foi interrompido injustificadamente antes que o ponto pudesse ser claramente apresentado, os juízes devem tratar a situação como se o debatedor não tivesse aceitado um POI e aplicar a penalidade adequada.', 'Em um debate onde o líder de oposição faz um discurso integralmente argumentativo e o adjunto faz um discurso integralmente comparativo, o LO deve receber mais speaker points que o adjunto.'], 'answer': ['Cada orador deve aceitar pelo menos um POI ou será penalizado por ausência de engajamento.', 'Os juízes devem reduzir os speaker points dos debatedores que não aceitaram POIs para refletir o seu baixo engajamento.', 'Se o POI foi interrompido injustificadamente antes que o ponto pudesse ser claramente apresentado, os juízes devem tratar a situação como se o debatedor não tivesse aceitado um POI e aplicar a penalidade adequada.']}]



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
        return "Test successfully submited."

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







