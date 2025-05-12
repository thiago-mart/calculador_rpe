import streamlit as st
import numpy as np
import math

## Função de pertinência triangular
def T(a,m,n,b=None):
    if b is None:
      b = n
      n = m
    def triangularFuzzy(x):
        return np.maximum(0,np.minimum((x-a)/(m-a),np.minimum(1,(b-x)/(b-n))))
    return triangularFuzzy

## t-norma do mínimo e s-norma do máximo
def t_min(y1, y2=None):
    if y2 is None:
        return np.min(y1)
    else:
        return np.minimum(y1, y2)

def s_max(y1,y2=None):
    if y2 is None:
        return np.max(y1)
    else:
        return np.maximum(y1, y2)

## Deffuzificação por Centroide
def centroide(x_value, y_value):
    numerador = np.sum(x_value * y_value)
    denominador = np.sum(y_value)

    if denominador == 0:
        return np.nan  # Divisão por zero

    return numerador / denominador

## Definindo como a inferência é calculada
def inferencia(x_value, y_value, t_value):
    infe = np.zeros(len(z))
    for i,A in enumerate(conjunto_rpe_ant):
        for j,B in enumerate(conjunto_disposicao):
            w = t_norm(A(x_value),B(y_value))
            infe = s_norm(infe,t_norm(w,BaseRegras[i][j][t_value](z)))
    return infe


### Definindo as variáveis

t_norm = t_min  # t-norma utilizada
s_norm = s_max  # s-norma utilizada
size = 501  # Quantidade de pontos na discretização

## Criando domínio e imagem
x = np.linspace(1, 10, size)  # Definição do eixo x; Usado para RPE (conjunto A)
y = np.linspace(0, 10, size)  # Definição do eixo y; Usado para disposição (conjunto b)
z = np.linspace(0, 10, size)  # Sla pra que serve isso, é usado no gráfico do centroide


### Sistema de Base de Regras

## Conjuntos fuzzy para RPE
A1_ant = T(0,1,4,5.5)      # Muito baixo
A1 = T(4,5,5.5)         # Muito baixo
A2 = T(4.5,5.5,6,7.5)   # Baixo
A3 = T(5.5,7,8.5)       # Moderado
A4 = T(7.5,8.5,10)      # Pesado alto
A5 = T(9,9.5,10,11)     # Muito alto

## Conjuntos fuzzy para Disposição
B1 = T(-1,0,3,4)             # Indisposto
B2 = T(2,3,4,5)              # Pouco Disposto
B3 = T(3.5,4.5,5.5,6.5)      # Moderadamente Disposto
B4 = T(5,6,7,8)              # Disposto
B5 = T(6,8,10,11)             # Muito Disposto

## Criando a Base de Regras 
BaseRegras = [
    [[A2, A3, A3], [A3, A4, A4], [A4, A4, A5], [A4, A5, A5], [A5, A5, A5]],
    [[A2, A2, A3], [A2, A3, A3], [A3, A4, A4], [A4, A4, A5], [A4, A5, A5]],
    [[A1, A2, A3], [A2, A3, A3], [A3, A3, A4], [A3, A4, A4], [A4, A4, A4]],
    [[A1, A1, A2], [A1, A2, A3], [A2, A3, A3], [A3, A3, A3], [A3, A3, A4]],
    [[A1, A1, A1], [A1, A1, A2], [A1, A2, A2], [A2, A2, A3], [A2, A3, A4]]
]

conjunto_rpe_ant = [A1_ant,A2,A3,A4,A5]
conjunto_disposicao = [B1,B2,B3,B4,B5]


### Site

## Números para os dias
numbers_um = {
    "Ontem": 0,
    "Antes de ontem": 1,
    "Três ou mais dias": 2
}

st.header("Calculador de RPE", divider="rainbow")  # Título
st.subheader("Quanto se esforçar no treino de hoje?")  # Subtítulo

st.markdown("Responda as perguntas abaixo para saber!")  # Questionário

## Pergunta para o tempo de treino
t_select = st.selectbox(            
    "Quando foi seu último treino?",
    numbers_um
)
t_teste = numbers_um[t_select]  # Transformando resposta em número

## Pergunta para o RPE anterior
x_teste = st.slider(
    "Como você avalia o RPE de seu último treino? (Sendo: muito leve = 1, e muito pesado = 10): ",
    min_value=1.0,    # Valor mínimo
    max_value=10.0,   # Valor máximo
    value=7.5,        # Valor inicial automático
    step=0.5,         # Incremento em 0.5
    format="%g"       # Correção das casas decimais
)

## Pergunta para a disposição
y_teste = st.slider(
    "Como você avalia a sua disposição hoje? (Sendo: sem disposição = 0, moderada = 5, e alta = 10): ",
    min_value=0.0,    # Valor mínimo
    max_value=10.0,   # Valor máximo
    value=6.5,        # Valor inicial automático
    step=0.5,         # Incremento em 0.5
    format="%g"       # Correção das casas decimais
)

## Cálculo do RPE
if st.button("Descobrir RPE"):
    teste_inferencia = inferencia(x_teste, y_teste, t_teste)  # Inferência
    teste_centroide = np.round(centroide(z,teste_inferencia)*2)/2  # Defuzzificação de 0.5 em 0.5
    st.success(f"O RPE sugerido para o treino de hoje é: **{teste_centroide}**")  # Resultado
