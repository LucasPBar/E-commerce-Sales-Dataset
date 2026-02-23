<h1 align="center">📦 E-Commerce Sales Dataset</h1>
<h3 align="center">Análise Exploratória e Performance Operacional | Janeiro 2026</h3>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Concluído-brightgreen?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data_Analysis-150458?style=for-the-badge&logo=pandas" />
  <img src="https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/b9293560-ac39-4cd2-b028-f121c3857f69" width="800"/>
</p>

---

## 🎯 Visão Geral

Este projeto realiza uma **Análise Exploratória de Dados (EDA)** em um ecossistema de E-commerce com foco em performance operacional e tomada de decisão.

O objetivo foi conduzir um verdadeiro **Health Check de Negócio**, avaliando:

- Performance de vendas  
- Impacto de descontos no faturamento  
- Eficiência logística (Lead Time)  
- Distribuição geográfica da operação  
- Comportamento de compra dos clientes  

O dataset contempla exclusivamente **Janeiro de 2026**, permitindo uma análise aprofundada do comportamento mensal.

---

## 🧠 Problema de Negócio

Em operações de E-commerce, crescimento de vendas não significa necessariamente aumento de rentabilidade.

Durante o período analisado:

- **98% das vendas ocorreram com desconto**
- A operação apresentou alta concentração de vendas na primeira quinzena
- O frete impactou diretamente a margem em determinadas regiões

A pergunta central foi:

> A operação está crescendo de forma saudável ou sacrificando margem e eficiência logística?

---

## 🔎 Principais Análises Realizadas

### 📊 1. Health Check de Vendas

- Concentração geográfica de clientes (Estado / Cidade)
- Top 10 categorias com maior volume
- Impacto real dos descontos no ticket médio
- Relação entre frete e conversão
- Métodos de pagamento mais utilizados
- Frequência de recompra e retenção de clientes
- Receita líquida considerando custo de envio

Insight relevante:
> O volume foi sustentado por descontos agressivos, pressionando margem e concentrando faturamento na primeira quinzena.

---

### 🚚 2. Eficiência Logística (Lead Time Analysis)

Foram criadas três métricas principais:

- **Tempo de Despacho:** `ship_date - order_date`
- **Tempo Total de Entrega:** `delivery_date - order_date`
- **Tempo de Transporte:** diferença entre envio e entrega

Análises realizadas:

- Categorias com maior tempo médio de envio
- Regiões com maior variabilidade logística (desvio padrão elevado)
- Estados com maior proporção de frete sobre valor do produto
- Envios realizados acima do tempo médio

Insight relevante:
> Em algumas regiões, o frete ultrapassa 15–20% do valor do produto, indicando possível ineficiência operacional.

---

### 📦 3. Análise de Mix de Produtos

Estrutura hierárquica analisada:

Brand → Category → Subcategory


Foi desenvolvido um Treemap para entender:

- Marcas dominantes por categoria
- Concentração de faturamento
- Distribuição estratégica do inventário no mês

---

## 📈 Dashboard Interativo

O projeto também conta com uma aplicação interativa desenvolvida em Streamlit:

🚀 **Acesse aqui:**  
https://ecomerceprojectkaggle.streamlit.app/

---

## 💾 Fonte dos Dados

Dataset público disponível no Kaggle:

🔗 https://www.kaggle.com/datasets/sharmajicoder/e-commerce-sales-dataset

---

## 🛠️ Stack Tecnológica

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

---

## 🔬 Metodologia

1. Limpeza e tratamento de inconsistências temporais  
2. Criação de métricas logísticas (Feature Engineering)  
3. Análise estatística descritiva  
4. Visualização executiva orientada a decisão  
5. Construção de dashboard interativo  

---

## 📂 Estrutura do Repositório

📁 data/ → Base de dados original
📓 E-commerce-Sales-Project.ipynb → Notebook completo com EDA
📊 app.py → Aplicação interativa em Streamlit
README.md → Documentação do projeto


---

## 📌 Possíveis Próximos Passos

- Análise de margem bruta estimada
- Modelagem preditiva de tempo de entrega
- Clusterização de clientes por comportamento de compra
- Simulação de impacto de redução de descontos

---

## 👤 Autor

<p>
<b>Lucas Pimenta Barretto</b><br>
Analista de Dados | Foco em Performance & Estratégia
</p>

<p>
<a href="https://www.linkedin.com/in/lucaspimentabarretto">
  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linkedin/linkedin-original.svg" width="20"/> LinkedIn
</a>
<br>
📧 lucaspimenta1805@gmail.com
<br>
💼 Portfólio: https://www.datascienceportfol.io/lucaspimenta1805
</p>

---

<p align="center">
  <i>Dados bem analisados contam histórias. Histórias bem contadas geram decisão.</i>
</p>
