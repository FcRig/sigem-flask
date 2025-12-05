<template>
<<<<<<< HEAD
    <v-container style="display: flex; max-width: 77.1%; margin-left: 11.1%; margin-top: 13px;">
        <v-row>
            <v-col cols="12" md="6">
                <v-card class="pa-4 mb-4" elevation="2" title="Criação de Despachos SEI">

                    <v-form ref="formRef" v-model="valid">
                        <v-text-field label="Número do Processo" v-model="processo" :rules="[rules.required]" />

                        <v-container style="display: flex; flex-direction: row-reverse; gap: 13px">
                            <v-btn color="primary" type="button" @click="pesquisarProcesso">
                                PESQUISAR
                            </v-btn>
                            <v-btn color="secondary" type="button" @click="reabrir_Processo" v-show="btn_reabrir">
                                Reabrir Processo
                            </v-btn> </v-container>

                    </v-form>
                    <v-card class="pa-4 mb-4">
                        <v-form>
                            <v-text-field label="Descrição" :disabled="!formularios" v-model="descricao_despacho" />
                            <v-text-field label="Nome na Árvore" :disabled="!formularios" v-model="arvore_despacho" />
                        </v-form>

                        <v-card>
                            <v-textarea label="Observações desta unidade" :disabled="!formularios"
                                persistent-placeholder style="height: 200px;" rows="10" auto-grow
                                v-model="obs_unidade_despacho"></v-textarea>
                        </v-card>

                        <v-btn color="primary" style="margin-top: 25px;">SUBMETER</v-btn>
                        <v-btn color="secondary" style="margin-left: 10px; margin-top: 25px;">LIMPAR</v-btn>
                    </v-card>
                </v-card>
            </v-col>
        </v-row>
    </v-container>

    <v-snackbar v-model="snackbar" :color="snackbarColor" value="snackbar" location="top right" timeout="3000">
        {{ text }}
    </v-snackbar>
</template>

<script setup>
import { ref } from 'vue';
// import { funcaoTeste } from '../services/sei';
import { procurarProcesso } from '../services/sei';
import { reabrirProcesso } from '../services/sei';

//Snackbar
const text = ref('');
const snackbar = ref(false);
const snackbarColor = ref("success")

const formularios = ref(false);
const processo = ref('');

const descricao_despacho = ref('');
const arvore_despacho = ref('');
const obs_unidade_despacho = ref('');

const btn_reabrir = ref(false);

async function pesquisarProcesso() {

    // Esta função enviar um payload (número do processo) ao backend para procurar a existência de um processo.
    //Existem 3 possibilidades de retorno
    // 1 - Processo está aberto e pode ser despachado
    // 2 - Processo existe mas não está aberto
    // 4 - Processo não existe

    try {

        let payload = { 'processo': processo.value };
        console.log(payload);

        let procurar = await procurarProcesso(payload);

        let msg = procurar.data.msg

        console.log(procurar.data);
        console.log(msg);

        if (msg === "PROCESSO_ENCONTRADO") {
            snackbar.value = true;
            text.value = "Processo Encontrado";
            snackbarColor.value = "success";
            formularios.value = true;
        }

        if (msg === "PROCESSO_FECHADO") {
            snackbar.value = true;
            text.value = "Processo Fechado";
            snackbarColor.value = "error";
            formularios.value = false;
            btn_reabrir.value = true;
        }

        if (msg === "PROCESSO_NAO_EXISTE") {
            snackbar.value = true;
            text.value = "Processo Inválido";
            snackbarColor.value = "error";
            formularios.value = false;
            btn_reabrir.value = false;
        }

    } catch (error) {

        snackbar.value = true;
        text.value = "Erro no Sistema";
        snackbarColor.value = "error"
        formularios.value = false;
        return error;

    }
}

async function reabrir_Processo() {

    let reabrir = await reabrirProcesso();

    try {
        console.log(reabrir)

        if (reabrir.data.msg == "processo_reaberto") {

            snackbar.value = true;
            text.value = "Processo Reaberto"
            snackbarColor.value = "success";
            formularios.value = true;
            return

        } else {
            if (reabrir.data.msg == "erro_ao_reabrir_processo") {
                snackbar.value = true;
                snackbar.color = "error";
                text.value = "Erro ao Reabrir Processo"
                formularios.value = false;
                return
            }
        }


    }
    catch (error) {
        snackbar.value = true;
        text.value = "Erro no Sistema";
        snackbarColor.value = "error"
        formularios.value = false;
        return error;
    }
}

const rules = {
    required: v => !!v || 'Campo Obrigatório'
=======
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

>>>>>>> af9f80444eb1b993bc694cb0aae4ddcb97f28a85
}

</script>