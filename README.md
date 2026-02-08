# RecruitAI -- (readme melhorado com inteligencia artificial para melhor entendimento)

Plataforma inteligente para triagem de currículos e correspondência de candidatos usando IA local.

## Visão Geral
O SkillMatch AI automatiza a pré-seleção: empresas cadastram vagas com requisitos técnicos; candidatos enviam dados e currículo por formulário lido por IA. Modelos de IA locais extraem competências, analisam experiência e calculam compatibilidade com vaga.

## Fluxo do Sistema
1. **Cadastro da vaga (empresa)**  
   Requisitos obrigatórios e desejáveis, senioridade, stack, perguntas eliminatórias. Tudo é estruturado e salvo.
2. **Candidatura via formulário lido por IA (candidato)**  
   Coleta guiada de dados pessoais, formação, experiência, competências e upload do currículo (PDF/DOCX), com leitura automática pela IA.
3. **Processamento do currículo**  
   Extração de texto → identificação e normalização de habilidades (ex.: JS → JavaScript) → análise semântica → dados estruturados usando modelos locais (Ollama).
4. **Matching engine**  
   Combinações via pesos (must-have vs nice-to-have), similaridade semântica por embeddings e critérios técnicos objetivos. Gera pontuação, requisitos atendidos e pontos de melhoria.
5. **Feedback ao candidato**  
   Envia percentual de compatibilidade, competências atendidas e ausentes, reforçando que a decisão final é humana.

## Tecnologias

- **Frontend:** Vue.js;
- **Backend:** FastAPI (Python); API RESTful; validação com Pydantic.
- **Inteligência Artificial:** Ollama (LLMs local llama3); 
