import json
import datetime
import os

arquivo_dados = 'dados_clinica.json'

pacientes_cadastrados = []
agendamentos = []


def serialize_datetime(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()


def salvar_dados():
    with open(arquivo_dados, 'w') as f:
        dados = {'pacientes': pacientes_cadastrados,
                 'agendamentos': agendamentos}
        json.dump(dados, f, default=serialize_datetime)


def carregar_dados():
    if os.path.exists(arquivo_dados):
        with open(arquivo_dados, 'r') as f:
            dados = json.load(f)
            return dados.get('pacientes', []), dados.get('agendamentos', [])
    return [], []


pacientes_cadastrados, agendamentos = carregar_dados()


def cadastrar_paciente():
    nome = input('Digite o nome do paciente: ')
    telefone = input('Digite o telefone do paciente: ')

    for paciente in pacientes_cadastrados:
        if paciente['telefone'] == telefone:
            print('Paciente já cadastrado!')
            return

    paciente = {'nome': nome, 'telefone': telefone}
    pacientes_cadastrados.append(paciente)
    print('Paciente cadastrado com sucesso!')
    salvar_dados()


def listar_pacientes():
    print('Pacientes cadastrados:')
    for i, paciente in enumerate(pacientes_cadastrados, 1):
        print(f"{i}. {paciente['nome']} - {paciente['telefone']}")


def marcar_consulta():
    listar_pacientes()
    escolha = int(input('Escolha o número correspondente ao paciente: ')) - 1

    paciente = pacientes_cadastrados[escolha]

    data_hora = input(
        'Digite a data e hora da consulta (formato: dd/mm/yyyy hh:mm): ')
    data_hora_consulta = datetime.datetime.strptime(
        data_hora, "%d/%m/%Y %H:%M")

    for consulta in agendamentos:
        if consulta['data_hora'] == data_hora_consulta:
            print('Horário já agendado. Escolha outro.')
            return

    if data_hora_consulta < datetime.datetime.now():
        print('Não é possível agendar consultas retroativas.')
        return

    especialidade = input('Digite a especialidade da consulta: ')

    agendamento = {'paciente': paciente, 'data_hora': data_hora_consulta,
                   'especialidade': especialidade}
    agendamentos.append(agendamento)
    print('Consulta marcada com sucesso!')
    salvar_dados()


def cancelar_consulta():
    if not agendamentos:
        print('Não há consultas agendadas.')
        return

    print('Consultas agendadas:')
    for i, consulta in enumerate(agendamentos, 1):
        print(f"{i}. {consulta['paciente']['nome']} - "
              f"{consulta['data_hora']} - {consulta['especialidade']}")

    escolha = int(input(
        'Escolha o número correspondente à consulta que deseja cancelar: '
        )) - 1

    consulta = agendamentos[escolha]
    print(f"Consulta marcada para {consulta['data_hora']} - "
          f"{consulta['especialidade']}")

    confirmacao = input(
        'Deseja cancelar esta consulta? (Digite "sim" para confirmar): '
        ).lower()

    if confirmacao == 'sim':
        agendamentos.pop(escolha)
        print('Consulta cancelada com sucesso!')
        salvar_dados()


while True:
    print('\nMENU:')
    print('1. Cadastrar Paciente')
    print('2. Marcar Consulta')
    print('3. Cancelar Consulta')
    print('4. Sair')

    opcao = input('Escolha uma opção (1/2/3/4): ')

    if opcao == '1':
        cadastrar_paciente()
    elif opcao == '2':
        marcar_consulta()
    elif opcao == '3':
        cancelar_consulta()
    elif opcao == '4':
        print('Saindo do programa. Até mais!')
        break
    else:
        print('Opção inválida. Tente novamente.')
