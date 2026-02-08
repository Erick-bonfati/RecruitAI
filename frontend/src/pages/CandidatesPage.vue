<template>
  <section class="card section">
    <p class="eyebrow">Cadastrar vagas</p>
    <div class="split">
      <div>
        <h1>Cadastre vagas com requisitos e descrição completa.</h1>
        <p>
          Esta área é para empresas. Defina requisitos, descreva a vaga e indique
          a faixa salarial.
        </p>
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
            <li>Defina faixa salarial.</li>
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
        <label>
          Local
          <input v-model="location" placeholder="Ex: Remoto · Brasil" />
        </label>
        <label>
          Senioridade/Nível
          <input v-model="level" placeholder="Ex: Pleno" />
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
          Faixa salarial
          <input v-model="salary" placeholder="Ex: R$ 10.000 - 14.000" />
        </label>
        <div class="form-actions">
          <button class="btn" type="button" @click="saveJob">Salvar vaga</button>
          <button class="btn btn--ghost" type="button">Publicar depois</button>
        </div>
        <p v-if="info" class="helper">{{ info }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </section>

  <section class="card section">
  <h2>Vagas cadastradas</h2>
  <p v-if="jobsError" class="error">{{ jobsError }}</p>

  <div class="candidate-grid">
    <article v-for="job in jobs" :key="job.id" class="candidate-card">
      <header>
        <div>
          <strong>{{ job.title }}</strong>
          <span> - {{ job.location }}</span>
        </div>
        <button class="btn btn--ghost" type="button" @click="excluirJob(job.id)">
          Excluir
        </button>
      </header>
      <p>{{ job.description }}</p>
    </article>
  </div>
</section>

</template>

<script setup>
import { ref, onMounted } from 'vue'

const title = ref('')
const description = ref('')
const mustInput = ref('')
const niceInput = ref('')
const mustList = ref([])
const niceList = ref([])
const salary = ref('')
const location = ref('')
const level = ref('')
const info = ref('')
const error = ref('')

// Variaveis dos Jobs
const jobs = ref([])
const jobsErrors = ref('')

const carregarJobs = async () => {
  jobsErrors.value = ""
  try {
    const res = await fetch("http://127.0.0.1:8000/jobs")
    if(!res.ok) throw new Error("Erro ao carregar vagas")
    jobs.value = await res.json()
  } catch (err) {
    jobsErrors.value = err.message || "Falha ao carregar vagas"
  }
}

onMounted(carregarJobs)

const excluirJob = async (jobId) => {
  if (!confirm('Deseja excluir esta vaga?')) return
  try {
    const res = await fetch(`http://127.0.0.1:8000/jobs/${jobId}`, {
      method: 'DELETE',
    })
    if (!res.ok) throw new Error('Erro ao excluir vaga')
    jobs.value = jobs.value.filter((j) => j.id !== jobId)
  } catch (err) {
    jobsErrors.value = err.message || 'Falha ao excluir'
  }
}

const saveJob = async () => {
  info.value = ''
  error.value = ''

  const job = {
    id: crypto.randomUUID(),
    title: title.value.trim(),
    description: description.value.trim(),
    location: location.value.trim() || 'Não especificado',
    level: level.value.trim() || 'Não especificado',
    area: 'tech',
    must: [...mustList.value],
    nice: [...niceList.value],
    salary: salary.value.trim() || 'Não especificado',
    tasks: [],
    yearsExp: null,
    seniority: level.value.trim() || 'Não especificado',
  }

  if (!job.title || !job.description) {
    error.value = 'Preencha pelo menos título e descrição.'
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:8000/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(job),
    })
    if (!res.ok) throw new Error('Erro ao salvar vaga')
    info.value = 'Vaga salva em jobs.json.'

    await carregarJobs()

    title.value = ''
    description.value = ''
    location.value = ''
    level.value = ''
    mustList.value = []
    niceList.value = []
    salary.value = ''
  } catch (err) {
    error.value = err.message || 'Falha ao salvar'
  }
}

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
