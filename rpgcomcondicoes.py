import os
import random

# ==========================================================
# FUNÇÕES DE SAVE/LOAD
# ==========================================================
def salvar_jogo(vida, xp, level, espada, pocao_vida, amigos, alerta_inimigos, situacoes):
    with open("save.txt", "w") as arquivo:
        amigos_str = "|".join(amigos)
        alerta_str = "|".join(alerta_inimigos)
        situacoes_str = "|".join(situacoes)
        arquivo.write(f"{vida},{xp},{level},{espada},{pocao_vida},{amigos_str},{alerta_str},{situacoes_str}")
    print("💾 Progresso salvo com sucesso!")

def carregar_jogo():
    if os.path.exists("save.txt"):
        with open("save.txt", "r") as arquivo:
            conteudo = arquivo.read().strip()
            if conteudo == "":
                return None
            dados = conteudo.split(",")
            vida = int(dados[0])
            xp = int(dados[1])
            level = int(dados[2])
            espada = dados[3] == "True" if len(dados) > 3 else False
            pocao_vida = int(dados[4]) if len(dados) > 4 else 1
            amigos = dados[5].split("|") if len(dados) > 5 and dados[5] else []
            alerta_inimigos = dados[6].split("|") if len(dados) > 6 and dados[6] else []
            situacoes = dados[7].split("|") if len(dados) > 7 and dados[7] else []
            return vida, xp, level, espada, pocao_vida, amigos, alerta_inimigos, situacoes
    else:
        return None

# ==========================================================
# FUNÇÃO: SITUAÇÃO QUANDO TE VEEM
# ==========================================================
def inimigo_te_ve(inimigo, situacoes):
    falas = {
        "soldado de black": ["Voce nao escapa!", "Prepare-se!", "Black vai rir de voce!"],
        "assassino": ["Achou que podia se esconder?", "Vou acabar com voce!", "Nao tente fugir!"],
        "espio": ["Te encontrei!", "Ninguem se esconde de mim!", "Alertarei os outros!"]
    }
    situacao = random.randint(1,4)
    fala = random.choice(falas.get(inimigo, ["O inimigo te viu!"]))

    if situacao == 1:
        print(f"\n💥 {inimigo.upper()} te viu e gritou: '{fala}'")
        situacoes.append(f"{inimigo} alertou reforcos")
        return "alerta"
    elif situacao == 2:
        dano = random.randint(5,15)
        print(f"\n⚔️ {inimigo.upper()} te atacou de surpresa: '{fala}'! Voce perdeu {dano} de vida!")
        return dano
    elif situacao == 3:
        print(f"\n🏃 {inimigo.upper()} te persegue: '{fala}'")
        escolha = input("Voce quer lutar ou fugir? ").lower()
        if escolha == "lutar":
            dano = random.randint(10,20)
            print(f"Voce enfrenta o {inimigo} e toma {dano} de dano!")
            return dano
        else:
            print("Voce fugiu, mas o inimigo esta alerta e reforcos podem aparecer depois!")
            situacoes.append(f"{inimigo} fugiu e alertou reforcos")
            return "alerta"
    elif situacao == 4:
        dano = random.randint(5,25)
        print(f"\n⚠️ Armadilha! {inimigo.upper()} te surpreende: '{fala}'")
        print(f"Voce perdeu {dano} de vida!")
        situacoes.append(f"{inimigo} colocou armadilha")
        return dano

# ==========================================================
# INICIO DO JOGO
# ==========================================================
print("Bem vindo ao mundo dos ninjas!")
nome = input("Digite o nome do seu ninja: ")

cachecol_magico = True

save = carregar_jogo()
if save:
    vida, xp, level, espada, pocao_vida, amigos, alerta_inimigos, situacoes = save
    print("📂 Save encontrado! Carregando progresso...")
else:
    vida = 100
    xp = 0
    level = 1
    espada = False
    pocao_vida = 1
    amigos = []
    alerta_inimigos = []
    situacoes = []
    print("✨ Novo jogo iniciado!")

print(f"\n{nome}, voce recebeu do seu pai o cachecol magico, que funciona como um tentaculo.")
print("Voce vive numa cidade tranquila ate que um vilao chamado Black aparece com seu exercito.")

# ==========================================================
# LOOP PRINCIPAL
# ==========================================================
while True:
    print("\n=== MENU DO JOGO ===")
    print("[1] Explorar")
    print("[2] Observar")
    print("[3] Treinar")
    print("[4] Ver status")
    print("[5] Usar pocao de vida")
    print("[6] Salvar jogo")
    print("[7] Sair")

    opc = input("Escolha: ")

    if opc == "1":
        print("\nVoce explora a cidade...")
        inimigo = random.choice(["soldado de black","assassino","espio"])
        print(f"Um {inimigo} apareceu!")

        acao = input("Voce quer lutar ou fugir? ").lower()
        if acao == "lutar":
            dano = random.randint(5,20)
            ganho_xp = random.randint(15,30)
            vida -= dano
            xp += ganho_xp
            print(f"\nVoce derrotou o {inimigo} mas tomou {dano} de dano")
            print(f"Ganhou {ganho_xp} XP")

            if xp >= level*100:
                level +=1
                xp=0
                vida=100
                print(f"LEVEL UP! Agora voce e nivel {level}")
                print("Vida restaurada!")

            item = random.choice(["espada","nenhum","pocao"])
            if item=="espada":
                espada=True
                print("Voce encontrou uma espada!")
            elif item=="pocao":
                pocao_vida+=1
                print("Voce encontrou uma pocao de vida!")

            resultado = inimigo_te_ve(inimigo, situacoes)
            if resultado=="alerta":
                alerta_inimigos.append(inimigo)
            elif isinstance(resultado,int):
                vida-=resultado

            if vida<=0:
                print("\nVOCE CAIU EM BATALHA... FIM DE JOGO")
                break
        else:
            print("Voce fugiu com seguranca...")

    elif opc=="2":
        print("\nVoce tenta observar a area...")
        chance = random.randint(1,4)
        if chance==1:
            inimigo = random.choice(["soldado de black","assassino","espio"])
            print(f"Ops! {inimigo.upper()} te viu!")
            resultado = inimigo_te_ve(inimigo,situacoes)
            if resultado=="alerta":
                alerta_inimigos.append("alerta")
            elif isinstance(resultado,int):
                vida-=resultado
        else:
            print("Voce observou sem ser visto, aprendeu algo util!")

    elif opc=="3":
        print("\nVoce esta treinando...")
        treino = input("Escolha treino: forca ou agilidade: ").lower()
        if treino=="forca":
            print("Voce aumentou a forca! XP +20")
            xp+=20
        elif treino=="agilidade":
            print("Voce aumentou a agilidade! XP +20")
            xp+=20
        else:
            print("Treino invalido!")

        if xp>=level*100:
            level+=1
            xp=0
            vida=100
            print(f"LEVEL UP! Agora voce e nivel {level}")
            print("Vida restaurada!")

    elif opc=="4":
        print("\n=== STATUS DO JOGADOR ===")
        print(f"Nome: {nome}")
        print(f"Vida: {vida}")
        print(f"XP: {xp}")
        print(f"Level: {level}")
        print(f"Espada: {espada}")
        print(f"Cachecol magico: {cachecol_magico}")
        print(f"Pocoes de vida: {pocao_vida}")
        if amigos:
            print("Amigos ninjas:", amigos)
        else:
            print("Amigos ninjas: Nenhum")
        if alerta_inimigos:
            print("Inimigos alertados:", alerta_inimigos)
        else:
            print("Inimigos alertados: Nenhum")
        if situacoes:
            print("Eventos passados:", situacoes)
        else:
            print("Eventos passados: Nenhum")

    elif opc=="5":
        if pocao_vida>0:
            vida+=30
            if vida>100:
                vida=100
            pocao_vida-=1
            print("Voce usou uma pocao e recuperou 30 de vida!")
            print(f"Vida atual: {vida}")
        else:
            print("Voce nao tem pocao de vida!")

    elif opc=="6":
        salvar_jogo(vida,xp,level,espada,pocao_vida,amigos,alerta_inimigos,situacoes)

    elif opc=="7":
        print("Saindo do jogo...")
        break

    else:
        print("Opcao invalida!")
