<template>
    <v-container>
        <v-row>
            <v-col cols="12" md="6">

                <v-card class="pa-4 mb-4" elevation="2" title="Busca de Processos SEI">


                    <v-form ref="formRef" v-model="valid">
                        <v-text-field v-model=processo label="Número do Processo" clearable type="input" />
                    </v-form>
                    <v-container class="formulario">

                        <v-btn @click="buscarProcesso" color="primary" class="mt-2">Buscar</v-btn>
                        <v-btn @click="buscarTodos" color="primary" class="mt-2">MOSTRAR TODOS OS PROCESSOS</v-btn>
                    </v-container>
                </v-card>

            </v-col>
            <v-row>
                <v-snackbar v-model="snackbar" :color="snackbarColor" location="top right" timeout="3000">
                    {{ snackbarMsg }}
                </v-snackbar>
            </v-row>
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
import { procurarProcesso } from '../../services/sei';

const processo = ref('');
const snackbar = ref(false)
const snackbarMsg = ref('')
const snackbarColor = ref('success')

async function buscarProcesso() {

    if (!processo.value || processo.value === '') {
        return Error("Processo não identificado.")
    }

    const payload = { processo: processo.value }

    try {

        procurarProcesso(payload)

        return

    } catch (error) {
        snackbarMsg.value = err.response?.data?.msg || 'Erro ao carregar tipos'
        snackbarColor.value = 'error'
        snackbar.value = true

    }

}

async function buscarTodos() {

    console.log("BUSCANDO TODOS OS PROJETOS")

}

</script>