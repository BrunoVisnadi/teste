from flask import Flask, render_template, request, redirect, url_for, session, render_template_string
#import sqlite3
import uuid
import random
from datetime import datetime, timedelta
import psycopg2



def get_connection():
    return psycopg2.connect("postgresql://neondb_owner:npg_RxU8dZQOm9uL@ep-red-fire-akn3nhqn.c-3.us-west-2.aws.neon.tech/neondb") # it is OK to hardcode for this use case
app = Flask(__name__)
app.secret_key = 'blahh'

QUESTIONS = [{'question': 'Atribuição de Speaker Points', 'choices': ['Ao avaliar uma dupla, caso o painel de adjudicação acredite que o argumento vencedor foi provado no discurso da primeira fala, o painel deve dar speaker points maiores para a primeira fala do que para a segunda fala.', 'É comum que um discurso não se encaixe perfeitamente em uma faixa específica de Speaker Points, visto que muitas vezes o conteúdo pode estar em uma faixa, a estrutura em outra e a relevância em uma terceira. A avaliação de um discurso deve levar isso em consideração e dar um Speaker Point que reflita a combinação desses fatores, sendo nenhum deles mais importante que o outro para definir Speaker Points.', 'Os Speaker Points devem refletir a proximidade das comparativas, se o painel concorda que uma comparativa foi próxima deve dar Speaker Points próximos (no total) para os debatedores da comparativa.', 'Após uma deliberação um painel de três pessoas chega em um split onde a call majoritária e minoritária são:<br>Maj: 2O &gt; 2G &gt; 1G &gt; 1O<br>Min: 2G &gt; 2O &gt; 1G &gt; 1O<br>O membro do painel que está na comparativa minoritária não deve participar da atribuição de Speaker Points de Segundo Governo e Segunda Oposição.', 'É fortemente recomendado que caso um Chair esteja na comparativa minoritária ao final de uma deliberação (ou seja, tenha sido rolado) que o Chair selecione um wing para dar o feedback oral da rodada por completo e que o Chair explique somente o seu split.'], 'answer': ['É comum que um discurso não se encaixe perfeitamente em uma faixa específica de Speaker Points, visto que muitas vezes o conteúdo pode estar em uma faixa, a estrutura em outra e a relevância em uma terceira. A avaliação de um discurso deve levar isso em consideração e dar um Speaker Point que reflita a combinação desses fatores, sendo nenhum deles mais importante que o outro para definir Speaker Points.', 'Os Speaker Points devem refletir a proximidade das comparativas, se o painel concorda que uma comparativa foi próxima deve dar Speaker Points próximos (no total) para os debatedores da comparativa.', 'Após uma deliberação um painel de três pessoas chega em um split onde a call majoritária e minoritária são:<br>Maj: 2O &gt; 2G &gt; 1G &gt; 1O<br>Min: 2G &gt; 2O &gt; 1G &gt; 1O<br>O membro do painel que está na comparativa minoritária não deve participar da atribuição de Speaker Points de Segundo Governo e Segunda Oposição.', 'É fortemente recomendado que caso um Chair esteja na comparativa minoritária ao final de uma deliberação (ou seja, tenha sido rolado) que o Chair selecione um wing para dar o feedback oral da rodada por completo e que o Chair explique somente o seu split.']},
             {'question': 'Eleitor Médio Global', 'choices': ['Em um debate, a adjunta da oposição afirma que parte do argumento central do primeiro governo é um apelo à autoridade e, por isso, não deve ser creditado pelo painel. Caso a adjunta não explique o que significa apelo à autoridade, sua resposta estará prejudicada, pois “apelo à autoridade” se trata de um conceito acadêmico específico e não faz parte do arcabouço de conhecimento do Eleitor Médio do modelo BP.', 'É de conhecimento do eleitor médio do modelo BP que a Polônia é um produtor agrícola importante da União Europeia.', 'Ao comparar dois argumentos suficientemente e similarmente provados, o adjudicador pode considerar que um deles é mais persuasivo por ser mais intuitivo que o outro.', 'Um adjudicador pode justificar que um argumento é mais persuasivo que outro por carregar uma quantidade maior de razões (mecanismos).', 'O adjudicador deve considerar inerentemente mais persuasivos argumentos que afetam, positiva ou negativamente, stakeholders em condição de vulnerabilidade, mesmo que não haja sopesamento específico destes stakeholders.'], 'answer': ['É de conhecimento do eleitor médio do modelo BP que a Polônia é um produtor agrícola importante da União Europeia.']},
             {'question': 'Condução de Mesa', 'choices': ['Mesmo que devam ser ouvidos durante a deliberação, adjudicadores trainees não têm poder de voto, ou seja, não contabilizam split em deliberações.', 'Se um wing discorda de uma comparativa e a deliberação encerra em um split, onde o wing está na minoria e a call final é a do Chair, o Chair deve avaliar o wing negativamente, pois este prejudicou a condução da deliberação e insistiu em uma call errada.', 'Em um painel com três adjudicadores onde as calls são as seguintes:<br>Chair: 1G&gt;2G&gt;1O&gt;2O<br>Wing A: 2G&gt;1G&gt;1O&gt;2O<br>Wing B: 2G&gt;1O&gt;1G&gt;2O<br>É recomendado que o Chair inicie a deliberação pela comparativa entre 1 Governo e 1 Oposição, tanto por essa ser a comparativa mais distante entre o chair e um membro do painel, quanto pelo fato de que caso Wing B altere a sua comparativa o debate já terá uma call majoritária.', 'É fortemente recomendado que tanto Chairs quanto Wings façam as comparativas enquanto o debate ocorre, ou seja que ao final do debate de bancadas altas estes já tenham uma opinião formada sobre quem ganhou entre o Primeiro Governo e a Primeira Oposição.', 'Ao avaliar um membro do Painel de adjudicação a nota 5 implica uma performance ruim do trainee/wing/chair.', 'É recomendado que Chairs cronometrem a deliberação para que não exceda a duração recomendada, bem como que cortem painelistas que excedam dois minutos em uma comparativa, caso já tenham entendido as razões do painelista.'], 'answer': ['Mesmo que devam ser ouvidos durante a deliberação, adjudicadores trainees não têm poder de voto, ou seja, não contabilizam split em deliberações.', 'Em um painel com três adjudicadores onde as calls são as seguintes:<br>Chair: 1G&gt;2G&gt;1O&gt;2O<br>Wing A: 2G&gt;1G&gt;1O&gt;2O<br>Wing B: 2G&gt;1O&gt;1G&gt;2O<br>É recomendado que o Chair inicie a deliberação pela comparativa entre 1 Governo e 1 Oposição, tanto por essa ser a comparativa mais distante entre o chair e um membro do painel, quanto pelo fato de que caso Wing B altere a sua comparativa o debate já terá uma call majoritária.', 'É fortemente recomendado que tanto Chairs quanto Wings façam as comparativas enquanto o debate ocorre, ou seja que ao final do debate de bancadas altas estes já tenham uma opinião formada sobre quem ganhou entre o Primeiro Governo e a Primeira Oposição.', 'É recomendado que Chairs cronometrem a deliberação para que não exceda a duração recomendada, bem como que cortem painelistas que excedam dois minutos em uma comparativa, caso já tenham entendido as razões do painelista.']},
             {'question': 'Tipos de Moção', 'choices': ['Na moção, “EC prefere que o alistamento Militar no Brasil seja realizado por sorteio” é ônus das oposições defenderem o Status Quo.', 'Na moção “EC, enquanto cidadão chinês, apoia o fim do Partido Comunista Chinês”, uma equipe argumenta que seu caso é mais relevante porque é impossível que um cidadão chinês tenha acesso às informações trazidas no caso da equipe contrária. Caso provada, esta análise é válida e creditada, visto que moções de agente devem ser debatidas de forma circunscrita aos interesses, valores e conhecimento do agente em questão.', 'Na moção “EC baniria cirurgias estéticas”, o primeiro governo delimita que não irá aplicar a medida para vítimas de acidentes (como incêndios, ferimentos graves, etc). A limitação do primeiro governo é legítima.', 'Na moção EC aboliria a ONU, a primeira oposição pode apresentar uma contraproposta de reforma da ONU em vez de defender o status quo.', 'Na moção “Esta Casa lamenta a escolha de Kamala Harris como candidata democrata”, o contrafactual elaborado pelo primeiro ministro tem a capacidade de alterar os incentivos dos membros do partido democrata, por exemplo, o primeiro governo pode argumentar que a escolha feita - à época - seria a de Zohran Mandani, mesmo que esse candidato não tivesse apoio majoritário do partido democrata para o cargo.', 'A moção “EC celebra a candidatura de Ronaldo Caiado ao executivo brasileiro” deve ser lida como se fossem redigida com o verbete EC Apoia'], 'answer': ['Na moção, “EC prefere que o alistamento Militar no Brasil seja realizado por sorteio” é ônus das oposições defenderem o Status Quo.', 'Na moção “EC baniria cirurgias estéticas”, o primeiro governo delimita que não irá aplicar a medida para vítimas de acidentes (como incêndios, ferimentos graves, etc). A limitação do primeiro governo é legítima.', 'Na moção EC aboliria a ONU, a primeira oposição pode apresentar uma contraproposta de reforma da ONU em vez de defender o status quo.', 'A moção “EC celebra a candidatura de Ronaldo Caiado ao executivo brasileiro” deve ser lida como se fossem redigida com o verbete EC Apoia']},
             {'question': 'Extensão/Derivação', 'choices': ['Na moção “EC baniria cirurgias estéticas”, o primeiro governo delimita que não irá aplicar a medida para vítimas de acidentes (como incêndios, ferimentos graves, etc). O segundo governo argumenta de forma competente que um banimento completo das cirurgias estéticas (sem as limitações de 1G) ainda seria positivo. A extensão do segundo governo é significativa e provavelmente se posiciona acima da sua casa alta, pois compra um ônus maior.', 'Novos impactos, mesmo que dependentes dos mecanismos da bancada alta, configuram material de extensão e devem ser creditados como tal.', 'Novos sopesamentos, novos mecanismos e novos enquadramentos para argumentos já feitos pela bancada alta configuram extensão.', 'Na moção “EC lamenta a centralidade do arrependimento na religião organizada”, o primeiro governo analisa que no contrafactual  menos indivíduos são pressionados a confessar informações pessoais para líderes religiosos, dando menos poder coercitivo para estes. O segundo governo, por sua vez, analisa que a falta de poder coercitivo força que a religião organizada busque outras formas de legitimação, como caridade, com mais intensidade. Em razão do argumento do segundo governo ser dependente da perda de poder coercitivo, o segundo governo não tem extensão significativa e não poderá se posicionar acima da sua bancada alta.'], 'answer': ['Novos impactos, mesmo que dependentes dos mecanismos da bancada alta, configuram material de extensão e devem ser creditados como tal.', 'Novos sopesamentos, novos mecanismos e novos enquadramentos para argumentos já feitos pela bancada alta configuram extensão.']},
             {'question': 'Esfaqueamento/Contradições', 'choices': ['Na moção “Esta casa lamenta a centralidade do arrependimento na religião organizada” o primeiro governo analisa que no contrafactual  menos indivíduos são pressionados a confessar informações pessoais para líderes religiosos, dando menos poder coercitivo para estes. O segundo governo, por sua vez, analisa que no contrafactual a ausência de ênfase no arrependimento permite com que pessoas sejam mais egoístas se auto priorizando mais, o que é positivo para elas em um nível individual. Em razão de primeiro e segundo governo terem contrafactuais diferentes ocorre esfaqueamento entre as bancadas.', 'No caso de contradições entre o discurso de uma mesma equipe, o material contraditório da segunda fala não deve ser avaliado pelo painel.', 'O segundo governo não pode, em hipótese alguma, contrariar as premissas lançadas pelo primeiro governo no debate sob a pena de seu material contributivo ser considerado um “esfaqueamento”.', 'Na moção “EC invadiria a Coreia do Norte” o PM, em sua primeira análise, argumenta que com o poder bélico norte-coreano o país tem fortes incentivos a adotar posturas mais belicosas, como por exemplo alocação de tropas nas fronteiras com a Coreia do Sul, exercícios militares frequentes, apoio bélico a aliados políticos e possibilidade de expansão territorial. Outrossim, em uma segunda análise, argumenta que em caso de invasão a Coreia do Norte não tem incentivos a retaliação - ou seja, não existirão guerras no território coreano e o governo provavelmente se renderia - isso pois, a Coreia do Norte não tem poder bélico para se defender e não gostaria de colocar em risco seus exércitos. Admitindo que as análises, autonomamente, foram munidas de incentivos persuasivos suficientes. Ambas as análises devem ser integralmente creditadas'], 'answer': ['No caso de contradições entre o discurso de uma mesma equipe, o material contraditório da segunda fala não deve ser avaliado pelo painel.']},
             {'question': 'Sopesamento', 'choices': ['Na moção “Em democracias desenvolvidas, Esta Casa acredita que crescer como adolescente da geração Millennial foi melhor do que crescer como adolescente da geração Z”,  o primeiro governo argumenta que crescer como parte da geração Z foi negativo, pois o amplo acesso à internet fez mal aos jovens. A primeira oposição argumenta que crescer na geração Z foi preferível, pois o mundo é muito mais receptivo a adolescentes minoritários. A primeira oposição leva vantagem na comparativa contra o primeiro governo, por ter o stakeholder mais vulnerável.', 'Na moção, “EC, enquanto Paquistão, assinaria um acordo nuclear com os EUA”, a primeira oposição argumenta que o Paquistão não deveria assinar esse acordo, pois isso minaria sua capacidade de se defender de ataques externos na região. Já a extensão de oposição sustenta que o Paquistão, por ser uma república islâmica, não assinaria um acordo com um país ocidental que apoia Israel. Ademais, o Whip de oposição afirma que o caso da segunda oposição deve avançar por estar ligado a uma característica inerente ao agente, argumentando que a primeira oposição trabalha apenas com incentivos que um agente genérico teria para não assinar o acordo, enquanto a segunda oposição demonstraria que o Paquistão nunca o assinaria. Nesse cenário, mesmo supondo que todas as análises estejam bem fundamentadas, é falso afirmar que o caso da segunda oposição sempre avança na comparativa.', 'Argumentos principiológicos, por independerem de lógicas consequencialistas, são intuitivamente anteriores a argumentos com impactos pragmáticos. Portanto, supondo que ambas as bancadas provem suas análises, ao sopesar entre um argumento pragmático de Primeiro Governo e um argumento principiológico de Segunda Oposição o adjudicador deve considerar que o princípio avança na comparação.'], 'answer': []},
             {'question': 'Argumentação Geral', 'choices': ['Na moção “EC Apoia a escolha de Fernando Haddad como candidato a governador de São Paulo” a extensão de governo argumenta que a escolha de Fernando Haddad é boa, pois ele é o candidato que melhor se conecta com e representa o cidadão médio de São Paulo. O whip de governo argumenta que o cidadão médio de São Paulo é comparativamente mais escolarizado e por isso se conecta mais com figuras com perfis acadêmicos, como Haddad, visto que indivíduos sentem mais empatia por pessoas semelhantes a si. O whip também argumenta que é um dever moral das democracias serém representativas. Em virtude do material do whip ser novo ele não deve ser considerado.', 'Na moção “EC Prefere um mundo onde a Constituição Brasileira de 1988 é minimalista em detrimento de garantista” o primeiro governo argumenta que a assembleia constituinte é a mesma nos dois cenários e por isso ainda existem fortes incentivos para que a constituição proteja direitos minoritários, como ocorreu no status quo. A análise contrafactual do primeiro governo configura fuga do ônus e portanto não é legítima.', 'Assim como em moções de medida (policy), em que somente o primeiro ministro tem fiat para impor o modelo de governos, em moções de contrafactual obrigatório (Lamenta e Prefere um Mundo) somente o primeiro ministro tem fiat para impor o contrafactual.', 'Na moção “ECAQ a educação deveria ser privatizada”, o PM defende que no “seu mundo” todas as universidades serão privatizadas, em contrapartida, o LO diz que a análise de primeiro governo é injusta argumentando que o termo educação abrange não só as universidades como também o ensino médio, fundamental e técnico. Nesse cenário, a contestação da primeira oposição não deve avançar, pois o Primeiro Ministro possui Fiat.', 'Refutações, sopesamentos, mitigações e demais contributos responsivos não podem ser creditados se o debatedor não fundamentar o motivo pelo qual estes contributos são verdadeiros. Por exemplo, a mesa adjudicadora não deverá creditar uma refutação que se limite a afirmar que a bancada oposta não cumpriu com determinado ônus de prova.', 'Argumentos que ferem normas de equidade não devem ser considerados pela mesa de adjudicação.'], 'answer': ['Na moção “ECAQ a educação deveria ser privatizada”, o PM defende que no “seu mundo” todas as universidades serão privatizadas, em contrapartida, o LO diz que a análise de primeiro governo é injusta argumentando que o termo educação abrange não só as universidades como também o ensino médio, fundamental e técnico. Nesse cenário, a contestação da primeira oposição não deve avançar, pois o Primeiro Ministro possui Fiat.', 'Refutações, sopesamentos, mitigações e demais contributos responsivos não podem ser creditados se o debatedor não fundamentar o motivo pelo qual estes contributos são verdadeiros. Por exemplo, a mesa adjudicadora não deverá creditar uma refutação que se limite a afirmar que a bancada oposta não cumpriu com determinado ônus de prova.']}]
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


#init_db()

@app.route("/admin/generate-urls")
def generate_urls():
    return
    conn = get_connection()
    c = conn.cursor()
    urls = []
    names = """Deborah Simonetti
Luís Otávio Mury
Fabrício Guimarães
Juliana Vasconcelos
Ana Luiza Araújo
Fernanda Caldas
Maria Clara de Assis
Isabelle Neris
Rayssa Teixeira
Victor Christofari
Bárbara Guimarâes
Bianca Raduken
Lucas Felinto
Malu Moura
Leticia Calazans
Cecília Henrique
Victor Andrey
Lorena Medeiros
Pedro Paradela
Lucas Mesquita
Nicolas Paes
Igor Castelo Branco
Lettícia Cardoso
Emily Louise
Pedro Schaefer
Lívia Vasconcelos
Renata Souza
Francisca Patrícia Lima
Isadora Girão
Maria Eduarda Teles
João Victor Santos
Emili de Santana
Lucas Salomão de Freitas
Pedro Nogueira
Anna Clara Belfort
Heitor Cunico
Rafael Ribeiro
Renata Barboza
Yasmin Brito
Ana Beatriz da Silva
João Gabriel Jacó
Larissa Santana
Igor Calmon
Lucas Cerqueira
Murilo Nascimento
Caio Roberto
Thainá Murta
Israel Carvalho
Elias Ravizza
Isadora Calil
Adriely Silva
Thiago Bassani"""
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








