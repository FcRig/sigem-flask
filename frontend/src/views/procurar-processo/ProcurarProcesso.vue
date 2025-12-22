<template>
    <v-container>
        <v-row>
            <v-col cols="12" md="6">

                <v-card class="pa-4 mb-4" elevation="2" title="Busca de Processos SEI">


                    <v-form ref="formRef" v-model="valid">
                        <v-text-field v-model=processo label="Número do Processo" clearable type="input" />
                    </v-form>
                    <v-container class="formulario">

                    <v-btn @click="buscar" color="primary" class="mt-2">Buscar</v-btn>
                    <v-btn @click="buscar_todos" color="primary" class="mt-2">MOSTRAR TODOS OS PROCESSOS</v-btn>
                    </v-container>
    </v-card>

    </v-col>
    </v-row>
    </v-container>
</template>

<style scoped>

.formulario {
    display: flex;
    gap: 8.4em;
}

</style>

<script setup>

import { ref } from 'vue';

const processo = ref('');

async function buscar() {

    if (!processo.value || processo.value === '') {
        return Error("Processo não identificado.")
    }

    console.log(processo.value)

}

async function buscar_todos() {

    console.log("BUSCANDO TODOS OS PROJETOS")

}

</script>