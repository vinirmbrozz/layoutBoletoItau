def extrairValores(codigo):
    gDAC = calcularDACCodigoBarras(codigo)
    print('gDAC',gDAC)
    
    json = {
        'codigo_banco': codigo[0:3],
        'moeda': codigo[3],
        'DAC_Codigo_Barras': str(gDAC),
        'fator_vencimento': codigo[5:9],
        'valor': codigo[9:19],
        'carteira': codigo[19:22],
        'nosso_numero': codigo[22:30],
        'DAC_Agencia_Conta_Carteira_NossoNumero': codigo[30], # 'DAC' é o dígito verificador do 'agencia' + 'seu_numero' + 'codigo_cliente
        'agencia': codigo[31:35],
        'conta': codigo[35:40],
        'DAC_Agencia_ContaCorrente': codigo[40], # 'DAC' é o dígito verificador do 'agencia' + 'conta_corrente
        'zeros': codigo[41:44],
        'codigo': codigo[0:4] + str(gDAC) +codigo[19:44]
    }
    
    dacAgencia = calcularDAC(json['agencia'] + json['conta'] + json['carteira'] + json['nosso_numero'])
    print('DAC Agência:',dacAgencia)
    
    
    json['DAC_Agencia_Conta_Carteira_NossoNumero'] = dacAgencia
    return json
# codigo_barras = '341 9 1 9617 0000016090 109 15173281 8 7892 99886 0 000'

def calcularDACCodigoBarras(codigo):
    modulo11 = '4329876543298765432987654329876543298765432'
    codigo = codigo[:4] + codigo[5:]
    print('CÓDIGO SEM O CV DE BOLETO, LOGO, 43 DIGITOS:',codigo)
    soma = 0
    codigo = codigo[::-1]
    for i in range(0, len(codigo)):
        soma += int(codigo[i]) * int(modulo11[i])
    resto = soma % 11
    return 11 - resto

def calcularDAC(campo):
    campo_str = str(campo)[::-1]  # Inverte o campo para iterar da direita para a esquerda
    soma = 0
    multiplicadores = [2, 1]
    for i, algarismo in enumerate(campo_str):
        multiplicador = multiplicadores[i % len(multiplicadores)]
        produto = int(algarismo) * multiplicador
        soma += produto if produto < 10 else sum(int(d) for d in str(produto))
    return 10 - (soma % 10)

def montarLinhaDigitavel(codigo):
    valores = extrairValores(codigo)
    print(valores)
    
    campo1 = valores['codigo_banco'] + valores['moeda'] + valores['carteira'] + valores['nosso_numero'][:2]
    dac1 = calcularDAC(campo1)
    campo1 = campo1 + str(dac1)
    campo1 = campo1[:5] + '.' + campo1[5:10]
    print('Campo1:',campo1)
    
    campo2 = valores['nosso_numero'][2:] + str(valores['DAC_Agencia_Conta_Carteira_NossoNumero']) + valores['agencia'][:3]
    dac2 = calcularDAC(campo2)
    campo2 = campo2 + str(dac2)
    campo2 = campo2[:5] + '.' + campo2[5:11]
    print('Campo2:',campo2)
    
    campo3 = valores['agencia'][3:] + valores['conta']
    print('Campo3:',campo3)
    dac3 = calcularDAC(campo3)
    print('DAC3:',dac3)
    campo3 = campo3 + str(dac3)
    campo3 = campo3[:5] + '.' + campo3[5:11]
    print('Campo3:',campo3)
    
    return {'linhaDigitável': campo1 + '.' + campo2 + '.' + campo3 + '.' + valores['DAC_Codigo_Barras'] + '.' + valores['fator_vencimento'] + valores['valor']}

codigo_barras = '34191961700000160901091517328187892998860000'
codigo_de_barras_montado = montarLinhaDigitavel(codigo_barras)
print(codigo_de_barras_montado)
campo1 = '34191.09156.17328.187897.29988.600002.1.96170000016090'