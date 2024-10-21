from crewai import Agent, Task, Crew, Process
from tools import check_images_alt_in_page, generate_bi_report

# Criando o agente que verifica imagens em uma página
web_image_checker_agent = Agent(
    role='Web Image Checker',
    goal='Verifique as tags de imagem em uma página web e veja se todas possuem texto alternativo.',
    backstory='Você é um especialista em acessibilidade da web, focado em garantir que todas as imagens em sites tenham texto alternativo. {url} é um site que precisa ser verificado.',
    tools=[check_images_alt_in_page],  # A ferramenta criada anteriormente
    verbose=True
)


# Criando o agente responsável por gerar o BI
bi_audit_agent = Agent(
    role='Data BI Auditor',
    goal='Analisar os dados e gerar um relatório de BI com insights para auditoria.',
    backstory='Você é um auditor especializado em Business Intelligence. Sua tarefa é identificar padrões e anomalias nos dados e gerar insights valiosos para auditoria.',
    tools=[generate_bi_report],  # A ferramenta criada anteriormente
    verbose=True
)

# Criando a task
check_images_task = Task(
    description=(
        "Verifique se todas as tags de imagem em uma página web possuem o atributo 'alt'. "
        "Você deve acessar a página e fazer uma análise das tags de imagem."
        "Seu relatório final deve listar todas as imagens que estão sem o atributo 'alt'."
    ),
    expected_output='Um relatório que lista as imagens que não possuem atributo alt.',
    tools=[check_images_alt_in_page],
    agent=web_image_checker_agent,
)

# Criando a task de auditoria e BI
bi_audit_task = Task(
    description=(
        "Analise os dados fornecidos, gere gráficos e identifique possíveis anomalias para auditoria. "
        "Você deve fornecer um resumo estatístico dos dados e apontar quaisquer padrões ou outliers que encontrar."
    ),
    expected_output='Um relatório com insights de BI e um gráfico salvo para visualização.',
    tools=[generate_bi_report],
    agent=bi_audit_agent,
)

# Criando o Crew
crew = Crew(
    agents=[web_image_checker_agent],
    tasks=[check_images_task],
    process=Process.sequential
)

# Executando o processo para verificar imagens na página
result = crew.kickoff(inputs={'url': 'https://www.setdig.ms.gov.br/'})
print(result)