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
            <strong>{{ vagasAtivas }}</strong>
            <span>vagas ativas</span>
          </div>
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

const vagasAtivas = ref(0)

const carregarVagasAtivas = async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/vagas-ativas")
    if (!res.ok) throw new Error("Erro ao carregar vagas ativas")
    const data = await res.json()
    vagasAtivas.value = data.count ?? 0
  } catch (err) {
    vagasAtivas.value = 0
  }
}

onMounted(carregarVagasAtivas)


const persona = ref('empresa')

const personas = [
  { label: 'Empresa', value: 'empresa' },
  { label: 'Candidato', value: 'candidato' },
]

const benefits = computed(() => {
  if (persona.value === 'candidato') {
    return [
      'Feedback claro sobre competências faltantes.',
      'Formulário lido por IA para explicar experiências.',
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
