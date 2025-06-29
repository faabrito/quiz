from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
# Chave secreta para a sessão (necessário para usar 'session')
# Troque por uma string aleatória e complexa em um ambiente de produção real!
app.secret_key = os.urandom(24)

# Lista de perguntas, opções e respostas corretas
quiz_questions = [
    {
        "pergunta": "O que é poupança?",
        "opcoes": [
            "a) Gastar todo o dinheiro que você tem.",
            "b) Guardar uma parte do dinheiro para usar no futuro.",
            "c) Pedir dinheiro emprestado para comprar o que quiser.",
            "d) Doar todo o seu dinheiro para caridade."
        ],
        "resposta": "b",
        "explicacao": "Poupança é o ato de guardar dinheiro com um objetivo futuro, seja para uma compra, uma emergência ou um investimento."
    },
    {
        "pergunta": "Qual a diferença entre 'necessidade' e 'desejo'?",
        "opcoes": [
            "a) Necessidade é algo que queremos muito, desejo é o que precisamos para sobreviver.",
            "b) Necessidade é o que precisamos para viver (comida, moradia), desejo é algo que gostaríamos de ter (brinquedo novo, celular).",
            "c) Não há diferença, são a mesma coisa.",
            "d) Necessidade é um luxo, desejo é uma obrigação."
        ],
        "resposta": "b",
        "explicacao": "Necessidades são itens essenciais para a sobrevivência e bem-estar básico, enquanto desejos são coisas que gostaríamos de ter, mas não são indispensáveis."
    },
    {
        "pergunta": "Se você recebe sua mesada e anota tudo o que entra e sai de dinheiro, você está fazendo um:",
        "opcoes": [
            "a) Gasto desnecessário.",
            "b) Orçamento.",
            "c) Desperdício.",
            "d) Empréstimo."
        ],
        "resposta": "b",
        "explicacao": "Um orçamento é uma ferramenta para planejar e controlar suas finanças, registrando receitas e despesas."
    },
    {
        "pergunta": "O que pode acontecer se você gastar mais dinheiro do que ganha constantemente?",
        "opcoes": [
            "a) Você ficará rico rapidamente.",
            "b) Você acumulará dívidas.",
            "c) Seu dinheiro vai multiplicar automaticamente.",
            "d) Você receberá um bônus."
        ],
        "resposta": "b",
        "explicacao": "Gastar mais do que se ganha leva ao endividamento, que pode gerar juros e dificultar sua situação financeira."
    },
    {
        "pergunta": "Por que é importante comparar preços antes de comprar algo?",
        "opcoes": [
            "a) Para gastar mais dinheiro.",
            "b) Para economizar e fazer o seu dinheiro render mais.",
            "c) Para encontrar o item mais caro.",
            "d) Para mostrar que você tem dinheiro."
        ],
        "resposta": "b",
        "explicacao": "Comparar preços ajuda a encontrar a melhor oferta, economizar dinheiro e fazer compras mais inteligentes."
    }
]

@app.route('/')
def index():
    """Página inicial do quiz."""
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """Gerencia as perguntas do quiz."""
    if request.method == 'GET':
        # Reinicia o quiz ao carregar a página pela primeira vez ou recarregar
        session['score'] = 0
        session['current_question_index'] = 0
        return render_questionario()
    elif request.method == 'POST':
        # Processa a resposta do usuário
        user_answer = request.form.get('answer')
        current_index = session.get('current_question_index', 0)

        # Se não houver resposta selecionada, retorna para a mesma pergunta com um aviso
        if not user_answer:
            current_question = quiz_questions[current_index]
            error_message = "Por favor, selecione uma opção antes de continuar."
            return render_template('question.html', 
                                   question=current_question, 
                                   question_number=current_index + 1, 
                                   total_questions=len(quiz_questions),
                                   error=error_message)

        # Verifica se a resposta está correta
        if user_answer == quiz_questions[current_index]['resposta']:
            session['score'] += 1

        # Avança para a próxima pergunta
        session['current_question_index'] += 1

        # Verifica se há mais perguntas
        if session['current_question_index'] < len(quiz_questions):
            return render_questionario()
        else:
            return redirect(url_for('result'))

def render_questionario():
    """Função auxiliar para renderizar a página da pergunta atual."""
    current_index = session.get('current_question_index', 0)
    current_question = quiz_questions[current_index]
    return render_template('question.html',
                           question=current_question,
                           question_number=current_index + 1,
                           total_questions=len(quiz_questions))

@app.route('/resultados')
def resultados():
    """Exibe o resultado final do quiz."""
    final_score = session.get('score', 0)
    total_questions = len(quiz_questions)

    feedback = ""
    if final_score == total_questions:
        feedback = "Parabéns! Você é um(a) expert em educação financeira básica! 💰"
    elif final_score >= total_questions / 2:
        feedback = "Muito bom! Você tem um bom conhecimento de educação financeira. Continue aprendendo! 👍"
    else:
        feedback = "Você está no caminho certo! Continue estudando para melhorar seu conhecimento financeiro. 📚"

    return render_template('resultados.html', score=final_score, total=total_questions, feedback=feedback)

if __name__ == '__main__':
    # Para rodar o app localmente, o modo debug é útil para desenvolvimento
    app.run(debug=True)