<template>
  <v-container>
    <!-- Cabeçalho -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4" elevation="2">
          <h2>
            Lavrar Auto de Infração
            <v-chip color="green" text-color="white">CTB</v-chip>
          </h2>
        </v-card>
      </v-col>
    </v-row>

    <!-- Identificação da Infração -->
    <v-card class="pa-4 mb-4" elevation="2">
      <h3>Identificação da Infração</h3>
      <v-row dense>
        <v-col cols="12" md="8">
          <v-text-field label="Código/Descrição da infração" readonly />
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field label="Amparo Legal" readonly />
        </v-col>
        <v-col cols="6" md="4">
          <v-text-field label="Gravidade" readonly />
        </v-col>
        <v-col cols="6" md="4">
          <v-select
            :items="['Condutor', 'Proprietário']"
            label="Tipo de Infrator"
          />
        </v-col>
      </v-row>

      <v-radio-group inline label="Abordagem">
        <v-radio label="Com Abordagem" value="com" />
        <v-radio label="Sem Abordagem" value="sem" />
      </v-radio-group>
    </v-card>

    <!-- Identificação do Veículo -->
    <v-card class="pa-4" elevation="2">
      <h3>Identificação do Veículo</h3>
      <v-row dense>
        <v-col cols="12" md="3">
          <v-select label="Emplacamento" :items="['Nacional']" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field label="Placa" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field label="Chassi" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field label="Renavam" />
        </v-col>
        <v-col cols="12" md="3">
          <v-select label="País" :items="['Brasil']" />
        </v-col>
        <v-col cols="12" md="2">
          <v-select label="UF" :items="['RS', 'SP', 'RJ']" />
        </v-col>
        <v-col cols="12" md="4">
          <v-select label="Marca" :items="['FIAT', 'CHEVROLET', 'FORD']" />
        </v-col>
        <v-col cols="12" md="2">
          <v-checkbox label="Outra Marca" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field label="Modelo" />
        </v-col>
        <v-col cols="6" md="3">
          <v-select label="Cor" :items="['Preta', 'Branca', 'Prata']" />
        </v-col>
        <v-col cols="6" md="3">
          <v-select label="Espécie" :items="['Passageiro', 'Carga']" />
        </v-col>
        <v-col cols="6" md="3">
          <v-select label="Tipo do Veículo" :items="['Automóvel']" />
        </v-col>
        <v-col cols="6" md="3">
          <v-select label="Categoria" :items="['Oficial', 'Particular']" />
        </v-col>
        <v-col cols="12" md="3">
          <v-select label="Tipo Documento" :items="['CNPJ', 'CPF']" />
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field label="Nº Documento" />
        </v-col>
        <v-col cols="12" md="6">
          <v-text-field label="Nome/Razão Social" />
        </v-col>
        <v-col cols="12">
          <v-radio-group inline label="Tipo de Composição">
            <v-radio label="Simples" value="simples" />
            <v-radio label="Combinação" value="combinacao" />
          </v-radio-group>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
</script>
