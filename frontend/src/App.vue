<template>
  <div class="page">
    <header class="shell header">
      <strong>RecruitAI</strong>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/vagas">Vagas</RouterLink>
        <RouterLink to="/candidatos">Candidatos</RouterLink>
      </nav>
    </header>

    <main class="shell hero">
      <RouterView />
    </main>

    <footer class="shell footer">
      <small>RecruitAI · IA local para recrutamento justo e rápido.</small>
    </footer>
  </div>
</template>
