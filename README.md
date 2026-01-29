# RecruitAI -- (README melhorado com inteligencia artificial para melhor entendimento)

Plataforma inteligente para triagem de currículos e correspondência de candidatos usando IA local.

## Visão Geral
O SkillMatch AI automatiza a pré-seleção: empresas cadastram vagas com requisitos técnicos; candidatos conversam com um chatbot para enviar dados e currículo. Modelos de IA locais extraem competências, analisam experiência e calculam compatibilidade de forma explicável, priorizando privacidade e escalabilidade.

## Fluxo do Sistema
1. **Cadastro da vaga (empresa)**  
   Requisitos obrigatórios e desejáveis, senioridade, stack, perguntas eliminatórias. Tudo é estruturado e salvo.
2. **Candidatura via chatbot (candidato)**  
   Coleta guiada de dados pessoais, formação, experiência, competências e upload do currículo (PDF/DOCX).
3. **Processamento do currículo**  
   Extração de texto → identificação e normalização de habilidades (ex.: JS → JavaScript) → análise semântica → dados estruturados usando modelos locais (Ollama).
4. **Matching engine**  
   Combinações via pesos (must-have vs nice-to-have), similaridade semântica por embeddings e critérios técnicos objetivos. Gera pontuação, requisitos atendidos e pontos de melhoria.
5. **Feedback ao candidato**  
   Envia percentual de compatibilidade, competências atendidas e ausentes, reforçando que a decisão final é humana.

## Tecnologias

- **Frontend:** Vue.js; Tailwind CSS; interface de chatbot customizada.
- **Backend:** FastAPI (Python); API RESTful; validação com Pydantic.
- **Processamento assíncrono:** Celery + Redis (broker/cache).
- **Banco de dados:** PostgreSQL (vagas, candidatos, candidaturas, avaliações).
- **Inteligência Artificial:** Ollama (LLMs locais); Sentence Transformers (embeddings); NLP para extração de competências.
- **Infraestrutura:** Docker e Docker Compose; arquitetura containerizada.
