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
line_width = 1  # Espessura da curva no gráfico

## Criando domínio e imagem
dominio_min = 0
dominio_max = 10

x = np.linspace(dominio_min, dominio_max, size)  # Definição do eixo x; Usado para RPE (conjunto A)
y = np.linspace(dominio_min, dominio_max, size)  # Definição do eixo y; Usado para disposição (conjunto b)
z = np.linspace(dominio_min, dominio_max, size)  # Sla pra que serve isso, é usado no gráfico do centroide

dominio_tick = np.arange(dominio_min, dominio_max+1, 1)  # Arruma o domínio no Gráfico
imagem_tick = np.arange(0, 1.1, 0.2)  # Arruma a imagem no Gráfico

## Conjuntos fuzzy para RPE
A1 = T(0,1,3,5.5)  # Muito Leve (muito baixo)
A2 = T(4,5,5.5,7.5)  # Leve (baixo)
A3 = T(5.5,7,8.5)  # Moderado
A4 = T(7.5,8.5,10)  # Pesado (alto)
A5 = T(9,9.5,10,11)  # Muito Pesado (muito alto)

## Conjuntos fuzzy para Disposição
B1 = T(-1,0,3,4)  # Indisposto
B2 = T(2,3,4,5)  # Pouco Disposto
B3 = T(3.5,4.5,5.5,6.5)  # Moderadamente Disposto
B4 = T(5,6,7,8)  # Disposto
B5 = T(6,8,9,11)  # Muito Disposto

## Criando a Base de Regras 
BaseRegras = [
    [[A2, A3, A3], [A3, A4, A4], [A4, A4, A5], [A4, A5, A5], [A5, A5, A5]],
    [[A2, A2, A3], [A2, A3, A3], [A3, A4, A4], [A4, A4, A5], [A4, A5, A5]],
    [[A1, A2, A3], [A2, A3, A3], [A3, A3, A4], [A3, A4, A4], [A4, A4, A4]],
    [[A1, A1, A2], [A1, A2, A3], [A2, A3, A3], [A3, A3, A3], [A3, A3, A4]],
    [[A1, A1, A1], [A1, A1, A2], [A1, A2, A2], [A2, A2, A3], [A2, A3, A4]]
]

conjunto_rpe_ant = [A1,A2,A3,A4,A5]
conjunto_disposicao = [B1,B2,B3,B4,B5]

numbers_um = {
    "Ontem": 0,
    "Antes de ontem": 1,
    "A três ou mais dias": 2
}


st.header("Calculador de RPE", divider="rainbow")
st.subheader("Quanto se esforçar no treino de hoje?")

t_select = st.selectbox(
    "Quando foi seu último treino?",
    numbers_um
)
t_teste = numbers_um[t_select]

x_teste = st.slider(
    "Como você avalia o RPE do seu último treino? (Sendo muito leve = 1 e muito pesado = 10): ",
    min_value=1,    # Minimum value (float)
    max_value=10,   # Maximum value (float)
    value=7.5,       # Default starting value
    step=0.5,         # Increment by 0.5
    format="%g"
)

y_teste = st.slider(
    "Como você avalia a sua disposição hoje? (Sendo indisposto = 0, moderada = 5, e muito disposto = 10): ",
    min_value=0,    # Minimum value (float)
    max_value=10,   # Maximum value (float)
    value=6,       # Default starting value
    step=0.5,         # Increment by 0.5
    format="%g"
)

# if button_clicked:
st.markdown("Responda as perguntas abaixo:")



if st.button("Calcular RPE"):
    teste_inferencia = inferencia(x_teste, y_teste, t_teste)  # Inferencia
    teste_centroide = np.round(centroide(z,teste_inferencia)*2)/2  # Defuzzificação de 0.5 em 0.5
    st.success(f"O RPE sugerido para o treino de hoje é: **{teste_centroide}**")
