<template>
    <v-conteiner style="display: flex; max-width: 77.1%; margin-left: 11.1%; margin-top: 13px;">
        <v-row>
            <v-col cols="12" md="6">
                <v-card class="pa-4 mb-4" elevation="2" title="Criação de Despachos SEI">
                    <v-form ref="formRef" v-model="valid">
                        <v-text-field label="Número do Processo" v-model="descricao_despacho" />
                        <v-conteiner style="display: flex; flex-direction: row-reverse;">
                            <v-btn color="primary" @click="ativar" style="margin-bottom: 20px; ">PESQUISAR</v-btn>
                        </v-conteiner>
                    </v-form>
                    <v-form>
                        <v-text-field label="Descrição" :disabled="!botoes" v-model="descricao_despacho" />
                        <v-text-field label="Nome na Árvore" :disabled="!botoes" v-model="arvore_despacho" />
                    </v-form>
                    <v-card>
                        <v-textarea label="Observações desta unidade" :disabled="!botoes" persistent-placeholder style="height: 200px;"
                            rows="10" auto-grow v-model="obs_unidade_despacho"></v-textarea>
                    </v-card>

                    <v-btn color="primary"  style="margin-top: 25px;" >SUBMETER</v-btn>

                    <v-btn color="secondary" style="margin-left: 10px; margin-top: 25px;" >LIMPAR</v-btn>
                </v-card>

            </v-col>
        </v-row>
        <v-snackbar v-model="snackbar" :color="snackbarColor" location="top right" timeout="3000">

            {{ snackbarMsg }}

        </v-snackbar>
    </v-conteiner>
</template>

<script setup>

import { ref } from 'vue';

const botoes = ref(false);


async function ativar(){

    botoes.value = true;

}

</script>