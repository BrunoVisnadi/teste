from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
#import sqlite3
import uuid
import random
from datetime import datetime, timedelta
import psycopg2



def get_connection():
    return psycopg2.connect("postgresql://db_user:5Uvb9zTvYJqk0rotHKMiOV0kEq7vvT16@dpg-d073hok9c44c739lgtjg-a/db_name_7q54") # it is OK to hardcode for this use case
app = Flask(__name__)
app.secret_key = 'blahh'

QUESTIONS = [
    {
        "question": "Em relação a atribuição de Speaker Points, selecione as alternativas verdadeiras.",
        "choices":
            [
                "O debatedor com a nota de speaker points mais alta pode, no resultado do debate, ficar em 4º lugar",
                "Um debatedor que discursar por menos de 3 minutos pode ter uma nota mais alta que seus adversários que discursarem por 7 minutos",
                "A dupla que venceu o debate, necessariamente, precisa ter a soma de speaker points maior do que a de qualquer outra dupla do debate",
                "Uma resposta falha a um Ponto de Informação implica em uma dedução maior aos speaker points do que se nenhum POI tivesse sido aceito",
                "Refutações, geralmente, contribuirão menos para os speaker points do que material construtivo",
                "Os speaker points são uma nota de 0 a 100 atribuída ao desempenho individual de cada debatedor",
                "Embora sejam notas tecnicamente possíveis, é altamente improvável que um campeonato contenha discursos com notas superiores a 80"
            ],
            "answer": [
                "O debatedor com a nota de speaker points mais alta pode, no resultado do debate, ficar em 4º lugar",
                "Um debatedor que discursar por menos de 3 minutos pode ter uma nota mais alta que seus adversários que discursarem por 7 minutos",
                "A dupla que venceu o debate, necessariamente, precisa ter a soma de speaker points maior do que a de qualquer outra dupla do debate",
            ]
    },
    {
        "question": "Selecione as alternativas verdadeiras referentes às regras gerais do modelo Parlamento Britânico.",
        "choices":
            [
                "Se um debatedor do segundo governo repetir uma análise feita pelo primeiro governo, ainda que a apresente com vocabulário diferente, ela deverá ser completamente desconsiderada",
                "Um discurso de whip está autorizado a trazer novas refutações, caracterizações e exemplos que fortaleçam o caso de sua extensão",
                "Um discurso de whip pode receber crédito por expandir e aprimorar linhas de análise trazidas por sua extensão, mas não por fazer o mesmo com linhas de análise trazidas por sua casa alta",
                "Se um discurso ultrapassar 7 minutos e 15 segundos, o debatedor deve ser imediatamente interrompido pelo presidente da mesa",
                "Pontos de Informação podem ser oferecidos em qualquer momento, até o 6º minuto de fala de um debatedor da bancada oposta",
                "Se o Primeiro Governo explica que determinada métrica é importante, e o segundo governo o contradiz explicitamente, argumentando que a dita métrica não é importante, a análise de 2G deve ser desconsiderada por esfaqueamento."
            ],
        "answer": [
            "Se um debatedor do segundo governo repetir uma análise feita pelo primeiro governo, ainda que a apresente com vocabulário diferente, ela deverá ser completamente desconsiderada",
            "Um discurso de whip está autorizado a trazer novas refutações, caracterizações e exemplos que fortaleçam o caso de sua extensão",
        ]
    },
    {
        "question": "Selecione as alternativas verdadeiras referentes ao conceito do Eleitor Bem Informado e Inteligente.",
        "choices":
            [
                "O Eleitor possui um conhecimento genérico, mas não profundo, sobre assuntos gerais e atualidades. Ele acompanha os principais portais de notícias e está familiarizado com as manchetes dos maiores jornais",
                "Apesar de o Eleitor não ter familiaridade com jargões técnicos, como termos econômicos e jurídicos específicos, é possível utilizá-los em um debate para persuadi-lo",
                'Se uma dupla cometer falácias argumentativas ou saltos lógicos, mas tais falhas não forem apontadas durante o debate, o Eleitor não irá considerar a argumentação como defeituosa',
                "As opiniões pré-concebidas pelo Eleitor são, a grosso modo, as opiniões médias da população geral",
                "Oratória e estilos mais sofisticados, tendencialmente, são mais persuasivos e bem creditados pelo Eleitor",
            ],
        "answer": [
            "O Eleitor possui um conhecimento genérico, mas não profundo, sobre assuntos gerais e atualidades. Ele acompanha os principais portais de notícias e está familiarizado com as manchetes dos maiores jornais",
            "Apesar de o Eleitor não ter familiaridade com jargões técnicos, como termos econômicos e jurídicos específicos, é possível utilizá-los em um debate de modo a persuadi-lo",
        ]
    },
    {
        "question": "Selecione as alternativas verdadeiras referentes a tipos de moção.",
        "choices":
            [
                'Moções “EC lamenta X” sempre exigem uma análise retrospectiva de como seria o mundo se determinado fato não tivesse ocorrido',
                'Na moção “EC prefere um mundo em que o Brasil sempre foi governado pela esquerda política”, as oposições não podem defender um mundo em que o Brasil sempre tenha sido governado pela direita política',
                'Moções que iniciam com “EC celebra” impõem às bancadas de governo exatamente o mesmo ônus que moções de “EC apoia”',
                'Na moção “EC prefere um mundo em que movimentos sociais priorizem abordagens conciliatórias sobre abordagens combativas", o primeiro-ministro pode delimitar, por exemplo, situações de exceção nas quais abordagens combativas ainda serão utilizadas',
                "Em moções de policy, a primeira oposição está autorizada a apresentar qualquer contraproposta, que será vinculativa ao resto do debate, desde que exija uma quantidade de recursos comparáveis com os da Policy apresentada pelo Primeiro Governo",
                "Em moções “EC lamenta X” deve-se sopesar os impactos positivos e negativos ao mundo causados diretamente por X.",
                'Na moção "ECAQ países em desenvolvimento deveriam priorizar políticas sociais a de políticas de classe", a 1O pode propor que tais países deem igual atenção às políticas sociais e de classe',
                'Na moção “ECAQ os EUA deveriam intervir no Oriente Médio”, o primeiro governo pode estabelecer um modelo de como, exatamente, a intervenção será realizada'
            ],
        "answer": [
            'Moções “EC lamenta X” sempre exigem uma análise retrospectiva de como seria o mundo se determinado fato não tivesse ocorrido',
            'Na moção “EC prefere um mundo em que o Brasil sempre foi governado pela esquerda política”, as oposições não podem defender um mundo em que o Brasil sempre tenha sido governado pela direita política',
            'Moções que iniciam com “EC celebra” impõem às bancadas de governo exatamente o mesmo ônus que moções de “EC apoia”',
            'Na moção “EC prefere um mundo em que movimentos sociais priorizem abordagens conciliatórias sobre abordagens combativas", o primeiro-ministro pode delimitar, por exemplo, situações de exceção nas quais abordagens combativas ainda serão utilizadas',
        ]
    },
    {
        "question": "Selecione as alternativas verdadeiras referentes a tipos de moção.",
        "choices":
            [
                'Moções “EC lamenta X” sempre exigem uma análise retrospectiva de como seria o mundo se determinado fato não tivesse ocorrido',
                'Na moção “EC prefere um mundo em que o Brasil sempre foi governado pela esquerda política”, as oposições não podem defender um mundo em que o Brasil sempre tenha sido governado pela direita política',
                'Moções que iniciam com “EC celebra” impõem às bancadas de governo exatamente o mesmo ônus que moções de “EC apoia”',
                'Na moção “ECAQ os EUA deveriam intervir no Oriente Médio”, o primeiro governo pode estabelecer um modelo de como, exatamente, a intervenção será realizada',
                "Em moções de policy, a primeira oposição está autorizada a apresentar qualquer contraproposta, que será vinculativa ao resto do debate, desde que exija uma quantidade de recursos comparáveis com os da Policy apresentada pelo Primeiro Governo",
                "Em moções “EC lamenta X” deve-se sopesar os impactos positivos e negativos ao mundo causados diretamente por X.",
                'Na moção "ECAQ países em desenvolvimento deveriam priorizar políticas sociais a de políticas de classe", a 1O pode propor que tais países deem igual atenção às políticas sociais e de classe',
            ],
        "answer": [
            'Moções “EC lamenta X” sempre exigem uma análise retrospectiva de como seria o mundo se determinado fato não tivesse ocorrido',
            'Na moção “EC prefere um mundo em que o Brasil sempre foi governado pela esquerda política”, as oposições não podem defender um mundo em que o Brasil sempre tenha sido governado pela direita política',
            'Moções que iniciam com “EC celebra” impõem às bancadas de governo exatamente o mesmo ônus que moções de “EC apoia”',
            'Na moção “ECAQ os EUA deveriam intervir no Oriente Médio”, o primeiro governo pode estabelecer um modelo de como, exatamente, a intervenção será realizada'
        ]
    },
    {
        "question": "Selecione as alternativas verdadeiras referentes a comparativas entre duplas.",
        "choices":
            [
                'É possível que a Segunda Oposição vença do Primeiro Governo, mesmo que não apresente nenhuma resposta, comparação, e que nem sequer mencione o caso de 1G em seus discursos',
                'Na comparativa entre Primeira Oposição e Segundo Governo, pode ser preciso considerar os discursos do Primeiro Governo, para “subtrair” de 2G material repetido',
                'Uma extensão vertical competente, que consista de análises corretas e relevantes que agreguem ao caso da primeira metade, é capaz de “roubar” alguns dos pontos previamente inaugurados. Nesse cenário, na comparativa entre as duplas desta bancada, os juízes não devem mais considerar para a 1ª casa os pontos “roubados” pela 2ª casa',
                'Se uma dupla executa uma extensão completamente horizontal, ela precisa, para vencer de sua casa alta, fazer uma comparação explícita justificando que sua métrica ou impacto é mais relevante que o apresentado na primeira metade',
                "Na comparativa entre as primeiras casas pode-se precisar levar em consideração, por exemplo, os discursos do Segundo Governo, caso a contribuição de 2G tenha apresentado refutações destrutivas e exposto falhas lógicas significativas do caso da Primeira Oposição",
                'Após o fim do discurso do adjunto da oposição, já é sempre possível determinar qual o resultado da comparativa entre as primeiras metades',
            ],
        "answer": [
            'É possível que a Segunda Oposição vença do Primeiro Governo, mesmo que não apresente nenhuma resposta, comparação, e que nem sequer mencione o caso de 1G em seus discursos',
            'Na comparativa entre Primeira Oposição e Segundo Governo, pode ser preciso considerar os discursos do Primeiro Governo, para “subtrair” de 2G material repetido',
        ]
    },
    {
        "question": "Selecione as alternativas verdadeiras referentes ao processo de deliberação.",
        "choices":
            [
                'O chair, ao coletar a call inicial de cada membro da mesa, sempre deve começar pelo juiz menos experiente, progredindo até o mais experiente, e revelando sua call por último',
                'Caso não seja possível atingir unanimidade sobre certa comparativa e ela precise ser votada, apenas o chair e os wings têm poder de voto, excetuando-se os trainees.',
                'Normalmente, todas as comparativas bilaterais devem ser discutidas entre o painel. No entanto, caso todos os juízes tenham a mesma call inicial, dispensa-se a deliberação individualizada das comparativas, sendo permitido que o painel tenha uma discussão do debate sob uma visão ampla',
                'O chair sempre é o principal responsável pela explicação do feedback oral, mas pode convidar seus wings para contribuírem com comentários pontuais'
            ],
        "answer": [
            'O chair, ao coletar a call inicial de cada membro da mesa, sempre deve começar pelo juiz menos experiente, progredindo até o mais experiente, e revelando sua call por último',
            'Caso não seja possível atingir unanimidade sobre certa comparativa e ela precise ser votada, apenas o chair e os wings têm poder de voto, excetuando-se os trainees.',
        ]
    }
]


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
