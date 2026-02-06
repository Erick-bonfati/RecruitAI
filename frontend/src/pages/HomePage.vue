<template>
  <section class="hero-grid">
    <div class="card hero-card">
      <p class="eyebrow">Visão geral</p>
      <h1>Triagem inteligente que respeita tempo, privacidade e contexto.</h1>
      <p>
        Reúna vagas, currículos e feedback em um fluxo simples. A IA local organiza
        competências, compara requisitos e entrega explicações claras.
      </p>
      <div class="segmented">
        <button
          v-for="item in personas"
          :key="item.value"
          type="button"
          class="segment"
          :class="{ active: persona === item.value }"
          @click="persona = item.value"
        >
          {{ item.label }}
        </button>
      </div>
      <ul class="bullets">
        <li v-for="benefit in benefits" :key="benefit">{{ benefit }}</li>
      </ul>
      <div class="cta-row">
        <RouterLink class="btn" to="/candidatos">Criar candidatura</RouterLink>
      </div>
    </div>

    <div class="stack">
      <div class="card summary-card">
        <p class="eyebrow">Status hoje</p>
        <div class="stat-grid">
          <div class="stat">
            <strong>{{ metricas.vagas_ativas }}</strong>
            <span>vagas ativas</span>
          </div>
          <div class="stat">
            <strong>{{ metricas.candidaturas }}</strong>
            <span>candidaturas</span>
          </div>
          <div class="stat">
            <strong>{{ matchPercent }}%</strong>
            <span>match médio</span>
          </div>
        </div>
        <div class="progress">
          <span>Triagens concluídas</span>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: matchPercent + '%' }"></div>
          </div>
          <small>+12% nesta semana</small>
        </div>
      </div>

      <div class="card timeline">
        <p class="eyebrow">Fluxo em 4 passos</p>
        <ol>
          <li>Cadastre requisitos e pesos por vaga.</li>
          <li>Receba candidatos por formulário lido por IA.</li>
          <li>Extraia competências com IA local.</li>
          <li>Entregue ranking e feedback padrão.</li>
        </ol>
      </div>
    </div>
  </section>

  <section class="card section">
    <p class="eyebrow">Verificar vagas</p>
    <div class="form-grid">
      <div>
        <h2>Veja todas as oportunidades disponíveis</h2>
        <p>
          A página de vagas reúne todas as posições abertas. Você pode informar suas
          qualificações em um formulário lido por IA, receber feedback e seguir com
          a candidatura.
        </p>
      </div>
      <div class="callout">
        <strong>Resumo rápido</strong>
        <ul>
          <li>Vagas abertas com requisitos e descrição clara.</li>
          <li>Formulário guiado lido por IA para mapear competências.</li>
          <li>Compatibilidade exibida antes de enviar.</li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'

const metricas = ref({vagas_ativas: 0, candidaturas: 0, match_medio: 0})
const metricasLoading = ref(true)
const metricasErro = ref("")

const carregarMetricas = async () => {
  metricasLoading.value = true
  metricasErro.value = ""
  try {
    const res = await fetch("http://127.0.0.1:8000/metricas")
    if(!res.ok) throw new Error("Erro ao carregar métricas")
    metricas.value = await res.json()
  } catch (err) {
    metricasErro.value = err.message
  } finally {
    metricasLoading.value = false
  }
}

onMounted(carregarMetricas)


const persona = ref('empresa')

const personas = [
  { label: 'Empresa', value: 'empresa' },
  { label: 'Candidato', value: 'candidato' },
]

const benefits = computed(() => {
  if (persona.value === 'candidato') {
    return [
      'Feedback claro sobre competências faltantes.',
      'Chat guiado para explicar experiências.',
      'Privacidade e transparência no uso dos dados.',
    ]
  }
  return [
    'Requisitos obrigatórios e desejáveis com pesos.',
    'Ranking explicável, com justificativas por requisito.',
    'Dashboards de tempo e qualidade da triagem.',
  ]
})
</script>
