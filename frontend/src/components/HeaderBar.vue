<template>
  <header class="shell header">
    <div class="brand">
      <div class="logo-mark">RA</div>
      <div>
        <strong>RecruitAI</strong>
        <span>triagem local e explicável</span>
      </div>
    </div>

    <nav class="nav">
      <RouterLink to="/" class="nav-link">Início</RouterLink>
      <RouterLink to="/vagas" class="nav-link">Vagas</RouterLink>
      <RouterLink to="/candidatos" class="nav-link">Cadastrar vagas</RouterLink>
    </nav>

    <div class="header-actions">
      <button class="btn" type="button">Criar vaga</button>
    </div>
  </header>
</template>
