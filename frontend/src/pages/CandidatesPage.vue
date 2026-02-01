<template>
  <section class="card section">
    <p class="eyebrow">Cadastrar vagas</p>
    <div class="split">
      <div>
        <h1>Cadastre vagas com requisitos e descrição completa.</h1>
        <p>
          Esta área é para empresas. Defina requisitos, descreva a vaga e indique
          a faixa salarial ou pretensão.
        </p>
      </div>
      <div class="card mini-card">
        <p class="eyebrow">Resumo</p>
        <div class="summary-list">
          <div>
            <strong>3</strong>
            <span>vagas rascunho</span>
          </div>
          <div>
            <strong>5</strong>
            <span>em triagem</span>
          </div>
          <div>
            <strong>2</strong>
            <span>publicadas</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="card section">
    <div class="form-grid">
      <div>
        <h2>Detalhes da vaga</h2>
        <p>Complete apenas o essencial para publicar.</p>
        <div class="callout">
          <strong>Checklist rápido</strong>
          <ul>
            <li>Inclua requisitos obrigatórios e desejáveis.</li>
            <li>Descreva responsabilidades e contexto.</li>
            <li>Defina faixa salarial ou pretensão.</li>
          </ul>
        </div>
      </div>
      <form class="form" @submit.prevent>
        <label>
          Título da vaga
          <input v-model="title" placeholder="Ex: Dev Full Stack" />
        </label>
        <label>
          Descrição da vaga
          <textarea v-model="description" rows="4" placeholder="Resumo das responsabilidades"></textarea>
        </label>
        <div class="field-group">
          <span class="field-label">Requisitos obrigatórios</span>
          <div class="skill-row">
            <input v-model="mustInput" placeholder="Ex: Vue.js" />
            <button class="btn" type="button" @click="addRequirement('must')">
              Adicionar
            </button>
          </div>
          <div class="chip-row">
            <span class="chip" v-for="(item, index) in mustList" :key="`must-${index}`">
              {{ item }}
              <button type="button" @click="removeRequirement('must', index)">×</button>
            </span>
          </div>
        </div>
        <div class="field-group">
          <span class="field-label">Requisitos desejáveis</span>
          <div class="skill-row">
            <input v-model="niceInput" placeholder="Ex: TypeScript" />
            <button class="btn btn--ghost" type="button" @click="addRequirement('nice')">
              Adicionar
            </button>
          </div>
          <div class="chip-row">
            <span class="chip chip--ghost" v-for="(item, index) in niceList" :key="`nice-${index}`">
              {{ item }}
              <button type="button" @click="removeRequirement('nice', index)">×</button>
            </span>
          </div>
        </div>
        <label>
          Faixa salarial ou pretensão
          <input v-model="salary" placeholder="Ex: R$ 10.000 - 14.000" />
        </label>
        <div class="form-actions">
          <button class="btn" type="button">Salvar vaga</button>
          <button class="btn btn--ghost" type="button">Publicar depois</button>
        </div>
      </form>
    </div>
  </section>

  <section class="card section">
    <h2>Rascunhos recentes</h2>
    <div class="candidate-grid">
      <article class="candidate-card" v-for="draft in drafts" :key="draft.title">
        <header>
          <div>
            <strong>{{ draft.title }}</strong>
            <span>{{ draft.location }}</span>
          </div>
          <span class="badge badge--novo">Rascunho</span>
        </header>
        <p>{{ draft.summary }}</p>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const title = ref('')
const description = ref('')
const mustInput = ref('')
const niceInput = ref('')
const mustList = ref(['Vue.js', 'APIs REST'])
const niceList = ref(['TypeScript'])
const salary = ref('')

const drafts = ref([
  {
    title: 'Backend Engineer',
    location: 'Remoto · Brasil',
    summary: 'API REST, integrações e documentação clara.',
  },
  {
    title: 'Customer Success',
    location: 'Híbrido · Belo Horizonte',
    summary: 'Relacionamento com clientes e onboarding.',
  },
  {
    title: 'Data Engineer',
    location: 'Remoto · Brasil',
    summary: 'Pipelines, ETL e monitoramento de dados.',
  },
])

const addRequirement = (type) => {
  if (type === 'must') {
    const value = mustInput.value.trim()
    if (!value) return
    mustList.value.push(value)
    mustInput.value = ''
    return
  }
  const value = niceInput.value.trim()
  if (!value) return
  niceList.value.push(value)
  niceInput.value = ''
}

const removeRequirement = (type, index) => {
  if (type === 'must') {
    mustList.value.splice(index, 1)
    return
  }
  niceList.value.splice(index, 1)
}
</script>
