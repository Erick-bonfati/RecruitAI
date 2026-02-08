<template>
  <section class="card section">
    <p class="eyebrow">Vagas</p>
    <div class="split">
      <div>
        <h1>Vagas abertas para quem quer se candidatar.</h1>
        <p>
          Encontre as posições disponíveis, veja requisitos e descrição completa.
          Quando estiver pronto, clique em candidatar-se para iniciar a candidatura.
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
      <article v-for="job in visibleJobs" :key="job.title" class="candidate-card">
        <header>
          <div>
            <strong>{{ job.title }} </strong>
            <span> - {{ job.location }}</span>
          </div>
          <span class="badge badge--avaliado">{{ job.level }}</span>
        </header>
        <p v-if="job.salary"><strong>Salário:</strong> R${{ job.salary }}</p>
        <div class="chip-row">
          <span class="chip" v-for="(item, index) in job.must" :key="`m-${index}`">
            {{ item }}
          </span>
          <span class="chip chip--ghost" v-for="(item, index) in job.nice" :key="`n-${index}`">
            {{ item }}
          </span>
        </div>
        <div class="card-actions">
          <button class="btn" type="button" @click="detailJob = job">
            Ver vaga
          </button>
        </div>
      </article>
    </div>
  </section>

  <section v-if="detailJob" class="card section">
    <div class="section-header">
      <div>
        <p class="eyebrow">Detalhe da vaga</p>
        <h2>{{ detailJob.title }}</h2>
        <p>{{ detailJob.location }} · {{ detailJob.level }}</p>
      </div>
      <div class="detail-actions">
        <button class="btn btn--ghost" type="button" @click="detailJob = null">
          Fechar
        </button>
      </div>
    </div>

    <p>{{ detailJob.description }}</p>
    <p v-if="detailJob.salary"><strong>Salário:</strong> R${{ detailJob.salary }}</p>

    <div class="chip-row">
      <strong>Requisitos:</strong>
      <span class="chip" v-for="(item, i) in detailJob.must" :key="`dm-${i}`">{{ item }}</span>
    </div>

    <div class="chip-row">
      <strong>Diferenciais:</strong>
      <span class="chip chip--ghost" v-for="(item, i) in detailJob.nice" :key="`dn-${i}`">{{ item }}</span>
    </div>

    <div v-if="detailJob.tasks?.length">
      <strong>Tarefas:</strong>
      <ul>
        <li v-for="(t, i) in detailJob.tasks" :key="`dt-${i}`">{{ t }}</li>
      </ul>
    </div>

    <div v-if="detailJob.yearsExp">
      <strong>Experiência mínima:</strong> {{ detailJob.yearsExp }} anos
    </div>

    <div v-if="detailJob.seniority">
      <strong>Senioridade desejada:</strong> {{ detailJob.seniority }}
    </div>

    <div class="upload-card">
      <div>
        <p class="eyebrow">Currículo</p>
        <p class="helper">Envie o PDF e depois clique em Candidatar-se para calcular a compatibilidade com a vaga.</p>
        <label class="upload-field">
          <input
            type="file"
            accept="application/pdf"
            @change="onResumeChange"
          />
          <span>{{ resumeFile ? resumeFile.name : 'Escolher arquivo PDF' }}</span>
        </label>
      </div>
      <button
        class="btn"
        type="button"
        :disabled="!resumeFile || isUploading"
        @click="openApply(detailJob)"
      >
        {{ isUploading ? 'Enviando...' : 'Candidatar-se' }}
      </button>
    </div>
  </section>

  <section v-if="selectedJob" class="card section">
    <p class="eyebrow">Candidatura</p>
    <h2>Candidatura para {{ selectedJob.title }}</h2>
    
    <p v-if="isUploading" class="info">Estamos analisando seu currículo, aguarde...</p>
    <p v-if="uploadError" class="error">{{ uploadError }}</p>

    <div v-if="matchResult" class="card mini-card">
      <p class="eyebrow">Compatibilidade</p>
      <p><strong>{{ matchResult.pct }}%</strong> de compatibilidade total</p>
      <p v-if="matchResult.mustHit.length"><strong>Obrigatórios possuidos:</strong> {{ matchResult.mustHit.join(', ') }}</p>
      <p v-if="matchResult.mustMissing.length" class="error"><strong>Obrigatórios faltando:</strong> {{ matchResult.mustMissing.join(', ') }}</p>
      <p v-if="matchResult.niceHit.length"><strong>Diferenciais batidos:</strong> {{ matchResult.niceHit.join(', ') }}</p>
      <p v-if="matchResult.niceMissing.length" class="error"><strong>Diferenciais faltando:</strong> {{ matchResult.niceMissing.join(', ') }}</p>
    </div>
    
    <button
      v-if="resumeJson"
      class="btn btn--ghost"
      type="button"
      @click="showJson = !showJson"
    >
      {{ showJson ? 'Fechar JSON' : 'Ver JSON' }}
    </button>

    <pre v-if="resumeJson && showJson" class="json-view">
    {{ JSON.stringify(resumeJson, null, 2) }}
    </pre>

    <button class="btn btn--ghost" type="button" @click="selectedJob = null">
      Fechar
    </button>
  </section>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

const areaFilter = ref('todas')
const selectedJob = ref(null)
const detailJob = ref(null)
const resumeFile = ref(null)

const isUploading = ref(false)
const resumeJson = ref(null)
const uploadError = ref(null)
const showJson = ref(false)

const enviaCurriculoOllama = async(file) => {
  if(!file) return;

  isUploading.value = true
  uploadError.value = ''
  resumeJson.value = null
  showJson.value = false

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

const jobs = ref([])

const carregarVagas = async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/jobs')
    if (!res.ok) throw new Error('Erro ao carregar vagas')
    jobs.value = await res.json()
  } catch (err) {
    console.error(err)
  }
}

const filteredJobs = computed(() => {
  if (areaFilter.value === 'todas') return jobs.value
  return jobs.value.filter((job) => job.area === areaFilter.value)
})

const visibleJobs = computed(() => {
  if (!detailJob.value) return filteredJobs.value
  return [detailJob.value]
})

const openApply = async (job) => {
  selectedJob.value = job
  await enviaCurriculoOllama(resumeFile.value)
}

const onResumeChange = (event) => {
  const file = event.target.files?.[0] || null
  resumeFile.value = file
}

const norm = (list = []) => list.filter(Boolean).map((s) => s.toLowerCase().trim())

const matchResult = computed(() => {
  if (!resumeJson.value || !selectedJob.value) return null

  const skills = new Set(norm(resumeJson.value.skills))
  const required = norm(selectedJob.value.must)
  const nice = norm(selectedJob.value.nice)

  const mustHit = required.filter((req) => skills.has(req))
  const mustMissing = required.filter((req) => !skills.has(req))
  const niceHit = nice.filter((req) => skills.has(req))
  const niceMissing = nice.filter((req) => !skills.has(req))

  const mustWeight = 2 / 3
  const niceWeight = 1 / 3

  let pct = 0
  if (required.length > 0) {
    pct += (mustHit.length / required.length) * (mustWeight * 100)
  }
  if (nice.length > 0) {
    pct += (niceHit.length / nice.length) * (niceWeight * 100)
  }
  if (required.length === 0 && nice.length > 0) {
    pct = (niceHit.length / nice.length) * 100
  }

  return {
    pct: Math.round(pct),
    mustHit,
    mustMissing,
    niceHit,
    niceMissing,
  }
})

onMounted(() => {
  carregarVagas()
})

</script>
