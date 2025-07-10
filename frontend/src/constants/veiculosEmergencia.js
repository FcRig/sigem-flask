export const instituicoes = {
  '89175541000164': 'Brigada Militar',
  '00058163000125': 'Polícia Civil',
  '28610005000155': 'Corpo de Bombeiros',
  '02510700000151': 'EPTC',
  '00394429000179': 'PRF',
  '07963160000130': 'SUSEPE',
  '09734605000187': 'Polícia Legislativa',
  '87934675000196': 'Estado do Rio Grande do Sul',
  '92883834000100': 'DAER',
}

export const justificativas = {
  '00394429000179': {
    orgao: 'PRF',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Polícia Rodoviária Federal). Requerimento em anexo',
    justificativa: 'Viatura policial'
  },
  '00058163000125': {
    orgao: 'Polícia Civil',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Polícia Civil do Estado do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial'
  },
  '09734605000187': {
    orgao: 'Polícia Legislativa',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Polícia Legislativa). Requerimento em anexo',
    justificativa: 'Viatura policial'
  },
  '07963160000130': {
    orgao: 'SUSEPE',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial da polícia penal (Superintendência dos Serviços Penitenciários do Estado do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial'
  },
  '89175541000164': {
    orgao: 'Brigada Militar',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Brigada Militar do Estado do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial'
  },
  '87934675000196': {
    orgao: 'Estado do Rio Grande do Sul',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão policial (Brigada Militar do Estado do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial'
  },
  '28610005000155': {
    orgao: 'Corpo de Bombeiros Militar do Estado do Rio Grande do Sul',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão destinados a socorro de incêndio e salvamento (Corpo de Bombeiros Militar do Estado do Rio Grande do Sul). Requerimento em anexo',
    justificativa: 'Viatura policial'
  },
  '92883834000100': {
    orgao: 'Departamento Autônomo de Estradas de Rodagem do Rio Grande do Sul',
    motivo:
      'Enquadramento no art. 280, § 6º do CTB, por se tratar de viatura oficial de órgão ligado à fiscalização de trânsito (Departamento Autônomo de Estradas de Rodagem do Rio Grande do Sul - DAER). Requerimento em anexo',
    justificativa: 'Viatura policial'
  }
}

export const codigosPermitidos = ['745-50', '746-30', '747-10']
export const codigosPermitidosDigits = codigosPermitidos.map(c => c.replace(/\D/g, ''))
