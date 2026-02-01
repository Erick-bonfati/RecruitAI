<template>
  <section class="card section">
    <p class="eyebrow">Vagas</p>
    <div class="split">
      <div>
        <h1>Vagas abertas para quem quer se candidatar.</h1>
        <p>
          Encontre as posições disponíveis, veja requisitos e descrição completa.
          Quando estiver pronto, clique em candidatar-se para iniciar o chatbot.
        </p>
      </div>
      <div class="card mini-card">
        <p class="eyebrow">Como funciona</p>
        <ol>
          <li>Escolha a vaga certa.</li>
          <li>Leia os requisitos.</li>
          <li>Inicie a candidatura.</li>
        </ol>
      </div>
    </div>
  </section>

  <section class="card section">
    <div class="section-header">
      <h2>Vagas disponíveis</h2>
      <select v-model="areaFilter">
        <option value="todas">Todas as áreas</option>
        <option value="tech">Tech</option>
        <option value="design">Design</option>
        <option value="dados">Dados</option>
      </select>
    </div>
    <div class="candidate-grid">
      <article v-for="job in filteredJobs" :key="job.title" class="candidate-card">
        <header>
          <div>
            <strong>{{ job.title }}</strong>
            <span>{{ job.location }}</span>
          </div>
          <span class="badge badge--avaliado">{{ job.level }}</span>
        </header>
        <p>{{ job.description }}</p>
        <div class="chip-row">
          <span class="chip" v-for="(item, index) in job.must" :key="`m-${index}`">
            {{ item }}
          </span>
          <span class="chip chip--ghost" v-for="(item, index) in job.nice" :key="`n-${index}`">
            {{ item }}
          </span>
        </div>
        <button class="btn" type="button" @click="openApply(job)">Candidatar-se</button>
      </article>
    </div>
  </section>

  <section v-if="selectedJob" class="card section">
    <p class="eyebrow">Candidatura</p>
    <h2>Chatbot para {{ selectedJob.title }}</h2>
    <p>
      Aqui vamos abrir o formulário/chatbot para entender suas qualificações.
      Esta etapa ainda não foi implementada.
    </p>
    <button class="btn btn--ghost" type="button" @click="selectedJob = null">
      Fechar
    </button>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const areaFilter = ref('todas')
const selectedJob = ref(null)

const jobs = ref([
  {
    title: 'Frontend Engineer',
    location: 'Remoto · Brasil',
    level: 'Pleno',
    area: 'tech',
    description: 'Construir experiências web acessíveis e performáticas com Vue.',
    must: ['Vue.js', 'JavaScript', 'APIs REST'],
    nice: ['TypeScript', 'Testes'],
  },
  {
    title: 'Product Designer',
    location: 'Híbrido · São Paulo',
    level: 'Sênior',
    area: 'design',
    description: 'Desenhar fluxos de candidatura e dashboards de triagem.',
    must: ['Pesquisa', 'Design System', 'Figma'],
    nice: ['Prototipagem'],
  },
  {
    title: 'Data Analyst',
    location: 'Remoto · Brasil',
    level: 'Júnior',
    area: 'dados',
    description: 'Analisar métricas de compatibilidade e qualidade da triagem.',
    must: ['SQL', 'Dashboard', 'Estatística básica'],
    nice: ['Python'],
  },
])

const filteredJobs = computed(() => {
  if (areaFilter.value === 'todas') return jobs.value
  return jobs.value.filter((job) => job.area === areaFilter.value)
})

const openApply = (job) => {
  selectedJob.value = job
}
</script>
