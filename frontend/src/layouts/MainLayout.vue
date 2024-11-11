<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>
          Able
        </q-toolbar-title>
        <a href="https://github.com/ErikUmble/hackrpi-2024" target="_blank" rel="noopener noreferrer" class="text-white">About</a>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">

defineOptions({
  name: 'MainLayout'
});

</script>
