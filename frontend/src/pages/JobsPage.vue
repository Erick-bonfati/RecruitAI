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
        <div class="resume-row">
          <input
            class="resume-input"
            type="file"
            accept=".pdf,.doc,.docx"
            @change="onResumeChange"
          />
          <button
            class="btn"
            type="button"
            :disabled="!resumeFile"
            @click="openApply(job)"
          >
            Candidatar-se
          </button>
        </div>
      </article>
    </div>
  </section>

  <section v-if="selectedJob" class="card section">
    <p class="eyebrow">Candidatura</p>
    <h2>Chatbot para {{ selectedJob.title }}</h2>
    
    <p v-if="isUploading">Enviando currículo...</p>
    <p v-if="uploadError" class="error">{{ uploadError }}</p>

    <pre v-if="resumeJson" class="json-view">
    {{ JSON.stringify(resumeJson, null, 2) }}
    </pre>

    <button class="btn btn--ghost" type="button" @click="selectedJob = null">
      Fechar
    </button>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const areaFilter = ref('todas')
const selectedJob = ref(null)
const resumeFile = ref(null)

const isUploading = ref(false)
const resumeJson = ref(null)
const uploadError = ref(null)

const enviaCurriculoOllama = async(file) => {
  if(!file) return;

  isUploading.value = true
  uploadError.value = ''
  resumeJson.value = null

  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('http://127.0.0.1:8000/extrair', {
      method: 'POST',
      body: formData,
    })

    if(!response.ok) {
      const err = await response.json()
      throw new Error(err.detail || 'Erro ao enviar currículo')
    }

    resumeJson.value = await response.json()

  } catch(err)
  {
    uploadError.value = err.message || 'Falha no upload'
  } finally {
    isUploading.value = false
  }
 

}

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

const onResumeChange = async (event) => {
  const file = event.target.files?.[0] || null
  resumeFile.value = file
  await enviaCurriculoOllama(file)
}
</script>
